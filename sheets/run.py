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

from util.project import project
from util.sheets import sheets_tab_create, sheets_read, sheets_tab_copy, sheets_clear
from util.bigquery import get_schema, csv_to_table
from util.csv import rows_to_type, rows_to_csv

def sheets():
  if project.verbose: print 'SHEETS'

  # clear if specified
  if project.task.get('clear', False):
    sheets_clear(project.task['auth'], project.task['sheet'], project.task['tab'], project.task['range'])

  # create or copy if specified
  if 'template' in project.task:
    sheets_tab_copy(project.task['auth'], project.task['template']['sheet'], project.task['template']['tab'], project.task['sheet'], project.task['tab'])
  else:
    sheets_tab_create(project.task['auth'], project.task['sheet'], project.task['tab'])

  # move if specified
  if 'out' in project.task:
    rows = sheets_read(project.task['auth'], project.task['sheet'], project.task['tab'], project.task['range'])

    if rows:
      schema = []

      rows = rows_to_type(rows)
      #rows = get_schema(rows, schema, project.task.get('header', False))
      data = rows_to_csv(rows) # schema ONLY becomes filled here ( iterator consumed )

      csv_to_table(
        project.task['auth'],
        project.id,
        project.task['out']['bigquery']['dataset'],
        project.task['out']['bigquery']['table'],
        data,
        project.task['out']['bigquery']['schema'],
      )

    else:
      print 'SHEET EMPTY'


if __name__ == "__main__":
  project.load('sheets')
  sheets()
