###########################################################################
# 
#  Copyright 2019 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

import os
import fcntl
import json
import uuid
import time
import signal
import traceback
import subprocess
import threading
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.conf import settings

from starthinker_ui.recipe.models import Recipe, utc_milliseconds, JOB_LOOKBACK_MS, JOB_INTERVAL_MS, JOB_RECHECK_MS
from starthinker_ui.ui.log import log_manager_start, log_manager_end, log_manager_error
from starthinker_ui.ui.log import log_job_timeout, log_job_error, log_job_start, log_job_end, log_job_cancel
from starthinker_ui.ui.log import log_verbose, get_instance_name


MANAGER_ON = True
def signal_exit(self, signum):
  global MANAGER_ON
  MANAGER_ON = False

signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


def worker_ping(worker_uid, recipe_uids):
  # update recipes that belong to this worker
  if recipe_uids:
    Recipe.objects.filter(worker_uid=worker_uid, id__in=recipe_uids).update(worker_utm=utc_milliseconds())


def worker_check(worker_uid):
  return set(Recipe.objects.filter(worker_uid=worker_uid).values_list('id', flat=True))


def worker_status(worker_uid, recipe_uid, script, instance, hour, event, stdout, stderr):
  try:
    job = Recipe.objects.get(worker_uid=worker_uid, id=recipe_uid)
    job.set_task(script, instance, hour, event, stdout, stderr)
  except Recipe.DoesNotExist:
    print('Expired Worker Job:', worker_uid, recipe_uid, script, instance, hour, event)


def worker_pull(worker_uid, jobs=1):
  '''Atomic reservation of worker in jobs.

  Args:
    - worker_uid ( string ) - identifies a unique worker, must be same for every call from same worker.
    - jobs ( integer ) - number of jobs to pull
  '''

  # if the worker cannot do any work, do nothing
  if jobs <= 0: return

  tasks = []
  worker_utm = utc_milliseconds()
  worker_lookback = worker_utm - JOB_LOOKBACK_MS
  worker_recheck = worker_utm - JOB_RECHECK_MS

  with transaction.atomic():

    # every half hour put jobs back in rotation so worker can trigger get_status logic, triggers status at 24 hour mark
    Recipe.objects.filter(active=True, manual=False, worker_utm__lt=worker_recheck).select_for_update(skip_locked=True).update(job_done=False)

    #for r in Recipe.objects.all().values():
    #  print('R', r)

    # find recipes that are available but have not been pinged recently to this worker
    where = Recipe.objects.filter(
      job_done=False,
      active=True,
      worker_utm__lt=worker_lookback,
    ).select_for_update(skip_locked=True).order_by('worker_utm').values_list('id', flat=True)[:jobs]

    #print('W', where)

    # mark those recipes as belonging to this worker
    Recipe.objects.filter(id__in=where).update(worker_uid=worker_uid, worker_utm=worker_utm)

    # find all recipes that belong to this worker and check if they have tasks
    for job in Recipe.objects.filter(worker_uid=worker_uid, worker_utm=worker_utm):
      task = job.get_task()
      if task: tasks.append(task)

  return tasks


def make_non_blocking(file_io):
  fd = file_io.fileno()
  fl = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


