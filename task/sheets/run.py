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

from starthinker.util.project import project
from starthinker.util.sheets import sheets_tab_create, sheets_read, sheets_write, sheets_clear, sheets_tab_copy, sheets_tab_delete
from starthinker.util.bigquery import get_schema, rows_to_table
from starthinker.util.csv import rows_to_type
from starthinker.util.data import get_rows

def sheets():
  if project.verbose: print 'SHEETS'

  # clear if specified
  if project.task.get('clear', False):
    sheets_clear(project.task['auth'], project.task['sheet'], project.task['tab'], project.task['range'])

  # delete if specified ( after clear to prevent errors in case both are given )
  if project.task.get('delete', False):
    sheets_tab_delete(project.task['auth'], project.task['sheet'], project.task['tab'])

  # create or copy if specified
  if 'template' in project.task:
    sheets_tab_copy(project.task['auth'], project.task['template']['sheet'], project.task['template']['tab'], project.task['sheet'], project.task['tab'])
  else:
    sheets_tab_create(project.task['auth'], project.task['sheet'], project.task['tab'])

  # write data if specified
  if 'write' in project.task:
    rows = get_rows(project.task['auth'], project.task['write'])
    sheets_write(project.task['auth'], project.task['sheet'], project.task['tab'], project.task['range'], rows)

  # move if specified
  if 'out' in project.task:
    rows = sheets_read(project.task['auth'], project.task['sheet'], project.task['tab'], project.task['range'])

    if rows:
      schema = None

      # RECOMMENDED: define schema in json
      if project.task['out']['bigquery'].get('schema'):
        if project.verbose: print 'SHEETS SCHEMA DEFINED'
        schema = project.task['out']['bigquery']['schema']
      # NOT RECOMMENDED: determine schema if missing 
      else:
        if project.verbose: print 'SHEETS SCHEMA DETECT ( Note Recommended - Define Schema In JSON )'
        # cast rows to types ( for schema detection )
        rows = rows_to_type(rows)
        rows, schema = get_schema(rows, project.task.get('header', False), infer_type=project.task.get('infer_type', True))

      # write to table ( not using put because no use cases for other destinations )
      rows_to_table(
        auth=project.task['auth'],
        project_id=project.id,
        dataset_id=project.task['out']['bigquery']['dataset'],
        table_id=project.task['out']['bigquery']['table'],
        rows=rows,
        schema=schema,
        skip_rows=1 if project.task.get('header', False) else 0,
        disposition=project.task['out']['bigquery'].get('disposition', 'WRITE_TRUNCATE')
      )

    else:
      print 'SHEET EMPTY'


if __name__ == "__main__":
  project.load('sheets')
  sheets()
