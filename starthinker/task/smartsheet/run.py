###########################################################################
#
#  Copyright 2020 Google Inc.
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

This script translates JSON instructions into operations on smartsheet reporting.

"""

import json

from smartsheet import Smartsheet

from starthinker.util.project import project
from starthinker.util.data import put_rows
from starthinker.util.csv import column_header_sanitize

SMARTSHEET_TYPES = {
  'AUTO_NUMBER':'STRING',
  'CREATED_BY':'STRING',
  'CREATED_DATE':'DATE',
  'MODIFIED_BY':'STRING',
  'MODIFIED_DATE':'DATE',
  'ABSTRACT_DATETIME':'DATETIME',
  'CHECKBOX':'STRING',
  'CONTACT_LIST':'STRING',
  'DATE':'DATE',
  'DATETIME':'DATETIME',
  'DURATION':'STRING',
  'MULTI_CONTACT_LIST':'STRING',
  'MULTI_PICKLIST':'STRING',
  'PICKLIST':'STRING',
  'PREDECESSOR':'STRING',
  'TEXT_NUMBER':'STRING'
}

def get_schema(sheet):
  return [{ "name":column_header_sanitize(column.title), "type":SMARTSHEET_TYPES.get(str(column.type), "STRING"), "mode":"NULLABLE" } for column in sheet.columns]


def get_rows(sheet, header=True):
  columns = [{'title':column.title, 'id':column.id} for column in sheet.columns]

  if header:
    yield [column['title'] for column in columns]

  for row in sheet.rows:
    cells =  [row.get_column(column['id']).display_value for column in columns]
    yield cells  

    
@project.from_parameters
def smartsheet():
  if project.verbose: print('Smartsheet')

  smart = Smartsheet(access_token=project.task['token'])

  smart.errors_as_exceptions(True)
  sheet = smart.Sheets.get_sheet(project.task['sheet'])

  default_schema = get_schema(sheet)
  print('DEFAULT_SCHEMA = %s' % json.dumps(default_schema, indent=2))
  project.task.setdefault('out', {}).setdefault('bigquery', {}).setdefault('schema', default_schema)

  rows = get_rows(sheet, False) 

  if rows: put_rows(project.task['auth'], project.task['out'], rows)


if __name__ == "__main__":
  smartsheet()
