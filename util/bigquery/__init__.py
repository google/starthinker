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

# https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#resource
# https://cloud.google.com/bigquery/docs/reference/v2/jobs#resource
# https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list

import re
import sys
import csv
import pprint
import uuid
import json
import httplib2
from time import sleep

from google.cloud import bigquery
from google.cloud.bigquery.table import Table
from googleapiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload

from util.project import project
from util.auth import get_service, get_client


BIGQUERY_RETRIES = 3
CHUNKSIZE = 2 * 1024 * 1024
#RE_SCHEMA = re.compile(r'[ \=\:\-\/\(\)\+\&\%]')
RE_SCHEMA = re.compile('[^0-9a-zA-Z]+')

reload(sys)
sys.setdefaultencoding('utf-8')


def field_list_to_schema(field_list):
  result = []
  field_names = []

  for field in field_list:
    field_name = re.sub(r'[ \=\:\-\/\(\)\+\&\%]', '_', field.strip())

    suffix = ''
    ct = 0
    while field_name + suffix in field_names:
      ct += 1
      suffix = '_' + str(ct)

    field_name += suffix
    field_names.append(field_name)

    result.append({
        'name': field_name,
        'type': 'STRING',
        'mode': 'NULLABLE'
    })

  return result


def bigquery_date(value):
  return value.strftime('%Y%m%d')


def _retry(job, retries=10, wait=5):
  try:
    data = job.execute()
    #pprint.PrettyPrinter().pprint(data)
    return data
  except HttpError, e:
    if project.verbose: print str(e)
    if e.resp.status in [403, 429, 500, 503]:
      if retries > 0:
        sleep(wait)
        if project.verbose: print 'DCM RETRY', retries
        return _retry(job, retries - 1, wait * 2)
      elif json.loads(e.content)['error']['code'] == 409:
        pass # already exists ( ignore )
      else:
        raise


def job_wait(service, job):
  if project.verbose: print 'BIGQUERY JOB WAIT:', job['jobReference']['jobId']

  request = service.jobs().get(
    projectId=job['jobReference']['projectId'],
    jobId=job['jobReference']['jobId']
  )

  while True:
    sleep(1)
    if project.verbose: print '.',
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


# NOT USED SO RIPPING IT OUT, use util.sheets.query_to_rows and util.storage.object_put instead
#def query_to_local_file(auth, sql, local_file_name, use_legacy_sql=True):
#  result = query(sql, use_legacy_sql)
#  out_file = open(local_file_name, 'w')
#  out = csv.writer(out_file)
#
#  for row in result:
#    out.writerow(row)
#
#  out_file.close()


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

  def getSize(fileObject):
    fileObject.seek(0,2)
    retVal = fileObject.tell()
    return retVal

  if(getSize(data) > 0):
    media = MediaIoBaseUpload(data, mimetype='application/octet-stream', resumable=True, chunksize= 100 * 1024000) # 100MB


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
    #print 'BODY', body

    job = service.jobs().insert(projectId=project_id, body=body, media_body=media)
    response = None
    while response is None:
      status, response = job.next_chunk()
      if project.verbose and status: print "Uploaded %d%%." % int(status.progress() * 100)
    if project.verbose: print "Uploaded 100%."
    job_wait(service, job.execute(num_retries=BIGQUERY_RETRIES))

  else:
    try:
      service.tables().delete(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute(num_retries=BIGQUERY_RETRIES)
      print 'APR table exists. deleting current table...'
    except:
      print 'APR table does not exist. creating empty table...'
    body = {
      "tableReference": {
        "projectId": project_id,
        "datasetId": dataset_id,
        "tableId": table_id
      },
      "schema": {
        "fields": schema
      }
    }
    service.tables().insert(projectId=project_id, datasetId=dataset_id, body=body).execute(num_retries=BIGQUERY_RETRIES)


def tables_get(auth, project_id, name):
  dataset_id, table_id = name.split(':', 1)
  service = get_service('bigquery', 'v2', auth)
  return service.tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()


def table_to_rows(auth, project_id, dataset_id, table_id, fields=None, row_start=0, row_max=None):
  if project.verbose: print 'BIGQUERY ROWS:', project_id, dataset_id, table_id
  service = get_service('bigquery', 'v2', auth)
  next_page = None
  while next_page != '':
    response = service.tabledata().list(projectId=project_id, datasetId=dataset_id, tableId=table_id, selectedFields=fields, startIndex=row_start, maxResults=row_max, pageToken=next_page).execute()
    next_page = response.get('PageToken', '')
    converters = _build_converter_array(table_to_schema(auth, project_id, dataset_id, table_id), fields, len(response['rows'][0].get('f')))
    for row in response['rows']:
      yield [converters[i](r.values()[0]) for i, r in enumerate(row['f'])] # may break if we attempt nested reads


def table_to_schema(auth, project_id, dataset_id, table_id):
  if project.verbose: print 'TABLE SCHEMA:', project_id, dataset_id, table_id
  service = get_service('bigquery', 'v2', auth)
  response = _retry(service.tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id))
  return response['schema']


