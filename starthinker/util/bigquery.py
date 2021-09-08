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

import re
import sys
import codecs
import base64
import csv
import uuid
import json
import datetime
from time import sleep
from io import BytesIO
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from google.cloud.bigquery._helpers import _row_tuple_from_json

from starthinker.config import BUFFER_SCALE
from starthinker.util import flag_last
from starthinker.util.google_api import API_BigQuery, API_Retry
from starthinker.util.csv import row_header_sanitize

BIGQUERY_BUFFERMAX = 4294967296
BIGQUERY_CHUNKSIZE = int(200 * 1024000 *
                         BUFFER_SCALE)  # 200 MB * scale in config.py
BIGQUERY_BUFFERSIZE = min(BIGQUERY_CHUNKSIZE * 4,
                          BIGQUERY_BUFFERMAX)  # 1 GB * scale in config.py

RE_TABLE_NAME = re.compile(r'[^\w]+')
RE_INDENT = re.compile(r' {5,}')

BIGQUERY_DATE_FORMAT = "%Y-%m-%d"
BIGQUERY_TIME_FORMAT = "%H:%M:%S"


class JSON_To_BigQuery(json.JSONEncoder):
  """Translate complex Python objects into BigQuery formats where json does not have defaults.

  Usage: json.dumps(..., cls=JSON_To_BigQuery)

  Currently translates:
    bytes -> base64
    detetime - > str
    dete - > str
    time - > str

  Args:
    obj -  any json dumps parameter without a default handler

  Returns:
    Always a string version of the object passed in.

  """

  def default(self, obj):
    if isinstance(obj, bytes):
      return base64.standard_b64encode(obj).decode("ascii")
    elif isinstance(obj, datetime.datetime):
      return obj.strftime("%s %s" % ( self.BIGQUERY_DATE_FORMAT, self.BIGQUERY_TIME_FORMAT))
    elif isinstance(obj, datetime.date):
      return obj.strftime(self.BIGQUERY_DATE_FORMAT)
    elif isinstance(obj, datetime.time):
      return obj.strftime(self.BIGQUERY_TIME_FORMAT)
    elif isinstance(obj, map):
      return list(obj)
    else:
      return super(JSON_To_BigQuery, self).default(obj)


def row_to_json(row, schema, as_object=False):

  if as_object:
    row_raw = {'f': [{'v': row}]}
    schema_raw = [{
        'name': 'wrapper',
        'type': 'RECORD',
        'mode': 'REQUIRED',
        'fields': schema
    }]
    return _row_tuple_from_json(row_raw, schema_raw)[0]

  else:
    row_raw = row
    schema_raw = schema
    return list(_row_tuple_from_json(row_raw, schema_raw))


def bigquery_date(value):
  return value.strftime('%Y%m%d')


def table_name_sanitize(name):
  return RE_TABLE_NAME.sub('_', name)


def query_parameters(query, parameters):
  """Replace variables in a query string with values.

  CAUTION: Possible SQL injection, please check up stream.
  query = "SELECT * FROM {project}.{dataset}.Some_Table"
  parameters = {'project': 'Test_Project', 'dataset':'Test_dataset'}
  print query_parameters(query, parameters)
  """

  # no effect other than visual formatting
  query = RE_INDENT.sub(r'\n\g<0>', query)

  if not parameters:
    return query
  elif isinstance(parameters, dict):
    return query.format(**parameters)
  else:
    while '[PARAMETER]' in query:
      try:
        parameter = parameters.pop(0)
      except IndexError:
        raise IndexError('BigQuery: Missing PARAMETER values for this query.')
      if isinstance(parameter, list) or isinstance(parameter, tuple):
        parameter = ', '.join([str(p) for p in parameter])
      query = query.replace('[PARAMETER]', parameter, 1)
    print('QUERY:', query)
    return query


def job_wait(config, auth, job):
  if job:
    if config.verbose:
      print('BIGQUERY JOB WAIT:', job['jobReference']['jobId'])

    request = API_BigQuery(config, auth).jobs().get(
        projectId=job['jobReference']['projectId'],
        jobId=job['jobReference']['jobId'])

    while True:
      sleep(5)
      if config.verbose:
        print('.', end='')
      sys.stdout.flush()
      result = API_Retry(request)
      if 'errors' in result['status']:
        raise Exception(
            'BigQuery Job Error: %s' %
            ' '.join([e['message'] for e in result['status']['errors']]))
      elif 'errorResult' in result['status']:
        raise Exception('BigQuery Job Error: %s' %
                        result['status']['errorResult']['message'])
      elif result['status']['state'] == 'DONE':
        if config.verbose:
          print('JOB COMPLETE:', result['id'])
        break


