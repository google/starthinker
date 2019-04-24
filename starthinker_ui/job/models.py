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
from datetime import datetime 

from django.db import models, connection
from django.conf import settings

from starthinker.util.project import project
from starthinker_ui.account.models import Account
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


def job_status(account, recipe_uid):
  status = {}
  try: 
    job = Job.objects.get(account=account, recipe_uid=recipe_uid)
    status = job.get_status()
    utm = job.worker_utm
    try: recipe = json.loads(job.recipe_json)
    except ValueError: recipe = {}

  except Job.DoesNotExist:
    status = {}
    recipe = {}
    utm = 0

  error = False
  for task in status.get('tasks', {}).values():
    task['utc'] = datetime.strptime(task['utc'].split('.', 1)[0], "%Y-%m-%d %H:%M:%S")
    task['ltc'] = utc_to_timezone(task['utc'], recipe.get('setup', {}).get('timezone', settings.TIME_ZONE))
    task['ago'] = time_ago(task['utc'])

    if 'utc' not in status or status['utc'] < task['utc']: status['utc'] = task['utc']
    if task['event'] == 'JOB_ERROR': error = True

  if 'utc' not in status: status['utc'] = datetime.utcnow()
  status['utl'] = utc_to_timezone(status['utc'], recipe.get('setup', {}).get('timezone', settings.TIME_ZONE))
  status['ago'] = time_ago(status['utc'])
  status['percent'] = ( len(status.get('tasks', [])) * 100 ) / ( len(status.get('queue', [])) + len(status.get('tasks', [])) or 1)
  status['uid'] = recipe_uid

  if error:
    status['status'] = 'ERROR'
  elif len(status.get('queue', [])) == 0:
    status['status'] = 'FINISHED'
  elif utc_milliseconds() - utm < JOB_LOOKBACK_MS:
    status['status'] = 'RUNNING'
  else:
    status['status'] = 'QUEUED'

  return status


