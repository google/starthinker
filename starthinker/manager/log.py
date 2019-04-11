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

#https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry

import pytz
import urllib2
import json
from datetime import datetime

from starthinker.config import UI_PROJECT, UI_SERVICE
from starthinker.util.project import project
from starthinker.util.google_api import API_StackDriver

MANAGER_START = 'MANAGER_START'
MANAGER_END = 'MANAGER_END'
MANAGER_ERROR = 'MANAGER_ERROR'
MANAGER_EXCEPTION = 'MANAGER_EXCEPTION'


JOB_DISPATCH = 'JOB_DISPATCH'
JOB_RECEIVE = 'JOB_RECEIVE'
JOB_BOUNCE = 'JOB_BOUNCE'
JOB_DUPLICATE = 'JOB_DUPLICATE'
JOB_CANCEL = 'JOB_CANCEL'
JOB_START = 'JOB_START'
JOB_COMPLETE = 'JOB_COMPLETE'
JOB_EXCEPTION = 'JOB_EXCEPTION'
JOB_FAIL = 'JOB_FAIL'
JOB_TASK_START = 'JOB_TASK_START'
JOB_TASK_COMPLETE = 'JOB_TASK_COMPLETE'
JOB_TIMEOUT = 'JOB_TIMEOUT'


class LogSeverity():
  DEFAULT = 0 # The log entry has no assigned severity level.
  DEBUG = 100 # Debug or trace information.
  INFO = 200 # Routine information, such as ongoing status or performance.
  NOTICE = 300 # Normal but significant events, such as start up, shut down, or a configuration change.
  WARNING = 400 # Warning events might cause problems.
  ERROR = 500 # Error events are likely to cause problems.
  CRITICAL = 600 # Critical events cause more severe problems or outages.
  ALERT = 700 # A person must take an action immediately.
  EMERGENCY = 800 # One or more systems are unusable.


VERBOSE = False
def log_verbose(verbose=True):
  global VERBOSE
  VERBOSE = verbose


INSTANCE_ID = None
def get_instance_id():
  global INSTANCE_ID
  if INSTANCE_ID is None:
    try:
      return urllib2.urlopen(urllib2.Request(
        "http://metadata.google.internal/computeMetadata/v1/instance/id", 
        headers={"Metadata-Flavor" : 'Google'}
      )).read()
    except:
      INSTANCE_ID = 'UNKNOWN'
  return INSTANCE_ID


INSTANCE_ZONE = None
def get_instance_zone():
  global INSTANCE_ZONE
  if INSTANCE_ZONE is None:
    try:
      INSTANCE_ZONE = urllib2.urlopen(urllib2.Request(
        "http://metadata.google.internal/computeMetadata/v1/instance/zone", 
        headers={"Metadata-Flavor" : 'Google'}
      )).read()
      return zone.rsplit('/', 1)[1]
    except:
      INSTANCE_ZONE = 'UNKNOWN'
  return INSTANCE_ZONE


