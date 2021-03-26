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

from starthinker.util import bigquery
from starthinker.util import csv
from starthinker.util import data
from starthinker.util import project
from starthinker.util import sheets
from starthinker.util.bigquery import functions
from starthinker.util.bigquery import us_geography


# TODO: Remove class rename monkeypatch after project refactor
if not hasattr(project, 'Project'):
  project.Project = project.project


def bigquery_function():
  """Generate custom tables or functions.

  See: scripts/bigquery_function.json
  """

  if project.Project.verbose:
    print('FUNCTION', project.Project.task['function'])

  if project.Project.task['function'] == 'Pearson Significance Test':
    bigquery.run_query(
      project.Project.task['auth'],
      project.Project.id,
      functions.pearson_significance_test(),
      False,
      project.Project.task['to']['dataset']
    )

  elif project.Project.task['function'] == 'US Geography':
    bigquery.json_to_table(
      project.Project.task['auth'],
      project.Project.id,
      project.Project.task['to']['dataset'],
      'US_Geography',
      us_geography.US_GEOGRAPHY_DATA,
      us_geography.US_GEOGRAPHY_SCHEMA
    )


def bigquery_run():
  """Execute a query without expected return results.

  See: scripts/bigquery_run_query.json
  """

  if project.Project.verbose:
    print('RUN QUERY', project.Project.task['run']['query'])

  bigquery.run_query(
    project.Project.task['auth'],
    project.Project.id,
    bigquery.query_parameters(
      project.Project.task['run']['query'],
      project.Project.task['run'].get('parameters')
    ),
    project.Project.task['run'].get('legacy', True)
  )


def bigquery_values():
  """Write explicit values to a table.

  TODO: Replace with get_rows.

  See: scripts/bigquery_run_query.json
  """

  if project.Project.verbose:
    print('VALUES', project.Project.task['from']['values'])

  rows = data.get_rows(project.Project.task['auth'], project.Project.task['from'])
  bigquery.rows_to_table(
    project.Project.task['to'].get('auth', project.Project.task['auth']),
    project.Project.id,
    project.Project.task['to']['dataset'],
    project.Project.task['to']['table'],
    rows,
    project.Project.task.get('schema', []),
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

  if 'table' in project.Project.task['to']:
    if project.Project.verbose:
      print('QUERY TO TABLE', project.Project.task['to']['table'])

    bigquery.query_to_table(
      project.Project.task['auth'],
      project.Project.id,
      project.Project.task['to']['dataset'],
      project.Project.task['to']['table'],
      bigquery.query_parameters(
        project.Project.task['from']['query'],
        project.Project.task['from'].get('parameters')
      ),
      disposition=project.Project.task['write_disposition']
        if 'write_disposition' in project.Project.task
        else 'WRITE_TRUNCATE',
      legacy=project.Project.task['from'].get(
        'legacy',
        project.Project.task['from'].get('useLegacySql', True)
      ),  # DEPRECATED: useLegacySql,
      target_project_id=project.Project.task['to'].get('project_id', project.Project.id)
    )

  elif 'sheet' in project.Project.task['to']:
    if project.Project.verbose:
      print('QUERY TO SHEET', project.Project.task['to']['sheet'])

    rows = bigquery.query_to_rows(
      project.Project.task['auth'],
      project.Project.id,
      project.Project.task['from']['dataset'],
      bigquery.query_parameters(
        project.Project.task['from']['query'],
        project.Project.task['from'].get('parameters')
      ),
      legacy=project.Project.task['from'].get('legacy', True)
    )

    # makes sure types are correct in sheet
    rows = csv.rows_to_type(rows)

    sheets.sheets_clear(
      project.Project.task['to'].get('auth', project.Project.task['auth']),
      project.Project.task['to']['sheet'],
      project.Project.task['to']['tab'],
      project.Project.task['to'].get('range', 'A2')
    )
    sheets.sheets_write(
      project.Project.task['to'].get('auth', project.Project.task['auth']),
      project.Project.task['to']['sheet'],
      project.Project.task['to']['tab'],
      project.Project.task['to'].get('range', 'A2'),
      rows
    )

  elif 'sftp' in project.Project.task['to']:
    if project.Project.verbose:
      print('QUERY TO SFTP')

    rows = bigquery.query_to_rows(
      project.Project.task['auth'],
      project.Project.id,
      project.Project.task['from']['dataset'],
      bigquery.query_parameters(
        project.Project.task['from']['query'],
        project.Project.task['from'].get('parameters')
      ),
      legacy=project.Project.task['from'].get('use_legacy_sql', True)
    )

    if rows:
      data.put_rows(project.Project.task['auth'], project.Project.task['to'], rows)

  else:
    if project.Project.verbose:
      print('QUERY TO VIEW', project.Project.task['to']['view'])

    bigquery.query_to_view(
      project.Project.task['auth'],
      project.Project.id,
      project.Project.task['to']['dataset'],
      project.Project.task['to']['view'],
      bigquery.query_parameters(
        project.Project.task['from']['query'],
        project.Project.task['from'].get('parameters')
      ),
      project.Project.task['from'].get(
        'legacy',
        project.Project.task['from'].get('useLegacySql', True)
      ),  # DEPRECATED: useLegacySql
      project.Project.task['to'].get('replace', False)
    )


def bigquery_storage():
  """Read from storage into a table.

  See: scripts/bigquery_storage.json
  """

  if project.Project.verbose:
    print('STORAGE TO TABLE', project.Project.task['to']['table'])

  bigquery.storage_to_table(
    project.Project.task['auth'], project.Project.id, project.Project.task['to']['dataset'],
    project.Project.task['to']['table'],
    project.Project.task['from']['bucket'] + ':' + project.Project.task['from']['path'],
    project.Project.task.get('schema', []), project.Project.task.get('skip_rows', 1),
    project.Project.task.get('structure', 'CSV'),
    project.Project.task.get('disposition', 'WRITE_TRUNCATE')
  )


@project.Project.from_parameters
def bigquery():

  if 'function' in project.Project.task:
    bigquery_function()
  elif 'run' in project.Project.task and 'query' in project.Project.task.get('run', {}):
    bigquery_run()
  elif 'values' in project.Project.task['from']:
    bigquery_values()
  elif 'query' in project.Project.task['from']:
    bigquery_query()
  elif 'bucket' in project.Project.task['from']:
    bigquery_query()
  else:
    raise NotImplementedError('The bigquery task has no such handler.')

if __name__ == '__main__':
  bigquery()
