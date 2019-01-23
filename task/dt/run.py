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

#import gzip
import zlib

from starthinker.util.project import project
from starthinker.util.bigquery import query_to_table, query_to_view, storage_to_table, query_to_rows, rows_to_table
from starthinker.util.storage import object_list, object_get_chunks
from starthinker.util.csv import column_header_sanitize, csv_to_rows
from starthinker.task.dt.schema.Lookup import DT_Field_Lookup


#HEADER_SIZE = 1024 * 10 # 10K should be enough for longest possible DT header


#def dt_header():
#  if project.verbose: print "DT HEADER",
#
#  # find first dt file to match pattern
#  path = '%s:%s' % (project.task['from']['bucket'], project.task['from']['path'])
#  sample_object = object_list(project.task['auth'], path, files_only=True).next()
#
#  # find first line of file ( gzip will decompress partial, and pull header out )
#  sample_data = object_get_chunks(project.task['auth'], sample_object, HEADER_SIZE).next()
#  with gzip.GzipFile(fileobj=sample_data, mode='rb') as fo: sample_header = fo.read(HEADER_SIZE).split('\n')[0]
#
#  if project.verbose: print sample_header
#  return sample_header.split(',')


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


def dt_csv():
  if project.verbose: print "DT ROWS",

  delimiter = '\n'
  first_file = True

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
      view += gz_handler.decompress(data_gz.read())

      # loop all rows in chunk, strip and send for processing
      end = view.find(delimiter)
      while end > -1:
        # send first row of only first file to avoid headers mid row stream, ( row sent as string )
        if first_file or not first_row:
          yield view[:end] 

        first_row = False 
        view = view[end + 1:]
        end = view.find(delimiter)

    first_file = False


def dt():
  if project.verbose: print "DT TO TABLE", project.task['to']['table']

  # get iterator of each row as a string
  csv = dt_csv()

  # convert each rows string into row list
  rows = csv_to_rows(csv)

  # detect schema based on first row
  schema = dt_schema(rows.next())

  # write to BigQuery, appending and chunking is automatically handled by BUFFER_SCALE
  rows_to_table(
    project.task['auth'],
    project.id,
    project.task['to']['dataset'],
    project.task['to']['table'],
    rows,
    schema,
    0,
    'WRITE_TRUNCATE'
  )


# BigQuery Storage Connector is subject to max file size limits, failing for many DT files ( replaced with above streaming code )
#def dt():
#  if project.verbose: print "DT TO TABLE", project.task['to']['table']
#
#  storage_to_table(
#    project.task['auth'],
#    project.id,
#    project.task['to']['dataset'],
#    project.task['to']['table'],
#    '%s:%s*' % (project.task['from']['bucket'], project.task['from']['path']), # append * to match all files with prefix
#    dt_schema(dt_header()), # fetch schema from first dt file
#    1,
#    'CSV',
#    'WRITE_TRUNCATE'
#  )


if __name__ == "__main__":
  project.load('dt')
  dt()
