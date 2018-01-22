###########################################################################
#
#  Copyright 2017 Google Inc.
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

#https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#resource
# https://cloud.google.com/bigquery/docs/reference/v2/jobs#resource

import sys
import csv
import pprint
import uuid
import json
import httplib2
from time import sleep

from util.bigquery.file_processor import FileProcessor

from google.cloud import bigquery
from google.cloud.bigquery.table import Table
from googleapiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload

from util.project import project
from util.auth import get_service, get_client


BIGQUERY_RETRIES = 3
CHUNKSIZE = 2 * 1024 * 1024
processor = FileProcessor()

reload(sys)
sys.setdefaultencoding('utf-8')


def bigquery_date(value):
  return value.strftime('%Y%m%d')


def job_wait(service, job):
  if project.verbose: print 'BIGQUERY JOB WAIT:', job['jobReference']['jobId']

  request = service.jobs().get(
    projectId=job['jobReference']['projectId'],
    jobId=job['jobReference']['jobId']
  )

  while True:
    sleep(1)
    print '.',
    sys.stdout.flush()
    result = request.execute(num_retries=BIGQUERY_RETRIES)
    if result['status']['state'] == 'DONE':
      if 'errorResult' in result['status']: print 'JOB ERROR:', result['status']['errorResult']
      if project.verbose: print 'JOB COMPLETE:', result['id']
      return


def job_insert(auth, job_id):
  if project.verbose: print 'BIGQUERY JOB RUN:', job_id
  project_id, job_id = job_id.split(':', 1)
  service = get_service('bigquery', 'v2', auth)

  # fetch existing job
  request = service.jobs().get(projectId=project_id, jobId=job_id)
  job_old = request.execute()

  #pprint.PrettyPrinter(depth=20).pprint(job_old)
  #exit()

  # copy configuration
  job_new = {
    'jobReference': {
      'projectId': project_id,
      'jobId': str(uuid.uuid4())
    },
   'configuration':job_old['configuration'],
  }

  # execute new job and wait completion
  job = service.jobs().insert(projectId=project_id, body=job_new).execute(num_retries=BIGQUERY_RETRIES)
  job_wait(service, job)


def jobs_insert(auth, job_ids):
  for job_id in job_ids: job_insert(auth, job_id)


def datasets_get(auth, project_id, name):
  service = get_service('bigquery', 'v2', auth)
  return service.datasets().get()


def datasets_create(auth, project_id, dataset_id):

  service = get_service('bigquery', 'v2', auth)

  body = {
    "description":dataset_id,
    "datasetReference": { 
      "projectId":project_id,
      "datasetId":dataset_id,
    },
    "location":"US",
    "friendlyName":dataset_id,
  }

  try:
    job = service.datasets().insert(projectId=project_id, body=body).execute(num_retries=BIGQUERY_RETRIES)
    sleep(1)
  except HttpError, e:
    if e.resp.status in [403, 500, 503]: sleep(5)
    elif json.loads(e.content)['error']['code'] == 409: pass # already exists ( ignore )
    else: raise


# roles = READER, WRITER, OWNER
def datasets_access(auth, project_id, dataset_id, role='READER', emails=[], groups=[], views=[]):
  service = get_service('bigquery', 'v2', auth)

  if emails or groups or views:
    access = service.datasets().get(projectId=project_id, datasetId=dataset_id).execute(num_retries=BIGQUERY_RETRIES)["access"]

    # if emails
    for email in emails:
      access.append({
        "userByEmail":email,
        "role":role,
      })

    # if groups
    for group in groups:
      access.append({
        "groupByEmail":group,
        "role":role,
      })

    for view in views:
      access.append({
        "view": {
          "projectId": project_id,
          "datasetId": view['dataset'],
          "tableId": view['view']
        }
      })

    job = service.datasets().patch(projectId=project_id, datasetId=dataset_id, body={'access':access}).execute(num_retries=BIGQUERY_RETRIES)
    sleep(1)


# Creator, Viewer, Admin
#def job_access(auth, project, role=['Creator', 'Viewer', 'Admin'], emails=[], groups=[], services=[], domains=[]):
#  service = get_service('bigquery', 'v1', auth)
#
#  if emails or groups or services or groups:
#    access = service.jobs().getIamPolicy().execute(num_retries=RETRIES)
#
#    access['bindings'] = []
#    for r in role:
#      access['bindings'].append({
#        "role":"roles/bigquery.object%s" % r,
#        "members": ['user:%s' % m for m in emails] + \
#                   ['group:%s' % m for m in groups] + \
#                   ['serviceAccount:%s' % m for m in services] + \
#                   ['domain:%s' % m for m in domains]
#      })
#
#    job = service.jobs().setIamPolicy(body=access).execute(num_retries=RETRIES)
#    sleep(1)


