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
from util.storage import parse_path, makedirs_safe, object_put, bucket_create
from util.bigquery import query_to_rows, rows_to_table
from util.sheets import sheets_read, sheets_write, sheets_clear
from util.csv import rows_to_csv


def get_rows(auth, source):

  if 'values' in source:
    for value in source['values']:
      yield value if source.get('single_cell', False) else [value]

  if 'sheet' in source:
    rows = sheets_read(project.task['auth'], source['sheet']['url'], source['sheet']['tab'], source['sheet']['range'])
    for row in rows:
      yield row[0] if source.get('single_cell', False) else row

  if 'bigquery' in source:
    rows = query_to_rows(
      source['bigquery'].get('auth', auth),
      project.id,
      source['bigquery']['dataset'],
      source['bigquery']['query'],
      legacy=source['bigquery'].get('legacy', False)
    )
    for row in rows:
      yield row[0] if source.get('single_cell', False) else row


def put_rows(auth, target, filename, rows):

  if 'bigquery' in target:
    rows_to_table(
      target['bigquery'].get('auth', auth),
      project.id,
      target['bigquery']['dataset'],
      target['bigquery']['table'],
      rows,
      schema=target['bigquery'].get('schema', []),
      skip_rows=target['bigquery'].get('skip_rows', 1),
      structure='CSV',
      disposition=target['bigquery'].get('disposition', 'WRITE_TRUNCATE'),
      destination_project_id=target['bigquery'].get('project_id', None),
    )

  if 'sheets' in target:
    if target['sheets'].get('delete', False): sheets_clear(auth, target['sheets']['sheet'], target['sheets']['tab'], target['sheets']['range'])
    sheets_write(auth, target['sheets']['sheet'], target['sheets']['tab'], target['sheets']['range'], rows) 

  if 'directory' in target:
    file_out = target['directory'] + filename
    if project.verbose: print 'SAVING', file_out
    makedirs_safe(parse_path(file_out))
    with open(file_out, 'wb') as save_file:
      save_file.write(rows_to_csv(rows).read())

  if 'storage' in target and target['storage'].get('bucket') and target['storage'].get('path'):
    # create the bucket
    bucket_create(auth, project.id, target['storage']['bucket'])

    # put the file
    file_out = target['storage']['bucket'] + ':' + target['storage']['path'] + filename
    if project.verbose: print 'SAVING', file_out
    object_put(auth, file_out, rows_to_csv(rows))

  if 'trix' in target:
    trix_update(auth, target['trix']['sheet_id'], target['trix']['sheet_range'], rows_to_csv(rows), target['trix']['clear'])

  if 'email' in target:
    pass
