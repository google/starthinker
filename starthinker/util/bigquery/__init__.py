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

# https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#resource
# https://cloud.google.com/bigquery/docs/reference/v2/jobs#resource
# https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list

import re
import sys
import codecs
import csv
import pprint
import uuid
import json
from time import sleep
from io import BytesIO
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from starthinker.config import BUFFER_SCALE
from starthinker.util import flag_last
from starthinker.util.project import project
from starthinker.util.google_api import API_BigQuery, API_Retry
from starthinker.util.csv import row_header_sanitize


BIGQUERY_BUFFERMAX = 4294967296
BIGQUERY_CHUNKSIZE = int(200 * 1024000 * BUFFER_SCALE) # 200 MB * scale in config.py
BIGQUERY_BUFFERSIZE = min(BIGQUERY_CHUNKSIZE * 4, BIGQUERY_BUFFERMAX) # 1 GB * scale in config.py

RE_TABLE_NAME = re.compile(r'[^\w]+')
RE_INDENT = re.compile(r' {5,}')

def bigquery_date(value):
  return value.strftime('%Y%m%d')


def table_name_sanitize(name):
  return RE_TABLE_NAME.sub('_', name)


def query_parameters(query, parameters):
  '''
  Replace variables in a query string with values.
  CAUTION: Possible SQL injection, please check up stream.

  query = "SELECT * FROM {project}.{dataset}.Some_Table"
  parameters = {'project': 'Test_Project', 'dataset':'Test_dataset'}
  print query_parameters(query, parameters)
  '''

  # no effect other than visual formatting
  query = RE_INDENT.sub(r'\n\g<0>', query)

  if not parameters:
    return query
  elif isinstance(parameters, dict):
    print('BQ PARAM')
    return query.format(**parameters)
  else:
    while '[PARAMETER]' in query:
      try:
        parameter = parameters.pop(0)
      except IndexError:
        raise IndexError('BigQuery: Missing PARAMETER values for this query.')
      if isinstance(parameter, list) or isinstance(parameter, tuple): parameter = ', '.join([str(p) for p in parameter])
      query = query.replace('[PARAMETER]', parameter, 1)
    if project.verbose: print('QUERY:', query)
    return query


def job_wait(auth, job):
  if job:
    if project.verbose: print('BIGQUERY JOB WAIT:', job['jobReference']['jobId'])

    request = API_BigQuery(auth).jobs().get(
      projectId=job['jobReference']['projectId'],
      jobId=job['jobReference']['jobId']
    )

    while True:
      sleep(5)
      if project.verbose: print('.', end='')
      sys.stdout.flush()
      result = API_Retry(request)
      if 'errors' in result['status']:
        raise Exception('BigQuery Job Error: %s' % ' '.join([e['message'] for e in result['status']['errors']]))
      elif 'errorResult' in result['status']:
        raise Exception('BigQuery Job Error: %s' % result['status']['errorResult']['message'])
      elif result['status']['state'] == 'DONE':
        if project.verbose: print('JOB COMPLETE:', result['id'])
        break


def datasets_create(auth, project_id, dataset_id):

  body = {
    "description": dataset_id,
    "datasetReference": {
      "projectId": project_id,
      "datasetId": dataset_id,
    },
    "location": "US",
    "friendlyName": dataset_id,
  }

  API_BigQuery(auth).datasets().insert(projectId=project_id, body=body).execute()


# roles = READER, WRITER, OWNER
def datasets_access(auth, project_id, dataset_id, role='READER', emails=[], groups=[], views=[]):

  if emails or groups or views:
    access = API_BigQuery(auth).datasets().get(projectId=project_id, datasetId=dataset_id).execute()["access"]

    # if emails
    for email in emails:
      access.append({
        "userByEmail": email,
        "role": role,
      })

    # if groups
    for group in groups:
      access.append({
        "groupByEmail": group,
        "role": role,
      })

    for view in views:
      access.append({
        "view": {
          "projectId": project_id,
          "datasetId": view['dataset'],
          "tableId": view['view']
        }
      })

    API_BigQuery(auth).datasets().patch(projectId=project_id, datasetId=dataset_id, body={'access': access}).execute()

def run_query(auth, project_id, query, legacy=True):

  body={
    'configuration': {
      'query': {
        'useLegacySql': legacy,
        'query': query
      }
    }
  }

  job_wait(auth, API_BigQuery(auth).jobs().insert(projectId=project_id, body=body).execute())