def log_put(event, recipe, severity, text=''):
  """Generic log writer used by helper functions. Writes to StackDriver.

  Creates a record that can be read using log_get function. Entire recipe is
  logged, worker data and stdout and stderr are added to the JOSN under worker key. 
  Only JOB_EXCEPTION and MANAGER_EXCEPTION logs to text in case JSON is corrupt, 
  everythng else is JSON.

  Do not call this directly, use helper functions instead:
    - log_manager_start
    - log_manager_error
    - log_manager_exception
    - log_job_dispatch
    - log_job_receive
    - log_job_bounce
    - log_job_duplicate
    - log_job_exception
    - log_job_start
    - log_job_task_start
    - log_job_task_complete
    - log_job_fail
    - log_job_complete
    - log_job_timeout
    - log_job_cancel

  WARNING: Do not corrupt recipe, it is actively being used by workers while being logged.

  Args:
    - event ( string ): One of the JOB_* enums.
    - recipe ( json ): Recipe workflow to execute.
    - severity ( enum ): Stackdriver severity level.
    - text ( string ): Mesaging output form the task. Usual stdout and stderr.
  """

  if VERBOSE: print "LOGGING:", event, severity

  body = {
    "entries": [
      {
        "logName": "projects/%s/logs/StarThinker" % UI_PROJECT,
        "severity": severity,
        "resource": { 
          "type": "gce_instance",
          "labels": { 
            "instanceId": get_instance_id(),
            "zone": get_instance_zone()
          }
        },
        "labels": {
          "version":"1",
          "layer":event.split('_')[0],
          "event": event,
        },
        "operation": {
          "id": recipe.get('setup', {}).get('uuid', 'UKNOWN'),
          "producer": recipe.get('worker', {}).get('container_name', 'UKNOWN'),
          "first": event in (JOB_START, ),
          "last": event in (JOB_COMPLETE, JOB_CANCEL, JOB_FAIL, JOB_EXCEPTION, JOB_TIMEOUT, )
        },
        # already in recipe worker logging task and instance, does this have additional value?
        #"sourceLocation": {
        #  "file": string,
        #  "line": string,
        #  "function": string
        #},
      }
    ],
    "partialSuccess": False,
    "dryRun": False
  }

  if text:
    body['entries'][0]["textPayload"] = text
  else:
    # Removing tasks from recipe REMOVES ALL POTENTIAL CREDENTIALS IN CODE
    recipe_buffer = json.loads(json.dumps(recipe, indent=2, sort_keys=True, default=str))
    if 'tasks' in recipe_buffer: del recipe_buffer['tasks']
    body['entries'][0]["jsonPayload"] = recipe_buffer

  project.initialize(_service=UI_SERVICE, _project=UI_PROJECT)
  API_StackDriver("service").entries().write(body=body).execute()


def log_get(recipe_id=None, timezone='America/Los_Angeles'):
  """Returns last actionable job run for a specific recipe or all recipes.

  Pulls status entries from StackDriver in reverse order.  First record for each recipe
  is assumed to be offical last known status.  All tasks within the same day as the first
  record are logged giving summary of last known run.  

  A single recipe may be run multiple times for multiple tasks at different hours, do not
  assume a JOB_COMPLETE means a recipe is complete.  Only way to ensure a recipe is complete
  is to compare all tasks run against all tasks in recipe ( not done by log code, handled
  bu upstream caller ).

  Loads a record in the format:

  { recipe_uuid:{
    "date": "< timezone adjusted date of job, defines valid 24 hour period for all tasks to execute >",
    "status": "< last reported job status other than JOB_BOUNCE, JOB_DUPLICATE >",
    "tasks": {
      "<task-instance>": [
        datetime(< timestamp adjusted to local timezone of run within same [date] period >),
      ], 
    }
    "stdout":"< text of task output if present in last run of task >",
    "stderr":"< text of task error if present in last run of task >",
  }

  Args:
    - recipe_id ( string ) - Optional, if provided returns a single record for a single job.
    - timezone ( string ) - The local timezone to cast all record times into.

  Returns:
    - A dictionary of logs keyed by job uid or a single record.

  """

  # ignore JOB_DISPATCH, JOB_RECEIVE, JOB_BOUNCE, JOB_DUPLICATE because they obscure last actionable job run
  body = {
    "resourceNames": [
      "projects/%s" % UI_PROJECT,
    ],
    "filter": '\
       logName="projects/%s/logs/StarThinker" \
       AND labels.version="1" \
       AND labels.layer="JOB" \
       AND labels.event!="JOB_DISPATCH" \
       AND labels.event!="JOB_RECEIVE" \
       AND labels.event!="JOB_BOUNCE" \
       AND labels.event!="JOB_DUPLICATE" \
       AND labels.event!="JOB_TASK_START" \
    ' % UI_PROJECT,
    "orderBy": "timestamp desc",
    "pageSize": 1000 
  }

  if recipe_id:
    body['filter'] += ' AND operation.id="%s"' % recipe_id

  logs = {}

  project.initialize(_service=UI_SERVICE, _project=UI_PROJECT)
  for entry in API_StackDriver("service", iterate=True).entries().list(body=body).execute():
    try:
      uuid = entry['operation']['id']

      # first time a recipe status appears, log it ( its the last status in a reverse sort )
      if uuid not in logs:
        logs[uuid] = {
          'date':entry['jsonPayload']['worker']['job_date'],
          'status':entry['labels']['event'],
          'tasks':{},
          'stderr':[],
          'stdout':[],
        }

      # only log tasks from the same job_date
      if entry['jsonPayload']['worker']['job_date'] == logs[uuid]['date']:
        if entry['labels']['event'] == 'JOB_TASK_COMPLETE':
          key = '%s-%d' % (entry['jsonPayload']['worker']['task'], entry['jsonPayload']['worker']['instance'])
          if key not in logs[uuid]['tasks']:
            # only log stdout and dtderr from most recent execution of a task
            logs[uuid]['stdout'].append(entry['jsonPayload']['worker']['stdout'])           
            logs[uuid]['stderr'].append(entry['jsonPayload']['worker']['stderr'])
            logs[uuid]['tasks'][key] = []
          # log all execution times
          logs[uuid]['tasks'][key].append(time_local(datetime.strptime(entry['timestamp'][:-4], "%Y-%m-%dT%H:%M:%S.%f"), timezone))
           
    except Exception, e: 
      # aggressive ignore because logs is a best effort thing, mostly catches legacy log key exceptions when field names change
      pass

  # reverse all logs per recipe to make them chronological again
  for value in logs.values():
    value['stderr'] = '\n'.join(reversed(value['stderr']))
    value['stdout'] = '\n'.join(reversed(value['stdout']))

  return logs.get(recipe_id, {}) if recipe_id else logs