def job_update(account, recipe, force, pause):

  # update only json, and pause 
  defaults={ 
    'recipe_json':json.dumps(recipe, default=str), 
    'job_pause':pause, 
    'job_done':False, # forces a review by workers at least once
    #'job_errors':0,
  }

  # if force, also update status to clear all executed tasks
  if force:
    defaults['job_status'] = json.dumps({
      'date_tz':str(utc_to_timezone(datetime.utcnow(), recipe.get('setup', {}).get('timezone', settings.TIME_ZONE)).date()),
      'force':True,
      'queue':[],
      'tasks':{}
    })

  job = Job.objects.update_or_create(
    account=account, 
    recipe_uid=recipe['setup']['uuid'],
    defaults=defaults
  )

  log_job_update({'recipe':recipe})

  return True


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
    FROM job_job 
    WHERE job_done=%s AND job_pause=%s AND worker_utm < %s
    ORDER BY worker_utm ASC 
    %s 
    LIMIT %d
  """ % (db_false, db_false, worker_interval, worker_skip_locked, jobs)

  with connection.cursor() as cursor:
    #cursor.execute("SELECT recipe_uid, worker_uid, worker_utm from job_job")
    #print ''
    #for row in cursor.fetchall():
    #  print 'Before', row

    cursor.execute("""
      UPDATE job_job 
      SET worker_uid='%s', worker_utm=%s 
      WHERE id IN ( %s )
    """ % (worker_uid, worker_utm, where))

    #cursor.execute("SELECT recipe_uid, worker_uid, worker_utm from job_job")
    #print 'Compare', worker_uid, 'current = ', worker_interval, 'worker_utm < ', worker_utm, 'gap = ', JOB_LOOKBACK_MS
    #for row in cursor.fetchall():
    #  print 'After', row

  tasks = []
  for job in Job.objects.filter(worker_uid=worker_uid, worker_utm=worker_utm):
    task = job.get_task()    
    if task: tasks.append(task)

  return tasks


def worker_ping(worker_uid, recipe_uid):
  Job.objects.filter(worker_uid=worker_uid, recipe_uid=recipe_uid).update(worker_utm=utc_milliseconds())


def worker_status(worker_uid, recipe_uid, script, instance, hour, event, stdout, stderr):
  try: 
    job = Job.objects.get(worker_uid=worker_uid, recipe_uid=recipe_uid)
    job.set_task(script, instance, hour, event, stdout, stderr)
  except Job.DoesNotExist:
    print 'Expired Worker Job:', worker_uid, recipe_uid, script, instance, hour, event


class Job(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  recipe_uid = models.CharField(max_length=128, unique=True)
  recipe_json = models.TextField(default='{}')
  #job_errors = models.PositiveIntegerField(blank=True, default = 0)
  job_done = models.BooleanField(blank=True, default=False)
  job_pause = models.BooleanField(blank=True, default=False)
  job_status = models.TextField(default='{}')
  worker_uid = models.CharField(max_length=128)
  worker_utm = models.BigIntegerField(blank=True, default=0)

  def __unicode__(self):
    return self.recipe_uid 

  def get_status(self, force=False):
    try: recipe = json.loads(self.recipe_json)
    except ValueError: recipe = {}

    # current 24 hour time zone derived frame to RUN the job
    date_tz = utc_to_timezone(datetime.utcnow(), recipe.get('setup', {}).get('timezone', settings.TIME_ZONE)).date()

    # load prior status ( reset if new 24 hour block or force )
    try: prior_status = json.loads(self.job_status)
    except ValueError: prior_status = {}
    if force or str(date_tz) != prior_status.get('date_tz'): 
      prior_status = {}

    # carry force over from prior status in same 24 hour block
    force |= prior_status.get('force', False)

    # create a vanilla status with all tasks pending ( always do this because recipe may change )
    status = {
      'date_tz':str(date_tz),
      'force':force,
      'queue':[],
      'tasks':{}
    }

    instances = {}
    for task in recipe.get('tasks', []):
      script, task = task.items()[0]
      instances.setdefault(script, 0)
      instances[script] += 1

      task_key = '%s - %d' % (script, instances[script])
      status['tasks'][task_key] = {
        'script':script, 
        'instance':instances[script], 
        'utc':str(datetime.utcnow()),
        'hours':[],
        'event':'JOB_PENDING',
        'stdout':'',
        'stderr':'',
      }

      # if force, queue each task in sequence without hours
      if force: 
        hours = [None]
      # create an entry for each hour
      else: 
        hours = task.get('hour', recipe['setup'].get('hour')) or [None]

      for hour in hours:
        status['queue'].append({'script':script, 'instance':instances[script], 'hour':hour})

    # otherwise merge old status in if it exists at this point
    for task_key, task in prior_status.get('tasks', {}).items():
      # check if task exists in new status ( maybe recipe was edited )
      if task_key in status['tasks']:
        # synchronize complete tasks
        status['tasks'][task_key] = prior_status['tasks'][task_key]
        # remove complete task from queue ( some will not be in queue already )
        for hour in status['tasks'][task_key]['hours']:
          try:
            status['queue'].remove({'script':task['script'], 'instance':task['instance'], 'hour':hour})
          except ValueError:
            pass

    return status
   

  def get_task(self):
    status = self.get_status()
    try: recipe = json.loads(self.recipe_json)
    except ValueError: recipe = {}

    # check if done ( maybe recipe changed )
    if self.job_done != (bool(status['queue']) == False):
      Job.objects.filter(pk=self.pk).update(job_done=(bool(status['queue']) == False))

    # find next task without hour or task with smallest hour ( earliest )
    hour_tz = utc_to_timezone(datetime.utcnow(), recipe.get('setup', {}).get('timezone', settings.TIME_ZONE)).hour
    job = None
    for task in status['queue']:
      if task['hour'] is None:
        job = task
        break
      elif task['hour'] <= hour_tz:
        if job is None or task['hour'] < job['hour']: 
          job = task

    if job: job['recipe'] = json.loads(self.recipe_json)
    return job 


  def set_task(self, script, instance, hour, event, stdout, stderr):
    status = self.get_status()
   
    if event == 'JOB_END':
      try:
        status['queue'].remove({'script':script, 'instance':instance, 'hour':hour})
      except ValueError: 
        pass

    task_key = '%s - %d' % (script, instance)
    if task_key in status['tasks']:
      status['tasks'][task_key]['utc'] = str(datetime.utcnow())
      status['tasks'][task_key]['event'] = event
      status['tasks'][task_key]['stdout'] = stdout
      status['tasks'][task_key]['stderr'] = stderr
      if event == 'JOB_END': status['tasks'][task_key]['hours'].append(hour)

    self.worker_utm=utc_milliseconds()
    self.job_status = json.dumps(status)
    self.job_done = (bool(status['queue']) == False)

    self.save(update_fields=['worker_utm', 'job_status', 'job_done']) 
