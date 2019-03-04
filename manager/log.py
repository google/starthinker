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
import logging
import json
from datetime import datetime
from google.cloud import bigquery

from starthinker.config import UI_PROJECT, UI_SERVICE, UI_LOG_NAMESPACE, UI_LOG_KIND, UI_LOG_DATASET, UI_LOG_TABLE
from starthinker.util.bigquery import query_to_rows
from starthinker.util.project import project
from starthinker.util.datastore import datastore_list, datastore_write, datastore_read


JOB_STARTED = 'JOB_STARTED'
JOB_COMPLETED = 'JOB_COMPLETED'
JOB_FAILED = 'JOB_FAILED'
JOB_TIMEDOUT = 'JOB_TIMEDOUT'


def log_put(event, job_id, execution_id, stdout='', stderr=''):
  """Generic log weiter used by helper functions. Writes to datastore.

  Creates a record that can be read using log_get function. Only the job_id is used as a key.
  Do not call this directly, use helper functions instead:
    - log_started
    - log_failed
    - log_completed
    - log_timedout

  Stores the following enitity:

    ```
    [UI_PROJECT].Datastore.[UI_LOG_NAMESPACE].[UI_LOG_KIND].name[job_id] = {
      execution_id 
      execution_status
      execution_timestamp
      execution_stdout
      execution_stderr
    }
    ```

  Args:
    - event ( string ): One of the following: JOB_STARTED, JOB_COMPLETED, JOB_FAILED, JOB_TIMEDOUT
    - job_id ( string ): The universal identifier of a job, used as key for record.
    - execution_id ( string ): The id of the specific run of the job.
    - stdout ( string ): Mesaging output form the task. Present depending on task.
    - stderr ( string ): Error output form the task. Present if job failed.
  """

  project.initialize(_service=UI_SERVICE, _project=UI_PROJECT)
  datastore_write(
    "service", 
    UI_PROJECT,
    UI_LOG_NAMESPACE,
    UI_LOG_KIND, 
    job_id, 
    {
      'execution_id':execution_id,
      'execution_status':event,
      'execution_timestamp':datetime.utcnow(),
      'execution_stdout':stdout,
      'execution_stderr':stderr
    }
  )

  client = bigquery.Client.from_service_account_json(UI_SERVICE)
  dataset = client.dataset(UI_LOG_DATASET)
  events_table = dataset.table(UI_LOG_TABLE)
  events_table.reload()
  events_table.insert_data([[datetime.utcnow(), event, job_id, execution_id, stdout or '', stderr or '']])


def log_get(job_id=None, timezone='America/Los_Angeles'):
  """Returns a log for the specified job or all jobs using given timezone for timestamps.

  Uses datastore to maintian logs of execution. All times are stored in UTC and converted at load.
  Catches ALL exceptions because fetching a alog can fail gracefully by returning no log.

  Loads a record in the format:

  [UI_PROJECT].Datastore.[UI_LOG_NAMESPACE].[UI_LOG_KIND].name[job_id] = {
    recipe_uid - computed from job id to allow list of values
    execution_id - from entity
    execution_status - from entity
    execution_timestamp - altered by applying time zone
    execution_timeago - computed from timestamp to allow relative execution age
    execution_stdout - from entity
    execution_stderr - from entity
  }

  Args:
    - job_id ( string ) - Optional, if provided returns a single record for a single job.
    - timezone ( string ) - The time zone to cast all record times into.

  Returns:
    - A dictionary of logs keyed by job uid or a single record.

  """

  try:
    project.initialize(_service=UI_SERVICE, _project=UI_PROJECT)

    if job_id: 
      ignore, log = datastore_read("service", UI_PROJECT, UI_LOG_NAMESPACE, UI_LOG_KIND, job_id).next()

      log['recipe_uid'] = job_id
      log['execution_timeago'] = time_ago(log['execution_timestamp'])
      log['execution_timestamp'] = time_local(log['execution_timestamp'], timezone)
      return log

    else: 
      logs = dict(datastore_list("service", UI_PROJECT, UI_LOG_NAMESPACE, UI_LOG_KIND))
      for k, v in logs.items():
        v['recipe_uid'] = k
        v['execution_timeago'] = time_ago(v['execution_timestamp'])
        v['execution_timestamp'] = time_local(v['execution_timestamp'], timezone)
      return logs

  except Exception, e:
    print 'manager.log.log_get(...) Exception:', str(e)
    return {} 


def log_started(worker):
  log_put(JOB_STARTED, worker['uuid'], worker.get('container_name', 'UKNOWN'))


def log_failed(worker):
  stdout, stderr = worker_log(worker)
  log_put(JOB_FAILED, worker['uuid'], worker.get('container_name', 'UKNOWN'), stdout=stdout, stderr=stderr)


def log_completed(worker):
  stdout, stderr = worker_log(worker)
  log_put(JOB_COMPLETED, worker['uuid'], worker.get('container_name', 'UKNOWN'), stdout=stdout, stderr=stderr)


def log_timedout(worker):
  log_put(JOB_TIMEDOUT, worker['uuid'], worker.get('container_name', 'UKNOWN'))


def is_job_running(job_id):
  log_entry = log_get(job_id)

  print log_entry
  if log_entry and 'execution_timestamp' in log_entry:
    log_entry['execution_timestamp'] = log_entry['execution_timestamp'].replace(tzinfo=None)

    if (datetime.now() - log_entry['execution_timestamp']).seconds < (3 * 60 * 60):
      return log_entry.get('execution_status', '') == JOB_STARTED
    return False
  else:
    return False

def worker_log(worker):
  stdout = ''
  stderr = ''

  for line in worker['job'].stdout:
    logging.debug('%s: %s' % (worker['uuid'], line))
    stdout += '%s\n' % line

  for line in worker['job'].stderr:
    logging.debug('%s: %s' % (worker['uuid'], line))
    stderr += '%s\n' % line

  return stdout, stderr


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
