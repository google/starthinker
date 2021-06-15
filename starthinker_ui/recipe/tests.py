###########################################################################
#
#  Copyright 2020 Google LLC
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
import pytz
from time import time, sleep
from datetime import date, datetime, timedelta

from django.core import management
from django.conf import settings
from django.test import TestCase
from django.test.testcases import TransactionTestCase

from starthinker_ui.account.tests import account_create
from starthinker_ui.project.tests import project_create
from starthinker_ui.recipe.models import Recipe, utc_milliseconds, utc_to_timezone, timezone_to_utc, utc_milliseconds_to_timezone, JOB_INTERVAL_MS, JOB_LOOKBACK_MS, time_ago
from starthinker_ui.recipe.views import autoscale
from starthinker_ui.recipe.management.commands.job_worker import Workers, worker_pull, worker_status, worker_ping, worker_downscale

# test recipe done to undone

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

WORKER_LOOKBACK_EXPIRE = (JOB_LOOKBACK_MS + 1000)


def test_job_utm(hour=0, days_offset=0):
  utc = datetime.utcnow().replace(hour=hour, minute=0, second=0, microsecond=0)
  if days_offset:
    utc += timedelta(days=days_offset)
  return utc_milliseconds(utc)


def assertRecipeDone(cls, recipe):
  recipe.refresh_from_db()
  status = recipe.get_status()
  job_time = datetime.utcfromtimestamp(int(recipe.job_utm / 1000))

  cls.assertTrue(all(task['done'] == True for task in status['tasks']))
  if recipe.manual:
    cls.assertEqual(recipe.job_utm, 0)
  else:
    cls.assertGreater(recipe.job_utm, utc_milliseconds())
  cls.assertEqual(job_time.minute, 0)


def assertRecipeNotDone(cls, recipe):
  recipe.refresh_from_db()
  status = recipe.get_status()
  job_time = datetime.utcfromtimestamp(int(recipe.job_utm / 1000))

  cls.assertFalse(all(task['done'] == True for task in status['tasks']))
  cls.assertLessEqual(recipe.job_utm, utc_milliseconds())
  cls.assertEqual(job_time.minute, 0)


class StatusTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.recipe = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NEW',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([1, 3, 23]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'test',
                'values': {},
                'sequence': 1
            },
        ]),
    )

  def test_interval(self):
    self.assertNotEqual(JOB_INTERVAL_MS / 1000, 0)

  def test_time(self):
    utc_now = datetime.utcnow().replace(second=0, microsecond=0)
    tz_now = datetime.now(tz=pytz.timezone(self.recipe.timezone)).replace(
        second=0, microsecond=0)

    utm = utc_milliseconds(utc_now)
    tz1 = utc_milliseconds_to_timezone(utm, self.recipe.timezone)
    tz2 = utc_to_timezone(utc_now, self.recipe.timezone)
    tz3 = timezone_to_utc(tz_now)

    self.assertEqual(tz1, tz2)
    self.assertEqual(tz3, utc_now)

  def test_schedule(self):
    tz_now = datetime.now(tz=pytz.timezone(self.recipe.timezone)).replace(
        second=0, microsecond=0)

    # pull new recipe, nothing in it until update is called
    status = self.recipe.get_status()

    self.assertEqual(status['date_tz'], str(tz_now.date()))
    self.assertEqual(status['tasks'], [])

    # causes recipe status to be filled in
    status = self.recipe.update()

    # new recipe
    job_utm = self.recipe.get_job_utm(status)
    tz_recipe = utc_milliseconds_to_timezone(job_utm, self.recipe.timezone)

    self.assertEqual(tz_recipe.date(), tz_now.date() + timedelta(days=1))
    self.assertEqual(tz_recipe.hour, self.recipe.get_hours()[0])

    # done recipe
    for task in status['tasks']:
      task['done'] = True

    job_utm = self.recipe.get_job_utm(status)
    tz_recipe = utc_milliseconds_to_timezone(job_utm, self.recipe.timezone)

    self.assertEqual(tz_recipe.date(), tz_now.date() + timedelta(days=1))
    self.assertEqual(tz_recipe.hour, self.recipe.get_hours()[0])

    # forced recipe
    status = self.recipe.force()

    job_utm = self.recipe.get_job_utm(status)
    tz_recipe = utc_milliseconds_to_timezone(job_utm, self.recipe.timezone)

    self.assertEqual(tz_recipe.date(), tz_now.date())
    self.assertEqual(tz_recipe.hour, tz_now.hour)

    # cancelled recipe
    status = self.recipe.cancel()

    job_utm = self.recipe.get_job_utm(status)
    tz_recipe = utc_milliseconds_to_timezone(job_utm, self.recipe.timezone)

    self.assertEqual(tz_recipe.date(), tz_now.date() + timedelta(days=1))
    self.assertEqual(tz_recipe.hour, self.recipe.get_hours()[0])

  def test_status(self):
    status = self.recipe.update()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())
    hour_tz = now_tz.hour

    self.assertEqual(status['date_tz'], date_tz)
    self.assertEqual(len(status['tasks']), 1 + 1 + 1 + 3 + 3 + 1)

    # order two is hidden unless forced ( so it is skipped ) hour = [] excludes it from list
    # each task runs multiple hours, hence repeats
    self.assertEqual(status['tasks'][0]['hour'], 1)
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][1]['hour'], 1)
    self.assertEqual(status['tasks'][1]['instance'], 5)
    self.assertEqual(status['tasks'][2]['hour'], 1)
    self.assertEqual(status['tasks'][2]['instance'], 6)
    self.assertEqual(status['tasks'][3]['hour'], 3)
    self.assertEqual(status['tasks'][3]['instance'], 2)
    self.assertEqual(status['tasks'][4]['hour'], 3)
    self.assertEqual(status['tasks'][4]['instance'], 5)
    self.assertEqual(status['tasks'][5]['hour'], 3)
    self.assertEqual(status['tasks'][5]['instance'], 6)
    self.assertEqual(status['tasks'][6]['hour'], 3)
    self.assertEqual(status['tasks'][6]['instance'], 7)
    self.assertEqual(status['tasks'][7]['hour'], 23)
    self.assertEqual(status['tasks'][7]['instance'], 4)
    self.assertEqual(status['tasks'][8]['hour'], 23)
    self.assertEqual(status['tasks'][8]['instance'], 5)
    self.assertEqual(status['tasks'][9]['hour'], 23)
    self.assertEqual(status['tasks'][9]['instance'], 6)

  def test_all_hours(self):

    # reduce the hours so that fewer permutations are created
    self.recipe.hour = json.dumps([])
    self.recipe.save()
    self.recipe.update()

    status = self.recipe.get_status()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())

    self.assertEqual(status['date_tz'], date_tz)
    self.assertEqual(len(status['tasks']), 1 + 1 + 1 + 0 + 3 + 1)

  def test_forced(self):
    status = self.recipe.force()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())

    self.assertEqual(status['date_tz'], date_tz)
    self.assertEqual(len(status['tasks']), len(self.recipe.get_json()['tasks']))

    # includes all tasks in sequence including hours=[], normally #2 is skipped
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][2]['instance'], 3)
    self.assertEqual(status['tasks'][3]['instance'], 4)
    self.assertEqual(status['tasks'][4]['instance'], 5)
    self.assertEqual(status['tasks'][5]['instance'], 6)
    self.assertEqual(status['tasks'][6]['instance'], 7)

  def test_canceled(self):
    self.recipe.force()
    status = self.recipe.get_status()

    self.assertFalse(status['tasks'][0]['done'])
    self.assertEqual(status['tasks'][0]['event'], 'JOB_PENDING')
    self.assertFalse(status['tasks'][1]['done'])
    self.assertEqual(status['tasks'][1]['event'], 'JOB_PENDING')
    self.assertFalse(status['tasks'][2]['done'])
    self.assertEqual(status['tasks'][2]['event'], 'JOB_PENDING')
    self.assertFalse(status['tasks'][3]['done'])
    self.assertEqual(status['tasks'][3]['event'], 'JOB_PENDING')
    self.assertFalse(status['tasks'][4]['done'])
    self.assertEqual(status['tasks'][4]['event'], 'JOB_PENDING')
    self.assertFalse(status['tasks'][5]['done'])
    self.assertEqual(status['tasks'][5]['event'], 'JOB_PENDING')
    self.assertFalse(status['tasks'][6]['done'])
    self.assertEqual(status['tasks'][6]['event'], 'JOB_PENDING')
    self.assertEqual(self.recipe.job_utm, self.recipe.get_job_utm(status))

    self.recipe.cancel()
    status = self.recipe.get_status()

    self.assertTrue(status['tasks'][0]['done'])
    self.assertEqual(status['tasks'][0]['event'], 'JOB_CANCEL')
    self.assertTrue(status['tasks'][1]['done'])
    self.assertEqual(status['tasks'][1]['event'], 'JOB_CANCEL')
    self.assertTrue(status['tasks'][2]['done'])
    self.assertEqual(status['tasks'][2]['event'], 'JOB_CANCEL')
    self.assertTrue(status['tasks'][3]['done'])
    self.assertEqual(status['tasks'][3]['event'], 'JOB_CANCEL')
    self.assertTrue(status['tasks'][4]['done'])
    self.assertEqual(status['tasks'][4]['event'], 'JOB_CANCEL')
    self.assertTrue(status['tasks'][5]['done'])
    self.assertEqual(status['tasks'][5]['event'], 'JOB_CANCEL')
    self.assertTrue(status['tasks'][6]['done'])
    self.assertEqual(status['tasks'][6]['event'], 'JOB_CANCEL')
    self.assertEqual(self.recipe.job_utm, self.recipe.get_job_utm(status))

  def test_hour_pulls(self):
    hour_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone).hour

    if hour_tz == 23:
      print('SKIPPING test_hour_pulls, need 1 spare hour for test.')
    else:
      task = self.recipe.get_task()
      while task != None:
        self.recipe.set_task(task['script'], task['instance'], task['hour'],
                             'JOB_END', 'Some output.', '')
        task = self.recipe.get_task()

      status = self.recipe.get_status()

      self.assertTrue(
          all([(task['done'] and task['hour'] <= hour_tz) or
               (not task['done'] and task['hour'] > hour_tz)
               for task in status['tasks']]))

  def test_worker(self):

    # remove time dependency for this test, force all tasks
    self.recipe.force()
    status = self.recipe.get_status()

    for task in status['tasks']:

      ignore, job = worker_pull('SAMPLE_WORKER', jobs=1)
      self.assertEqual(len(job), 1)
      job = job[0]

      self.assertEqual(job['event'], 'JOB_PENDING')
      self.assertEqual(job['instance'], task['instance'])
      self.assertEqual(job['hour'], task['hour'])

      # job is not run through actual worker, so 'job' key will be missing, simulate it
      job['job'] = {
          'worker': 'SAMPLE_WORKER',
          'id': 'SAMPLE_JOB_UUID',
          'process': None,
          'utc': datetime.utcnow(),
      }

      worker_status(job['job']['worker'], job['recipe']['setup']['uuid'],
                    job['script'], job['instance'], job['hour'], 'JOB_END',
                    'Output is OK.', '')

      sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # after completing all tasks, check if they whole recipe is done
    self.recipe.refresh_from_db()
    assertRecipeDone(self, self.recipe)

    #self.assertGreater(self.recipe.job_utm, utc_milliseconds())

    #status = self.recipe.get_status()
    #self.assertTrue(all(task['event'] == 'JOB_END' for task in status['tasks']))

  def test_log(self):
    self.recipe.update()
    log = self.recipe.get_log()

    self.assertEqual(log['ago'], '1 Minute Ago')
    self.assertEqual(log['uid'], self.recipe.uid())
    self.assertEqual(log['percent'], 0)
    self.assertEqual(log['status'], 'NEW')

    self.recipe.force()
    log = self.recipe.get_log()

    self.assertEqual(log['ago'], '1 Minute Ago')
    self.assertEqual(log['uid'], self.recipe.uid())
    self.assertEqual(log['percent'], 0)
    self.assertEqual(log['status'], 'QUEUED')


class ManualTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.recipe = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_MANUAL',
        active=True,
        manual=True,
        week=[],
        hour=[],
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'manual',
                'values': {},
                'sequence': 1
            },
        ]),
    )
    self.recipe.update()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)

    self.recipe_done = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_MANUAL',
        active=True,
        manual=True,
        week=[],
        hour=[],
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'manual',
                'values': {},
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date()),
            'tasks': [{
                'instance': 1,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow()),
                'script': 'manual',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': True
            }]
        }),
        worker_uid='TEST_WORKER',
        worker_utm=utc_milliseconds() - WORKER_LOOKBACK_EXPIRE)
    self.recipe_done.update()

  def test_done(self):
    self.assertIsNone(self.recipe_done.get_task())
    self.recipe_done.force()
    self.assertIsNotNone(self.recipe_done.get_task())

  def test_status(self):
    # without force manual tasks do not pull
    status = self.recipe.get_status()

    now_tz = utc_to_timezone(datetime.utcnow(), self.recipe.timezone)
    date_tz = str(now_tz.date())
    hour_tz = now_tz.hour

    self.assertEqual(status['date_tz'], date_tz)
    self.assertEqual(len(status['tasks']), 0)

    # force a run now on a manual task
    self.recipe.force()
    status = self.recipe.get_status()
    self.assertEqual(len(status['tasks']), 1)

  def test_worker(self):

    # no jobs
    ignore, job = worker_pull('SAMPLE_WORKER', jobs=0)
    self.assertEqual(len(job), 0)

    # manual mode ( without force always returns no tasks )
    ignore, job = worker_pull('SAMPLE_WORKER', jobs=1)
    self.assertEqual(len(job), 0)

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # remove time dependency for this test, force all tasks in first recipe
    status = self.recipe.force()

    for task in status['tasks']:

      ignore, job = worker_pull('SAMPLE_WORKER', jobs=1)
      self.assertEqual(len(job), 1)
      job = job[0]

      self.assertEqual(job['event'], 'JOB_PENDING')
      self.assertEqual(job['instance'], task['instance'])
      self.assertEqual(job['hour'], task['hour'])

      # job is not run through actual worker, so 'job' key will be missing, simulate it
      job['job'] = {
          'worker': 'SAMPLE_WORKER',
          'id': 'SAMPLE_JOB_UUID',
          'process': None,
          'utc': datetime.utcnow(),
      }

      worker_status(job['job']['worker'], job['recipe']['setup']['uuid'],
                    job['script'], job['instance'], job['hour'], 'JOB_END',
                    'Output is OK.', '')

      sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # after completing all tasks, check if the whole recipe is done
    assertRecipeDone(self, self.recipe)


