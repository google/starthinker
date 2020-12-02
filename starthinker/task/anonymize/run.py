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

from datetime import date, datetime, timedelta
import re
import random

from googleapiclient.errors import HttpError

from starthinker.util.bigquery import json_to_table
from starthinker.util.bigquery import query_to_view
from starthinker.util.bigquery import rows_to_table
from starthinker.util.bigquery import table_to_rows
from starthinker.util.google_api import API_BigQuery
from starthinker.util.project import project

RE_EMAIL = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
INTEGER_MULTIPLY = random.randint(2, 9)
INTEGER_OFFSET = random.randint(17, 99)
DATE_OFFSET = timedelta(days=random.randint(3, 13), weeks=random.randint(3, 23))

STRING_IDS = {}


def anonymize_string(cell, column):
  global STRING_IDS
  STRING_IDS.setdefault(column, {})
  STRING_IDS[column].setdefault(cell, len(STRING_IDS[column]) + 1)

  # email
  if RE_EMAIL.match(cell):
    return '%s_%d@email.com' % (column.rsplit('.',
                                              1)[-1], STRING_IDS[column][cell])
  # any string
  else:
    return '%s_%d' % (column.rsplit('.', 1)[-1], STRING_IDS[column][cell])


def anonymize_integer(cell, column):
  # possible date ( legacy Data Studio format )
  if len(str(cell)) == 4 + 2 + 2:
    return cell
  else:
    # integer
    return (cell * INTEGER_MULTIPLY) + INTEGER_OFFSET


def anonymize_float(cell, column):
  # replace integers randonly within float to preserve semaintics ( in case 0 - 1 range is percent )
  return float(''.join([
      '.' if char == '.' else str(random.randint(0, 9))
      for char in str(cell).lstrip('0')
  ]))


def anonymize_date(cell, column):
  # shift date back in time to prevent future dates
  # convert to string because its being written back to BigQuery
  return str(cell - DATE_OFFSET)


def anonymize_value(value, column):
  if isinstance(value, int):
    return anonymize_integer(value, column)
  elif isinstance(value, str):
    return anonymize_string(value, column)
  elif isinstance(value, float):
    return anonymize_float(value, column)
  elif isinstance(value, date):
    return anonymize_date(value, column)
  elif isinstance(value, datetime):
    return anonymize_date(value, column)


def anonymize_json(struct, parent=None):
  if isinstance(struct, dict):
    for key, value in struct.items():
      if isinstance(value, (dict, list)):
        anonymize_json(value, '.'.join((parent, key)) if parent else key)
      else:
        struct[key] = anonymize_value(
            value, '.'.join((parent, key)) if parent else key)
  elif isinstance(struct, list):
    for index, value in enumerate(struct):
      if isinstance(value, (dict, list)):
        anonymize_json(value, parent)
      else:
        struct[index] = anonymize_value(value, parent)

  return struct


def anonymize_csv(row, schema):
  for index, cell in enumerate(row):
    if cell is not None:
      if schema[index]['type'] == 'STRING':
        row[index] = anonymize_string(cell, schema[index]['name'])
      elif schema[index]['type'] in ('INTEGER', 'INT64', 'NUMERIC'):
        row[index] = anonymize_integer(cell, schema[index]['name'])
      elif schema[index]['type'] in ('FLOAT', 'FLOAT64'):
        row[index] = anonymize_float(cell, schema[index]['name'])
      elif schema[index]['type'] in ('DATE', 'DATETIME'):
        row[index] = anonymize_date(cell, schema[index]['name'])
  return row


def anonymize_rows(rows, schema, is_object):
  for row in rows:
    if is_object:
      yield anonymize_json(row)
    else:
      yield anonymize_csv(row, schema)


def anonymize_table(table_id):

  if project.verbose:
    print('ANONYMIZE TABLE', project.task['bigquery']['to']['dataset'],
          table_id)

  schema = API_BigQuery(project.task['auth']).tables().get(
      projectId=project.task['bigquery']['from']['project'],
      datasetId=project.task['bigquery']['from']['dataset'],
      tableId=table_id).execute()['schema']['fields']

  is_object = any([s['type'] == 'RECORD' for s in schema])

  rows = table_to_rows(
      project.task['auth'],
      project.task['bigquery']['from']['project'],
      project.task['bigquery']['from']['dataset'],
      table_id,
      as_object=is_object)

  rows = anonymize_rows(rows, schema, is_object)

  if is_object:
    json_to_table(
        project.task['auth'],
        project.task['bigquery']['to']['project'],
        project.task['bigquery']['to']['dataset'],
        table_id,
        rows,
        schema,
        disposition='WRITE_TRUNCATE')
  else:
    rows_to_table(
        project.task['auth'],
        project.task['bigquery']['to']['project'],
        project.task['bigquery']['to']['dataset'],
        table_id,
        rows,
        schema,
        skip_rows=0,
        disposition='WRITE_TRUNCATE')


def copy_view(view_id):
  if project.verbose:
    print('ANONYMIZE VIEW', project.task['bigquery']['to']['dataset'], view_id)

  view = API_BigQuery(project.task['auth']).tables().get(
      projectId=project.task['bigquery']['from']['project'],
      datasetId=project.task['bigquery']['from']['dataset'],
      tableId=view_id).execute()['view']

  project_dataset_template = '[%s:%s.' if view['useLegacySql'] else '`%s.%s.'

  query = view['query'].replace(
      project_dataset_template % (project.task['bigquery']['from']['project'],
                                  project.task['bigquery']['from']['dataset']),
      project_dataset_template % (project.task['bigquery']['to']['project'],
                                  project.task['bigquery']['to']['dataset']))

  query_to_view(
      project.task['auth'],
      project.task['bigquery']['to']['project'],
      project.task['bigquery']['to']['dataset'],
      view_id,
      query,
      legacy=view['useLegacySql'],
      replace=True)


@project.from_parameters
def anonymize():

  views = []

  for table in API_BigQuery(
      project.task['auth'], iterate=True).tables().list(
          projectId=project.task['bigquery']['from']['project'],
          datasetId=project.task['bigquery']['from']['dataset']).execute():
    if table['type'] == 'VIEW':
      views.append(table['tableReference']['tableId'])
    else:
      anonymize_table(table['tableReference']['tableId'])

  # views have dependencies, loop through all and create until no more errors or no change in view list
  last_copy = True
  while last_copy:
    retry_views = []
    last_copy = False
    while views:
      view = views.pop()
      try:
        copy_view(view)
        last_copy = True
      except HttpError as e:
        if e.resp.status == 404:
          retry_views.append(view)
        else:
          raise e
    views = retry_views


if __name__ == '__main__':
  anonymize()
