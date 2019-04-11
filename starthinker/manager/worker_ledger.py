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
import traceback
import copy
import pickle
from subprocess import Popen
from datetime import datetime, timedelta

from starthinker.manager.log import log_job_complete, log_job_timeout, log_job_fail

workers_file_name = 'workers'

_workers = []
_need_restart = False


def _kill_worker(worker):
  global _need_restart

  kill = Popen(['docker', 'kill', worker['worker']['container_name']])
  try:
    kill.wait(timeout=300)
  except Exception as e:
    _need_restart = True

  # this shouldn't log timeout, if the job was cancelled need to log different status
  #
  # (mauriciod) Yes, it is timeout, the only reason workers are killed is
  # because they timed out
  log_job_timeout(worker)
  if 'job_file_name' in worker and os.path.exists(
      worker['worker']['job_file_name']):
    os.remove(worker['worker']['job_file_name'])

def cancel_job(job_id):
  global _workers
  result = False

  new_workers = []
  for worker in _workers:
    if worker['setup']['uuid'] == job_id:
      _kill_worker(worker)
      result = True
    else:
      new_workers += [worker]

  set_workers(new_workers)

  return result

def update_workers():
  global _workers
  global _need_restart

  if _need_restart and not _workers:
    Popen(['sudo', 'reboot'])
    return

  new_workers = []

  for worker in _workers:
    try:
      if datetime.utcnow() > (worker['worker']['start_datetime'] + timedelta(seconds=worker['setup']['timeout_seconds'])):
        _kill_worker(worker)

      else:
        worker['worker']['job'].poll()

        if worker['worker']['job'].returncode == None:
          new_workers += [worker]
        else:
          worker['worker']['end_datetime'] = datetime.now()
          if worker['worker']['job'].returncode == 0:
            log_job_complete(worker)
          else:
            log_job_fail(worker)
          os.remove(worker['worker']['job_file_name'])
    except:
      traceback.print_exc()
      pass

  set_workers(new_workers)


def set_workers(workers):
  global _workers

  _workers = workers

def get_workers():
  global _workers

  return _workers
