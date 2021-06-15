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

import re
import pytz
import json
import functools
from itertools import chain
from datetime import date, datetime, timedelta

from django.db import models
from django.conf import settings

from starthinker_ui.account.models import Account, token_generate
from starthinker_ui.project.models import Project
from starthinker_ui.recipe.scripts import Script

JOB_INTERVAL_MS = float(1600)  # milliseconds
JOB_LOOKBACK_MS = 5 * JOB_INTERVAL_MS  # 8 seconds ( must guarantee to span several pings )
JOB_RECHECK_MS = 30 * 60 * 1000  # 30 minutes

RE_SLUG = re.compile(r'[^\w]')


def utc_milliseconds(utc_timestamp=None):
  if utc_timestamp is None:
    utc_timestamp = datetime.utcnow()
  utc_epoch = datetime.utcfromtimestamp(0)
  return int((utc_timestamp - utc_epoch) / timedelta(milliseconds=1))


def utc_milliseconds_to_timezone(utm, timezone):
  return utc_to_timezone(datetime.utcfromtimestamp(int(utm / 1000)), timezone)


def utc_to_timezone(utc_timestamp, timezone):
  tz = pytz.timezone(timezone)
  return tz.normalize(utc_timestamp.replace(tzinfo=pytz.utc).astimezone(tz))


def timezone_to_utc(tz_timestamp):
  return tz_timestamp.astimezone(pytz.utc).replace(tzinfo=None)


def time_ago(timestamp):
  ago = ''
  seconds = (datetime.utcnow() - timestamp).total_seconds()

  if seconds is None:
    ago = 'Unknown'
  elif seconds == 0:
    ago = 'Just Now'
  else:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 60)

    if d:
      ago += '%d Days ' % d
    if h:
      ago += '%d Hours ' % h
    if m:
      ago += '%d Minutes ' % m
    if ago == '' and s:
      ago = '1 Minute Ago'
    else:
      ago += 'Ago'

  return ago


def reference_default():
  return token_generate(Recipe, 'token', 32)