def query_to_local_file(auth, sql, local_file_name, use_legacy_sql=True):
  result = query(sql, use_legacy_sql)
  out_file = open(local_file_name, 'w')
  out = csv.writer(out_file)

  for row in result:
    out.writerow(row)

  out_file.close()


def query_to_table(auth, project_id, dataset_id, table_id, query, disposition='WRITE_TRUNCATE', use_legacy_sql=True):
  service = get_service('bigquery', 'v2', auth)

  body={
    'configuration': {
      'query': {
        'useLegacySql': use_legacy_sql,
        'query':query,
        'destinationTable': {
          'projectId':project_id,
          'datasetId':dataset_id,
          'tableId':table_id
        },
        'createDisposition':'CREATE_IF_NEEDED',
        'writeDisposition':disposition,
        'allowLargeResults':True
      },
    }
  }

  #try:
  job = service.jobs().insert(projectId=project_id, body=body).execute(num_retries=BIGQUERY_RETRIES)
  job_wait(service, job)

  #print job
  #except HttpError, e:
  #  if e.resp.status in [403, 500, 503]: sleep(5)
  #  #elif json.loads(e.content)['error']['code'] == 409: pass # already exists ( ignore )
  #  else: raise


def query_to_view(auth, project_id, dataset_id, view_id, query, legacy=True, replace=False):
  service = get_service('bigquery', 'v2', auth)
  
  body={
    'tableReference': {
      'projectId':project_id,
      'datasetId':dataset_id,
      'tableId':view_id,
    }, 
    'view': {
      'query':query,
      'useLegacySql':legacy
    }
  }

  try:
    job = service.tables().list(projectId=project_id, datasetId=dataset_id).execute(num_retries=BIGQUERY_RETRIES)
    if replace and ('%s:%s.%s' % (project_id, dataset_id, view_id)) in [table['id'] for table in job['tables']]:
      job = service.tables().update(
          projectId=project_id,
          datasetId=dataset_id,
          tableId=view_id, body=body).execute(num_retries=BIGQUERY_RETRIES)
    else:
      job = service.tables().insert(projectId=project_id, datasetId=dataset_id, body=body).execute(num_retries=BIGQUERY_RETRIES)
  except HttpError, e:
    #if e.resp.status in [403, 500, 503]: sleep(5)
    if json.loads(e.content)['error']['code'] == 409: pass # already exists ( ignore )
    else: raise


#struture = CSV, NEWLINE_DELIMITED_JSON
#disposition = WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
def storage_to_table(auth, project_id, dataset_id, table_id, path, schema=[], skip_rows=1, structure='CSV', disposition='WRITE_TRUNCATE'):

  service = get_service('bigquery', 'v2', auth)

  body = {
    'configuration': {
      'load': {
        'destinationTable': {
          'projectId': project_id,
          'datasetId': dataset_id,
          'tableId': table_id,
        }, 
        'sourceFormat': 'NEWLINE_DELIMITED_JSON',
        'writeDisposition': disposition,
        'autodetect': True,
        'ignoreUnknownValues':True,
        'sourceUris': [
          'gs://%s' % path.replace(':', '/'),
        ], 
      }
    } 
  }

  if schema:
    body['configuration']['load']['schema'] = { 'fields':schema }
    body['configuration']['load']['autodetect'] = False
    
  if structure == 'CSV':
    body['configuration']['load']['sourceFormat'] = 'CSV'
    body['configuration']['load']['skipLeadingRows'] = skip_rows

  job = service.jobs().insert(projectId=project_id, body=body).execute(num_retries=BIGQUERY_RETRIES)
  job_wait(service, job)


