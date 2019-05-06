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
from time import time, sleep

from datetime import datetime
from django.test import TestCase
from django.core import management

from starthinker_ui.account.tests import account_create
from starthinker_ui.project.tests import project_create
from starthinker_ui.recipe.models import Recipe, worker_pull, worker_status, worker_ping, utc_milliseconds, utc_to_timezone, JOB_LOOKBACK_MS, time_ago

# starthinker/gtech/script_test.json
#
# Hours will equal 1 + 1 + 1 + n + 3 + 1 where n is the number of hours given in the setup
#
#  { "hello":{ +1 hour
#      "auth":"user",
#      "hour":[1],
#      "say":"Hello At 1",
#      "sleep":0
#    }},
#    { "hello":{ +1 hour
#      "auth":"user",
#      "hour":[3],
#      "say":"Hello At 3",
#      "sleep":0
#    }},
#    { "hello":{ +1 hour
#      "auth":"user",
#      "hour":[23],
#      "say":"Hello At 23 Sleep",
#      "sleep":30
#    }},
#    { "hello":{ + n hours
#      "auth":"user",
#      "say":"Hello At 1, 3, 23 Default",
#      "sleep":0
#    }},
#    { "hello":{ + 3 hours
#      "auth":"user",
#      "hour":[1, 3, 23],
#      "say":"Hello At 1, 3, 23 Explicit",
#      "sleep":0
#    }},
#    { "hello":{ + 1 hour
#      "auth":"user",
#      "hour":[3],
#      "say":"Hello At 3 Reorder",
#      "sleep":0
#    }}


class StatusTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.recipe = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_NEW',
      active = True,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([1,3,23]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "test",
          "values": {},
          "sequence": 1
        },
      ]),
    )

  def test_status(self):
    status = self.recipe.get_status()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())
    hour_tz = now_tz.hour

    self.assertEqual(status['date_tz'], date_tz)
    self.assertEqual(len(status['tasks']), 1 + 1 + 1 + 3 + 3 + 1)
    self.assertFalse(status['force'])

    self.assertEqual(status['tasks'][0]['hour'], 1)
    self.assertEqual(status['tasks'][0]['order'], 0)
    self.assertEqual(status['tasks'][1]['hour'], 1)
    self.assertEqual(status['tasks'][1]['order'], 3)
    self.assertEqual(status['tasks'][2]['hour'], 1)
    self.assertEqual(status['tasks'][2]['order'], 4)
    self.assertEqual(status['tasks'][3]['hour'], 3)
    self.assertEqual(status['tasks'][3]['order'], 1)
    self.assertEqual(status['tasks'][4]['hour'], 3)
    self.assertEqual(status['tasks'][4]['order'], 3)
    self.assertEqual(status['tasks'][5]['hour'], 3)
    self.assertEqual(status['tasks'][5]['order'], 4)
    self.assertEqual(status['tasks'][6]['hour'], 3)
    self.assertEqual(status['tasks'][6]['order'], 5)
    self.assertEqual(status['tasks'][7]['hour'], 23)
    self.assertEqual(status['tasks'][7]['order'], 2)
    self.assertEqual(status['tasks'][8]['hour'], 23)
    self.assertEqual(status['tasks'][8]['order'], 3)
    self.assertEqual(status['tasks'][9]['hour'], 23)
    self.assertEqual(status['tasks'][9]['order'], 4)


  def test_all_hours(self):
    self.recipe.hour = json.dumps([])
    self.recipe.save() 

    status = self.recipe.get_status()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())

    self.assertEqual(status['date_tz'], date_tz)
    self.assertEqual(len(status['tasks']), 1 + 1 + 1 + 24 + 3 + 1) 
    self.assertFalse(status['force'])


  def test_forced(self):
    self.recipe.run(force=True, remote=True)
    status = self.recipe.get_status()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())

    self.assertEqual(status['date_tz'], date_tz)
    self.assertTrue(status['force'])
    self.assertEqual(len(status['tasks']), len(self.recipe.get_json()['tasks'])) 


  def test_hour_pulls(self):
    hour_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone).hour

    if hour_tz == 23:
      print 'SKIPPING test_hour_pulls, need 1 spare hour for test.'
    else:
      task = self.recipe.get_task()
      while task != None:
        self.recipe.set_task(task['script'], task['instance'], task['hour'], 'JOB_END', 'Some output.', '')
        task = self.recipe.get_task()

      status = self.recipe.get_status()
      
      self.assertTrue(
        all([
          (task['done'] and task['hour'] <= hour_tz) or (not task['done'] and task['hour'] > hour_tz)
          for task in status['tasks']
        ])
      )


  def test_worker(self):

    # remove time dependency for this test, force all tasks
    self.recipe.force()
    status = self.recipe.get_status()

    for task in status['tasks']:

      job = worker_pull('SAMPLE_WORKER', jobs=1)
      self.assertEqual(len(job), 1)
      job = job[0]

      self.assertEqual(job['event'], 'JOB_PENDING')
      self.assertEqual(job['instance'], task['instance'])
      self.assertEqual(job['hour'], task['hour'])

      # job is not run through actual worker, so 'job' key will be missing, simulate it
      job['job'] = {
        'worker':'SAMPLE_WORKER',
        'id':'SAMPLE_JOB_UUID',
        'process':None,
        'utc':datetime.utcnow(),
      }

      worker_status(
        job['job']['worker'],
        job['recipe']['setup']['uuid'],
        job['script'],
        job['instance'],
        job['hour'],
        'JOB_END',
        "Output is OK.",
        ""
      )

      sleep((JOB_LOOKBACK_MS * 2) / 1000.0)

    # after completing all tasks, check if they whole recipe is done
    self.recipe.refresh_from_db()
    self.assertTrue(self.recipe.job_done)
    status = self.recipe.get_status()
    self.assertTrue(
      all([
        (task['event'] == 'JOB_END')
        for task in status['tasks']
      ])
    )


  def test_log(self):
    log = self.recipe.get_log()

    #print json.dumps(log, indent=2, default=str)

    self.assertEqual(log["ago"], "1 Minute Ago") 
    self.assertFalse(log["force"])
    self.assertEqual(log["uid"], self.recipe.uid())
    self.assertEqual(log["percent"], 0) 
    self.assertEqual(log["status"], "QUEUED")


