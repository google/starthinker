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
from datetime import datetime, timedelta
from time import sleep
from StringIO import StringIO
#from io import BytesIO

from google.cloud import bigquery
from googleapiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload

from setup import BUFFER_SCALE
from util import flag_last
from util.project import project
from util.auth import get_service
from util.google_api import API_BigQuery

BIGQUERY_RETRIES = 3
BIGQUERY_CHUNKSIZE = int(200 * 1024000 * BUFFER_SCALE) # 200 MB * scale in setup.py
BIGQUERY_BUFFERSIZE = BIGQUERY_CHUNKSIZE * 5 # 1 GB * scale in setup.py
RE_SCHEMA = re.compile('[^0-9a-zA-Z]+')

reload(sys)
sys.setdefaultencoding('utf-8')


# DEPRECATED, USE THE FOLLOWING:
# WHY: The other header sanitizes are compatible with DT + DCM fields and defining schema in JSON is safer and more maintainable.
# 1. Provide Schema in JSON instead of defaulting to string.
# 2. To detect schema use: from util.bigquery import get_schema(rows, header=True, infer_type=True)
# 3. To sanitize field names use: from util.csv import row_header_sanitize(field_list)
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
      if json.loads(e.content)['error']['code'] == 409:
        return # already exists ( ignore )
      elif retries > 0:
        sleep(wait)
        if project.verbose: print 'BIGQUERY RETRY', retries
        return _retry(job, retries - 1, wait * 2)
      else:
        raise
    else:
      raise


def job_wait(service, job):
  if project.verbose: print 'BIGQUERY JOB WAIT:', job['jobReference']['jobId']

  request = service.jobs().get(
    projectId=job['jobReference']['projectId'],
    jobId=job['jobReference']['jobId']
  )

  while True:
    sleep(5)
    if project.verbose: print '.',
    sys.stdout.flush()
    result = _retry(request)
    if 'errorResult' in result['status']: 
      errors = ' '.join([e['message'] for e in result['status']['errors']])
      raise Exception('BigQuery Job Error: %s' % errors)
    elif result['status']['state'] == 'DONE':
      if project.verbose: print 'JOB COMPLETE:', result['id']
      break


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