def query_to_table(auth, project_id, dataset_id, table_id, query, disposition='WRITE_TRUNCATE', legacy=True, billing_project_id=None, target_project_id=None):
  target_project_id = target_project_id or project_id

  if not billing_project_id:
    billing_project_id = project_id

  body={
    'configuration': {
      'query': {
        'useLegacySql': legacy,
        'query': query,
        'destinationTable': {
          'projectId': target_project_id,
          'datasetId': dataset_id,
          'tableId': table_id
        },
        'createDisposition': 'CREATE_IF_NEEDED',
        'writeDisposition': disposition,
        'allowLargeResults': True
      },
    }
  }

  job_wait(auth, API_BigQuery(auth).jobs().insert(projectId=billing_project_id, body=body).execute())


def query_to_view(auth, project_id, dataset_id, view_id, query, legacy=True, replace=False):

  body={
    'tableReference': {
      'projectId': project_id,
      'datasetId': dataset_id,
      'tableId': view_id,
    },
    'view': {
      'query': query,
      'useLegacySql': legacy
    }
  }

  response = API_BigQuery(auth).tables().insert(projectId=project_id, datasetId=dataset_id, body=body).execute()
  if response is None and replace:
    return API_BigQuery(auth).tables().update(projectId=project_id,datasetId=dataset_id, tableId=view_id, body=body).execute()



#struture = CSV, NEWLINE_DELIMITED_JSON
#disposition = WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
def storage_to_table(auth, project_id, dataset_id, table_id, path, schema=[], skip_rows=1, structure='CSV', disposition='WRITE_TRUNCATE', wait=True):
  if project.verbose: print('BIGQUERY STORAGE TO TABLE: ', project_id, dataset_id, table_id)

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
        'allowQuotedNewlines': True,
        'ignoreUnknownValues': True,
        'sourceUris': [
          'gs://%s' % path.replace(':', '/'),
        ],
      }
    }
  }

  if schema:
    body['configuration']['load']['schema'] = { 'fields': schema }
    body['configuration']['load']['autodetect'] = False

  if structure == 'CSV':
    body['configuration']['load']['sourceFormat'] = 'CSV'
    body['configuration']['load']['skipLeadingRows'] = skip_rows

  job = API_BigQuery(auth).jobs().insert(projectId=project_id, body=body).execute()
  if wait:
    try: job_wait(auth, job)
    except Exception as e: print('BIGQUERY SKIPPING: %s, %s' % (path, str(e)))
  else:
    return job


def rows_to_table(auth, project_id, dataset_id, table_id, rows, schema=[], skip_rows=1, disposition='WRITE_TRUNCATE', wait=True):
  if project.verbose: print('BIGQUERY ROWS TO TABLE: ', project_id, dataset_id, table_id)

  buffer_data = BytesIO()
  buffer_writer = codecs.getwriter('utf-8')
  writer = csv.writer(buffer_writer(buffer_data), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  has_rows = False

  if rows == []:
    if project.verbose: print('BigQuery Zero Rows')
    return io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'CSV', schema, skip_rows, disposition, wait)

  for is_last, row in flag_last(rows):

    # write row to csv buffer
    writer.writerow(row)

    # write the buffer in chunks
    if is_last or buffer_data.tell() + 1 > BIGQUERY_BUFFERSIZE:
      if project.verbose: print('BigQuery Buffer Size', buffer_data.tell())
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
    if project.verbose: print('BigQuery Zero Rows')
    return io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'CSV', schema, skip_rows, disposition, wait)


def json_to_table(auth, project_id, dataset_id, table_id, json_data, schema=None, disposition='WRITE_TRUNCATE', wait=True):
  if project.verbose: print('BIGQUERY JSON TO TABLE: ', project_id, dataset_id, table_id)

  buffer_data = BytesIO()
  has_rows = False

  for is_last, record in flag_last(json_data):

    # check if json is already string encoded, and write to buffer
    buffer_data.write((record if isinstance(record, str) else json.dumps(record)).encode('utf-8'))

    # write the buffer in chunks
    if is_last or buffer_data.tell() + 1 > BIGQUERY_BUFFERSIZE:
      if project.verbose: print('BigQuery Buffer Size', buffer_data.tell())
      buffer_data.seek(0) # reset for read
      io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'NEWLINE_DELIMITED_JSON', schema, 0, disposition)

      # reset buffer for next loop, be sure to do an append to the table
      buffer_data.seek(0) #reset for write
      buffer_data.truncate() # reset for write ( yes its needed for EOF marker )
      disposition = 'WRITE_APPEND' # append all remaining records
      has_rows = True

    # if not end append newline, for newline delimited json
    else:
      buffer_data.write('\n'.encode('utf-8'))

  # if no rows, clear table to simulate empty write
  if not has_rows:
    if project.verbose: print('BigQuery Zero Rows')
    return io_to_table(auth, project_id, dataset_id, table_id, buffer_data, 'NEWLINE_DELIMITED_JSON', schema, skip_rows, disposition, wait)


