# -*- coding: utf-8 -*-

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

import pytz
import json
from datetime import date, datetime

from django.db import models, connection
from django.conf import settings
from django.utils.text import slugify

from starthinker.util.project import project
from starthinker_ui.account.models import Account, token_generate
from starthinker_ui.project.models import Project
from starthinker_ui.recipe.scripts import Script
from starthinker_ui.ui.log import log_job_update


JOB_INTERVAL_MS = 500 # milliseconds
JOB_LOOKBACK_MS = 3 * JOB_INTERVAL_MS # milliseconds


def utc_milliseconds(timestamp=None):
  if timestamp is None: timestamp = datetime.utcnow()
  epoch = datetime.utcfromtimestamp(0)
  return long((timestamp - epoch).total_seconds() * 1000)


def utc_to_timezone(timestamp, timezone):
  if timestamp: return timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
  else: return None


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

    if d: ago += '%d Days ' % d
    if h: ago += '%d Hours ' % h
    if m: ago += '%d Minutes ' % m
    if ago == '' and s: ago = '1 Minute Ago'
    else: ago += 'Ago'

  return ago


def worker_pull(worker_uid, jobs=1):
  '''Atomic reservation of worker in jobs.

  Unfortunately this needs to be done at the DB level for performance.

  Args:
    - worker_uid ( string ) - identifies a unique worker, must be same for every call from same worker.
    - jobs ( integer ) - number of jobs to pull

  '''

  worker_utm = utc_milliseconds()
  worker_interval = worker_utm - JOB_LOOKBACK_MS

  # sql level is necessary evil to get the most concurrency
  worker_skip_locked = 'FOR UPDATE SKIP LOCKED' if connection.vendor == 'postresql' else ''
  db_false = '0' if connection.vendor == 'sqlite' else 'false'

  where = """SELECT id 
    FROM recipe_recipe 
    WHERE job_done=%s AND active!=%s AND worker_utm < %s
    ORDER BY worker_utm ASC 
    %s 
    LIMIT %d
  """ % (db_false, db_false, worker_interval, worker_skip_locked, jobs)

  with connection.cursor() as cursor:
    #cursor.execute("SELECT id, worker_uid, worker_utm from recipe_recipe")
    #print ''
    #for row in cursor.fetchall():
    #  print 'Before', row

    cursor.execute("""
      UPDATE recipe_recipe 
      SET worker_uid='%s', worker_utm=%s 
      WHERE id IN ( %s )
    """ % (worker_uid, worker_utm, where))

    #cursor.execute("SELECT id, worker_uid, worker_utm from recipe_recipe")
    #print 'Compare', worker_uid, 'current = ', worker_interval, 'worker_utm < ', worker_utm, 'gap = ', JOB_LOOKBACK_MS
    #for row in cursor.fetchall():
    #  print 'After', row

  tasks = []
  for job in Recipe.objects.filter(worker_uid=worker_uid, worker_utm=worker_utm):
    task = job.get_task()
    if task: tasks.append(task)

  return tasks


def worker_ping(worker_uid, recipe_uid):
  Recipe.objects.filter(worker_uid=worker_uid, id=recipe_uid).update(worker_utm=utc_milliseconds())


def worker_status(worker_uid, recipe_uid, script, instance, hour, event, stdout, stderr):
  try:
    job = Recipe.objects.get(worker_uid=worker_uid, id=recipe_uid)
    job.set_task(script, instance, hour, event, stdout, stderr)
  except Recipe.DoesNotExist:
    print 'Expired Worker Job:', worker_uid, recipe_uid, script, instance, hour, event