class Recipe(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  token = models.CharField(max_length=8, unique=True)
  reference = models.CharField(
      max_length=32, unique=True, default=reference_default)

  project = models.ForeignKey(
      Project, on_delete=models.SET_NULL, null=True, blank=True)

  name = models.CharField(max_length=64)
  active = models.BooleanField(default=True)
  manual = models.BooleanField(default=False)

  week = models.CharField(
      max_length=64,
      default=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
  hour = models.CharField(max_length=128, default=json.dumps([3]))

  timezone = models.CharField(
      max_length=32, blank=True, default='America/Los_Angeles')

  tasks = models.TextField()

  job_utm = models.BigIntegerField(blank=True, default=0)
  job_status = models.TextField(default='{}')
  worker_uid = models.CharField(max_length=128, default='')
  worker_utm = models.BigIntegerField(blank=True, default=0)

  birthday = models.DateField(auto_now_add=True)

  _cache_log = None

  def __str__(self):
    return self.name

  def slug(self):
    return RE_SLUG.sub('_', self.name)

  def save(self, *args, **kwargs):
    self.get_token()
    self.get_reference()
    super(Recipe, self).save(*args, **kwargs)
    self._cache_log = None

  def uid(self):
    return self.pk or 'NEW'

  def link_edit(self):
    return '/recipe/edit/%d/' % self.pk

  def link_delete(self):
    return '/recipe/delete/%d/' % self.pk

  def link_run(self):
    return '/recipe/run/%d/' % self.pk if self.pk else ''

  def link_cancel(self):
    return '/recipe/cancel/%d/' % self.pk if self.pk else ''

  def link_json(self):
    return '/recipe/json/%d/' % self.pk if self.pk else ''

  def link_colab(self):
    return '/recipe/colabs/%d/' % self.pk if self.pk else ''

  def link_airflow(self):
    return '/recipe/airflow/%d/' % self.pk if self.pk else ''

  def link_start(self):
    return '%s/recipe/start/' % settings.CONST_URL

  def link_stop(self):
    return '%s/recipe/stop/' % settings.CONST_URL

  def is_running(self):
    return self.get_log()['status'] == 'RUNNING'

  def get_token(self):
    if not self.token:
      self.token = token_generate(Recipe, 'token')
    return self.token

  def get_reference(self):
    if not self.reference:
      self.reference = token_generate(Recipe, 'reference', 32)
    return self.reference

  def get_values(self):
    constants = {
        'recipe_project':
            self.get_project_identifier(),
        'recipe_name':
            self.name,
        'recipe_slug':
            self.slug(),
        'recipe_token':
            self.get_token(),
        'recipe_timezone':
            self.timezone,
        'recipe_email':
            self.account.email if self.account else None,
        'recipe_email_token':
            self.account.email.replace('@', '+%s@' % self.get_token())
            if self.account else None,
    }
    tasks = json.loads(self.tasks or '[]')
    for task in tasks:
      task['values'].update(constants)
    return tasks

  def set_values(self, scripts):
    self.tasks = json.dumps(scripts)

  def get_hours(self):
    return [int(h) for h in json.loads(self.hour or '[]')]

  def get_days(self):
    return json.loads(
        self.week or '[]') or ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  def get_icon(self):
    return ''  #get_icon('')

  def get_credentials_user(self):
    return self.account.get_credentials_path() if self.account else '{}'

  def get_credentials_service(self):
    return self.project.service if self.project and self.project.service else '{}'

  def get_project_identifier(self):
    return self.project.get_project_id() if self.project else ''

  def get_project_key(self):
    return self.project.key if self.project else ''

  def get_scripts(self):
    for value in self.get_values():
      yield Script(value['tag'])

  def get_tasks(self):
    for task in chain.from_iterable(
        map(lambda s: s.get_tasks(), self.get_scripts())):
      yield next(iter(task.items()))  # script, task

  def get_json(self, credentials=True):
    return Script.get_json(
      self.uid(),
      self.get_project_identifier(),
      self.get_project_key() if credentials else '',
      self.get_credentials_user() if credentials else '',
      self.get_credentials_service() if credentials else '', self.timezone,
      self.get_days(), self.get_hours(), self.get_values()
    )

  def activate(self):
    self.active = True
    self.save(update_fields=['active'])

  def deactivate(self):
    self.active = False
    self.save(update_fields=['active'])

  def update(self):
    return self.get_status(update=True)

  def force(self):
    status = self.get_status(force=True)
    self.worker_uid = ''  # forces current worker to cancel job
    self.save(update_fields=['worker_uid'])
    return status

  def cancel(self):
    status = self.get_status(cancel=True)
    self.worker_uid = ''  # forces current worker to cancel job
    self.save(update_fields=['worker_uid'])
    return status

  def get_job_utm(self, status):
    now_tz = utc_to_timezone(datetime.utcnow(), self.timezone)

    # check if tasks remain for today
    hour = None
    if now_tz.strftime('%a') in self.get_days():
      for task in status['tasks']:
        if task['done']:
          continue
        else:
          hour = task['hour']
          break

    # all tasks done, advance to next day first task
    if hour is None:
      now_tz += timedelta(hours=24)
      for i in range(0, 7):
        if now_tz.strftime('%a') in self.get_days():
          break
        else:
          now_tz += timedelta(hours=24)

      # get the first hour ( if tasks exist, lame use of for loop but works )
      for script, task in self.get_tasks():
        try:
          hour = task.get('hour', self.get_hours())[0]
        except IndexError:
          hour = 0
        break

    now_tz = now_tz.replace(hour=hour or 0, minute=0, second=0, microsecond=0)
    return utc_milliseconds(timezone_to_utc(now_tz))

  def get_status(self, update=False, force=False, cancel=False):
    # current 24 hour time zone derived frame to RUN the job
    now_utc = datetime.utcnow()
    now_tz = utc_to_timezone(now_utc, self.timezone)
    date_tz = str(now_tz.date())
    date_day =  now_tz.strftime('%a')

    # load prior status
    try:
      status = json.loads(self.job_status)
    except ValueError:
      status = {}

    # create default status for new recipes
    status.setdefault('date_tz', date_tz)
    status.setdefault('tasks', [])

    # if not saved yet, do nothing
    if not self.pk:
      return status

    # if cancel, do it on whatever status exists
    elif cancel:
      for task in status['tasks']:
        if not task['done']:
          task['done'] = True
          task['utc'] = str(now_utc)
          task['event'] = 'JOB_CANCEL'

      self.job_utm = self.get_job_utm(status)
      self.job_status = json.dumps(status)
      self.worker_uid = ''  # forces current worker to cancel job
      self.save(update_fields=['job_status', 'job_utm', 'worker_uid'])

    # if manual and all task are done set the utm to be ignored in worker pulls
    elif self.manual and not force and not update:
      if not status['tasks'] or all(task['done'] for task in status['tasks']):
        self.job_utm = 0
        self.save(update_fields=['job_utm'])

    # if updating, modify the status
    elif force or update or (date_tz > status['date_tz'] and
                             date_day in self.get_days()):
      status = {
          'date_tz': date_tz,
          'tasks': [],
          'days':[date_day] if force else self.get_days()
      }

      # create task list based on recipe json
      for instance, (script, task) in enumerate(self.get_tasks()):

        # if force use current hour, if schedule use task and recipe hours
        hours = [now_tz.hour] if force else task.get('hour', self.get_hours())

        # tasks with hours = [] will be skipped unless force=True
        if hours:
          for hour in hours:
            status['tasks'].append({
                'script': script,
                'instance': instance + 1,
                'hour': hour,
                'utc': str(datetime.utcnow()),
                'event': 'JOB_NEW' if update else 'JOB_PENDING',
                'stdout': '',
                'stderr': '',
                'done': update  # if saved by user, write as done for that day, user must force run first time
            })

      # sort new order by first by hour and second by instance
      def queue_compare(left, right):
        if left['hour'] < right['hour']:
          return -1
        elif left['hour'] > right['hour']:
          return 1
        else:
          if left['instance'] < right['instance']:
            return -1
          elif left['instance'] > right['instance']:
            return 1
          else:
            return 0

      status['tasks'].sort(key=functools.cmp_to_key(queue_compare))

      self.job_utm = self.get_job_utm(status)
      self.job_status = json.dumps(status)
      if force or update:
        self.worker_uid = ''  # cancel all current workers
        self.save(update_fields=['job_status', 'job_utm', 'worker_uid'])
      else:
        self.save(update_fields=['job_status', 'job_utm'])

    else:
      job_utm = self.get_job_utm(status)
      if job_utm != self.job_utm:
        self.job_utm = job_utm
        self.save(update_fields=['job_utm'])

    return status

  def get_task(self):
    status = self.get_status()

    # if not done return next task prior or equal to current time zone hour
    now_tz = utc_to_timezone(datetime.utcnow(), self.timezone)
    if now_tz.strftime('%a') in status.get('days', self.get_days()):
      for task in status['tasks']:
        if not task['done'] and task['hour'] <= now_tz.hour:
          task['recipe'] = self.get_json()
          return task

    return None

  def set_task(self, script, instance, hour, event, stdout, stderr):
    status = self.get_status()

    for task in status['tasks']:
      if task['script'] == script and task['instance'] == instance and task[
          'hour'] == hour:
        task['utc'] = str(datetime.utcnow())
        task['event'] = event
        if stdout:
          task['stdout'] += stdout
        if stderr:
          task['stderr'] += stderr
        task['done'] = (event != 'JOB_START')

        self.job_status = json.dumps(status)
        self.job_utm = self.get_job_utm(status)
        self.worker_utm = utc_milliseconds(
        )  # give worker some time to clean up
        self.save(update_fields=['worker_utm', 'job_utm', 'job_status'])
        break

  def get_log(self):
    if self._cache_log is None:
      self._cache_log = self.get_status()

      error = False
      timeout = False
      new = False
      cancel = False
      done = 0
      for task in self._cache_log['tasks']:
        task['utc'] = datetime.strptime(task['utc'].split('.', 1)[0],
                                        '%Y-%m-%d %H:%M:%S')
        task['ltc'] = utc_to_timezone(task['utc'], self.timezone)
        task['ago'] = time_ago(task['utc'])

        if task['done'] and task['event'] != 'JOB_NEW':
          done += 1
        if self._cache_log.get('utc', task['utc']) <= task['utc']:
          self._cache_log['utc'] = task['utc']

        if task['event'] == 'JOB_TIMEOUT':
          timeout = True
        elif task['event'] == 'JOB_NEW':
          new = True
        elif task['event'] == 'JOB_CANCEL':
          cancel = True
        elif task['event'] not in ('JOB_PENDING', 'JOB_START', 'JOB_END'):
          error = True

      if 'utc' not in self._cache_log:
        self._cache_log['utc'] = datetime.utcnow()
      self._cache_log['utl'] = utc_to_timezone(self._cache_log['utc'],
                                               self.timezone)
      self._cache_log['ago'] = time_ago(self._cache_log['utc'])
      self._cache_log['percent'] = int(
          (done * 100) / (len(self._cache_log['tasks']) or 1))
      self._cache_log['uid'] = self.uid()

      if timeout:
        self._cache_log['status'] = 'TIMEOUT'
      elif new:
        self._cache_log['status'] = 'NEW'
      elif cancel:
        self._cache_log['status'] = 'CANCELLED'
      elif error:
        self._cache_log['status'] = 'ERROR'
      elif not self._cache_log['tasks'] or all(
          task['done'] for task in self._cache_log['tasks']):
        self._cache_log['status'] = 'FINISHED'
      elif utc_milliseconds() - self.worker_utm < JOB_LOOKBACK_MS:
        self._cache_log['status'] = 'RUNNING'
      elif not self.active:
        self._cache_log['status'] = 'PAUSED'
      else:
        self._cache_log['status'] = 'QUEUED'

    return self._cache_log