class RecipeViewTest(TestCase):

  def test_recipe_list(self):
    resp = self.client.get('/')
    self.assertEqual(resp.status_code, 200)


  def test_recipe_edit(self):
    resp = self.client.get('/recipe/edit/')
    self.assertEqual(resp.status_code, 302)


class JobTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.job_new = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_NEW',
      active = True,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello", 
          "values": {"say_first":"Hi Once", "say_second":"Hi Twice", "sleep":0},
          "sequence": 1
        },
      ]),
    )
    self.RECIPE_NEW = self.job_new.uid()

    self.job_expired = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_EXPIRED',
      active = True,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello", 
          "values": {"say_first":"Hi Once", "say_second":"Hi Twice", "sleep":0},
          "sequence": 1
        },
      ]),
      job_done = False,
      worker_uid = "SAMPLE_WORKER",
      worker_utm = utc_milliseconds() - (JOB_LOOKBACK_MS * 2)
    )
    self.RECIPE_EXPIRED = self.job_expired.uid()

    self.job_running = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_RUNNING',
      active = True,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello", 
          "values": {"say_first":"Hi Once", "say_second":"Hi Twice", "sleep":0},
          "sequence": 1
        }
      ]),
      job_done = False,
      worker_uid = "OTHER_WORKER",
      worker_utm = utc_milliseconds()
    )
    self.RECIPE_RUNNING = self.job_running.uid()

    self.job_paused = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_PAUSED',
      active = False,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello", 
          "values": {"say_first":"Hi Once", "say_second":"Hi Twice", "sleep":0},
          "sequence": 1
        }
      ]),
      job_done = False,
      worker_uid = "OTHER_WORKER",
      worker_utm = utc_milliseconds() - (JOB_LOOKBACK_MS * 10)
    )
    self.RECIPE_PAUSED = self.job_paused.uid()

    # paused so its not part of the normal flow ( unpause to use in test )
    self.job_error = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_ERROR',
      active = False,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello", 
          "values": {"say_first":"Hi Once", "say_second":"Hi Twice", "sleep":0, "errror":"An error is triggered."},
          "sequence": 1
        },
      ]),
      job_done = False,
      worker_uid = "",
      worker_utm = 0
    )
    self.RECIPE_ERROR = self.job_error.uid()


  def test_single_pulls(self):

    # first pull new task 1
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_NEW)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

    # second pull expired task 1
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_EXPIRED)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

    # third pull is blank since all recipes have been pulled from
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 0)

    # expire all workers except OTHER_WORKER / RECIPE_RUNNING
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', self.RECIPE_RUNNING)

    # get oldest expired job first ( redo task since it never completes )
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_NEW)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)


  def test_multiple_pulls(self):

    # pull all jobs at once
    jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 2)

    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_NEW)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

    self.assertEqual(jobs[1]['recipe']['setup']['uuid'], self.RECIPE_EXPIRED)
    self.assertEqual(jobs[1]['script'], 'hello')
    self.assertEqual(jobs[1]['instance'], 1)
    self.assertEqual(jobs[1]['hour'], 0)


  def test_manager(self):

    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)
    
    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 2)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_END')
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_PENDING')

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', self.RECIPE_RUNNING)

    # second loop through manager
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 2)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_END')
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_END')

    # jobs were also marked as complete
    self.assertTrue(jobs[0].job_done)
    self.assertTrue(jobs[1].job_done)

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', self.RECIPE_RUNNING)

    # all jobs either run by other workers or done
    jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 0)


class JobErrorTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.recipe = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_NEW',
      active = True,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello",
          "values": { "error":"Triggered the error mchanic on purspose."},
          "sequence": 1
        },
      ]),
    )

  def test_manager_error(self):

    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 1)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_ERROR')
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_PENDING')

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)

    # second loop through manager
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 1)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_ERROR')
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_END')

    # check if recipe is removed from worker lookup ( job_done=True )
    self.recipe.refresh_from_db()
    self.assertTrue(self.recipe.job_done)


class JobTimeoutTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.recipe = Recipe.objects.create(
      account = self.account,
      project = self.project,
      name = 'RECIPE_NEW',
      active = True,
      week = json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
      hour = json.dumps([0]),
      timezone = 'America/Los_Angeles',
      tasks = json.dumps([
        { "tag": "hello",
          "values": { "sleep":15 }, # seconds
          "sequence": 1
        },
      ]),
    )

  def test_manager_timeout(self):

    # first loop through manager ( use short timeout )
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=5, verbose=True, test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 1)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_TIMEOUT')
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_PENDING')

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)

    # second loop through manager ( use normal timeout )
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 1)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_TIMEOUT')
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_END')

    # check if recipe is removed from worker lookup ( job_done=True )
    self.recipe.refresh_from_db()
    self.assertTrue(self.recipe.job_done)