class RecipeViewTest(TestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    self.recipe_new = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NEW',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'say_first': 'Hi Once',
                    'say_second': 'Hi Twice',
                    'sleep': 0
                },
                'sequence': 1
            },
        ]),
    )
    self.RECIPE_NEW = self.recipe_new.uid()

  def test_recipe_list(self):
    resp = self.client.get('/')
    self.assertEqual(resp.status_code, 200)

  def test_recipe_edit(self):
    resp = self.client.get('/recipe/edit/')
    self.assertEqual(resp.status_code, 302)

  def test_recipe_manual(self):
    resp = self.client.get('/recipe/edit/?manual=true')
    self.assertEqual(resp.status_code, 302)

  def test_recipe_start(self):
    resp = self.client.post('/recipe/start/',
                            {'reference': 'THISREFERENCEISINVALID'})
    self.assertEqual(resp.status_code, 404)
    self.assertEqual(resp.content, b'RECIPE NOT FOUND')

    resp = self.client.post('/recipe/start/',
                            {'reference': self.recipe_new.reference})
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.content, b'RECIPE STARTED')

    # start a recipe run to test interrupt
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 1)

    resp = self.client.post('/recipe/start/',
                            {'reference': self.recipe_new.reference})
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.content, b'RECIPE INTERRUPTED')

  def test_recipe_stop(self):
    resp = self.client.post('/recipe/stop/',
                            {'reference': 'THISREFERENCEISINVALID'})
    self.assertEqual(resp.status_code, 404)
    self.assertEqual(resp.content, b'RECIPE NOT FOUND')

    resp = self.client.post('/recipe/stop/',
                            {'reference': self.recipe_new.reference})
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.content, b'RECIPE STOPPED')

    #self.recipe_new.refresh_from_db()
    #self.assertTrue(self.recipe_new.job_done)
    assertRecipeDone(self, self.recipe_new)

    # recipe is stopped and cannot be pulled
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 0)

    # start a recipe run to test interrupt
    resp = self.client.post('/recipe/start/',
                            {'reference': self.recipe_new.reference})
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.content, b'RECIPE STARTED')

    #self.recipe_new.refresh_from_db()
    #self.assertFalse(self.recipe_new.job_done)
    assertRecipeNotDone(self, self.recipe_new)

    # wait for next worker cycle
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # recipe is started and can be pulled
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 1)

    resp = self.client.post('/recipe/stop/',
                            {'reference': self.recipe_new.reference})
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.content, b'RECIPE INTERRUPTED')

    self.recipe_new.refresh_from_db()
    #self.assertTrue(self.recipe_new.job_done)
    assertRecipeDone(self, self.recipe_new)

    # wait for next worker cycle
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # recipe is stopped and cannot be pulled
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 0)