def query_to_table(auth, project_id, dataset_id, table_id, query, disposition='WRITE_TRUNCATE', legacy=True, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  service = get_service('bigquery', 'v2', auth)

  body={
    'configuration': {
      'query': {
        'useLegacySql': legacy,
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
  job = service.jobs().insert(projectId=billing_project_id, body=body).execute(num_retries=BIGQUERY_RETRIES)
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
  if project.verbose: print 'BIGQUERY STORAGE TO TABLE: ', project_id, dataset_id, table_id

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
        'allowJaggedRows': True,
        'allowQuotedNewlines':True,
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


#def csv_to_table(auth, project_id, dataset_id, table_id, data, schema=[], skip_rows=1, disposition='WRITE_TRUNCATE'):
#  if project.verbose: print 'BIGQUERY CSV TO TABLE: ', project_id, dataset_id, table_id
#
#  service = get_service('bigquery', 'v2', auth)
#
#  def getSize(fileObject):
#    fileObject.seek(0,2)
#    retVal = fileObject.tell()
#    return retVal
#
#  if(getSize(data) > 0):
#    media = MediaIoBaseUpload(data, mimetype='application/octet-stream', resumable=True, chunksize=BIGQUERY_CHUNKSIZE)
#
#    body = {
#      'configuration': {
#        'load': {
#          'destinationTable': {
#            'projectId': project_id,
#            'datasetId': dataset_id,
#            'tableId': table_id,
#          },
#          'sourceFormat': 'CSV',
#          'skipLeadingRows': skip_rows,
#          'writeDisposition': disposition,
#          'autodetect': True,
#          'allowJaggedRows': True,
#          'allowQuotedNewlines':True,
#          'ignoreUnknownValues': True,
#        }
#      }
#    }
#
#    if schema:
#      body['configuration']['load']['schema'] = { 'fields':schema }
#      body['configuration']['load']['autodetect'] = False
#
#    job = service.jobs().insert(projectId=project.id, body=body, media_body=media)
#    response = None
#    while response is None:
#      status, response = job.next_chunk()
#      if project.verbose and status: print "Uploaded %d%%." % int(status.progress() * 100)
#    if project.verbose: print "Uploaded 100%."
#    job_wait(service, job.execute(num_retries=BIGQUERY_RETRIES))
#
#  else:
#    try:
#      service.tables().delete(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute(num_retries=BIGQUERY_RETRIES)
#      print 'APR table exists. deleting current table...'
#    except:
#      print 'APR table does not exist. creating empty table...'
#    body = {
#      "tableReference": {
#        "projectId": project_id,
#        "datasetId": dataset_id,
#        "tableId": table_id
#      },
#      "schema": {
#        "fields": schema
#      }
#    }
#    # change project_id to be project.id, better yet project.cloud_id from JSON
#    service.tables().insert(projectId=project.id, datasetId=dataset_id, body=body).execute(num_retries=BIGQUERY_RETRIES)


def rows_to_table(auth, project_id, dataset_id, table_id, rows, schema=[], skip_rows=1, disposition='WRITE_TRUNCATE'):
  if project.verbose: print 'BIGQUERY ROWS TO TABLE: ', project_id, dataset_id, table_id

  buffer_data = StringIO()
  writer = csv.writer(buffer_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  has_rows = False

  for is_last, row in flag_last(rows):

    # write row to csv buffer
    writer.writerow(row)

    # write the buffer in chunks
    if is_last or buffer_data.tell() + 1 > BIGQUERY_BUFFERSIZE:
      if project.verbose: print 'BigQuery Buffer Size', buffer_data.tell()
      buffer_data.seek(0) # reset for read
      io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'CSV', schema, skip_rows, disposition)

      # reset buffer for next loop, be sure to do an append to the table
      buffer_data.seek(0) #reset for write
      buffer_data.truncate() # reset for write ( yes its needed for EOF marker )
      disposition = 'WRITE_APPEND' # append all remaining records
      skip_rows = 0
      has_rows = True

  # if no rows, clear table to simulate empty write
  if not has_rows:
    if project.verbose: print 'BigQuery Zero Rows'
    io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'CSV', schema, skip_rows, disposition)


def json_to_table(auth, project_id, dataset_id, table_id, json_data, schema=None, disposition='WRITE_TRUNCATE'):
  if project.verbose: print 'BIGQUERY JSON TO TABLE: ', project_id, dataset_id, table_id

  buffer_data = StringIO()
  has_rows = False

  for is_last, record in flag_last(json_data):

    # check if json is already string encoded, and write to buffer
    buffer_data.write(record if isinstance(record, basestring) else json.dumps(record))

    # write the buffer in chunks
    if is_last or buffer_data.tell() + 1 > BIGQUERY_BUFFERSIZE:
      if project.verbose: print 'BigQuery Buffer Size', buffer_data.tell()
      buffer_data.seek(0) # reset for read
      io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'NEWLINE_DELIMITED_JSON', schema, 0, disposition)

      # reset buffer for next loop, be sure to do an append to the table
      buffer_data.seek(0) #reset for write
      buffer_data.truncate() # reset for write ( yes its needed for EOF marker )
      disposition = 'WRITE_APPEND' # append all remaining records
      has_rows = True

    # if not end append newline, for newline delimited json
    else:
      buffer_data.write('\n')

  # if no rows, clear table to simulate empty write
  if not has_rows:
    if project.verbose: print 'BigQuery Zero Rows'
    io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'NEWLINE_DELIMITED_JSON', schema, skip_rows, disposition)


# NEWLINE_DELIMITED_JSON, CSV
def io_to_table(auth, project_id, dataset_id, table_id, data, source_format='CSV', schema=None, skip_rows=0, disposition='WRITE_TRUNCATE'):
  service = get_service('bigquery', 'v2', auth)

  # if data exists, write data to table
  data.seek(0, 2)
  if data.tell() > 0:
    data.seek(0)

    media = MediaIoBaseUpload(
      data,
      mimetype='application/octet-stream',
      resumable=True,
      chunksize=BIGQUERY_CHUNKSIZE
    )

    body = {
      'configuration': {
        'load': {
          'destinationTable': {
            'projectId': project_id,
            'datasetId': dataset_id,
            'tableId': table_id,
          },
          'sourceFormat': source_format,
          'writeDisposition': disposition,
          'autodetect': True,
          'allowJaggedRows': True,
          'allowQuotedNewlines':True,
          'ignoreUnknownValues': True,
        }
      }
    }
 
    if schema:
      body['configuration']['load']['schema'] = { 'fields':schema }
      body['configuration']['load']['autodetect'] = False

    if source_format == 'CSV':
      body['configuration']['load']['skipLeadingRows'] = skip_rows

    job = API_BigQuery(auth).jobs().insert(projectId=project.id, body=body, media_body=media).execute(run=False)

    response = None
    while response is None:
      status, response = job.next_chunk()
      if project.verbose and status: print "Uploaded %d%%." % int(status.progress() * 100)
    if project.verbose: print "Upload End"
    job_wait(service, job.execute(num_retries=BIGQUERY_RETRIES))

  # if it does not exist and write, clear the table
  elif disposition == 'WRITE_TRUNCATE':
    if project.verbose: print "BIGQUERY: No data, clearing table."

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
    # change project_id to be project.id, better yet project.cloud_id from JSON
    service.tables().insert(projectId=project.id, datasetId=dataset_id, body=body).execute(num_retries=BIGQUERY_RETRIES)


def incremental_rows_to_table(auth, project_id, dataset_id, table_id, rows, schema=[], skip_rows=1, disposition='WRITE_APPEND', billing_project_id=None):
  if project.verbose: print 'BIGQUERY INCREMENTAL ROWS TO TABLE: ', project_id, dataset_id, table_id

  #load the data in rows to BQ into a temp table
  table_id_temp = table_id + str(uuid.uuid4()).replace('-','_')
  rows_to_table(auth, project_id, dataset_id, table_id_temp, rows, schema, skip_rows, disposition)

  #query the temp table to find the max and min date
  start_date = _get_min_date_from_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)
  end_date = _get_max_date_from_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)

  #check if master table exists: if not create it, if so clear old data
  if not check_table_exists(auth, project_id, dataset_id, table_id):
    create_table(auth, project_id, dataset_id, table_id)
  else:
    _clear_data_in_date_range_from_table(auth, project_id, dataset_id, table_id, start_date, end_date, billing_project_id=billing_project_id)

  #append temp table to master
  query = ('SELECT * FROM `' 
    + project_id + '.' + dataset_id + '.' + table_id_temp + '` ')
  query_to_table(auth, project_id, dataset_id, table_id, query, disposition, False, billing_project_id=billing_project_id)

  #delete temp table
  _drop_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)


