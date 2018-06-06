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

import gzip

from util.project import project
from util.bigquery import query_to_table, query_to_view, storage_to_table, query_to_rows
from util.storage import object_list, object_get_chunks
from util.csv import column_header_sanitize

from dt.schema.Lookup import DT_Field_Lookup

HEADER_SIZE = 1024 * 10 # 10K should be enough for longest possible DT header

def dt_header():
  if project.verbose: print "DT HEADER",

  # find first dt file to match pattern
  path = '%s:%s' % (project.task['from']['bucket'], project.task['from']['path'])
  sample_object = object_list(project.task['auth'], path, files_only=True).next()

  # find first line of file ( gzip will decompress partial, and pull header out )
  sample_data = object_get_chunks(project.task['auth'], sample_object, HEADER_SIZE).next()
  with gzip.GzipFile(fileobj=sample_data, mode='rb') as fo: sample_header = fo.read(HEADER_SIZE).split('\n')[0]

  if project.verbose: print sample_header
  return sample_header.split(',')


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


def dt():
  if project.verbose: print "DT TO TABLE", project.task['to']['table']

  storage_to_table(
    project.task['auth'],
    project.id,
    project.task['to']['dataset'],
    project.task['to']['table'],
    '%s:%s*' % (project.task['from']['bucket'], project.task['from']['path']), # append * to match all files with prefix
    dt_schema(dt_header()), # fetch schema from first dt file
    1,
    'CSV',
    'WRITE_TRUNCATE'
  )

if __name__ == "__main__":
  project.load('dt')
  dt()