# NEWLINE_DELIMITED_JSON, CSV
def io_to_table(auth, project_id, dataset_id, table_id, data_bytes, source_format='CSV', schema=None, skip_rows=0, disposition='WRITE_TRUNCATE', wait=True):

  # if data exists, write data to table
  data_bytes.seek(0, 2)
  if data_bytes.tell() > 0:
    data_bytes.seek(0)

    media = MediaIoBaseUpload(
      data_bytes,
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
          'allowQuotedNewlines': True,
          'ignoreUnknownValues': True,
        }
      }
    }

    if schema:
      body['configuration']['load']['schema'] = { 'fields': schema }
      body['configuration']['load']['autodetect'] = False

    if disposition == 'WRITE_APPEND':
      body['configuration']['load']['autodetect'] = False

    if source_format == 'CSV':
      body['configuration']['load']['skipLeadingRows'] = skip_rows

    job = API_BigQuery(auth).jobs().insert(projectId=project.id, body=body, media_body=media).execute(run=False)
    execution = job.execute()

    response = None
    while response is None:
      status, response = job.next_chunk()
      if project.verbose and status: print("Uploaded %d%%." % int(status.progress() * 100))
    if project.verbose: print("Uploaded 100%")
    if wait: job_wait(auth, job.execute())
    else: return job

  # if it does not exist and write, clear the table
  elif disposition == 'WRITE_TRUNCATE':
    if project.verbose: print("BIGQUERY: No data, clearing table.")

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
    API_BigQuery(auth).tables().insert(projectId=project.id, datasetId=dataset_id, body=body).execute()


def incremental_rows_to_table(auth, project_id, dataset_id, table_id, rows, schema=[], skip_rows=1, disposition='WRITE_APPEND', billing_project_id=None):
  if project.verbose: print('BIGQUERY INCREMENTAL ROWS TO TABLE: ', project_id, dataset_id, table_id)

  #load the data in rows to BQ into a temp table
  table_id_temp = table_id + str(uuid.uuid4()).replace('-','_')
  rows_to_table(auth, project_id, dataset_id, table_id_temp, rows, schema, skip_rows, disposition)

  try:
    #query the temp table to find the max and min date
    start_date = _get_min_date_from_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)
    end_date = _get_max_date_from_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)

    #check if master table exists: if not create it, if so clear old data
    if not table_exists(auth, project_id, dataset_id, table_id):
      table_create(auth, project_id, dataset_id, table_id)
    else:
      _clear_data_in_date_range_from_table(auth, project_id, dataset_id, table_id, start_date, end_date, billing_project_id=billing_project_id)

    #append temp table to master
    query = ('SELECT * FROM `'
      + project_id + '.' + dataset_id + '.' + table_id_temp + '` ')
    query_to_table(auth, project_id, dataset_id, table_id, query, disposition, False, billing_project_id=billing_project_id)

    #delete temp table
    drop_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)

  except:
    #delete temp table
    drop_table(auth, project_id, dataset_id, table_id_temp, billing_project_id=billing_project_id)


def table_create(auth, project_id, dataset_id, table_id, is_time_partition=False):

  body = {
    "tableReference": {
      "projectId": project_id,
      "tableId": table_id,
      "datasetId": dataset_id,
    }
  }

  if is_time_partition:
    body['timePartitioning'] = {
      "type": "DAY"
    }

  API_BigQuery(auth).tables().insert(projectId=project_id, datasetId=dataset_id, body=body).execute()


def table_get(auth, project_id, dataset_id, table_id):
  return API_BigQuery(auth).tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()


def table_exists(auth, project_id, dataset_id, table_id):
  try:
    table_get(auth, project_id, dataset_id, table_id)
    return True
  except HttpError as e:
    if e.resp.status != 404: raise
    return False


def table_copy(auth, from_project, from_dataset, from_table, to_project, to_dataset, to_table):

  body = {
    "copy": {
      "sourceTable": {
        "projectId": from_project,
        "datasetId": from_dataset,
        "tableId": from_table
      },
      "destinationTable": {
        "projectId": to_project,
        "datasetId": to_dataset,
        "tableId": to_table
      }
    }
  }

  job_wait(auth, API_BigQuery(auth).jobs().insert(projectId=project.id, body=body).execute())


