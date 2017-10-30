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
from util.trix import trix_read
from util.bigquery.file_processor import FileProcessor
from util.bigquery import local_file_to_table, datasets_create
import csv
import json
import uuid
import os

def trix():
  if project.verbose: print 'trix'

  processor = FileProcessor()

  auth = project.task['auth']
  trix_id = project.task['in']['id']
  trix_range = project.task['in']['range_a_notation']

  rows = trix_read(auth, trix_id, trix_range)['values']

  # if rows: put_files(project.task['auth'], project.task['out'], filename, data)
  # replace the below with the above
  if 'out' in project.task:
    if 'bigquery' in project.task['out']:
      if rows:
        dataset = project.task['out']['bigquery']['dataset']
        table_name = project.task['out']['bigquery']['table']
        replace = project.task['out']['bigquery']['replace']
        schema = processor.field_list_to_schema(rows[0])
        field_count = len(schema)
        temp_file_name = '/tmp/%s' % str(uuid.uuid1())
        f = open(temp_file_name, 'w')
        writer = csv.writer(f)
        datasets_create(auth, project.id, dataset)
        for row in rows[1:]:
          clean_row = [unicode(s).encode('utf-8') for s in row]
          while len(clean_row) < field_count:
            clean_row.append('')

          writer.writerow(clean_row)

        f.close()
        local_file_to_table(auth, dataset, table_name, schema, temp_file_name, replace=replace, file_type='CSV')
        os.remove(temp_file_name)


if __name__ == "__main__":
  project.load('trix')
  trix()