def datasets_create(config, auth, project_id, dataset_id):

  body = {
      'description': dataset_id,
      'datasetReference': {
          'projectId': project_id,
          'datasetId': dataset_id,
      },
      'location': 'US',
      'friendlyName': dataset_id,
  }

  API_BigQuery(config, auth).datasets().insert(
      projectId=project_id, body=body).execute()


def datasets_delete(config, auth, project_id, dataset_id, delete_contents=True):

  try:
    API_BigQuery(config, auth).datasets().delete(
      projectId=project_id,
      datasetId=dataset_id,
      deleteContents=delete_contents
    ).execute()
    return True
  except HttpError as e:
    if e.resp.status != 404:
      raise
    return False


# roles = READER, WRITER, OWNER
def datasets_access(config, auth,
                    project_id,
                    dataset_id,
                    role='READER',
                    emails=[],
                    groups=[],
                    views=[]):

  if emails or groups or views:
    access = API_BigQuery(config, auth).datasets().get(
        projectId=project_id, datasetId=dataset_id).execute()['access']

    # if emails
    for email in emails:
      access.append({
          'userByEmail': email,
          'role': role,
      })

    # if groups
    for group in groups:
      access.append({
          'groupByEmail': group,
          'role': role,
      })

    for view in views:
      access.append({
          'view': {
              'projectId': project_id,
              'datasetId': view['dataset'],
              'tableId': view['view']
          }
      })

    API_BigQuery(config, auth).datasets().patch(
        projectId=project_id, datasetId=dataset_id, body={
            'access': access
        }).execute()


def run_query(config, auth, project_id, query, legacy=True, dataset_id=None):

  body = {'query': query, 'useLegacySql': legacy}

  if dataset_id:
    body['defaultDataset'] = {'datasetId': dataset_id}

  job_wait(
      config, auth,
      API_BigQuery(config, auth).jobs().query(projectId=project_id,
                                      body=body).execute())


