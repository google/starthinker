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

"""Handler for "bigquery" task in recipes.

One of the oldest tasks in StarThinker, due for a refactor to get_rows and
put_rows. Please test thouroughly when modifying this module.

Includes:
  bigquery_function - generate custom tables or functions
  bigquery_query - execute a query and write results to table ( future get_rows / put_rows )
   table - write query results to a table
   sheet - write query results to a sheet
   view - write query results to a view
  bigquery_run - execute a query without expected return results
  bigquery_storage - read from storage into a table
  bigquery_values - write explicit values to a table ( future get_rows )
"""

from starthinker.util.project import project
from starthinker.util.csv import rows_to_type
from starthinker.util.sheets import sheets_clear
from starthinker.util.sheets import sheets_write
from starthinker.util.data import get_rows, put_rows
from starthinker.util.bigquery import query_to_table, query_to_view, storage_to_table, query_to_rows, json_to_table, rows_to_table, run_query, query_parameters
from starthinker.util.bigquery.functions import pearson_significance_test
from starthinker.util.bigquery.us_geography import US_GEOGRAPHY_DATA, US_GEOGRAPHY_SCHEMA


def bigquery_function():
  """Generate custom tables or functions.

  See: scripts/bigquery_function.json
  """

  if project.verbose:
    print('FUNCTION', project.task['function'])

  if project.task['function'] == 'Pearson Significance Test':
    run_query(
      project.task['auth'],
      project.id,
      pearson_significance_test(),
      False,
      project.task['to']['dataset']
    )

  elif project.task['function'] == 'US Geography':
    json_to_table(
      project.task['auth'],
      project.id,
      project.task['to']['dataset'],
      'US_Geography',
      US_GEOGRAPHY_DATA,
      US_GEOGRAPHY_SCHEMA
    )


def bigquery_run():
  """Execute a query without expected return results.

  See: scripts/bigquery_run_query.json
  """

  if project.verbose:
    print('RUN QUERY', project.task['run']['query'])

  run_query(
    project.task['auth'],
    project.id,
    query_parameters(
      project.task['run']['query'],
      project.task['run'].get('parameters')
    ),
    project.task['run'].get('legacy', True)
  )


def bigquery_values():
  """Write explicit values to a table.

  TODO: Replace with get_rows.

  See: scripts/bigquery_run_query.json
  """

  if project.verbose:
    print('VALUES', project.task['from']['values'])

  rows = get_rows(project.task['auth'], project.task['from'])
  rows_to_table(
    project.task['to'].get('auth', project.task['auth']),
    project.id,
    project.task['to']['dataset'],
    project.task['to']['table'],
    rows,
    project.task.get('schema', []),
    0
  )


def bigquery_query():
  """Execute a query and write results to table.

  TODO: Replace with get_rows and put_rows combination.

  See: scripts/bigquery_query.json
       scripts/bigquery_storage.json
       scripts/bigquery_to_sheet.json
       scripts/bigquery_view.json
  """

  if 'table' in project.task['to']:
    if project.verbose:
      print('QUERY TO TABLE', project.task['to']['table'])

    query_to_table(
      project.task['auth'],
      project.id,
      project.task['to']['dataset'],
      project.task['to']['table'],
      query_parameters(
        project.task['from']['query'],
        project.task['from'].get('parameters')
      ),
      disposition=project.task['write_disposition']
        if 'write_disposition' in project.task
        else 'WRITE_TRUNCATE',
      legacy=project.task['from'].get(
        'legacy',
        project.task['from'].get('useLegacySql', True)
      ),  # DEPRECATED: useLegacySql,
      target_project_id=project.task['to'].get('project_id', project.id)
    )

  elif 'sheet' in project.task['to']:
    if project.verbose:
      print('QUERY TO SHEET', project.task['to']['sheet'])

    rows = query_to_rows(
      project.task['auth'],
      project.id,
      project.task['from']['dataset'],
      query_parameters(
        project.task['from']['query'],
        project.task['from'].get('parameters')
      ),
      legacy=project.task['from'].get('legacy', True)
    )

    # makes sure types are correct in sheet
    rows = rows_to_type(rows)

    sheets_clear(
      project.task['to'].get('auth', project.task['auth']),
      project.task['to']['sheet'],
      project.task['to']['tab'],
      project.task['to'].get('range', 'A2')
    )
    sheets_write(
      project.task['to'].get('auth', project.task['auth']),
      project.task['to']['sheet'],
      project.task['to']['tab'],
      project.task['to'].get('range', 'A2'),
      rows
    )

  elif 'sftp' in project.task['to']:
    if project.verbose:
      print('QUERY TO SFTP')

    rows = query_to_rows(
      project.task['auth'],
      project.id,
      project.task['from']['dataset'],
      query_parameters(
        project.task['from']['query'],
        project.task['from'].get('parameters')
      ),
      legacy=project.task['from'].get('use_legacy_sql', True)
    )

    if rows:
      put_rows(project.task['auth'], project.task['to'], rows)

  else:
    if project.verbose:
      print('QUERY TO VIEW', project.task['to']['view'])

    query_to_view(
      project.task['auth'],
      project.id,
      project.task['to']['dataset'],
      project.task['to']['view'],
      query_parameters(
        project.task['from']['query'],
        project.task['from'].get('parameters')
      ),
      project.task['from'].get(
        'legacy',
        project.task['from'].get('useLegacySql', True)
      ),  # DEPRECATED: useLegacySql
      project.task['to'].get('replace', False)
    )


def bigquery_storage():
  """Read from storage into a table.

  See: scripts/bigquery_storage.json
  """

  if project.verbose:
    print('STORAGE TO TABLE', project.task['to']['table'])

  storage_to_table(
    project.task['auth'], project.id, project.task['to']['dataset'],
    project.task['to']['table'],
    project.task['from']['bucket'] + ':' + project.task['from']['path'],
    project.task.get('schema', []), project.task.get('skip_rows', 1),
    project.task.get('structure', 'CSV'),
    project.task.get('disposition', 'WRITE_TRUNCATE')
  )


@project.from_parameters
def bigquery():

  if 'function' in project.task:
    bigquery_function()
  elif 'run' in project.task and 'query' in project.task.get('run', {}):
    bigquery_run()
  elif 'values' in project.task['from']:
    bigquery_values()
  elif 'query' in project.task['from']:
    bigquery_query()
  elif 'bucket' in project.task['from']:
    bigquery_query()
  else:
    raise NotImplementedError('The bigquery task has no such handler.')

if __name__ == '__main__':
  bigquery()
