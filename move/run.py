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

# PARAMETIZE QUERIES: https://cloud.google.com/bigquery/docs/parameterized-queries

import uuid
import os

from util.project import project
from util.bigquery import query_to_table, query_to_view, query_to_local_file, storage_to_table, query
from util.trix import trix_update
from util.storage import object_put

# loop all parameters and replace with values, for lists turn them into strings
def query_parameters(query, parameters):
  while '[PARAMETER]' in query:
    parameter = parameters.pop(0)
    if isinstance(parameter, list) or isinstance(parameter, tuple): parameter = ', '.join([str(p) for p in parameter])
    query = query.replace('[PARAMETER]', parameter, 1)
  if project.verbose: print 'QUERY:', query
  return query

def move():

  if 'query' in project.task['from']:
    if 'table' in project.task['to']:
      if project.verbose: print "QUERY TO TABLE", project.task['to']['table']
      query_to_table(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        project.task['to']['table'],
        query_parameters(project.task['from']['query'], project.task['from'].get('parameters')),
        disposition = project.task['write_disposition'] if 'write_disposition' in project.task else 'WRITE_TRUNCATE',
        use_legacy_sql=project.task['from']['useLegacySql'] if 'useLegacySql' in project.task['from'] else True
      )
    elif 'storage' in project.task['to']:
      temp_file_name = str(uuid.uuid1()) + '.csv'
      if project.verbose: print "QUERY TO STORAGE", project.task['to']['storage']
      query_to_local_file(
        project.task['auth'],
        project.task['from']['query'],
        temp_file_name,
        use_legacy_sql=project.task['from']['useLegacySql'] if 'useLegacySql' in project.task['from'] else True
      )
      object_put(project.task['auth'], project.task['to']['storage'], open(temp_file_name))
      os.remove(temp_file_name)
    elif 'trix' in project.task['to']:
      result = query(project.task['from']['query'])

      trix_update(
        project.task['auth'],
        project.task['to']['trix'],
        project.task['to']['range'],
        {'values': [line for line in [column for column in [row for row in result]]]},
        clear=True)
    else:
      if project.verbose: print "QUERY TO VIEW", project.task['to']['view']
      query_to_view(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        project.task['to']['view'],
        query_parameters(project.task['from']['query'], project.task['from'].get('parameters'))
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
  project.load('move')
  move()
