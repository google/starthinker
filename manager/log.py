import pytz
import logging
from datetime import datetime

from starthinker.setup import UI_PROJECT, UI_SERVICE, UI_LOG_DATASET, UI_LOG_TABLE
from starthinker.util.bigquery import query_to_rows
from starthinker.util.project import project

JOB_STARTED = 'JOB_STARTED'
JOB_COMPLETED = 'JOB_COMPLETED'
JOB_FAILED = 'JOB_FAILED'
JOB_TIMEDOUT = 'JOB_TIMEDOUT'

JOB_STATUS_QUERY='''
SELECT
  job_id AS id,
  event AS status,
  DATETIME(event_timestamp, 'UTC') as time_stamp, 
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), event_timestamp, SECOND) AS time_ago
FROM
  `worker.events`
WHERE
  job_id = '%s'
GROUP BY
  1, 2, 3, 4
ORDER BY
  time_stamp DESC
LIMIT 1;
'''

JOBS_STATUS_QUERY='''
SELECT 
  id,
  status,
  time_stamp,
  time_ago
FROM (
  SELECT 
    job_id AS id,
    event as status,
    DATETIME(event_timestamp, 'UTC') as time_stamp, 
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), event_timestamp, SECOND) AS time_ago, 
    row_number() OVER(PARTITION BY job_id ORDER BY event_timestamp DESC) AS row_number
 FROM
   `worker.events`
) sub
WHERE row_number = 1;
'''

def log_put(event, job_id, execution_id):
  client = bigquery.Client.from_service_account_json(UI_SERVICE)
  dataset = client.dataset(UI_LOG_DATASET)
  events_table = dataset.table(UI_LOG_TABLE)
  events_table.reload()
  events_table.insert_data([[datetime.utcnow(), event, job_id, execution_id]])


def log_get(job_id=None, timezone='America/Los_Angeles'):
  try:
    project.initialize(_service=UI_SERVICE)
    if job_id:
      query = JOB_STATUS_QUERY % job_id
      row = query_to_rows('service', UI_PROJECT, UI_LOG_DATASET, query, row_max=1, legacy=False).next()
      return { 
        'id':row[0], 
        'status':row[1], 
        'time_stamp':time_local(row[2], timezone), 
        'time_ago':time_ago(row[3]),
      }  if row else {}
    else:
      query = JOBS_STATUS_QUERY
      rows = query_to_rows('service', UI_PROJECT, UI_LOG_DATASET, query, legacy=False)
      return dict([(
        row[0], 
        {
          'id':row[0],
          'status':row[1],
          'time_stamp':time_local(row[2], timezone),
          'time_ago':time_ago(row[3]),
        }
      ) for row in rows])
  except Exception, e:
    print str(e)
    return {} 


def log_started(worker):
  log_put(JOB_STARTED, worker['uuid'], worker.get('container_name', 'UKNOWN'))

def log_failed(worker):
  log_put(JOB_FAILED, worker['uuid'], worker.get('container_name', 'UKNOWN'))
  worker_log(worker)
    
def log_completed(worker):
  log_put(JOB_COMPLETED, worker['uuid'], worker.get('container_name', 'UKNOWN'))
  worker_log(worker)

def log_timedout(worker):
  log_put(JOB_TIMEDOUT, worker['uuid'], worker.get('container_name', 'UKNOWN'))
  #worker_log(worker)

def worker_log(worker):
  for line in worker['job'].stdout:
    logging.debug('%s: %s' % (worker['uuid'], line))

  for line in worker['job'].stderr:
    logging.debug('%s: %s' % (worker['uuid'], line))

def is_job_running(job_id):
  return log_get(job_id).get('status', '') == JOB_STARTED

def time_ago(seconds):
  ago = ''

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
    timestamp = datetime.strptime(timestamp.split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
    tz = pytz.timezone(timezone)
    return tz.localize(timestamp)
  else:
    return None
