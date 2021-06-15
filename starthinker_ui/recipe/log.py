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

#https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry

import urllib.request, urllib.error, urllib.parse
import json

from starthinker.config import UI_PROJECT, UI_SERVICE
from starthinker.util.configuration import Configuration
from starthinker.util.google_api import API_StackDriver

LOG_VERSION = '2'  # must be string

MANAGER_START = 'MANAGER_START'
MANAGER_END = 'MANAGER_END'
MANAGER_TIMEOUT = 'MANAGER_TIMEOUT'
MANAGER_ERROR = 'MANAGER_ERROR'
MANAGER_SCALE = 'MANAGER_SCALE'

JOB_UPDATE = 'JOB_UPDATE'
JOB_START = 'JOB_START'
JOB_END = 'JOB_END'
JOB_ERROR = 'JOB_ERROR'
JOB_CANCEL = 'JOB_CANCEL'
JOB_TIMEOUT = 'JOB_TIMEOUT'


class LogSeverity():
  DEFAULT = 0  # The log entry has no assigned severity level.
  DEBUG = 100  # Debug or trace information.
  INFO = 200  # Routine information, such as ongoing status or performance.
  NOTICE = 300  # Normal but significant events, such as start up, shut down, or a configuration change.
  WARNING = 400  # Warning events might cause problems.
  ERROR = 500  # Error events are likely to cause problems.
  CRITICAL = 600  # Critical events cause more severe problems or outages.
  ALERT = 700  # A person must take an action immediately.
  EMERGENCY = 800  # One or more systems are unusable.


VERBOSE = False


def log_verbose(verbose=True):
  global VERBOSE
  VERBOSE = verbose


INSTANCE_NAME = None


def get_instance_name(default='UNKNOWN'):
  global INSTANCE_NAME
  if INSTANCE_NAME is None:
    try:
      return urllib.request.urlopen(
          urllib.request.Request(
              'http://metadata.google.internal/computeMetadata/v1/instance/name',
              headers={'Metadata-Flavor': 'Google'})).read().decode()
    except:
      INSTANCE_NAME = default
  return INSTANCE_NAME


def log_put(event, severity, job=None, text=None, payload=None):
  """Generic log writer used by helper functions.

  Writes to StackDriver.

  Creates a record that can be read using log_get function. Entire recipe is
  logged, worker data and stdout and stderr are added to the JOSN under worker
  key.
  Only JOB_EXCEPTION and MANAGER_EXCEPTION logs to text in case JSON is corrupt,
  everythng else is JSON.

  Do not call this directly, use helper functions instead:
    - log_manager_start
    - log_manager_timeout
    - log_manager_error
    - log_manager_end
    - log_job_dispatch
    - log_job_receive
    - log_job_start
    - log_job_end
    - log_job_error
    - log_job_timeout

  WARNING: Do not corrupt recipe in log code, it is actively being used by
  workers while being logged.

  Args:
    - event ( string ): One of the JOB_* enums.
    - severity ( enum ): Stackdriver severity level.
    - job ( json ): Recipe workflow to execute.
    - text ( string ): Messaging output form the task. Usual stdout and stderr.
    - payload ( json ): Output from the scaler or any generic json payload.
  """

  if VERBOSE:
    print('LOGGING:', event, severity, text or '')

  body = {
      'entries': [{
          'logName': 'projects/%s/logs/StarThinker' % UI_PROJECT,
          'severity': severity,
          'resource': {
              'type': 'project',
              'labels': {
                  'key': UI_PROJECT
              },
          },
          'labels': {
              'version': LOG_VERSION,
              'layer': event.split('_')[0],
              'event': event,
              'instance': get_instance_name(),
          },
          #"operation": {
          #  "id": string
          #  "producer": string
          #  "first": False,
          #  "last": False,
          #},
          # already in recipe worker logging task and instance, does this have additional value?
          #"sourceLocation": {
          #  "file": string,
          #  "line": string,
          #  "function": string
          #},
      }],
      'partialSuccess': False,
      'dryRun': False
  }

  if text is not None:
    body['entries'][0]['textPayload'] = text
  elif payload is not None:
    body['entries'][0]['jsonPayload'] = payload
  else:
    # Removing tasks from job REMOVES ALL POTENTIAL CREDENTIALS IN CODE
    job_buffer = json.loads(
        json.dumps(job, indent=2, sort_keys=True, default=str))
    if 'tasks' in job_buffer['recipe']:
      del job_buffer['recipe']['tasks']
    if 'auth' in job_buffer['recipe']['setup']:
      del job_buffer['recipe']['setup']['auth']
    body['entries'][0]['jsonPayload'] = job_buffer

  try:
    API_StackDriver(
      Configuration(
        service=UI_SERVICE,
        project=UI_PROJECT
      ),
      'service'
    ).entries().write(body=body).execute()
  except:
    print('LOG EVENT ERROR')


def log_get(recipe_id=[], timezone='America/Los_Angeles', days=1):
  """Returns last actionable job run for a specific recipe or all recipes.

  Pulls status entries from StackDriver in reverse order.  A single recipe may
  be run multiple times for multiple tasks at different hours, do not
  assume a JOB_END means a recipe is complete.  Only way to ensure a recipe is
  complete
  is to compare all tasks run against all tasks in recipe ( not done by log
  code).

  Args: - recipe_id ( string or list ) - Optional, if provided returns a single
  record for a single job. - timezone ( string ) - The local timezone to cast
  all record times into.

  Returns:
    - ( iterator ) - Each log entry.

  """

  body = {
      'resourceNames': ['projects/%s' % UI_PROJECT,],
      'filter':
          '\
       logName="projects/%s/logs/StarThinker" \
       AND labels.version="%s" \
       AND labels.layer="JOB" \
    ' % (UI_PROJECT, LOG_VERSION),
      'orderBy':
          'timestamp desc',
      'pageSize':
          1000
  }

  if recipe_id:
    if isinstance(recipe_id, str):
      recipe_id = [recipe_id]
    body['filter'] += ' AND ( %s )' % ' OR '.join(
        'operation.id="%s"' % r for r in recipe_id)

  for entry in API_StackDriver(
      Configuration(
        service=UI_SERVICE,
        project=UI_PROJECT
      ),
      'service',
      iterate=True
    ).entries().list(body=body).execute():
    yield entry


def log_manager_start():
  log_put(MANAGER_START, LogSeverity.NOTICE, text='')


def log_manager_end():
  log_put(MANAGER_END, LogSeverity.NOTICE, text='')


def log_manager_timeout():
  log_put(MANAGER_TIMEOUT, LogSeverity.NOTICE, text='')


def log_manager_error(error):
  log_put(MANAGER_ERROR, LogSeverity.ALERT, text=error)


def log_manager_scale(record):
  log_put(MANAGER_SCALE, LogSeverity.NOTICE, payload=record)


def log_job_update(job):
  log_put(JOB_UPDATE, LogSeverity.NOTICE, job)


def log_job_start(job):
  log_put(JOB_START, LogSeverity.NOTICE, job)


def log_job_end(job):
  log_put(JOB_END, LogSeverity.NOTICE, job)


def log_job_error(job):
  log_put(JOB_ERROR, LogSeverity.ERROR, job)


def log_job_cancel(job):
  log_put(JOB_CANCEL, LogSeverity.WARNING, job)


def log_job_timeout(job):
  log_put(JOB_TIMEOUT, LogSeverity.ERROR, job)