class Workers():

  def __init__(self, uid, jobs_maximum, timeout_seconds, trace=False):
    self.uid = uid or get_instance_name(str(uuid.uuid1()))
    self.timeout_seconds = timeout_seconds
    self.trace = trace
    self.jobs_maximum = jobs_maximum
    self.jobs = []

    self.lock_thread = threading.Lock()
    self.ping_event = threading.Event()
    self.ping_thread = threading.Thread(target=self.ping)
    self.ping_thread.start()


  def available(self):
    return self.jobs_maximum - len(self.jobs)


  def pull(self):
    self.lock_thread.acquire()
    jobs = worker_pull(self.uid, jobs=self.available())
    self.lock_thread.release()

    if jobs:
      for job in jobs: 
        self.run(job)
    

  def run(self, job, force=False):
   
    self.lock_thread.acquire()
    self.jobs.append(job)
    self.lock_thread.release()

    job['recipe']['setup'].setdefault('timeout_seconds', self.timeout_seconds)

    job['job'] = {
      'worker':self.uid,
      'id':str(uuid.uuid1()),
      'process':None,
      'utc':datetime.utcnow(),
    }

    filename = '%s/%s.json' % (settings.UI_CRON, job['job']['id'])

    with open(filename, 'w') as job_file:
      job_file.write(json.dumps(job['recipe'], default=str))

    command = [
      '%s/starthinker_virtualenv/bin/python' % settings.UI_ROOT,
      '-W', 'ignore',
      '%s/starthinker/task/%s/run.py' % (settings.UI_ROOT, job['script']),
      filename,
      '-i', str(job['instance']),
      '--verbose',
    ]

    if self.trace: command.append('--trace_file')

    job['job']['process'] = subprocess.Popen(command, shell=False, cwd=settings.UI_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    make_non_blocking(job['job']['process'].stdout)
    make_non_blocking(job['job']['process'].stderr)

    worker_status(
      job['job']['worker'],
      job['recipe']['setup']['uuid'],
      job['script'],
      job['instance'],
      job['hour'],
      'JOB_START',
      "",
      ""
    )
    log_job_start(job)


  def check(self):
    self.lock_thread.acquire()
    try:
      recipes = worker_check(self.uid)
      last_job = len(self.jobs) - 1
      while last_job >= 0:
        if self.jobs[last_job]['recipe']['setup']['uuid'] not in recipes:
          self.jobs[last_job]['job']['process'].kill()
          self.cleanup(self.jobs[last_job])
          log_job_cancel(self.jobs[last_job])
          del self.jobs[last_job]
        last_job -= 1
    except Exception as e:
      log_manager_error(traceback.format_exc())
    self.lock_thread.release()


  def cleanup(self, job):
    filename = '%s/%s.json' % (settings.UI_CRON, job['job']['id'])
    if os.path.exists(filename):
      os.remove(filename)


  def ping(self):
    # update all jobs belonging to worker
    while not self.ping_event.wait(JOB_INTERVAL_MS / 1000):
      self.lock_thread.acquire()
      try:
        worker_ping(self.uid, [job['recipe']['setup']['uuid'] for job in self.jobs])
      except Exception as e:
        log_manager_error(traceback.format_exc())
      self.lock_thread.release()


  def poll(self):

    self.lock_thread.acquire()

    for job in self.jobs:

      # if job changes state, this is set, then sent to database
      status = None
 
      # read any incremental data from the process ( made non-blocking at construction )
      stdout = job['job']['process'].stdout.read()
      if stdout is not None: stdout = stdout.decode()
      stderr = job['job']['process'].stderr.read()
      if stderr is not None: stderr = stderr.decode()

      # if process still running, check timeout or ping keep alive 
      poll = job['job']['process'].poll()
      if poll is None:

        # check if task is a timeout 
        if (datetime.utcnow() - job['job']['utc']).total_seconds() > job['recipe']['setup']['timeout_seconds']:
          status = 'JOB_TIMEOUT'
          job['job']['process'].kill()
          self.cleanup(job)
          log_job_timeout(job)
          job['job']['process'] = None

        # otherwise task is running, update stdout and stderr if present
        elif stdout or stderr:
          status = 'JOB_START'

      # if process has return code, check if task is complete or error
      else:
        self.cleanup(job)

        # if error scrap whole worker and flag error
        if poll != 0: 
          status = 'JOB_ERROR'
          log_job_error(job)
          job['job']['process'] = None

        # if success, pop task off the stack and flag success
        else: 
          status = 'JOB_END'
          log_job_end(job)
          job['job']['process'] = None

      # if status is set, send it to the database
      if status:
        worker_status(
          job['job']['worker'],
          job['recipe']['setup']['uuid'],
          job['script'],
          job['instance'],
          job['hour'],
          status,
          stdout,
          stderr
        )

    # remove all workers without a process, they are done
    self.jobs = [job for job in self.jobs if job['job']['process'] is not None]

    self.lock_thread.release()

    # if workers remain, return True
    return bool(self.jobs)


  def shutdown(self):
    # wait for jobs to finish
    while self.poll():
      time.sleep(JOB_INTERVAL_MS / 1000)

    # turn off threads ( ping )
    self.ping_event.set()


class Command(BaseCommand):
  help = 'Executes a recipe job and writes status to the databse.'

  def add_arguments(self, parser):
    parser.add_argument(
      '--worker',
      action='store',
      dest='worker',
      default='',
      help='Name of worker to use when requesting jobs.',
    )

    parser.add_argument(
      '--jobs',
      action='store',
      dest='jobs',
      default=5,
      type=int,
      help='Maximum number of jobs simlutanelous processes to start within this worker.',
    )

    parser.add_argument(
      '--timeout',
      action='store',
      dest='timeout',
      default=60 * 60 * 12, # 12 hours
      type=int,
      help='Default seconds to allow a task to run before timing it out, also controlled by recipe.',
    )

    parser.add_argument(
      '--verbose',
      action='store_true',
      dest='verbose',
      default=False,
      help='Causes log messages to also print.',
    )

    parser.add_argument(
      '--trace',
      action='store_true',
      dest='trace',
      default=False,
      help='Create an execution trace in /tmp/starthinker_trace.log.',
    )

    parser.add_argument(
      '--test',
      action='store_true',
      dest='test',
      default=False,
      help='Set test mode to execute loop only once and return workers.',
    )

  def handle(self, *args, **kwargs):
    global MANAGER_ON
    MANAGER_ON = True

    print('Starting Up...')

    if kwargs['verbose']: log_verbose()

    log_manager_start()

    workers = Workers(
      kwargs['worker'], 
      kwargs['jobs'], 
      kwargs['timeout'],
      kwargs['trace'],
    ) 

    try:

      while MANAGER_ON:
        workers.pull()
        time.sleep(1)
        workers.check()
        time.sleep(1)
        workers.poll()
        time.sleep(1)
        if kwargs['test']: 
          MANAGER_ON = False

    except KeyboardInterrupt:
      MANAGER_ON = False
    except Exception as e:
      log_manager_error(traceback.format_exc())

    print('Shutting Down...')
    workers.shutdown()

    log_manager_end()
