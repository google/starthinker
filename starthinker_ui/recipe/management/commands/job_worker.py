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
import json
import uuid
import time
import signal
import traceback
import subprocess
import threading
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker_ui.recipe.models import worker_pull, worker_status, worker_check, worker_ping, utc_milliseconds, JOB_LOOKBACK_MS, JOB_INTERVAL_MS
from starthinker_ui.ui.log import log_manager_start, log_manager_end, log_manager_error
from starthinker_ui.ui.log import log_job_timeout, log_job_error, log_job_start, log_job_end, log_job_cancel
from starthinker_ui.ui.log import log_verbose, get_instance_name


MANAGER_ON = True
def signal_exit(self, signum):
  global MANAGER_ON
  MANAGER_ON = False

signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class Workers():

  def __init__(self, uid, jobs_maximum, timeout_seconds):
    self.uid = uid or get_instance_name(str(uuid.uuid1()))
    self.timeout_seconds = timeout_seconds
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

    job['job']['process'] = subprocess.Popen(command, shell=False, cwd=settings.UI_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    except Exception, e:
      log_manager_error(traceback.format_exc())
    self.lock_thread.release()


  def cleanup(self, job):
    filename = '%s/%s.json' % (settings.UI_CRON, job['job']['id'])
    if os.path.exists(filename):
      os.remove(filename)
    else:
      print "The file does not exist:", filename


  def ping(self):
    # update all jobs belonging to worker
    while not self.ping_event.wait(JOB_INTERVAL_MS / 1000):
      self.lock_thread.acquire()
      try:
        worker_ping(self.uid, [job['recipe']['setup']['uuid'] for job in self.jobs])
      except Exception, e:
        log_manager_error(traceback.format_exc())
      self.lock_thread.release()


  def poll(self):

    self.lock_thread.acquire()

    for job in self.jobs:

      # if process still running, check timeout or ping keep alive 
      poll = job['job']['process'].poll()
      if poll is None:

        # check if task is a timeout 
        if (datetime.utcnow() - job['job']['utc']).total_seconds() > job['recipe']['setup']['timeout_seconds']:
          job['job']['process'].kill()
          self.cleanup(job)
          worker_status(
            job['job']['worker'],
            job['recipe']['setup']['uuid'],
            job['script'],
            job['instance'],
            job['hour'],
            'JOB_TIMEOUT',
            '',
            ''
          )
          log_job_timeout(job)
          job['job']['process'] = None

        # otherwise task is running, do nothing
        else:
          pass

      # if process has return code, check if task is complete or error
      else:
        job['stdout'], job['stderr'] = job['job']['process'].communicate()
        self.cleanup(job)

        # if error scrap whole worker and flag error
        if job['stderr']: # possibly alter this to use poll != 0 ( which indicates errror as well )
          self.cleanup(job)
          worker_status(
            job['job']['worker'],
            job['recipe']['setup']['uuid'],
            job['script'],
            job['instance'],
            job['hour'],
            'JOB_ERROR',
            job['stdout'],
            job['stderr']
          )
          log_job_error(job)
          job['job']['process'] = None

        # if success, pop task off the stack and flag success
        else: 
          worker_status(
            job['job']['worker'],
            job['recipe']['setup']['uuid'],
            job['script'],
            job['instance'],
            job['hour'],
            'JOB_END',
            job['stdout'],
            job['stderr']
          )
          log_job_end(job)
          job['job']['process'] = None

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
      '--test',
      action='store_true',
      dest='test',
      default=False,
      help='Set test mode to execute loop only once and return workers.',
    )

  def handle(self, *args, **kwargs):
    global MANAGER_ON
    MANAGER_ON = True

    print 'Starting Up...'

    if kwargs['verbose']: log_verbose()

    log_manager_start()

    workers = Workers(
      kwargs['worker'], 
      kwargs['jobs'], 
      kwargs['timeout'],
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
    except Exception, e:
      log_manager_error(traceback.format_exc())

    print 'Shutting Down...'
    workers.shutdown()

    log_manager_end()