class JobTest(TransactionTestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    now_tz = utc_to_timezone(datetime.utcnow(), 'America/Los_Angeles')
    status = {
        'date_tz':
            str(now_tz.date()),
        'tasks': [
            {
                'instance': 1,
                'event': 'JOB_PENDING',
                'utc': str(datetime.utcnow()),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': False
            },
            {
                'instance': 2,
                'event': 'JOB_PENDING',
                'utc': str(datetime.utcnow()),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': False
            },
        ]
    }

    self.job_new = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NEW',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'say_first': 'Hi Once',
                    'say_second': 'Hi Twice',
                    'sleep': 0
                },
                'sequence': 1
            },
        ]),
    )
    self.RECIPE_NEW = self.job_new.uid()

    self.job_queued = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_QUEUED',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'say_first': 'Hi Once',
                    'say_second': 'Hi Twice',
                    'sleep': 0
                },
                'sequence': 1
            },
        ]),
        job_status=json.dumps(status.copy()),
        job_utm=test_job_utm())
    self.RECIPE_QUEUED = self.job_queued.uid()

    self.job_expired = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_EXPIRED',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'say_first': 'Hi Once',
                    'say_second': 'Hi Twice',
                    'sleep': 0
                },
                'sequence': 1
            },
        ]),
        job_status=json.dumps(status.copy()),
        job_utm=test_job_utm(),
        worker_uid='SAMPLE_WORKER',
        worker_utm=utc_milliseconds() - WORKER_LOOKBACK_EXPIRE)
    self.RECIPE_EXPIRED = self.job_expired.uid()

    self.job_running = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_RUNNING',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([{
            'tag': 'hello',
            'values': {
                'say_first': 'Hi Once',
                'say_second': 'Hi Twice',
                'sleep': 0
            },
            'sequence': 1
        }]),
        job_status=json.dumps(status.copy()),
        job_utm=test_job_utm(),
        worker_uid='OTHER_WORKER',
        worker_utm=utc_milliseconds())
    self.RECIPE_RUNNING = self.job_running.uid()

    self.job_paused = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_PAUSED',
        active=False,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([{
            'tag': 'hello',
            'values': {
                'say_first': 'Hi Once',
                'say_second': 'Hi Twice',
                'sleep': 0
            },
            'sequence': 1
        }]),
        job_status=json.dumps(status.copy()),
        job_utm=test_job_utm(),
        worker_uid='OTHER_WORKER',
        worker_utm=utc_milliseconds() - WORKER_LOOKBACK_EXPIRE)
    self.RECIPE_PAUSED = self.job_paused.uid()

    # paused so its not part of the normal flow ( unpause to use in test )
    self.job_error = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_ERROR',
        active=False,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'say_first': 'Hi Once',
                    'say_second': 'Hi Twice',
                    'sleep': 0,
                    'errror': 'An error is triggered.'
                },
                'sequence': 1
            },
        ]),
        job_status=json.dumps(status.copy()),
        job_utm=test_job_utm(),
        worker_uid='',
        worker_utm=0)
    self.RECIPE_ERROR = self.job_error.uid()

  def test_single_pulls(self):

    # first pull new task 1
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_QUEUED)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

    # second pull expired task 1
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_EXPIRED)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

    # third pull is blank since all recipes have been pulled from
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 0)

    # expire all workers except OTHER_WORKER / RECIPE_RUNNING
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)
    worker_ping('OTHER_WORKER', [self.RECIPE_RUNNING])

    # get oldest expired job first ( redo task since it never completes )
    ignore, jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_QUEUED)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

  def test_multiple_pulls(self):

    # pull all jobs at once
    ignore, jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 2)

    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], self.RECIPE_QUEUED)
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], 0)

    self.assertEqual(jobs[1]['recipe']['setup']['uuid'], self.RECIPE_EXPIRED)
    self.assertEqual(jobs[1]['script'], 'hello')
    self.assertEqual(jobs[1]['instance'], 1)
    self.assertEqual(jobs[1]['hour'], 0)

  def test_manager(self):

    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=60 * 60 * 1,
        verbose=True,
        test=True)

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
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)
    worker_ping('OTHER_WORKER', [self.RECIPE_RUNNING])

    # second loop through manager
    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=60 * 60 * 1,
        verbose=True,
        test=True)

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
    #self.assertTrue(jobs[0].job_done)
    #self.assertTrue(jobs[1].job_done)
    assertRecipeDone(self, jobs[0])
    assertRecipeDone(self, jobs[1])

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)
    worker_ping('OTHER_WORKER', [self.RECIPE_RUNNING])

    # all jobs either run by other workers or done
    ignore, jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 0)


