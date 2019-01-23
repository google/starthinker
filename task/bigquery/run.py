###########################################################################
#
#  Copyright 2018 Google Inc.
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

# PARAMETIZE QUERIES: https://cloud.google.com/bigquery/docs/parameterized-queries

import uuid
import os
import csv

from starthinker.util.project import project
from starthinker.util.bigquery import query_to_table, query_to_view, storage_to_table, query_to_rows, execute_statement
from starthinker.util.csv import rows_to_type
from starthinker.util.sheets import sheets_clear
from starthinker.util.sheets import sheets_write
from starthinker.util.storage import object_put
from starthinker.util.data import put_rows


# loop all parameters and replace with values, for lists turn them into strings
def query_parameters(query, parameters):
  while '[PARAMETER]' in query:
    parameter = parameters.pop(0)
    if isinstance(parameter, list) or isinstance(parameter, tuple): parameter = ', '.join([str(p) for p in parameter])
    query = query.replace('[PARAMETER]', parameter, 1)
  if project.verbose: print 'QUERY:', query
  return query


def bigquery():


  if 'query' in project.task['from']:
    if 'table' in project.task['to']:
      if project.verbose: print "QUERY TO TABLE", project.task['to']['table']

      if 'pre_process_query' in project.task['to']:
        print 'executing statement'
        execute_statement(
            project.task['auth'],
            project.id,
            project.task['to']['dataset'],
            project.task['to']['pre_process_query'],
            use_legacy_sql=project.task['from'].get('legacy', project.task['from'].get('useLegacySql', True))
        )
      query_to_table(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        project.task['to']['table'],
        query_parameters(project.task['from']['query'], project.task['from'].get('parameters')),
        disposition = project.task['write_disposition'] if 'write_disposition' in project.task else 'WRITE_TRUNCATE',
        legacy=project.task['from'].get('legacy', project.task['from'].get('useLegacySql', True)), # DEPRECATED: useLegacySql,
        target_project_id=project.task['to'].get('project_id', project.id)
      )
    # NOT USED SO RIPPING IT OUT
    # Mauriciod: Yes, it is used, look at project/mauriciod/target_winrate.json
    elif 'storage' in project.task['to']:
      if project.verbose: print "QUERY TO STORAGE", project.task['to']['storage']
      local_file_name = '/tmp/%s' % str(uuid.uuid1())
      rows = query_to_rows(project.task['auth'], project.id, project.task['from']['dataset'], project.task['from']['query'])

      f = open(local_file_name, 'wb')
      writer = csv.writer(f)
      writer.writerows(rows)
      f.close()

      f = open(local_file_name, 'rb')
      object_put(project.task['auth'], project.task['to']['storage'], f)
      f.close()

      os.remove(local_file_name)
    elif 'trix' in project.task['to']:
      if project.verbose: print "QUERY TO SHEET", project.task['to']['trix']
      rows = query_to_rows(project.task['auth'], project.id, project.task['from']['dataset'], project.task['from']['query'], legacy=project.task['from'].get('legacy', True))

      # makes sure types are correct in sheet
      rows = rows_to_type(rows)

      sheets_clear(project.task['auth'], project.task['to']['trix'], project.task['to']['range'].split('!')[0], project.task['to']['range'].split('!')[1])
      sheets_write(project.task['auth'], project.task['to']['trix'], project.task['to']['range'].split('!')[0], project.task['to']['range'].split('!')[1], rows)
    elif 'sftp' in project.task['to']:
      rows = query_to_rows(project.task['auth'], project.id, project.task['from']['dataset'], project.task['from']['query'], legacy=project.task['from'].get('use_legacy_sql', True))

      if rows:
        if project.verbose: print "QUERY TO SFTP"
        put_rows(project.task['auth'], project.task['to'], '', rows)
    else:
      if project.verbose: print "QUERY TO VIEW", project.task['to']['view']
      query_to_view(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        project.task['to']['view'],
        query_parameters(project.task['from']['query'], project.task['from'].get('parameters')),
        project.task['from'].get('legacy', project.task['from'].get('useLegacySql', True)) # DEPRECATED: useLegacySql
      )
  else:
    if project.verbose: print "STORAGE TO TABLE", project.task['to']['table']
    storage_to_table(
      project.task['auth'],
      project.id,
      project.task['to']['dataset'],
      project.task['to']['table'],
      project.task['from']['bucket'] + ':' + project.task['from']['path'],
      project.task.get('schema', []),
      project.task.get('skip_rows', 1),
      project.task.get('structure', 'CSV'),
      project.task.get('disposition', 'WRITE_TRUNCATE')
    )

if __name__ == "__main__":
  project.load('bigquery')
  bigquery()
