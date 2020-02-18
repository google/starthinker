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
  'ABSTRACT_DATETIME':'TIMESTAMP',
  'CHECKBOX':'STRING',
  'CONTACT_LIST':'STRING',
  'DATE':'DATE',
  'DATETIME':'TIMESTAMP',
  'DURATION':'STRING',
  'MULTI_CONTACT_LIST':'STRING',
  'MULTI_PICKLIST':'STRING',
  'PICKLIST':'STRING',
  'PREDECESSOR':'STRING',
  'TEXT_NUMBER':'STRING'
}

def get_schema(sheet):
  return [{ "name":column_header_sanitize(column.title), "type":SMARTSHEET_TYPES.get(str(column.type), "STRING"), "mode":"NULLABLE" } for column in sheet.columns]


def get_rows(sheet, header=True, link=True):
  columns = [{'title':column.title, 'id':column.id} for column in sheet.columns]

  if header:
    cells = [column['title'] for column in columns]
    if link: cells.insert(0, 'rowPermalink')
    yield cells

  for row in sheet.rows:
    cells =  [row.get_column(column['id']).value for column in columns]
    if link: cells.insert(0, row.permalink)
    yield cells  

    
@project.from_parameters
def smartsheet():
  if project.verbose: print('Smartsheet')

  link = project.task.get('link', True)

  smart = Smartsheet(access_token=project.task['token'])
  smart.errors_as_exceptions(True)

  sheet = smart.Sheets.get_sheet(project.task['sheet'], include=("rowPermalink" if link else ''))
  rows = get_rows(sheet, False, link) 

  project.task['out'].setdefault('bigquery', {}).setdefault('schema', get_schema(sheet))
  print('SCHEMA = %s' % json.dumps(project.task['out']['bigquery']['schema'], indent=2))

  if link: project.task['out']['bigquery']['schema'].insert(0, { "name":"rowPermalink", "type":"STRING", "mode":"NULLABLE" })

  if rows: put_rows(project.task['auth'], project.task['out'], rows)


if __name__ == "__main__":
  smartsheet()