def csv_to_table(auth, project_id, dataset_id, table_id, data, schema=[], skip_rows=1, structure='CSV', disposition='WRITE_TRUNCATE'):
  if project.verbose: print 'BIGQUERY: ', project_id, dataset_id, table_id

  service = get_service('bigquery', 'v2', auth)

  body = {
    'configuration': {
      'load': {
        'destinationTable': {
          'projectId': project_id,
          'datasetId': dataset_id,
          'tableId': table_id,
        },
        'sourceFormat': 'NEWLINE_DELIMITED_JSON',
        'writeDisposition': disposition,
        'autodetect': True,
        'ignoreUnknownValues': True,
      }
    }
  }

  if schema:
    body['configuration']['load']['schema'] = { 'fields':schema }
    body['configuration']['load']['autodetect'] = False
    
  if structure == 'CSV':
    body['configuration']['load']['sourceFormat'] = 'CSV'
    body['configuration']['load']['skipLeadingRows'] = skip_rows

  media = MediaIoBaseUpload(data, mimetype='application/octet-stream', resumable=True, chunksize= 100 * 1024000) # 100MB
  job = service.jobs().insert(projectId=project_id, body=body, media_body=media)
  response = None
  while response is None:
    status, response = job.next_chunk()
    if project.verbose and status: print "Uploaded %d%%." % int(status.progress() * 100)
  if project.verbose: print "Uploaded 100%."
  job_wait(service, job.execute(num_retries=BIGQUERY_RETRIES))


def tables_get(auth, project_id, name):
  dataset_id, table_id = name.split(':', 1)
  service = get_service('bigquery', 'v2', auth)
  return service.tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()


def list_to_table(rows, dataset, table_name, schema, replace=False):
  print(rows)


def list_jobs(auth, project_id):
  service = get_service('bigquery', 'v2', auth)
  client = get_client('bigquery')
  #return service.jobs().list(projectId=project_id).execute()
  return client.list_jobs()


def get_job(auth, project_id, job_id):
  service = get_service('bigquery', 'v2', auth)
  return service.jobs().get(projectId=project_id, jobId=job_id).execute()


def get_table(auth, dataset, table_name):
  client = get_client('bigquery', auth=auth)

  dataset = client.dataset(dataset)
  table = dataset.table(table_name)

  return table

# this all has to be done while streaming, so preserve the iterator, schema is returned by reference
# DO NOT rebind schema, it will break the pass by reference
# FIX: ADD HANDLERS FOR REPEAT AND RECORD FIELDS ( use pointers stack to track recursion depth )
def get_schema(rows, schema, header=True):

  # everything else defaults to STRING
  type_to_bq = {int:'INTEGER', long:'INTEGER', bool:'BOOLEAN'} 

  # first non null value determines type
  non_null_column = set()

  first = True
  for row in rows:
    # get header if exists
    if first:
      for index, value in enumerate(row): 
        schema.append({ "name":value if header else 'Field_%d' % index, "type":"STRING" }) # DO NOT REBIND, USE APPEND

    # then determine type of each column
    if not first and header: 
      for index, value in enumerate(row):
        # if null, set only mode
        if value == '': 
          schema[index]['mode'] = 'NULLABLE'
        else:
          column_type = type_to_bq.get(type(value), 'STRING')
          # if type is set, check to make sure its consistent
          if index in non_null_column:
            # change type only if its inconsistent
            if column_type != schema[index]['type']: 
              schema[index]['type'] = 'STRING'
          # if first non null value, then just set type
          else: 
            schema[index]['type'] = column_type
            non_null_column.add(index)

    # return row so iteration can continue
    yield row

    # no longer first row
    first = False


def local_file_to_table(auth, dataset, table_name, schema, file_name, replace=False, file_type='NEWLINE_DELIMITED_JSON'):
  table = get_table(auth, dataset, table_name)

  if replace and table.exists():
    table.delete()

  table.schema = schema

  if not table.exists():
    table.create()

  job = table.upload_from_file(open(file_name, 'rb'), file_type)

  while job.state != 'DONE':
    if project.verbose: print 'BigQuery load job status %s' % job.state
    sleep(10)
    job.reload()

# TODO: Change variant to query_to_table(....)
def query(query, dataset_name=None, use_legacy_sql=True, into_table=None, replace_append='APPEND', auth='user'):
  client = get_client('bigquery', auth=auth)
  if dataset_name: dataset = client.dataset(dataset_name)

  if not into_table:
    query = client.run_sync_query(query)
    query.use_legacy_sql = use_legacy_sql
    query.run()
    return query.fetch_data()
  else:
    table = dataset.table(name=into_table)
    job = client.run_async_query(str(uuid.uuid1()), query)
    job.destination = table
    if replace_append == 'APPEND':
      job.write_disposition = 'WRITE_APPEND'
    elif replace_append == 'REPLACE':
      job.write_disposition = 'WRITE_TRUNCATE'
    job.allow_large_results = True
    job.begin()
    return None
