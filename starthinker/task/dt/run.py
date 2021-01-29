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

import re
import zlib
import gzip
from io import BytesIO
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError

from starthinker.util.project import project
from starthinker.util.bigquery import io_to_table, storage_to_table, table_exists, job_wait
from starthinker.util.storage import object_list, object_get_chunks
from starthinker.util.csv import column_header_sanitize
from starthinker.task.dt.schema.Lookup import DT_Field_Lookup

HEADER_SIZE = 1024 * 10  # 10K should be enough for longest possible DT header
RE_DT_TIME = re.compile(r'.+?_(\d+)_\d+_\d+_\d+\.csv\.gz')


def dt_schema(header):
  schema = []
  for h in header:
    h = column_header_sanitize(h)
    schema.append({
        'name': h,
        'type': DT_Field_Lookup.get(h, 'STRING'),
        'mode': 'NULLABLE'
    })
  return schema


def dt_header(dt_file):
  if project.verbose:
    print('DT HEADER')

  # find first dt file to match pattern
  path = '%s:%s' % (project.task['bucket'], dt_file)

  # find first line of file ( gzip will decompress partial, and pull header out )
  sample_data = next(object_get_chunks(project.task['auth'], path, HEADER_SIZE))
  with gzip.GzipFile(fileobj=BytesIO(sample_data), mode='rb') as fo:
    sample_header = fo.read(HEADER_SIZE).decode('utf-8').split('\n')[0]

  return sample_header.split(',')


def dt_timestamp(dt_filepath):
  dt_time = None

  parts = RE_DT_TIME.match(dt_filepath)

  if parts:
    dt_time = parts.groups()[0]
    if len(dt_time) == 10:
      dt_time = project.timezone.localize(
          datetime.strptime(dt_time, '%Y%m%d%H'))
    else:
      dt_time = project.timezone.localize(datetime.strptime(dt_time, '%Y%m%d'))

  return dt_time


def dt_move_large(dt_file, dt_partition, jobs):
  if project.verbose:
    print('DT TO TABLE LARGE', dt_partition)

  delimiter = '\n'
  disposition = 'WRITE_TRUNCATE'

  # decompression handler for gzip ( must be outside of chunks as it keeps track of stream across multiple calls )
  gz_handler = zlib.decompressobj(32 + zlib.MAX_WBITS)

  # sliding view of data flowing out of decompression, used to buffer and delimit rows
  first_row = True
  view = ''

  # loop all chunks of file, decompress, and find row delimiter
  for data_gz in object_get_chunks(project.task['auth'],
                                   '%s:%s' % (project.task['bucket'], dt_file)):

    view += gz_handler.decompress(data_gz.read()).decode('utf-8')

    if first_row:
      end = view.find(delimiter)
      schema = dt_schema(view[:end].split(','))
      view = view[(end + 1):]
      first_row = False

    end = view.rfind(delimiter)

    jobs.append(
        io_to_table(project.task['auth'], project.id,
                    project.task['to']['dataset'], dt_partition,
                    BytesIO(view[:end].encode()), 'CSV', schema, 0, disposition,
                    False))
    disposition = 'WRITE_APPEND'
    view = view[min(end + 1, len(view)):]


def dt_move_small(dt_file, dt_partition, jobs):
  if project.verbose:
    print('DT TO TABLE SMALL', dt_partition)

  jobs.append(
      storage_to_table(project.task['auth'], project.id,
                       project.task['to']['dataset'], dt_partition,
                       '%s:%s*' % (project.task['bucket'], dt_file),
                       dt_schema(dt_header(dt_file)), 1, 'CSV',
                       'WRITE_TRUNCATE', False))


def dt_move(dt_object, dt_partition, jobs):
  """ Due to BQ limit, files over 5 GB need to be transfered using inline decompression ( slower but works 100% of the time )"""
  if int(dt_object['size']) > 5000000:
    dt_move_large(dt_object['name'], dt_partition, jobs)
  else:
    dt_move_small(dt_object['name'], dt_partition, jobs)


@project.from_parameters
def dt():
  jobs = []

  if project.verbose:
    print('DT To BigQuery')

  # legacy deprecated ( do not use )
  if 'path' in project.task:
    project.task['paths'] = [project.task['path']]

  # loop all dt files to match pattern or match any pattern
  print('PATHS', project.task['paths'])

  for path in (project.task['paths'] or ['']):

    print(path)
    for dt_object in object_list(
        project.task['auth'],
        '%s:%s' % (project.task['bucket'], path),
        raw=True):
      dt_size = dt_object['size']
      dt_file = dt_object['name']
      dt_time = dt_timestamp(dt_file)

      dt_partition = dt_file.split('.', 1)[0]
      if ((project.task.get('days') is None and
           project.task.get('hours') is None) or
          (dt_time > project.now - timedelta(
              days=project.task.get('days', 60),
              hours=project.task.get('hours', 0)))):
        if not table_exists(project.task['to']['auth'], project.id,
                            project.task['to']['dataset'], dt_partition):
          dt_move(dt_object, dt_partition, jobs)
        else:
          if project.verbose:
            print('DT Partition Exists:', dt_partition)

  for count, job in enumerate(jobs):
    print('Waiting For Job: %d of %d' % (count + 1, len(jobs)))
    job_wait(project.task['to']['auth'], job)


if __name__ == '__main__':
  dt()
