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

# BigQuery Storage Connector is subject to max file size limits, failing for many DT files ( avoiding BQ to storage connector ).

import zlib
from io import StringIO

from starthinker.util.project import project
from starthinker.util.bigquery import io_to_table
from starthinker.util.storage import object_list, object_get_chunks
from starthinker.util.csv import column_header_sanitize
from starthinker.task.dt.schema.Lookup import DT_Field_Lookup


def dt_schema(header):
  schema = []
  for h in header:
    h = column_header_sanitize(h)
    schema.append({ 
      'name':h, 
      'type':DT_Field_Lookup.get(h, 'STRING'), 
      'mode':'NULLABLE' 
    }) 
  return schema


@project.from_parameters
def dt():
  if project.verbose: print("DT TO TABLE", project.task['to']['table'])

  delimiter = '\n'
  disposition = 'WRITE_TRUNCATE'

  # loop all dt files to match pattern
  path = '%s:%s' % (project.task['from']['bucket'], project.task['from']['path'])
  for dt_file in object_list(project.task['auth'], path, files_only=True):

    # decompression handler for gzip ( must be outside of chunks as it keeps track of stream across multiple calls )
    gz_handler = zlib.decompressobj(32 + zlib.MAX_WBITS)

    # sliding view of data flowing out of decompression, used to buffer and delimit rows
    first_row = True
    view = ''

    # loop all chunks of file, decompress, and find row delimiter
    for data_gz in object_get_chunks(project.task['auth'], dt_file):

      view += gz_handler.decompress(data_gz.read()).decode()

      if first_row:
        end = view.find(delimiter)
        schema = dt_schema(view[:end].split(','))
        view = view[(end + 1):]
        first_row = False

      end = view.rfind(delimiter)

      io_to_table(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        project.task['to']['table'],
        StringIO(view[:end]),
        'CSV',
        schema,
        0,
        disposition,
        False
      )
      disposition = 'WRITE_APPEND'
      view = view[min(end + 1, len(view)):]


if __name__ == "__main__":
  dt()