def create_table(auth, project_id, dataset_id, table_id):
  service = get_service('bigquery', 'v2', auth)

  body = {
    "tableReference": {
      "projectId": project_id,
      "tableId": table_id,
      "datasetId": dataset_id,
    }
  }

  service.tables().insert(projectId=project_id, datasetId=dataset_id, body=body).execute()

def check_table_exists(auth, project_id, dataset_id, table_id):
  service = get_service('bigquery', 'v2', auth)

  table_list = service.tables().list(projectId=project_id, datasetId=dataset_id).execute()

  while table_list and table_list['tables']:
    for table in table_list['tables']:
      if table_id == table['tableReference']['tableId']:
        return True

    table_list = service.tables().list(projectId=project_id, datasetId=dataset_id, pageToken=table_list['nextPageToken']).execute()


  return False


def tables_get(auth, project_id, name):
  dataset_id, table_id = name.split(':', 1)
  service = get_service('bigquery', 'v2', auth)
  return service.tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()


def tables_get(auth, project_id, dataset_id, table_id):
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


# https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
def query_to_rows(auth, project_id, dataset_id, query, row_max=None, legacy=True):
  service = get_service('bigquery', 'v2', auth)

  # Create the query 
  body = {
    "kind": "bigquery#queryRequest",
    "query": query,
    "timeoutMs": 10000,
    "dryRun": False,
    "useQueryCache": True,
    "useLegacySql": legacy
  }

  if row_max: body['maxResults'] = row_max

  if dataset_id:
    body['defaultDataset'] = {
      "projectId": project_id,
      "datasetId": dataset_id
    }

  response = _retry(service.jobs().query(projectId=project_id, body=body))

  while not response['jobComplete']:
    sleep(5)
    response = _retry(service.jobs().getQueryResults(projectId=project_id, jobId=response['jobReference']['jobId']))

  # Fetch all results
  row_count = 0
  while 'rows' in response:
    converters = _build_converter_array(response.get('schema', None), None, len(response['rows'][0].get('f')))
    for row in response['rows']:
      yield [converters[i](r.values()[0]) for i, r in enumerate(row['f'])] # may break if we attempt nested reads
      row_count += 1

    if 'PageToken' in response:
      response = _retry(service.jobs().getQueryResults(projectId=project_id, jobId=response['jobReference']['jobId'], pageToken=response['PageToken']))
    elif row_count < response['totalRows']: 
      response = _retry(service.jobs().getQueryResults(projectId=project_id, jobId=response['jobReference']['jobId'], startIndex=row_count))