class JobErrorTest(TransactionTestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    now_tz = utc_to_timezone(datetime.utcnow(), 'America/Los_Angeles')

    self.recipe = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NEW',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'error': 'Triggered the error mechanic on purpose.'
                },
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date()),
            'tasks': [
                {
                    'instance': 1,
                    'event': 'JOB_PENDING',
                    'utc': str(datetime.utcnow()),
                    'script': 'hello',
                    'hour': 0,
                    'stdout': '',
                    'stderr': '',
                    'done': False
                },
                {
                    'instance': 2,
                    'event': 'JOB_PENDING',
                    'utc': str(datetime.utcnow()),
                    'script': 'hello',
                    'hour': 0,
                    'stdout': '',
                    'stderr': '',
                    'done': False
                },
            ]
        }),
        job_utm=test_job_utm())

  def test_manager_error(self):

    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=60 * 60 * 1,
        verbose=True,
        test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 1)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_ERROR')
    self.assertIn('PROJECT TASK SAY: Hello Once', status['tasks'][0]['stdout'])
    self.assertIn('Exception: Triggered the error mechanic on purpose.',
                  status['tasks'][0]['stderr'])

    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_PENDING')
    self.assertEqual('', status['tasks'][1]['stdout'])
    self.assertEqual('', status['tasks'][1]['stderr'])

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # second loop through manager
    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=60 * 60 * 1,
        verbose=True,
        test=True)

    jobs = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(jobs), 1)
    status = jobs[0].get_status()
    self.assertEqual(len(status['tasks']), 2)
    self.assertEqual(status['tasks'][0]['script'], 'hello')
    self.assertEqual(status['tasks'][0]['instance'], 1)
    self.assertEqual(status['tasks'][0]['hour'], 0)
    self.assertEqual(status['tasks'][0]['event'], 'JOB_ERROR')
    self.assertIn('PROJECT TASK SAY: Hello Once', status['tasks'][0]['stdout'])
    self.assertIn('Exception: Triggered the error mechanic on purpose.',
                  status['tasks'][0]['stderr'])
    self.assertEqual(status['tasks'][1]['script'], 'hello')
    self.assertEqual(status['tasks'][1]['instance'], 2)
    self.assertEqual(status['tasks'][1]['hour'], 0)
    self.assertEqual(status['tasks'][1]['event'], 'JOB_END')
    self.assertIn('PROJECT TASK SAY: Hello Twice', status['tasks'][1]['stdout'])
    self.assertEqual('', status['tasks'][1]['stderr'])

    # check if recipe is removed from worker lookup ( job_done=True )
    assertRecipeDone(self, self.recipe)


class JobTimeoutTest(TransactionTestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    now_tz = utc_to_timezone(datetime.utcnow(), 'America/Los_Angeles')

    self.recipe = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NEW',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'sleep': 15
                },  # seconds
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date()),
            'tasks': [
                {
                    'instance': 1,
                    'event': 'JOB_PENDING',
                    'utc': str(datetime.utcnow()),
                    'script': 'hello',
                    'hour': 0,
                    'stdout': '',
                    'stderr': '',
                    'done': False
                },
                {
                    'instance': 2,
                    'event': 'JOB_PENDING',
                    'utc': str(datetime.utcnow()),
                    'script': 'hello',
                    'hour': 0,
                    'stdout': '',
                    'stderr': '',
                    'done': False
                },
            ]
        }),
        job_utm=test_job_utm())

  def test_manager_timeout(self):

    # first loop through manager ( use short timeout )
    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=5,
        verbose=True,
        test=True)

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
    sleep(WORKER_LOOKBACK_EXPIRE / 1000)

    # second loop through manager ( use normal timeout )
    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=60 * 60 * 1,
        verbose=True,
        test=True)

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
    assertRecipeDone(self, self.recipe)


