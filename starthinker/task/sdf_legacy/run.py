###########################################################################
# 
#  Copyright 2018 Google LLC
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
from starthinker.util.dbm import sdf_read
from starthinker.util.bigquery import query_to_table
from starthinker.util.sdf import sdf_schema
from starthinker.util.sdf.schema.Lookup import SDF_Field_Lookup
from starthinker.util.csv import column_header_sanitize
from starthinker.util.data import put_rows, get_rows


@project.from_parameters
def sdf_legacy():
  if project.verbose: print('SDF')
  
  # Read Filter Ids
  filter_ids = list(get_rows(project.task['auth'], project.task['read']['filter_ids']))

  # Loop through requested file types
  for file_type in project.task['file_types']:
    disposition = 'WRITE_TRUNCATE'

    # if daily then create a seperate table for each day else accumulate all in one table
    table = ('SDF_%s_%s' % (file_type, str(project.date).replace('-', '_'))) if project.task['daily'] else ('SDF_%s' % file_type)

    # do one filter id at a time to avoid response too large error ( product knows )
    for filter_id in filter_ids:

      if project.verbose: print("SDF DOWNLOAD", project.task['filter_type'], file_type, filter_id)
      rows = sdf_read(project.task['auth'], [file_type], project.task['filter_type'], [filter_id], project.task.get('version', '5'))

      if rows:
        schema = sdf_schema(next(rows))
        if 'bigquery' in project.task['out']:
          project.task['out']['bigquery']['schema'] = schema
          project.task['out']['bigquery']['skip_rows'] = 0
          project.task['out']['bigquery']['table'] = table

        put_rows(project.task['auth'], project.task['out'], rows)

      else:
        if project.verbose: print("NO DATA")

    disposition = 'WRITE_APPEND'

    if project.task['daily']:

      if project.verbose: print("SDF COMBINE DAYS", file_type)
      # Load data into BigQuery
      query_to_table(project.task['auth'], 
        project.id, 
        project.task['out']['bigquery']['dataset'], 
        'SDF_%s' % file_type,
        "SELECT PARSE_DATE('%%Y_%%m_%%d',_TABLE_SUFFIX) as SDF_Day, * FROM `%s.%s.SDF_%s_*`" % (project.id, project.task['out']['bigquery']['dataset'], file_type), 
        disposition='WRITE_TRUNCATE',
        legacy=False
      )


if __name__ == "__main__":
  sdf_legacy()
