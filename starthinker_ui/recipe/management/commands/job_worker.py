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
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker_ui.recipe.models import worker_pull, worker_status, worker_ping, utc_milliseconds, JOB_LOOKBACK_MS, JOB_INTERVAL_MS
from starthinker_ui.ui.log import log_manager_start, log_manager_end, log_manager_error
from starthinker_ui.ui.log import log_job_timeout, log_job_error, log_job_start, log_job_end
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


  def available(self):
    return self.jobs_maximum - len(self.jobs)


  def pull(self):
    jobs = worker_pull(self.uid, jobs=self.available())
    for job in jobs: 
      self.run(job)
    

  def run(self, job, force=False):
   

    self.jobs.append(job)

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


  def cleanup(self, job):
    filename = '%s/%s.json' % (settings.UI_CRON, job['job']['id'])
    if os.path.exists(filename):
      os.remove(filename)
    else:
      print "The file does not exist:", filename


  def poll(self):

    for job in self.jobs:

      # if process still running, check timeout or ping keep alive 
      if job['job']['process'].poll() is None:

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

        # otherwise ping keep alive
        else:
          worker_ping(job['job']['worker'], job['recipe']['setup']['uuid'])

      # if process has return code, check if task is complete or error
      else:
        job['stdout'], job['stderr'] = job['job']['process'].communicate()
        self.cleanup(job)

        # if error scrap whole worker and flag error
        if job['stderr']: 
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

    # if workers remain, return True
    return bool(self.jobs)


  def shutdown(self):
    while self.poll():
      time.sleep(JOB_INTERVAL_MS / 1000)


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
      default=60 * 60 * 8, # 8 hours
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

    workers = Workers(
      kwargs['worker'], 
      kwargs['jobs'], 
      kwargs['timeout'],
    ) 

    log_manager_start()

    try:

      while MANAGER_ON:

        # track loop time
        run_start = utc_milliseconds()

        # load new workers
        workers.pull()

        # check on existing workers
        if workers.poll():

          # flag any runs that exceed lookback interval
          runtime_ms = utc_milliseconds() - run_start
          runtime_percent = (runtime_ms * 100) / JOB_LOOKBACK_MS
          print 'Run Time ( milliseconds ): %d %d%%' % (runtime_ms, runtime_percent)
          if (runtime_ms > JOB_LOOKBACK_MS):
            log_manager_error('Caution: Worker exceeded JOB_INTERVAL_MS by %d%%.' % runtime_percent)
            # possibly check each job and cancel if no longer owner

          # if extermely short run ( jobs in queue but no responses yet, wait 1/2 an interval)
          elif (runtime_ms < JOB_INTERVAL_MS):
            time.sleep(((JOB_INTERVAL_MS - runtime_ms) / 1000 / 2))

        else:
          runtime_ms = utc_milliseconds() - run_start
          print 'Run Time ( milliseconds ): %d %d%%' % (runtime_ms, (runtime_ms * 100) / JOB_LOOKBACK_MS)
          # if no workers sleep for a bit ( wait for next wave of jobs )
          time.sleep(JOB_LOOKBACK_MS / 1000)

        # if test run, then exit after first loop and return workers for inspection
        if kwargs['test']: 
          MANAGER_ON = False

    except KeyboardInterrupt:
      MANAGER_ON = False
    except Exception, e:
      log_manager_error(traceback.format_exc())

    print 'Shutting Down...'
    workers.shutdown()

    log_manager_end()