def query_to_rows(auth, project_id, dataset_id, query, row_max=None, use_legacy_sql=True):
  service = get_service('bigquery', 'v2', auth)

  body = {
    "kind": "bigquery#queryRequest",
    "query": query,
    "timeoutMs": 10000,
    "dryRun": False,
    "useQueryCache": True,
    "useLegacySql": use_legacy_sql
  }

  if row_max: body['maxResults'] = row_max

  if dataset_id:
    body['defaultDataset'] = {
      "projectId": project_id,
      "datasetId": dataset_id
    }

  next_page = None
  while next_page != '':
    response = service.jobs().query(projectId=project_id, body=body).execute()
    if 'rows' in response: #return empty array if there is no data
      next_page = response.get('PageToken', '')
      converters = _build_converter_array(response.get('schema', None), None, len(response['rows'][0].get('f')))
      for row in response['rows']:
        yield [converters[i](r.values()[0]) for i, r in enumerate(row['f'])] # may break if we attempt nested reads

    else:
      yield None




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


# CAUTION: Memory suck. This function sabotages iteration by iterating thorough the new object and returning a new iterator
# RECOMMEND: Define the schema yourself, it will also ensure data integrity downstream.
def get_schema(rows, header=True, infer_type=True):

  schema = []
  row_buffer = []

  # everything else defaults to STRING
  type_to_bq = {int:'INTEGER', long:'INTEGER', bool:'BOOLEAN', float:'FLOAT'} if infer_type else {} # empty lookup defaults to STRING below

  # first non null value determines type
  non_null_column = set()

  first = True
  ct_columns = 0

  for row in rows:

    # buffer the iterator to be returned with schema
    row += [None] * (ct_columns - len(row))
    row_buffer.append(row)

    # define schema field names and set defaults ( if no header enumerate fields )
    if first:
      ct_columns = len(row)
      for index, value in enumerate(row):
        schema.append({ "name":RE_SCHEMA.sub('_', value).strip('_') if header else 'Field_%d' % index, "type":"STRING" })

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
              # mixed integers and floats default to floats
              if column_type in ('INTEGER', 'FLOAT') and schema[index]['type'] in ('INTEGER', 'FLOAT'):
                schema[index]['type'] = 'FLOAT'
              # any strings are always strings
              else:
                schema[index]['type'] = 'STRING'
          # if first non null value, then just set type
          else:
            schema[index]['type'] = column_type
            non_null_column.add(index)

    # no longer first row
    first = False

  return row_buffer, schema


def _int_from_json(value):
  if value:
    return int(value)
  else:
    return value


def _float_from_json(value):
  if value:
    return float(value)
  else:
    return value


_JSON_CONVERTERS = {
  'INTEGER':  _int_from_json,
  'INT64':  _int_from_json,
  'FLOAT':  _float_from_json,
  'FLOAT64': _float_from_json,
  'BOOLEAN': lambda v: v,
  'BOOL': lambda v: v,
  'STRING': lambda v: v, #no conversion needed, adapt others as needed
  'BYTES': lambda v: v,
  'TIMESTAMP': lambda v: v,
  'DATETIME': lambda v: v,
  'DATE': lambda v: v,
  'TIME': lambda v: v,
  'RECORD': lambda v: v,
}


def _build_converter_array(schema, fields, col_count):
  converters = []
  if schema:
    for field in schema['fields']:
      if fields is None or field in fields:
        converters.append(_JSON_CONVERTERS[field['type']])
  else: 
    #No schema so simply return the string as string
    converters = [lambda v: v] * col_count
  #print converters
  return converters



# TODO: Deprecated, use query_to_rows or query_to_table
#def query(query, dataset_name=None, use_legacy_sql=True, into_table=None, replace_append='APPEND', auth='user'):
#  client = get_client('bigquery', auth=auth)
#  if dataset_name: dataset = client.dataset(dataset_name)
#
#  if not into_table:
#    query = client.run_sync_query(query)
#    query.use_legacy_sql = use_legacy_sql
#    query.run()
#    return query.fetch_data()
#  else:
#    table = dataset.table(name=into_table)
#    job = client.run_async_query(str(uuid.uuid1()), query)
#    job.destination = table
#    if replace_append == 'APPEND':
#      job.write_disposition = 'WRITE_APPEND'
#    elif replace_append == 'REPLACE':
#      job.write_disposition = 'WRITE_TRUNCATE'
#    job.allow_large_results = True
#    job.begin()
#    return None