#def list_jobs(auth, project_id):
#  service = get_service('bigquery', 'v2', auth)
#  client = get_client('bigquery')
#  #return service.jobs().list(projectId=project_id).execute()
#  return client.list_jobs()


def get_job(auth, project_id, job_id):
  service = get_service('bigquery', 'v2', auth)
  return service.jobs().get(projectId=project_id, jobId=job_id).execute()


#def get_table(auth, dataset, table_name):
#  client = get_client('bigquery', auth=auth)
#
#  dataset = client.dataset(dataset)
#  table = dataset.table(table_name)
#
#  return table


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


def _drop_table(auth, project_id, dataset_id, table_id, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  service = get_service('bigquery', 'v2', auth)
  query = ('DROP TABLE `' 
    + project_id + '.' + dataset_id + '.' + table_id + '` ')

  body = {
    "kind": "bigquery#queryRequest",
    'query': query,
    'defaultDataset': {
      'datasetId' : dataset_id,
    },
    'useLegacySql': False,
  }

  job = API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute(run=False)
  
  max_date = job_wait(service, job.execute(num_retries=BIGQUERY_RETRIES))


def _get_max_date_from_table(auth, project_id, dataset_id, table_id, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  service = get_service('bigquery', 'v2', auth)
  query = ('SELECT MAX(Date) FROM `' 
    + project_id + '.' + dataset_id + '.' + table_id + '` ')

  body = {
    "kind": "bigquery#queryRequest",
    'query': query,
    'defaultDataset': {
      'datasetId' : dataset_id,
    },
    'useLegacySql': False,
  }

  job = API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute()
  
  return job['rows'][0]['f'][0]['v']


def _get_min_date_from_table(auth, project_id, dataset_id, table_id, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  service = get_service('bigquery', 'v2', auth)
  query = ('SELECT MIN(Date) FROM `' 
    + project_id + '.' + dataset_id + '.' + table_id + '` ')

  body = {
    "kind": "bigquery#queryRequest",
    'query': query,
    'defaultDataset': {
      'datasetId' : dataset_id,
    },
    'useLegacySql': False,
  }

  job = API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute()
  
  return job['rows'][0]['f'][0]['v']

#start and end date must be in format YYYY-MM-DD
def _clear_data_in_date_range_from_table(auth, project_id, dataset_id, table_id, start_date, end_date, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  service = get_service('bigquery', 'v2', auth)

  query = ('DELETE FROM `' 
    + project_id + '.' + dataset_id + '.' + table_id + '` '
    + 'WHERE Date >= "' + start_date + '"' + 'AND Date <= "' + end_date + '"'
    )

  body = {
    "kind": "bigquery#queryRequest",
    'query': query,
    'defaultDataset': {
      'datasetId' : dataset_id,
    },
    'useLegacySql': False,
  }

  job = API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute(run=False)
  job_wait(service, job.execute(num_retries=BIGQUERY_RETRIES))