def log_manager_start():
  log_put(MANAGER_START, {}, LogSeverity.NOTICE)


def log_manager_end():
  log_put(MANAGER_END, {}, LogSeverity.NOTICE)


def log_manager_error(error):
  log_put(MANAGER_ERROR, {}, LogSeverity.ALERT, error)


def log_manager_exception(error):
  log_put(MANAGER_EXCEPTION, {}, LogSeverity.ALERT, error)


def log_job_bounce(recipe):
  log_put(JOB_BOUNCE, recipe, LogSeverity.WARNING)


def log_job_cancel(recipe):
  log_put(JOB_CANCEL, recipe, LogSeverity.NOTICE)


def log_job_duplicate(recipe):
  log_put(JOB_DUPLICATE, recipe, LogSeverity.WARNING)


def log_job_dispatch(recipe):
  log_put(JOB_DISPATCH, recipe, LogSeverity.NOTICE)


def log_job_receive(recipe):
  log_put(JOB_RECEIVE, recipe, LogSeverity.NOTICE)


def log_job_start(recipe):
  log_put(JOB_START, recipe, LogSeverity.NOTICE)


def log_job_fail(recipe):
  log_put(JOB_FAIL, recipe, LogSeverity.ERROR)


def log_job_complete(recipe):
  log_put(JOB_COMPLETE, recipe, LogSeverity.NOTICE)


def log_job_timeout(recipe):
  log_put(JOB_TIMEOUT, recipe, LogSeverity.ERROR)


def log_job_exception(recipe, error):
  log_put(
    JOB_EXCEPTION, 
    {}, # assume recipe may have malformed JSON so pass as stdout ( also json and text is exclusive in stackdriver )
    LogSeverity.CRITICAL, 
    (recipe if isinstance(recipe, basestring) else json.dumps(recipe, indent=2, sort_keys=True, default=str)) + '\n\n' + error
  )


def log_job_task_start(recipe, task, instance):
  recipe['worker']['task'] = task
  recipe['worker']['instance'] = instance
  log_put(JOB_TASK_START, recipe, LogSeverity.NOTICE)


def log_job_task_complete(recipe, task, instance, stdout, stderr):
  # this will mutate recipe, all future logs will record last task run, for example log_job_cancel(...) will retain the last task run
  recipe['worker']['task'] = task
  recipe['worker']['instance'] = instance
  recipe['worker']['stdout'] = stdout
  recipe['worker']['stderr'] = stderr
  log_put(JOB_TASK_COMPLETE, recipe, LogSeverity.ERROR if stderr else LogSeverity.NOTICE)


def is_job_running(recipe_id):
  # recipe may be running on a different worker, check the centralized logs
  return log_get(recipe_id).get('status') in (JOB_RECEIVE, JOB_START, JOB_TASK_START, JOB_TASK_COMPLETE)


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


def time_local(timestamp, timezone):
  if timestamp:
    tz = pytz.timezone(timezone)
    return timestamp.replace(tzinfo=pytz.utc).astimezone(tz)
  else:
    return None
