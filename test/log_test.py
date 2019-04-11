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


import json
import copy
from time import sleep
from uuid import uuid1
from datetime import date
from datetime import datetime
from subprocess import Popen, PIPE

from starthinker.manager.log import log_job_receive, log_job_bounce, log_job_cancel, log_job_duplicate, log_job_start, log_job_fail, log_job_complete, log_job_timeout, log_job_exception, log_job_task_start, log_job_task_complete, log_manager_start, log_manager_error, log_manager_exception, log_get


TEST_RECIPE = {
  "script":{
    "license":"Apache License, Version 2.0",
    "copyright":"Copyright 2018 Google Inc.",
    "icon":"folder",
    "product":"gTech",
    "title":"Sample Recipe",
    "description":"Used for testing.",
    "instructions":[
      "Import this recipe.",
      "Pass it to a test.",
      "Make test pass."
    ],
    "authors":["kenjora@google.com"]
  },
  "setup":{
    "uuid":"RECIPE_UUID",
    "id": "cloud-project-id", 
    "timezone": "America/Los_Angeles",
    "day":["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "hour":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
  },
  "tasks":[
    { "hello":{
        "auth":"user",
        "say":"Task One"
    }},
    { "hello":{
        "auth":"user",
        "say":"Task Two"
    }}
  ]
}

def log_test(
    uid,
    job_recieve=False,
    job_bounce=False,
    job_cancel=False,
    job_duplicate=False,
    job_exception=False,
    job_start=False,
    job_task_1=False,
    job_task_2=False,
    job_fail=False,
    job_complete=False,
    job_timeout=False
  ):


  recipe = copy.deepcopy(TEST_RECIPE)
  recipe['setup']['uuid'] = uid

  job_id = str(uuid1())

  if job_start:
    recipe['worker'] = {
      'container_name': job_id,
      'job': Popen('echo "PROCESS RAN"', shell=True, stdout=PIPE, stderr=PIPE),
      'start_datetime': datetime.utcnow(),
      'job_file_name': '/tmp/%s' % job_id,
      'job_date':str(date.today()),
    }

  if job_recieve: log_job_receive(recipe)
  if job_bounce: log_job_bounce(recipe)
  if job_duplicate: log_job_duplicate(recipe)
  if job_exception: log_job_exception(recipe, 'Incoming message failed to deploy as recipe.')
  if job_start: log_job_start(recipe)
  if job_task_1: log_job_task_start(recipe, 'hello', 1)
  if job_task_1 and not (job_fail or job_timeout): log_job_task_complete(recipe, 'hello', 1, 'Task 1 test output.', 'Task 1 test error' if job_fail else '')
  if job_task_2: log_job_task_start(recipe, 'hello', 2)
  if job_task_2 and not (job_fail or job_timeout): log_job_task_complete(recipe, 'hello', 2, 'Task 2 test output.', 'Task 2 test error' if job_fail else '')
  if job_fail: log_job_fail(recipe)
  if job_complete: log_job_complete(recipe)
  if job_timeout: log_job_timeout(recipe)
  if job_cancel: log_job_cancel(recipe)

if __name__ == '__main__':

  log_manager_start()
  log_manager_exception('Testing log manager exception messsage.')
  log_manager_error('Testing log manager error messsage.')

  # Test all logs
  log_test(
     'RECIPE_ALL',
    job_recieve=True,
    job_bounce=True,
    job_cancel=True,
    job_duplicate=True,
    job_exception=True,
    job_start=True,
    job_task_1=True,
    job_task_2=True,
    job_fail=True,
    job_complete=True,
    job_timeout=True
  )

  # Test bounce log
  log_test(
    'RECIPE_BOUNCE',
    job_recieve=True,
    job_bounce=True,
  )

  # Test duplicate log
  log_test(
    'RECIPE_DUPLICATE',
    job_recieve=True,
    job_duplicate=True,
  )

  # Test cancel log
  log_test(
    'RECIPE_CANCEL',
    job_recieve=True,
    job_start=True,
    job_task_1=True,
    job_cancel=True,
  )

  # Test fail log
  log_test(
    'RECIPE_FAIL',
    job_recieve=True,
    job_start=True,
    job_task_1=True,
    job_fail=True,
  )

  # Test fail log
  log_test(
    'RECIPE_TIMEOUT',
    job_recieve=True,
    job_start=True,
    job_task_1=True,
    job_timeout=True,
  )

  # Test complete log
  log_test(
    'RECIPE_COMPLETE',
    job_recieve=True,
    job_start=True,
    job_task_1=True,
    job_task_2=True,
    job_complete=True,
  )

  # Test parts log
  log_test(
    'RECIPE_PARTS',
    job_recieve=True,
    job_start=True,
    job_task_1=True,
    job_complete=True,
  )

  # Test parts log
  log_test(
    'RECIPE_PARTS',
    job_recieve=True,
    job_start=True,
    job_task_2=True,
    job_complete=True,
  )

  sleep(5) # could be a problem for is_running if there is a delay, but there is

  print 'Fetch all logs...'
  logs = log_get()
  print json.dumps(logs, indent=2, default=str)

  print 'Fetch single log...'
  log = log_get('RECIPE_COMPLETE')
  print json.dumps(log, indent=2, default=str)