class JobDayTest(TransactionTestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    now_tz = utc_to_timezone(datetime.utcnow(), 'America/Los_Angeles')
    today_tz = now_tz.strftime('%a')
    yesterday_tz = (now_tz - timedelta(days=1)).strftime('%a')
    tomorrow_tz = (now_tz + timedelta(days=1)).strftime('%a')

    self.recipe_today = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_TODAY',
        active=True,
        week=json.dumps([today_tz]),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {},
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date()),
            'tasks': [{
                'instance': 1,
                'event': 'JOB_PENDING',
                'utc': str(datetime.utcnow()),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': False
            }, {
                'instance': 2,
                'event': 'JOB_PENDING',
                'utc': str(datetime.utcnow()),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': False
            }]
        }),
        worker_uid='OTHER_WORKER',
        worker_utm=utc_milliseconds() - WORKER_LOOKBACK_EXPIRE,
        job_utm=test_job_utm())

    self.recipe_not_today = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NOT_TODAY',
        active=True,
        week=json.dumps([yesterday_tz, tomorrow_tz]),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {},
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date() - timedelta(days=1)),
            'tasks': [{
                'instance': 1,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow() - timedelta(days=1)),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': True
            }, {
                'instance': 2,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow() - timedelta(days=1)),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': True
            }]
        }),
        worker_uid='OTHER_WORKER',
        worker_utm=utc_milliseconds() - WORKER_LOOKBACK_EXPIRE,
        job_utm=test_job_utm(0, 1))

  def test_job_day(self):
    # test low level pull ( no worker involved )
    self.assertIsNotNone(self.recipe_today.get_task())
    self.assertIsNone(self.recipe_not_today.get_task())

    assertRecipeNotDone(self, self.recipe_today)
    assertRecipeDone(self, self.recipe_not_today)

    # first loop through manager ( use short timeout )
    management.call_command(
        'job_worker',
        worker='TEST_WORKER',
        jobs=5,
        timeout=60,
        verbose=True,
        test=True)

    recipes = Recipe.objects.filter(worker_uid='TEST_WORKER')
    self.assertEqual(len(recipes), 1)
    self.assertEqual(recipes[0].name, 'RECIPE_TODAY')


class JobCancelTest(TransactionTestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    now_tz = utc_to_timezone(datetime.utcnow(), 'America/Los_Angeles')

    self.recipe = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_NEW',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'sleep': 10
                },  # seconds
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date()),
            'tasks': [{
                'instance': 1,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow() - timedelta(days=1)),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': False
            }, {
                'instance': 2,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow() - timedelta(days=1)),
                'script': 'hello',
                'hour': 0,
                'stdout': '',
                'stderr': '',
                'done': False
            }]
        }),
        job_utm=test_job_utm())

    self.workers = Workers('TEST_WORKER', 5, 60)

  def tearDown(self):
    # if your threads are locking in the test, comment out the line below, that will allow the error to be printed before deadlocking
    self.workers.shutdown()

  def test_job_cancel(self):

    self.workers.pull()
    self.assertEqual(len(self.workers.jobs), 1)

    self.workers.poll()
    job = self.workers.jobs[0]
    self.assertEqual(job['job']['worker'], 'TEST_WORKER')
    self.assertEqual(job['recipe']['setup']['uuid'], self.recipe.uid())
    self.assertEqual(job['script'], 'hello')
    self.assertEqual(job['instance'], 1)
    self.assertIsNone(job['job']['process'].poll())

    self.recipe.cancel()

    self.assertEqual(len(self.workers.jobs), 1)
    self.workers.pull()
    self.assertEqual(len(self.workers.jobs), 0)

    assertRecipeDone(self, self.recipe)
    status = self.recipe.get_status()
    self.assertEqual(status['tasks'][0]['event'], 'JOB_CANCEL')

  def test_job_cancel_early(self):

    self.workers.pull()
    self.assertEqual(len(self.workers.jobs), 1)

    self.recipe.cancel()

    self.assertEqual(len(self.workers.jobs), 1)
    self.workers.pull()
    self.assertEqual(len(self.workers.jobs), 0)

    assertRecipeDone(self, self.recipe)
    status = self.recipe.get_status()
    self.assertEqual(status['tasks'][0]['event'], 'JOB_CANCEL')