def table_to_rows(auth, project_id, dataset_id, table_id, fields=None, row_start=0, row_max=None):
  if project.verbose: print('BIGQUERY ROWS:', project_id, dataset_id, table_id)

  schema = table_to_schema(auth, project_id, dataset_id, table_id)
  converter = None

  for row in API_BigQuery(auth, iterate=True).tabledata().list(
    projectId=project_id,
    datasetId=dataset_id,
    tableId=table_id,
    selectedFields=fields,
    startIndex=row_start,
    maxResults=row_max,
  ).execute():
    if converter is None:
      converter = _build_converter_array(schema, fields, len(row.get('f')))
    yield [converter[i](next(iter(r.values()))) for i, r in enumerate(row['f'])] # may break if we attempt nested reads


def table_to_schema(auth, project_id, dataset_id, table_id):
  if project.verbose: print('TABLE SCHEMA:', project_id, dataset_id, table_id)
  return API_BigQuery(auth).tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()['schema']


# https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
def query_to_rows(auth, project_id, dataset_id, query, row_max=None, legacy=True):

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

  # wait for query to complete

  response = API_BigQuery(auth).jobs().query(projectId=project_id, body=body).execute()
  while not response['jobComplete']:
    sleep(5)
    response = API_BigQuery(auth).jobs().getQueryResults(projectId=project_id, jobId=response['jobReference']['jobId']).execute(iterate=False)

  # fetch query results

  row_count = 0
  while 'rows' in response:
    converters = _build_converter_array(response.get('schema', None), None, len(response['rows'][0].get('f')))

    for row in response['rows']:
      yield [converters[i](next(iter(r.values()))) for i, r in enumerate(row['f'])] # may break if we attempt nested reads
      row_count += 1

    if 'PageToken' in response:
      response = API_BigQuery(auth).jobs().getQueryResults(projectId=project_id, jobId=response['jobReference']['jobId'], pageToken=response['PageToken']).execute(iterate=False)
    elif row_count < int(response['totalRows']):
      response = API_BigQuery(auth).jobs().getQueryResults(projectId=project_id, jobId=response['jobReference']['jobId'], startIndex=row_count).execute(iterate=False)
    else:
      break


def make_schema(header):
  return [{
    'name': name,
    'type': 'STRING',
    'mode': 'NULLABLE'
  } for name in row_header_sanitize(header)]


def get_schema(rows, header=True, infer_type=True):
  '''
  CAUTION: Memory suck. This function sabotages iteration by iterating thorough the new object and returning a new iterator
  RECOMMEND: Define the schema yourself, it will also ensure data integrity downstream.
  '''

  schema = []
  row_buffer = []

  # everything else defaults to STRING
  type_to_bq = {int: 'INTEGER', bool: 'BOOLEAN', float: 'FLOAT'} if infer_type else {} # empty lookup defaults to STRING below

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
      for index, value in enumerate(row_header_sanitize(row)):
        schema.append({ "name": value if header else 'Field_%d' % index, "type": "STRING" })

    # then determine type of each column
    if not first and header:
      for index, value in enumerate(row):
        # if null, set only mode
        if value is None or value == '':
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
  #print(converters)
  return converters


def drop_table(auth, project_id, dataset_id, table_id, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

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

  job_wait(auth, API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute())


def _get_max_date_from_table(auth, project_id, dataset_id, table_id, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  query = ('SELECT MAX(Report_Day) FROM `'
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

  query = ('SELECT MIN(Report_Day) FROM `'
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


def execute_statement(auth, project_id, dataset_id, statement, billing_project_id=None, use_legacy_sql=False):
  if not billing_project_id:
    billing_project_id = project_id

  body = {
    "kind": "bigquery#queryRequest",
    'query': statement,
    'defaultDataset': {
      'datasetId' : dataset_id,
    },
    'useLegacySql': use_legacy_sql,
  }

  job_wait(auth, API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute())


#start and end date must be in format YYYY-MM-DD
def _clear_data_in_date_range_from_table(auth, project_id, dataset_id, table_id, start_date, end_date, billing_project_id=None):

  if not billing_project_id:
    billing_project_id = project_id

  query = ('DELETE FROM `'
    + project_id + '.' + dataset_id + '.' + table_id + '` '
    + 'WHERE Report_Day >= "' + start_date + '"' + 'AND Report_Day <= "' + end_date + '"'
    )

  body = {
    "kind": "bigquery#queryRequest",
    'query': query,
    'defaultDataset': {
      'datasetId' : dataset_id,
    },
    'useLegacySql': False,
  }

  job_wait(auth, API_BigQuery(auth).jobs().query(projectId=billing_project_id, body=body).execute())