class Recipe(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  token = models.CharField(max_length=8, unique=True)

  project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

  name = models.CharField(max_length=64)
  active = models.BooleanField(default=True)

  week = models.CharField(max_length=64, default=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
  hour = models.CharField(max_length=64, default=json.dumps([3]))

  timezone = models.CharField(max_length=32, blank=True, default='America/Los_Angeles')

  tasks = models.TextField()

  job_done = models.BooleanField(blank=True, default=False)
  job_status = models.TextField(default='{}')
  worker_uid = models.CharField(max_length=128, default='')
  worker_utm = models.BigIntegerField(blank=True, default=0)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.get_token()
    super(Recipe, self).save(*args, **kwargs)

  def uid(self):
    #return "UI-RECIPE-%s" % (self.pk or 'NEW')
    return self.pk or 'NEW'

  def link_edit(self):
    return '/recipe/edit/%d/' % self.pk

  def link_delete(self):
    return '/recipe/delete/%d/' % self.pk

  def link_run(self):
    return '/recipe/run/%d/' % self.pk if self.pk else ''

  def link_download(self):
    return '/recipe/download/%d/' % self.pk if self.pk else ''

  def get_token(self):
    if not self.token: self.token = token_generate(Recipe)
    return self.token

  def get_values(self):
    constants = {
      'recipe_project':self.get_project_identifier(),
      'recipe_name':slugify(self.name),
      'recipe_token':self.get_token(),
      'recipe_timezone':self.timezone,
      'recipe_email':self.account.email if self.account else None,
      'recipe_email_token': self.account.email.replace('@', '+%s@' % self.get_token()) if self.account else None,
    }
    tasks = json.loads(self.tasks or '[]')
    for task in tasks: task['values'].update(constants)
    return tasks

  def set_values(self, scripts):
    self.tasks = json.dumps(scripts)

  def get_hours(self):
    return json.loads(self.hour or '[]')

  def get_days(self):
    return json.loads(self.week or '[]')

  def get_icon(self): return '' #get_icon('')

  def get_credentials_user(self):
    return self.account.get_credentials_path() if self.account else '{}'

  def get_credentials_service(self):
    return self.project.service if self.project and self.project.service else '{}'

  def get_project_identifier(self):
    return self.project.get_project_id() if self.project else ''
  
  def get_scripts(self):
    for value in self.get_values():  yield Script(value['tag'])

  def get_json(self, credentials=True):
    return Script.get_json(
        self.uid(),
        self.get_project_identifier(),
        self.get_credentials_user() if credentials else '',
        self.get_credentials_service() if credentials else '',
        self.timezone,
        self.get_days(),
        self.get_hours(),
        self.get_values()
      )

  def run(self, force=False, remote=True):
    if remote:
      if force: self.force()
    elif settings.UI_CRON:
      with open(settings.UI_CRON + '/recipe_%d.json' % self.pk, 'w') as f:
        f.write(json.dumps(self.get_json()))
    else:
      raise Exception('Neither UI_CRON configured nor remote set.')

  def force(self):
    status = self.get_status(force=True)
    self.job_status = json.dumps(status)
    self.save(update_fields=['job_status'])

  # WORKER METHODS

  def get_status(self, force=False):
    recipe = self.get_json()

    # current 24 hour time zone derived frame to RUN the job
    now_tz = utc_to_timezone(datetime.utcnow(), self.timezone)
    date_tz = str(now_tz.date())
    hour_tz = now_tz.hour

    # load prior status ( reset if new 24 hour block or force )
    try: prior_status = json.loads(self.job_status)
    except ValueError: prior_status = {}
    if force or date_tz != prior_status.get('date_tz'):
      prior_status = { 'force':force }

    # create a vanilla status with all tasks pending ( always do this because recipe may change )
    status = {
      'date_tz':date_tz,
      'force':prior_status.get('force', False), 
      'tasks':[],
    }

    instances = {}
    for order, task in enumerate(recipe.get('tasks', [])):
      script, task = task.items()[0]
      instances.setdefault(script, 0)
      instances[script] += 1

      # if force, queue each task in sequence without hours
      if prior_status.get('force', False):
        hours = [hour_tz]
      # create an entry for each hour, default tasks without hours to every hour of the day if recipe wide hours are not set
      else:
        hours = task.get('hour', [])
        if len(hours) == 0: hours = recipe['setup'].get('hour', [])
        if len(hours) == 0: hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

      for hour in hours:
        status['tasks'].append({
          'order':order,
          'script':script, 
          'instance':instances[script], 
          'hour':hour, 
          'utc':str(datetime.utcnow()),
          'event':'JOB_PENDING',
          'stdout':'',
          'stderr':'',
          'done':False
        })

    # sort new order by first by hour and second by order
    def queue_compare(left, right):
      if left['hour'] < right['hour']: return -1
      elif left['hour'] > right['hour']: return 1
      else:
        if left['order'] < right['order']: return -1
        elif left['order'] > right['order']: return 1
        else: return 0

    status['tasks'].sort(queue_compare)

    # merge old status in if it exists at this point
    for task_prior in prior_status.get('tasks', []):
      for task in status['tasks']:
        if task_prior['script'] == task['script'] and task_prior['instance'] == task['instance'] and task_prior['hour'] == task['hour']:
          task['utc'] = task_prior['utc']
          task['event'] = task_prior['event']
          task['stdout'] = task_prior['stdout']
          task['stderr'] = task_prior['stderr']
          task['done'] = task_prior['done']

    return status


  def get_task(self):
    status = self.get_status()

    # check if done ( maybe recipe changed )
    done = all([task['done'] for task in status['tasks']])
    if self.job_done != done:
      Recipe.objects.filter(pk=self.pk).update(job_done=done)

    # if not done return next task prior or equal to current time zone hour
    if not done:
      hour_tz = utc_to_timezone(datetime.utcnow(), self.timezone).hour
      for task in status['tasks']:
        if not task['done'] and task['hour'] <= hour_tz:
          task['recipe'] = self.get_json()
          return task 

    return None


  def set_task(self, script, instance, hour, event, stdout, stderr):
    status = self.get_status()

    for task in status['tasks']:
      if task['script'] == script and task['instance'] == instance and task['hour'] == hour:
        task['utc'] = str(datetime.utcnow())
        task['event'] = event
        task['stdout'] = stdout
        task['stderr'] = stderr
        task['done'] = (event != 'JOB_START')

        self.job_done = all([task['done'] for task in status['tasks']])
        self.job_status = json.dumps(status)
        self.worker_utm=utc_milliseconds()

        self.save(update_fields=['worker_utm', 'job_status', 'job_done'])
        break


  def get_log(self):
    status = self.get_status()

    error = False
    done = 0
    for task in status['tasks']:
      task['utc'] = datetime.strptime(task['utc'].split('.', 1)[0], "%Y-%m-%d %H:%M:%S")
      task['ltc'] = utc_to_timezone(task['utc'], self.timezone)
      task['ago'] = time_ago(task['utc'])
  
      if status.get('utc', task['utc']) <= task['utc']: status['utc'] = task['utc']
      if task['event'] not in ('JOB_PENDING', 'JOB_START', 'JOB_END'): error = True
      if task['done']: done += 1
  
    if 'utc' not in status: status['utc'] = datetime.utcnow()
    status['utl'] = utc_to_timezone(status['utc'], self.timezone)
    status['ago'] = time_ago(status['utc'])
    status['percent'] = ( done * 100 ) / ( len(status['tasks']) or 1 )
    status['uid'] = self.uid()
  
    if error:
      status['status'] = 'ERROR'
    elif self.job_done:
      status['status'] = 'FINISHED'
    elif utc_milliseconds() - self.worker_utm < JOB_LOOKBACK_MS:
      status['status'] = 'RUNNING'
    elif not self.active:
      status['status'] = 'PAUSED'
    else:
      status['status'] = 'QUEUED'

    return status