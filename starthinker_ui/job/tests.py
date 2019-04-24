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
from time import sleep
from datetime import datetime
from django.test import TestCase
from django.core import management

from starthinker_ui.job.models import Job, job_update, job_status, worker_pull, worker_status, worker_ping, utc_milliseconds, utc_to_timezone, JOB_LOOKBACK_MS, time_ago
from starthinker_ui.account.tests import account_create
from starthinker_ui.recipe.tests import uuid_timestamp, recipe_create, recipe_create_with_task_error, recipe_create_with_task_sleep


class JobTest(TestCase):

  def setUp(self):
    self.account = account_create()

    self.job_new = Job.objects.create(
      account = self.account,
      recipe_uid = 'RECIPE_NEW',
      recipe_json = json.dumps(recipe_create('RECIPE_NEW')),
      job_pause = False,
      job_done = False,
      #job_status = "{}",
      worker_uid = "",
      worker_utm = 0,
    )

    self.job_expired = Job.objects.create(
      account = self.account,
      recipe_uid = 'RECIPE_EXPIRED',
      recipe_json = json.dumps(recipe_create('RECIPE_EXPIRED')),
      job_pause = False,
      job_done = False,
      #job_status = "{}",
      worker_uid = "SAMPLE_WORKER",
      worker_utm = utc_milliseconds() - (JOB_LOOKBACK_MS * 2)
    )

    self.job_running = Job.objects.create(
      account = self.account,
      recipe_uid = 'RECIPE_RUNNING',
      recipe_json = json.dumps(recipe_create('RECIPE_RUNNING')),
      job_pause = False,
      job_done = False,
      #job_status = "{}",
      worker_uid = "OTHER_WORKER",
      worker_utm = utc_milliseconds()
    )

    self.job_paused = Job.objects.create(
      account = self.account,
      recipe_uid = 'RECIPE_PAUSED',
      recipe_json = json.dumps(recipe_create('RECIPE_PAUSED')),
      job_pause = True,
      job_done = False,
      #job_status = "{}",
      worker_uid = "OTHER_WORKER",
      worker_utm = utc_milliseconds() - (JOB_LOOKBACK_MS * 10)
    )

    # paused so its not part of the normal flow ( unpause to use in test )
    self.job_error = Job.objects.create(
      account = self.account,
      recipe_uid = 'RECIPE_ERROR',
      recipe_json = json.dumps(recipe_create_with_task_error('RECIPE_ERROR')),
      job_done = False,
      job_pause = True,
      #job_status = "{}",
      worker_uid = "",
      worker_utm = 0
    )


  def test_single_pulls(self):

    # first pull new task 1
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], 'RECIPE_NEW')
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], None)

    # second pull expired task 1
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], 'RECIPE_EXPIRED')
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], None)

    # third pull is blank since all recipes have been pulled from
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(len(jobs), 0)

    # expire all workers except OTHER_WORKER / RECIPE_RUNNING
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', 'RECIPE_RUNNING')

    # get oldest expired job first ( redo task since it never completes )
    jobs = worker_pull('SAMPLE_WORKER', 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], 'RECIPE_NEW')
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], None)


  def test_multiple_pulls(self):

    # pull all jobs at once
    jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 2)

    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], 'RECIPE_NEW')
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], None)

    self.assertEqual(jobs[1]['recipe']['setup']['uuid'], 'RECIPE_EXPIRED')
    self.assertEqual(jobs[1]['script'], 'hello')
    self.assertEqual(jobs[1]['instance'], 1)
    self.assertEqual(jobs[1]['hour'], None)


  def test_early_pulls(self):
    recipe = recipe_create('RECIPE_NEW')
    hour_tz = utc_to_timezone(datetime.utcnow(), recipe['setup']['timezone']).hour

    if hour_tz > 23:
      print 'SKIPPING test_early_pulls, need 1 spare hour for test.'

    else:
      # set up recipe to run at specific hour
      recipe['setup']['hour'] = [hour_tz, hour_tz + 1]

      # first task scheduled later
      recipe['tasks'][0]['hour'] = [hour_tz + 1]
      recipe['tasks'][0]['hello']['hour'] = [hour_tz + 1]

      # second task scheduled earlier
      recipe['tasks'][1]['hour'] = [hour_tz]
      recipe['tasks'][1]['hello']['hour'] = [hour_tz]

      job_update(self.account, recipe, force=False, pause=False)
      job = worker_pull('TEST_WORKER', 5)[0]

      self.assertEqual(job['recipe']['setup']['uuid'], 'RECIPE_NEW')
      self.assertEqual(job['script'], 'hello')
      self.assertEqual(job['instance'], 2)
      self.assertEqual(job['hour'], hour_tz)

      # complete job
      worker_status('TEST_WORKER', job['recipe']['setup']['uuid'], job['script'], job['instance'], job['hour'], 'JOB_END', '', '')

      jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()
      job_status = jobs[0].get_status()

      self.assertEqual(len(job_status['queue']), 1)
      self.assertEqual(len(job_status['tasks']), 2)
      self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_PENDING')
      self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_END')
      self.assertEqual(job_status['queue'][0]['script'], 'hello')
      self.assertEqual(job_status['queue'][0]['instance'], 1)
      self.assertEqual(job_status['queue'][0]['hour'], hour_tz + 1)


  def test_late_pulls(self):
    recipe = recipe_create('RECIPE_NEW')
    hour_tz = utc_to_timezone(datetime.utcnow(), recipe['setup']['timezone']).hour

    if hour_tz < 2:
      print 'SKIPPING test_late_pulls, need 1 elapsed hour for test.'

    else:
      # set up recipe to run at specific hour
      recipe['setup']['hour'] = [hour_tz - 1, hour_tz]

      # first task scheduled later
      recipe['tasks'][0]['hour'] = [hour_tz]
      recipe['tasks'][0]['hello']['hour'] = [hour_tz]

      # second task scheduled earlier
      recipe['tasks'][1]['hour'] = [hour_tz - 1]
      recipe['tasks'][1]['hello']['hour'] = [hour_tz - 1]

      job_update(self.account, recipe, force=False, pause=False)
      job = worker_pull('TEST_WORKER', 5)[0]

      self.assertEqual(job['recipe']['setup']['uuid'], 'RECIPE_NEW')
      self.assertEqual(job['script'], 'hello')
      self.assertEqual(job['instance'], 2)
      self.assertEqual(job['hour'], hour_tz - 1)

      # complete job
      worker_status('TEST_WORKER', job['recipe']['setup']['uuid'], job['script'], job['instance'], job['hour'], 'JOB_END', '', '')

      jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()
      job_status = jobs[0].get_status()

      self.assertEqual(len(job_status['queue']), 1)
      self.assertEqual(len(job_status['tasks']), 2)
      self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_PENDING')
      self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_END')
      self.assertEqual(job_status['queue'][0]['script'], 'hello')
      self.assertEqual(job_status['queue'][0]['instance'], 1)
      self.assertEqual(job_status['queue'][0]['hour'], hour_tz)

      #jobs = worker_pull('TEST_WORKER', 5)[0]
      #print jobs


  def test_manager(self):

    # PART I: call manager single loop, cheats a bit because shutdown will ensure current jobs finish
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)
    
    jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()

    self.assertEqual(len(jobs), 2)
    job_status = jobs[0].get_status()

    self.assertEqual(len(job_status['queue']), 1)
    self.assertEqual(len(job_status['tasks']), 2)
    self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_END')
    self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_PENDING')
    self.assertEqual(job_status['queue'][0]['script'], 'hello')
    self.assertEqual(job_status['queue'][0]['instance'], 2)
    self.assertEqual(job_status['queue'][0]['hour'], None)

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', 'RECIPE_RUNNING')

    # second loop through manager
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()
    self.assertEqual(len(jobs), 2)
    job_status = jobs[0].get_status()
    
    self.assertEqual(len(job_status['queue']), 0)
    self.assertEqual(len(job_status['tasks']), 2)
    self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_END')
    self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_END')

    # job was also marked as complete
    self.assertTrue(jobs[0].job_done)
    self.assertTrue(jobs[1].job_done)

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', 'RECIPE_RUNNING')

    # all jobs either run by other workers or done
    jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 0)

    # PART II: good break but now test if update works
    job_update(self.job_new.account, json.loads(self.job_new.recipe_json), force=False, pause=False)
    job = Job.objects.get(recipe_uid='RECIPE_NEW')
    self.assertFalse(job.job_done)

    # nothing comes back because recipe has not changed
    jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 0)

    # however job is now back to done ( because worker reserved only to find no task )
    job = Job.objects.get(recipe_uid='RECIPE_NEW')
    self.assertTrue(job.job_done)

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)
    worker_ping('OTHER_WORKER', 'RECIPE_RUNNING')

    # PART III: good break but now test if update force works
    job_update(self.job_new.account, json.loads(self.job_new.recipe_json), force=True, pause=False)
    job = Job.objects.get(recipe_uid='RECIPE_NEW')
    self.assertFalse(job.job_done)

    # first task comes back because recipe has been forced
    jobs = worker_pull('TEST_WORKER', 5)
    self.assertEqual(len(jobs), 1)
    self.assertEqual(jobs[0]['recipe']['setup']['uuid'], 'RECIPE_NEW')
    self.assertEqual(jobs[0]['script'], 'hello')
    self.assertEqual(jobs[0]['instance'], 1)
    self.assertEqual(jobs[0]['hour'], None)


  def test_manager_error(self):

    # pause all other jobs, and activate error recipe 
    job_update(self.job_new.account, json.loads(self.job_new.recipe_json), force=False, pause=True)
    job_update(self.job_expired.account, json.loads(self.job_expired.recipe_json), force=False, pause=True)
    job_update(self.job_running.account, json.loads(self.job_running.recipe_json), force=False, pause=True)
    job_update(self.job_paused.account, json.loads(self.job_paused.recipe_json), force=False, pause=True)
    job_update(self.job_error.account, json.loads(self.job_error.recipe_json), force=False, pause=False)

    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()
    self.assertEqual(len(jobs), 1)
    job_status = jobs[0].get_status()

    self.assertEqual(len(job_status['queue']), 2)
    self.assertEqual(len(job_status['tasks']), 3)
    self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_END')
    self.assertEqual(job_status['tasks']['task_does_not_exist - 1']['event'], 'JOB_PENDING')
    self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_PENDING')
    self.assertEqual(job_status['queue'][0]['script'], 'task_does_not_exist')
    self.assertEqual(job_status['queue'][0]['instance'], 1)
    self.assertEqual(job_status['queue'][0]['hour'], None)
    self.assertEqual(job_status['queue'][1]['script'], 'hello')
    self.assertEqual(job_status['queue'][1]['instance'], 2)
    self.assertEqual(job_status['queue'][1]['hour'], None)

    # advance time, since current jobs need to expire, artificially ping to keep out of queue
    sleep((JOB_LOOKBACK_MS * 2) / 1000.0)

    # second loop through manager
    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=60*60*1, verbose=True, test=True)

    jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()
    self.assertEqual(len(jobs), 1)
    job_status = jobs[0].get_status()

    self.assertEqual(len(job_status['queue']), 2)
    self.assertEqual(len(job_status['tasks']), 3)
    self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_END')
    self.assertEqual(job_status['tasks']['task_does_not_exist - 1']['event'], 'JOB_ERROR')
    self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_PENDING')
    self.assertEqual(job_status['queue'][0]['script'], 'task_does_not_exist')
    self.assertEqual(job_status['queue'][0]['instance'], 1)
    self.assertEqual(job_status['queue'][0]['hour'], None)
    self.assertEqual(job_status['queue'][1]['script'], 'hello')
    self.assertEqual(job_status['queue'][1]['instance'], 2)
    self.assertEqual(job_status['queue'][1]['hour'], None)


  def test_manager_timeout(self):
    # delete all recipes and create a timeout recipe
    Job.objects.all().delete()
    job_update(self.account, recipe_create_with_task_sleep('RECIPE_TIMEOUT'), force=False, pause=False)

    management.call_command('job_worker', worker='TEST_WORKER', jobs=5, timeout=5, verbose=True, test=True)

    jobs = Job.objects.filter(worker_uid='TEST_WORKER').all()
    self.assertEqual(len(jobs), 1)
    job_status = jobs[0].get_status()

    self.assertEqual(len(job_status['queue']), 2)
    self.assertEqual(len(job_status['tasks']), 2)
    self.assertEqual(job_status['tasks']['hello - 1']['event'], 'JOB_TIMEOUT')
    self.assertEqual(job_status['tasks']['hello - 2']['event'], 'JOB_PENDING')
    self.assertEqual(job_status['queue'][0]['script'], 'hello')
    self.assertEqual(job_status['queue'][0]['instance'], 1)
    self.assertEqual(job_status['queue'][0]['hour'], None)
    self.assertEqual(job_status['queue'][1]['script'], 'hello')
    self.assertEqual(job_status['queue'][1]['instance'], 2)
    self.assertEqual(job_status['queue'][1]['hour'], None)