def query_to_table(config, auth,
                   project_id,
                   dataset_id,
                   table_id,
                   query,
                   disposition='WRITE_TRUNCATE',
                   legacy=True,
                   billing_project_id=None,
                   target_project_id=None):
  target_project_id = target_project_id or project_id

  if not billing_project_id:
    billing_project_id = project_id

  body = {
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

  job_wait(
      config, auth,
      API_BigQuery(config, auth).jobs().insert(projectId=billing_project_id,
                                       body=body).execute())


def query_to_view(config, auth,
                  project_id,
                  dataset_id,
                  view_id,
                  query,
                  legacy=True,
                  replace=False):

  body = {
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

  response = API_BigQuery(config, auth).tables().insert(
      projectId=project_id, datasetId=dataset_id, body=body).execute()
  if response is None and replace:
    return API_BigQuery(config, auth).tables().update(
        projectId=project_id, datasetId=dataset_id, tableId=view_id,
        body=body).execute()


def storage_to_table(config, auth,
                     project_id,
                     dataset_id,
                     table_id,
                     path,
                     schema=[],
                     skip_rows=1,
                     structure='CSV',
                     disposition='WRITE_TRUNCATE',
                     wait=True):
  if config.verbose:
    print('BIGQUERY STORAGE TO TABLE: ', project_id, dataset_id, table_id)

  body = {
      'configuration': {
          'load': {
              'destinationTable': {
                  'projectId': project_id,
                  'datasetId': dataset_id,
                  'tableId': table_id,
              },
              'sourceFormat': 'NEWLINE_DELIMITED_JSON',
              'writeDisposition':
                  disposition,  # WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
              'autodetect': True,
              'allowJaggedRows': True,
              'allowQuotedNewlines': True,
              'ignoreUnknownValues': True,
              'sourceUris': ['gs://%s' % path.replace(':', '/'),],
          }
      }
  }

  if schema:
    body['configuration']['load']['schema'] = {'fields': schema}
    body['configuration']['load']['autodetect'] = False

  if structure == 'CSV':  # CSV, NEWLINE_DELIMITED_JSON
    body['configuration']['load']['sourceFormat'] = 'CSV'
    body['configuration']['load']['skipLeadingRows'] = skip_rows

  job = API_BigQuery(config, auth).jobs().insert(
      projectId=project_id, body=body).execute()
  if wait:
    try:
      job_wait(config, auth, job)
    except Exception as e:
      print('BIGQUERY SKIPPING: %s, %s' % (path, str(e)))
  else:
    return job


def rows_to_table(config, auth,
                  project_id,
                  dataset_id,
                  table_id,
                  rows,
                  schema=[],
                  skip_rows=1,
                  disposition='WRITE_TRUNCATE',
                  wait=True):
  if config.verbose:
    print('BIGQUERY ROWS TO TABLE: ', project_id, dataset_id, table_id)

  buffer_data = BytesIO()
  buffer_writer = codecs.getwriter('utf-8')
  writer = csv.writer(
      buffer_writer(buffer_data),
      delimiter=',',
      quotechar='"',
      quoting=csv.QUOTE_MINIMAL)
  has_rows = False

  for is_last, row in flag_last(rows):

    # write row to csv buffer
    writer.writerow(row)

    # write the buffer in chunks
    if is_last or buffer_data.tell() + 1 > BIGQUERY_BUFFERSIZE:
      if config.verbose:
        print('BigQuery Buffer Size', buffer_data.tell())
      buffer_data.seek(0)  # reset for read
      io_to_table(config, auth, project_id, dataset_id, table_id, buffer_data, 'CSV',
                  schema, skip_rows, disposition)

      # reset buffer for next loop, be sure to do an append to the table
      buffer_data.seek(0)  #reset for write
      buffer_data.truncate(
      )  # reset for write ( yes its needed for EOF marker )
      disposition = 'WRITE_APPEND'  # append all remaining records
      skip_rows = 0
      has_rows = True

  # if no rows, clear table to simulate empty write
  if not has_rows:
    return io_to_table(config, auth, project_id, dataset_id, table_id, buffer_data,
                       'CSV', schema, skip_rows, disposition, wait)


def json_to_table(config, auth,
                  project_id,
                  dataset_id,
                  table_id,
                  json_data,
                  schema=None,
                  disposition='WRITE_TRUNCATE',
                  wait=True):
  if config.verbose:
    print('BIGQUERY JSON TO TABLE: ', project_id, dataset_id, table_id)

  buffer_data = BytesIO()
  has_rows = False

  for is_last, record in flag_last(json_data):

    # check if json is already string encoded, and write to buffer
    buffer_data.write(
      (record if isinstance(record, str) else json.dumps(record, cls=JSON_To_BigQuery)
    ).encode('utf-8'))

    # write the buffer in chunks
    if is_last or buffer_data.tell() + 1 > BIGQUERY_BUFFERSIZE:
      if config.verbose:
        print('BigQuery Buffer Size', buffer_data.tell())
      buffer_data.seek(0)  # reset for read

      io_to_table(config, auth, project_id, dataset_id, table_id, buffer_data,
                  'NEWLINE_DELIMITED_JSON', schema, 0, disposition)

      # reset buffer for next loop, be sure to do an append to the table
      buffer_data.seek(0)  #reset for write
      buffer_data.truncate(
      )  # reset for write ( yes its needed for EOF marker )
      disposition = 'WRITE_APPEND'  # append all remaining records
      has_rows = True

    # if not end append newline, for newline delimited json
    else:
      buffer_data.write('\n'.encode('utf-8'))

  # if no rows, clear table to simulate empty write
  if not has_rows:
    return io_to_table(config, auth, project_id, dataset_id, table_id, buffer_data,
                       'NEWLINE_DELIMITED_JSON', schema, 0, disposition, wait)


def io_to_table(config, auth,
                project_id,
                dataset_id,
                table_id,
                data_bytes,
                source_format='CSV',
                schema=None,
                skip_rows=0,
                disposition='WRITE_TRUNCATE',
                wait=True):

  # if data exists, write data to table
  data_bytes.seek(0, 2)
  if data_bytes.tell() > 0:
    data_bytes.seek(0)

    media = MediaIoBaseUpload(
        data_bytes,
        mimetype='application/octet-stream',
        resumable=True,
        chunksize=BIGQUERY_CHUNKSIZE)

    body = {
        'configuration': {
            'load': {
                'destinationTable': {
                    'projectId': project_id,
                    'datasetId': dataset_id,
                    'tableId': table_id,
                },
                'sourceFormat': source_format,  # CSV, NEWLINE_DELIMITED_JSON
                'writeDisposition':
                    disposition,  # WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
                'autodetect': True,
                'allowJaggedRows': True,
                'allowQuotedNewlines': True,
                'ignoreUnknownValues': True,
            }
        }
    }

    if schema:
      body['configuration']['load']['schema'] = {'fields': schema}
      body['configuration']['load']['autodetect'] = False

    if disposition == 'WRITE_APPEND':
      body['configuration']['load']['autodetect'] = False

    if source_format == 'CSV':
      body['configuration']['load']['skipLeadingRows'] = skip_rows

    job = API_BigQuery(config, auth).jobs().insert(
        projectId=config.project, body=body, media_body=media).execute(run=False)
    execution = job.execute()

    response = None
    while response is None:
      status, response = job.next_chunk()
      if config.verbose and status:
        print('Uploaded %d%%.' % int(status.progress() * 100))
    if config.verbose:
      print('Uploaded 100%')

    if wait:
      job_wait(config, auth, execution)
    else:
      return execution

  # if it does not exist and write, clear the table
  elif disposition == 'WRITE_TRUNCATE':
    if config.verbose:
      print('BIGQUERY: No data, clearing table.')
    table_create(config, auth, project_id, dataset_id, table_id, schema)


def incremental_rows_to_table(config, auth,
                              project_id,
                              dataset_id,
                              table_id,
                              rows,
                              schema=[],
                              skip_rows=1,
                              disposition='WRITE_APPEND',
                              billing_project_id=None):
  if config.verbose:
    print('BIGQUERY INCREMENTAL ROWS TO TABLE: ', project_id, dataset_id,
          table_id)

  #load the data in rows to BQ into a temp table
  table_id_temp = table_id + str(uuid.uuid4()).replace('-', '_')
  rows_to_table(config, auth, project_id, dataset_id, table_id_temp, rows, schema,
                skip_rows, disposition)

  try:
    #query the temp table to find the max and min date
    start_date = _get_min_date_from_table(
        config, auth,
        project_id,
        dataset_id,
        table_id_temp,
        billing_project_id=billing_project_id)
    end_date = _get_max_date_from_table(
        config, auth,
        project_id,
        dataset_id,
        table_id_temp,
        billing_project_id=billing_project_id)

    #check if master table exists: if not create it, if so clear old data
    if not table_exists(config, auth, project_id, dataset_id, table_id):
      table_create(config, auth, project_id, dataset_id, table_id)
    else:
      _clear_data_in_date_range_from_table(
          config, auth,
          project_id,
          dataset_id,
          table_id,
          start_date,
          end_date,
          billing_project_id=billing_project_id)

    #append temp table to master
    query = ('SELECT * FROM `' + project_id + '.' + dataset_id + '.' +
             table_id_temp + '` ')
    query_to_table(
        config, auth,
        project_id,
        dataset_id,
        table_id,
        query,
        disposition,
        False,
        billing_project_id=billing_project_id)

    #delete temp table
    drop_table(
        config, auth,
        project_id,
        dataset_id,
        table_id_temp,
        billing_project_id=billing_project_id)

  except:
    #delete temp table
    drop_table(
        config, auth,
        project_id,
        dataset_id,
        table_id_temp,
        billing_project_id=billing_project_id)


def table_create(config, auth,
                 project_id,
                 dataset_id,
                 table_id,
                 schema=None,
                 overwrite=True,
                 is_time_partition=False):

  if overwrite:
    table_delete(config, auth, project_id, dataset_id, table_id)

  body = {
      'tableReference': {
          'projectId': project_id,
          'tableId': table_id,
          'datasetId': dataset_id,
      }
  }

  if schema:
    body['schema'] = {'fields': schema}

  if is_time_partition:
    body['timePartitioning'] = {'type': 'DAY'}

  API_BigQuery(config, auth).tables().insert(
      projectId=project_id, datasetId=dataset_id, body=body).execute()


def table_get(config, auth, project_id, dataset_id, table_id):
  return API_BigQuery(config, auth).tables().get(
      projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()


def table_list(config, auth, project_id, dataset_id=None):
  if dataset_id is None:
    datasets = [
      d['datasetReference']['datasetId'] for d in API_BigQuery(config, auth, iterate=True).datasets().list(
        projectId=project_id,
        fields='datasets.datasetReference.datasetId, nextPageToken'
      ).execute()
    ]
  else:
    datasets = [dataset_id]

  for dataset_id in datasets:
    for table in API_BigQuery(config, auth, iterate=True).tables().list(
        projectId=project_id,
        datasetId=dataset_id,
        fields='tables.tableReference, tables.type, nextPageToken'
    ).execute():
      yield table['tableReference']['datasetId'], table['tableReference']['tableId'], table['type']


def table_exists(config, auth, project_id, dataset_id, table_id):
  try:
    table_get(config, auth, project_id, dataset_id, table_id)
    return True
  except HttpError as e:
    if e.resp.status != 404:
      raise
    return False


def table_delete(config, auth, project_id, dataset_id, table_id):
  try:
    API_BigQuery(config, auth).tables().delete(
        projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()
    return True
  except HttpError as e:
    if e.resp.status != 404:
      raise
    return False



def table_copy(config, auth, from_project, from_dataset, from_table, to_project,
               to_dataset, to_table):

  body = {
      'copy': {
          'sourceTable': {
              'projectId': from_project,
              'datasetId': from_dataset,
              'tableId': from_table
          },
          'destinationTable': {
              'projectId': to_project,
              'datasetId': to_dataset,
              'tableId': to_table
          }
      }
  }

  job_wait(
      config, auth,
      API_BigQuery(config, auth).jobs().insert(projectId=config.project,
                                       body=body).execute())


def table_to_rows(config, auth,
                  project_id,
                  dataset_id,
                  table_id,
                  fields=None,
                  row_start=0,
                  row_max=None,
                  as_object=False):
  if config.verbose:
    print('BIGQUERY ROWS:', project_id, dataset_id, table_id)

  table = API_BigQuery(config, auth).tables().get(
      projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()
  table_schema = table['schema'].get('fields', [])
  table_type = table['type']
  table_legacy = table.get('view', {}).get('useLegacySql', False)

  if table_type == 'TABLE':

    for row in API_BigQuery(
        config, auth, iterate=True).tabledata().list(
            projectId=project_id,
            datasetId=dataset_id,
            tableId=table_id,
            selectedFields=fields,
            startIndex=row_start,
            maxResults=row_max,
        ).execute():
      yield row_to_json(row, table_schema, as_object)

  else:
    yield from query_to_rows(config, auth, project_id, dataset_id,
                             'SELECT * FROM %s' % table_id, row_max,
                             table_legacy, as_object)


def table_to_schema(config, auth, project_id, dataset_id, table_id):
  if config.verbose:
    print('TABLE SCHEMA:', project_id, dataset_id, table_id)
  return API_BigQuery(config, auth).tables().get(
      projectId=project_id, datasetId=dataset_id,
      tableId=table_id).execute()['schema'].get('fields', [])


def table_to_type(config, auth, project_id, dataset_id, table_id):
  if config.verbose:
    print('TABLE TYPE:', project_id, dataset_id, table_id)
  return API_BigQuery(config, auth).tables().get(
      projectId=project_id, datasetId=dataset_id,
      tableId=table_id).execute()['type']


def query_to_rows(config, auth,
                  project_id,
                  dataset_id,
                  query,
                  row_max=None,
                  legacy=True,
                  as_object=False):
  if config.verbose:
    print('BIGQUERY QUERY:', project_id, dataset_id)

  # Create the query
  body = {
      'kind': 'bigquery#queryRequest',
      'query': query,
      'timeoutMs': 10000,
      'dryRun': False,
      'useQueryCache': True,
      'useLegacySql': legacy
  }

  if row_max:
    body['maxResults'] = row_max

  if dataset_id:
    body['defaultDataset'] = {'projectId': project_id, 'datasetId': dataset_id}

  # wait for query to complete

  response = API_BigQuery(config, auth).jobs().query(
      projectId=project_id, body=body).execute()
  while not response['jobComplete']:
    sleep(5)
    response = API_BigQuery(config, auth).jobs().getQueryResults(
        projectId=project_id,
        jobId=response['jobReference']['jobId']).execute(iterate=False)

  # fetch query results
  schema = response.get('schema', {}).get('fields', None)

  row_count = 0
  while 'rows' in response:

    for row in response['rows']:
      yield row_to_json(row, schema, as_object)
      row_count += 1

    if 'PageToken' in response:
      response = API_BigQuery(config, auth).jobs().getQueryResults(
          projectId=project_id,
          jobId=response['jobReference']['jobId'],
          pageToken=response['PageToken']).execute(iterate=False)
    elif row_count < int(response['totalRows']):
      response = API_BigQuery(config, auth).jobs().getQueryResults(
          projectId=project_id,
          jobId=response['jobReference']['jobId'],
          startIndex=row_count).execute(iterate=False)
    else:
      break


def query_to_schema(config, auth, project_id, dataset_id, query, legacy=True):

  if config.verbose:
    print('BIGQUERY QUERY SCHEMA:', project_id, dataset_id)

  body = {
    'kind': 'bigquery#queryRequest',
    'query': query,
    'timeoutMs': 10000,
    'dryRun': True,
    'useLegacySql': legacy
  }

  if dataset_id:
    body['defaultDataset'] = {'projectId': project_id, 'datasetId': dataset_id}

  response = API_BigQuery(config, auth).jobs().query(
    projectId=project_id,
    body=body
  ).execute()

  return response['schema'].get('fields', [])


def make_schema(header):
  return [{
      'name': name,
      'type': 'STRING',
      'mode': 'NULLABLE'
  } for name in row_header_sanitize(header)]


def get_schema(rows, header=True, infer_type=True):
  """CAUTION: Memory suck.

  This function sabotages iteration by iterating thorough the new object and
  returning a new iterator RECOMMEND: Define the schema yourself, it will
  also ensure data integrity downstream.
  """

  schema = []
  row_buffer = []

  # everything else defaults to STRING
  type_to_bq = {
      int: 'INTEGER',
      bool: 'BOOLEAN',
      float: 'FLOAT'
  } if infer_type else {}  # empty lookup defaults to STRING below

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
        schema.append({
            'name': value if header else 'Field_%d' % index,
            'type': 'STRING'
        })

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
              if column_type in (
                  'INTEGER', 'FLOAT') and schema[index]['type'] in ('INTEGER',
                                                                    'FLOAT'):
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


def drop_table(config, auth, project_id, dataset_id, table_id, billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  query = ('DROP TABLE `' + project_id + '.' + dataset_id + '.' + table_id +
           '` ')

  body = {
      'kind': 'bigquery#queryRequest',
      'query': query,
      'defaultDataset': {
          'datasetId': dataset_id,
      },
      'useLegacySql': False,
  }

  job_wait(
      config, auth,
      API_BigQuery(config, auth).jobs().query(projectId=billing_project_id,
                                      body=body).execute())


def _get_max_date_from_table(config, auth,
                             project_id,
                             dataset_id,
                             table_id,
                             billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  query = ('SELECT MAX(Report_Day) FROM `' + project_id + '.' + dataset_id +
           '.' + table_id + '` ')

  body = {
      'kind': 'bigquery#queryRequest',
      'query': query,
      'defaultDataset': {
          'datasetId': dataset_id,
      },
      'useLegacySql': False,
  }

  job = API_BigQuery(config, auth).jobs().query(
      projectId=billing_project_id, body=body).execute()
  return job['rows'][0]['f'][0]['v']


def _get_min_date_from_table(config, auth,
                             project_id,
                             dataset_id,
                             table_id,
                             billing_project_id=None):
  if not billing_project_id:
    billing_project_id = project_id

  query = ('SELECT MIN(Report_Day) FROM `' + project_id + '.' + dataset_id +
           '.' + table_id + '` ')

  body = {
      'kind': 'bigquery#queryRequest',
      'query': query,
      'defaultDataset': {
          'datasetId': dataset_id,
      },
      'useLegacySql': False,
  }

  job = API_BigQuery(config, auth).jobs().query(
      projectId=billing_project_id, body=body).execute()

  return job['rows'][0]['f'][0]['v']


#start and end date must be in format YYYY-MM-DD
def _clear_data_in_date_range_from_table(config, auth,
                                         project_id,
                                         dataset_id,
                                         table_id,
                                         start_date,
                                         end_date,
                                         billing_project_id=None):

  if not billing_project_id:
    billing_project_id = project_id

  query = ('DELETE FROM `' + project_id + '.' + dataset_id + '.' + table_id +
           '` ' + 'WHERE Report_Day >= "' + start_date + '"' +
           'AND Report_Day <= "' + end_date + '"')

  body = {
      'kind': 'bigquery#queryRequest',
      'query': query,
      'defaultDataset': {
          'datasetId': dataset_id,
      },
      'useLegacySql': False,
  }

  job_wait(
      config, auth,
      API_BigQuery(config, auth).jobs().query(projectId=billing_project_id,
                                      body=body).execute())
