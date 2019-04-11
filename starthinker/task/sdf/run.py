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


from starthinker.util.project import project 
from starthinker.util.dbm import sdf_read
from starthinker.util.bigquery import create_table_if_not_exist, query_to_table, drop_table
from starthinker.task.sdf.schema.Lookup import SDF_Field_Lookup
from starthinker.util.csv import column_header_sanitize, csv_to_rows
from starthinker.util.data import put_rows, get_rows

API_VERSION = 'v1'
FILTER_ID_CHUNK_SIZE = 5


@project.from_parameters
def sdf():
  if project.verbose: print "SDF TO TABLE", project.task['out']['bigquery']['table']
  
  # Set is time partition and write disposition
  is_time_partition = project.task['out']['bigquery'].get('is_time_partition', False)
  disposition = 'WRITE_TRUNCATE'
  if is_time_partition:
    disposition = 'WRITE_APPEND'

  # Read Filter Ids
  filter_id_rows = list(get_rows(project.task['auth'], project.task['read']['filter_ids']))
  filter_ids = [filter_id_rows[i:i + FILTER_ID_CHUNK_SIZE] for i in xrange(0, len(filter_id_rows), FILTER_ID_CHUNK_SIZE)]
  # Loop through requested file types
  for file_type in project.task['file_types']:
    current_filter_id_iteration = 0
    i = 0
    table_names = []

    # Create the destination table
    destination_table = '%s_%s' % (project.task['out']['bigquery']['table'], file_type.lower())
    create_table_if_not_exist(
      project.task['auth'],
      project.id,
      project.task['out']['bigquery']['dataset'],
      destination_table,
      is_time_partition)

    # Request 5 filter ids at a time so the API doesn't timeout
    for partial_filter_ids in filter_ids:
      rows = sdf_read(project.task['auth'], [file_type], project.task['filter_type'], partial_filter_ids)

      if rows:
        schema = _sdf_schema(rows.next())
        table_suffix = '%s_%s' % (current_filter_id_iteration, file_type.lower())
        table_name = '%s%s' % (project.task['out']['bigquery']['table'], table_suffix)
        filename = '%s_%s.csv' % (file_type, project.date)
        # Check to see if the table exists, if not create it
        create_table_if_not_exist(
          project.task['auth'],
          project.id,
          project.task['out']['bigquery']['dataset'],
          table_name)

        if 'bigquery' in project.task['out']:
          project.task['out']['bigquery']['schema'] = schema
          project.task['out']['bigquery']['skip_rows'] = 0

        put_rows(project.task['auth'], 
          project.task['out'], 
          filename, 
          rows, 
          variant=table_suffix)

        table_names.append(table_name)

      current_filter_id_iteration= current_filter_id_iteration + 1

    query = _construct_combine_query(
      file_type,
      table_names,
      project.id,
      project.task['out']['bigquery']['dataset'],
      destination_table)

    query_to_table(project.task['auth'], 
      project.id, 
      project.task['out']['bigquery']['dataset'], 
      destination_table, 
      query, 
      disposition=disposition,
      legacy=False)

    # Delete all the temporary tables that were created
    for table_name in table_names:
      drop_table(project.task['auth'], 
        project.id, 
        project.task['out']['bigquery']['dataset'], 
        table_name)


def _construct_combine_query(file_type, table_names, project_id, dataset, dest_table_name):
  query = 'SELECT * FROM ('

  for i,table in enumerate(table_names):
    sub_table_path = '`%s.%s.%s` ' % (project_id, dataset, table)
    sub_query = 'SELECT * FROM ' + sub_table_path

    if i != (len(table_names)-1):
      sub_query = sub_query + 'UNION ALL '

    query = query + sub_query

  query = query + ')'

  return query


def _sdf_schema(header):
  schema = []

  for h in header:
    schema.append({ 
      'name':column_header_sanitize(h), 
      'type':SDF_Field_Lookup.get(h, 'STRING'), 
      'mode':'NULLABLE' 
    }) 

  return schema 


if __name__ == "__main__":
  sdf()
