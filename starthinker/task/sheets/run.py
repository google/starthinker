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

from starthinker.util.sheets import sheets_create, sheets_tab_create, sheets_read, sheets_write, sheets_clear, sheets_tab_copy, sheets_tab_delete
from starthinker.util.bigquery import get_schema, rows_to_table
from starthinker.util.csv import rows_to_type
from starthinker.util.data import get_rows


def sheets(config, task):
  if config.verbose:
    print('SHEETS')

  # if sheet or tab is missing, don't do anything
  if not task.get('sheet') or not task.get('tab'):
    if config.verbose:
      print('Missing Sheet and/or Tab, skipping task.')
    return

  # delete if specified, will delete sheet if no more tabs remain
  if task.get('delete', False):
    sheets_tab_delete(config, task['auth'], task['sheet'],
                      task['tab'])

  # create a sheet and tab if specified, if template
  if 'template' in task:
    sheets_create(
        config,
        task['auth'],
        task['sheet'],
        task['tab'],
        task['template'].get('sheet'),
        task['template'].get('tab'),
    )

  # copy template if specified ( clear in this context means overwrite )
  #if task.get('template', {}).get('sheet'):
  #  sheets_tab_copy(
  #    config,
  #    task['auth'],
  #    task['template']['sheet'],
  #    task['template']['tab'],
  #    task['sheet'],
  #    task['tab'],
  #    task.get('clear', False)
  #  )

  # if no template at least create tab
  #else:
  #  sheets_tab_create(
  #    config,
  #    task['auth'],
  #    task['sheet'],
  #    task['tab']
  #  )

  # clear if specified
  if task.get('clear', False):
    sheets_clear(config, task['auth'], task['sheet'],
                 task['tab'], task.get('range', 'A1'))

  # write data if specified
  if 'write' in task:
    rows = get_rows(config, task['auth'], task['write'])
    sheets_write(
        config,
        task['auth'],
        task['sheet'],
        task['tab'],
        task['range'],
        rows,
        append=False)

  # append data if specified
  if 'append' in task:
    rows = get_rows(config, task['auth'], task['append'])
    sheets_write(
        config,
        task['auth'],
        task['sheet'],
        task['tab'],
        task['range'],
        rows,
        append=True)

  # move data if specified
  # move data if specified
  if 'out' in task:
    rows = sheets_read(config, task['auth'], task['sheet'],
                       task['tab'], task.get('range', 'A1'))

    if rows:
      schema = None

      # RECOMMENDED: define schema in json
      if task['out']['bigquery'].get('schema'):
        if config.verbose:
          print('SHEETS SCHEMA DEFINED')
        schema = task['out']['bigquery']['schema']

      # NOT RECOMMENDED: determine schema if missing
      else:
        if config.verbose:
          print(
              'SHEETS SCHEMA DETECT ( Note Recommended - Define Schema In JSON )'
          )
        # cast rows to types ( for schema detection )
        rows = rows_to_type(rows)
        rows, schema = get_schema(
            rows,
            task.get('header', False),
            infer_type=task.get('infer_type', True))

      # write to table ( not using put because no use cases for other destinations )
      rows_to_table(
          config,
          auth=task['out'].get('auth', task['auth']),
          project_id=config.project,
          dataset_id=task['out']['bigquery']['dataset'],
          table_id=task['out']['bigquery']['table'],
          rows=rows,
          schema=schema,
          skip_rows=1 if task.get('header', False) else 0,
          disposition=task['out']['bigquery'].get(
              'disposition', 'WRITE_TRUNCATE'))

    else:
      print('SHEET EMPTY')