class WorkerTest(TransactionTestCase):

  def setUp(self):
    self.account = account_create()
    self.project = project_create()

    now_tz = utc_to_timezone(datetime.utcnow(), 'America/Los_Angeles')

    self.job_done = Recipe.objects.create(
        account=self.account,
        project=self.project,
        name='RECIPE_DONE',
        active=True,
        week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        hour=json.dumps([0]),
        timezone='America/Los_Angeles',
        tasks=json.dumps([
            {
                'tag': 'hello',
                'values': {
                    'say_first': 'Hi Once',
                    'say_second': 'Hi Twice',
                    'sleep': 0
                },
                'sequence': 1
            },
        ]),
        job_status=json.dumps({
            'date_tz':
                str(now_tz.date()),
            'tasks': [{
                'instance': 1,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow()),
                'script': 'hello',
                'hour': now_tz.hour,
                'stdout': '',
                'stderr': '',
                'done': True
            }, {
                'instance': 2,
                'event': 'JOB_END',
                'utc': str(datetime.utcnow()),
                'script': 'hello',
                'hour': now_tz.hour,
                'stdout': '',
                'stderr': '',
                'done': True
            }]
        }),
        worker_uid='SAMPLE_WORKER',
        worker_utm=utc_milliseconds() - WORKER_LOOKBACK_EXPIRE,
        job_utm=test_job_utm(0, 1))
    self.RECIPE_DONE = self.job_done.uid()

  #def test_ui_autoscale(self):
  #  resp = self.client.get('/recipe/autoscale/')
  #  self.assertEqual(resp.status_code, 200)

  #def test_worker_downscale(self):
  #  self.assertIsNone(worker_downscale())

  def test_worker_upscale_zero_jobs(self):
    self.assertJSONEqual(
        autoscale('TEST').content, {
            'jobs': 0,
            'workers': {
                'jobs': settings.WORKER_JOBS,
                'max': settings.WORKER_MAX,
                'existing': 3,
                'required': 0
            }
        })

  def test_worker_upscale_one_jobs(self):
    self.job_done.force()
    self.assertJSONEqual(
        autoscale('TEST').content, {
            'jobs': 1,
            'workers': {
                'jobs': settings.WORKER_JOBS,
                'max': settings.WORKER_MAX,
                'existing': 3,
                'required': 1
            }
        })

  def test_worker_upscale_many_jobs(self):
    for i in range(0, 7 * settings.WORKER_JOBS):
      self.job_new = Recipe.objects.create(
          account=self.account,
          project=self.project,
          name='RECIPE_NEW_%d' % i,
          active=True,
          week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
          hour=json.dumps([0]),
          timezone='America/Los_Angeles',
          tasks=json.dumps([
              {
                  'tag': 'hello',
                  'values': {
                      'say_first': 'Hi Once',
                      'say_second': 'Hi Twice',
                      'sleep': 0
                  },
                  'sequence': 1
              },
          ]),
      )
      self.job_new.force()

    self.assertJSONEqual(
        autoscale('TEST').content, {
            'jobs': 7 * settings.WORKER_JOBS,
            'workers': {
                'jobs': settings.WORKER_JOBS,
                'max': settings.WORKER_MAX,
                'existing': 3,
                'required': 7
            }
        })

  def test_worker_upscale_limit(self):
    for i in range(0, 70 * settings.WORKER_JOBS):
      self.job_new = Recipe.objects.create(
          account=self.account,
          project=self.project,
          name='RECIPE_NEW_%d' % i,
          active=True,
          week=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
          hour=json.dumps([0]),
          timezone='America/Los_Angeles',
          tasks=json.dumps([
              {
                  'tag': 'hello',
                  'values': {
                      'say_first': 'Hi Once',
                      'say_second': 'Hi Twice',
                      'sleep': 0
                  },
                  'sequence': 1
              },
          ]),
      )
      self.job_new.force()

    self.assertJSONEqual(
        autoscale('TEST').content, {
            'jobs': 70 * settings.WORKER_JOBS,
            'workers': {
                'jobs': settings.WORKER_JOBS,
                'max': settings.WORKER_MAX,
                'existing': 3,
                'required': settings.WORKER_MAX
            }
        })
