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
"""Handler that executes { "smartsheet":{...}} task in recipe JSON.

This script translates JSON instructions into operations on smartsheet
reporting.

"""

import re
import json

from smartsheet import Smartsheet

from starthinker.util.data import put_rows
from starthinker.util.csv import column_header_sanitize

SMARTSHEET_PAGESIZE = 10000
SMARTSHEET_DATE = re.compile(r'^\d{4}[-/_]\d{2}[-/_]\d{2}$')

SMARTSHEET_TYPES = {
    'AUTO_NUMBER': 'STRING',
    'CREATED_BY': 'STRING',
    'CREATED_DATE': 'DATE',
    'MODIFIED_BY': 'STRING',
    'MODIFIED_DATE': 'DATE',
    'ABSTRACT_DATETIME': 'TIMESTAMP',
    'CHECKBOX': 'STRING',
    'CONTACT_LIST': 'STRING',
    'DATE': 'DATE',
    'DATETIME': 'TIMESTAMP',
    'DURATION': 'STRING',
    'MULTI_CONTACT_LIST': 'STRING',
    'MULTI_PICKLIST': 'STRING',
    'PICKLIST': 'STRING',
    'PREDECESSOR': 'STRING',
    'TEXT_NUMBER': 'STRING'
}


def smartsheet_api(token):
  smart = Smartsheet(access_token=token)
  smart.errors_as_exceptions(True)
  return smart


def get_schema(sheet_or_report):
  return [{
      'name': column_header_sanitize(column.title),
      'type': SMARTSHEET_TYPES.get(str(column.type), 'STRING'),
      'mode': 'NULLABLE'
  } for column in sheet_or_report.columns]


def get_rows(sheet=None, report=None, header=True, link=True, key='id'):

  columns = {(column.id if sheet else column.virtual_id): {
      'title': column.title,
      'index': column.index,
      'type': str(column.type)
  } for column in (sheet or report).columns}

  if header:
    cells = [
        column['title']
        for column in sorted(columns.values(), key=lambda i: i['index'])
    ]
    if link:
      cells.insert(0, 'rowPermalink')
    yield cells

  for row in (sheet or report).rows:
    buffer = [None] * len(columns)
    for cell in row.cells:
      value = cell.value

      # correct the date column ( for reports it comes in as date and time even though column is DATE)
      if columns[cell.column_id if sheet else cell
                 .virtual_column_id]['type'] == 'DATE' and value is not None:
        if 'T' in value:
          value = value.split('T', 1)[0]
        if not SMARTSHEET_DATE.match(value):
          print('BAD DATE VALUE', value)
          value = None

      buffer[columns[cell.column_id if sheet else cell.virtual_column_id]
             ['index']] = value

    if link:
      buffer.insert(0, row.permalink)
    yield buffer


def get_sheet_schema(token, sheet, link=True):
  sheet_json = smartsheet_api(token).Sheets.get_sheet(
      sheet, include=('rowPermalink' if link else ''), page_size=0)
  return get_schema(sheet_json)


def get_report_schema(token, report, link=True):
  report_json = smartsheet_api(token).Reports.get_report(report, page_size=0)
  return get_schema(report_json)


def get_sheet_rows(token, sheet, link=True):
  sheet_json = smartsheet_api(token).Sheets.get_sheet(
      sheet, include=('rowPermalink' if link else ''))
  return get_rows(sheet=sheet_json, header=False, link=link)


def get_report_rows(token, report):
  count = 0
  total = 1
  page = 1

  api = smartsheet_api(token)
  while count < total:
    report_json = api.Reports.get_report(
        report, page_size=SMARTSHEET_PAGESIZE, page=page)
    total = report_json.total_row_count
    for row in get_rows(report=report_json, header=False, link=False):
      yield row
      count += 1
    page += 1


def smartsheet(config, task):
  if config.verbose:
    print('SMARTSHEET')

  if 'sheet' in task:
    link = task.get('link', True)
    rows = get_sheet_rows(task['token'], task['sheet'], link)
    schema = get_sheet_schema(task['token'], task['sheet'],
                              link)

  elif 'report' in task:
    link = False
    rows = get_report_rows(task['token'], task['report'])
    schema = get_report_schema(task['token'], task['report'])

  else:
    raise NameError('Either report or sheet must be in the recipe json.')

  if 'bigquery' in task['out']:
    task['out']['bigquery'].setdefault('schema', schema)
    print('SCHEMA = %s' %
          json.dumps(task['out']['bigquery']['schema'], indent=2))

    if link and 'schema' in task['out']['bigquery']:
      task['out']['bigquery']['schema'].insert(0, {
          'name': 'rowPermalink',
          'type': 'STRING',
          'mode': 'NULLABLE'
      })

  if rows:
    put_rows(config, task['auth'], task['out'], rows)
