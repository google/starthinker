###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  yoy may not use this file except in compliance with the License.
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

from starthinker.util import bigquery as bq
from starthinker.util import csv
from starthinker.util import data
from starthinker.util import sheets
from starthinker.util.bigquery_functions import pearson_significance_test, rgb_to_hsv

def bigquery_function(config, task):
  """Generate custom tables or functions.

  See: scripts/bigquery_function.json
  """

  if config.verbose:
    print('FUNCTION', task['function'])

  if task['function'] == 'Pearson Significance Test':
    bq.run_query(
      config,
      task['auth'],
      config.project,
      pearson_significance_test(),
      False,
      task['to']['dataset']
    )

  elif task['function'] == 'RGB To HSV':
    bq.run_query(
      config,
      task['auth'],
      config.project,
      rgb_to_hsv(),
      False,
      task['to']['dataset']
    )
  else:
    raise LookupError('Function Not Defined: %s' % task['function'])

def bigquery_run(config, task):
  """Execute a query without expected return results.

  See: scripts/bigquery_run_query.json
  """

  if config.verbose:
    print('RUN QUERY', task['run']['query'])

  bq.run_query(
    config,
    task['auth'],
    config.project,
    bq.query_parameters(
      task['run']['query'],
      task['run'].get('parameters')
    ),
    task['run'].get('legacy', True)
  )


def bigquery_values(config, task):
  """Write explicit values to a table.

  TODO: Replace with get_rows.

  See: scripts/bigquery_run_query.json
  """

  if config.verbose:
    print('VALUES', task['from']['values'])

  rows = data.get_rows(config, task['auth'], task['from'])
  bq.rows_to_table(
    config,
    task['to'].get('auth', task['auth']),
    config.project,
    task['to']['dataset'],
    task['to']['table'],
    rows,
    task.get('schema', []),
    0
  )


def bigquery_query(config, task):
  """Execute a query and write results to table.

  TODO: Replace with get_rows and put_rows combination.

  See: scripts/bigquery_query.json
       scripts/bigquery_storage.json
       scripts/bigquery_to_sheet.json
       scripts/bigquery_view.json
  """

  if 'table' in task['to']:
    if config.verbose:
      print('QUERY TO TABLE', task['to']['table'])

    bq.query_to_table(
      config,
      task['auth'],
      config.project,
      task['to']['dataset'],
      task['to']['table'],
      bq.query_parameters(
        task['from']['query'],
        task['from'].get('parameters')
      ),
      disposition=task['write_disposition']
        if 'write_disposition' in task
        else 'WRITE_TRUNCATE',
      legacy=task['from'].get(
        'legacy',
        task['from'].get('useLegacySql', True)
      ),  # DEPRECATED: useLegacySql,
      target_project_id=task['to'].get('project_id', config.project)
    )

  elif 'sheet' in task['to']:
    if config.verbose:
      print('QUERY TO SHEET', task['to']['sheet'])

    rows = bq.query_to_rows(
      config,
      task['auth'],
      config.project,
      task['from']['dataset'],
      bq.query_parameters(
        task['from']['query'],
        task['from'].get('parameters')
      ),
      legacy=task['from'].get('legacy', True)
    )

    # makes sure types are correct in sheet
    rows = csv.rows_to_type(rows)

    sheets.sheets_clear(
      config,
      task['to'].get('auth', task['auth']),
      task['to']['sheet'],
      task['to']['tab'],
      task['to'].get('range', 'A2')
    )
    sheets.sheets_write(
      config,
      task['to'].get('auth', task['auth']),
      task['to']['sheet'],
      task['to']['tab'],
      task['to'].get('range', 'A2'),
      rows
    )

  elif 'sftp' in task['to']:
    if config.verbose:
      print('QUERY TO SFTP')

    rows = bq.query_to_rows(
      config,
      task['auth'],
      config.project,
      task['from']['dataset'],
      bq.query_parameters(
        task['from']['query'],
        task['from'].get('parameters')
      ),
      legacy=task['from'].get('use_legacy_sql', True)
    )

    if rows:
      data.put_rows(config, task['auth'], task['to'], rows)

  else:
    if config.verbose:
      print('QUERY TO VIEW', task['to']['view'])

    bq.query_to_view(
      config,
      task['auth'],
      config.project,
      task['to']['dataset'],
      task['to']['view'],
      bq.query_parameters(
        task['from']['query'],
        task['from'].get('parameters')
      ),
      task['from'].get(
        'legacy',
        task['from'].get('useLegacySql', True)
      ),  # DEPRECATED: useLegacySql
      task['to'].get('replace', False)
    )


def bigquery_storage(config, task):
  """Read from storage into a table.

  See: scripts/bigquery_storage.json
  """

  if config.verbose:
    print('STORAGE TO TABLE', task['to']['table'])

  bq.storage_to_table(
    config,
    task['auth'], config.project, task['to']['dataset'],
    task['to']['table'],
    task['from']['bucket'] + ':' + task['from']['path'],
    task.get('schema', []), task.get('skip_rows', 1),
    task.get('structure', 'CSV'),
    task.get('disposition', 'WRITE_TRUNCATE')
  )


def bigquery(config, task):

  if 'function' in task:
    bigquery_function(config, task)
  elif 'run' in task and 'query' in task.get('run', {}):
    bigquery_run(config, task)
  elif 'values' in task['from']:
    bigquery_values(config, task)
  elif 'query' in task['from']:
    bigquery_query(config, task)
  elif 'bucket' in task['from']:
    bigquery_query(config, task)
  else:
    raise NotImplementedError('The bigquery task has no such handler.')
