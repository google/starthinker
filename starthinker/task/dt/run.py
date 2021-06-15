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


def dt_header(config, task, dt_file):
  if config.verbose:
    print('DT HEADER')

  # find first dt file to match pattern
  path = '%s:%s' % (task['bucket'], dt_file)

  # find first line of file ( gzip will decompress partial, and pull header out )
  sample_data = next(object_get_chunks(config, task['auth'], path, HEADER_SIZE))
  with gzip.GzipFile(fileobj=BytesIO(sample_data), mode='rb') as fo:
    sample_header = fo.read(HEADER_SIZE).decode('utf-8').split('\n')[0]

  return sample_header.split(',')


def dt_timestamp(config, task, dt_filepath):
  dt_time = None

  parts = RE_DT_TIME.match(dt_filepath)

  if parts:
    dt_time = parts.groups()[0]
    if len(dt_time) == 10:
      dt_time = config.timezone.localize(
          datetime.strptime(dt_time, '%Y%m%d%H'))
    else:
      dt_time = config.timezone.localize(datetime.strptime(dt_time, '%Y%m%d'))

  return dt_time


def dt_move_large(config, task, dt_file, dt_partition, jobs):
  if config.verbose:
    print('DT TO TABLE LARGE', dt_partition)

  delimiter = '\n'
  disposition = 'WRITE_TRUNCATE'

  # decompression handler for gzip ( must be outside of chunks as it keeps track of stream across multiple calls )
  gz_handler = zlib.decompressobj(32 + zlib.MAX_WBITS)

  # sliding view of data flowing out of decompression, used to buffer and delimit rows
  first_row = True
  view = ''

  # loop all chunks of file, decompress, and find row delimiter
  for data_gz in object_get_chunks(config, task['auth'],
                                   '%s:%s' % (task['bucket'], dt_file)):

    view += gz_handler.decompress(data_gz).decode('utf-8')

    if first_row:
      end = view.find(delimiter)
      schema = dt_schema(view[:end].split(','))
      view = view[(end + 1):]
      first_row = False

    end = view.rfind(delimiter)

    jobs.append(
        io_to_table(config, task['auth'], config.project,
                    task['to']['dataset'], dt_partition,
                    BytesIO(view[:end].encode()), 'CSV', schema, 0, disposition,
                    False))
    disposition = 'WRITE_APPEND'
    view = view[min(end + 1, len(view)):]


def dt_move_small(config, task, dt_file, dt_partition, jobs):
  if config.verbose:
    print('DT TO TABLE SMALL', dt_partition)

  jobs.append(
      storage_to_table(config, task['auth'], config.project,
                       task['to']['dataset'], dt_partition,
                       '%s:%s*' % (task['bucket'], dt_file),
                       dt_schema(dt_header(config, task, dt_file)), 1, 'CSV',
                       'WRITE_TRUNCATE', False))


def dt_move(config, task, dt_object, dt_partition, jobs):
  """ Due to BQ limit, files over 5 GB need to be transfered using inline decompression ( slower but works 100% of the time )"""
  if int(dt_object['size']) > 5000000:
    dt_move_large(config, task, dt_object['name'], dt_partition, jobs)
  else:
    dt_move_small(config, task, dt_object['name'], dt_partition, jobs)


def dt(config, task):
  jobs = []

  if config.verbose:
    print('DT To BigQuery')

  # legacy deprecated ( do not use )
  if 'path' in task:
    task['paths'] = [task['path']]

  # loop all dt files to match pattern or match any pattern
  print('PATHS', task['paths'])

  for path in (task['paths'] or ['']):

    for dt_object in object_list(
        config, task['auth'],
        '%s:%s' % (task['bucket'], path),
        raw=True):
      dt_size = dt_object['size']
      dt_file = dt_object['name']
      dt_time = dt_timestamp(config, task, dt_file)

      dt_partition = dt_file.split('.', 1)[0]
      if ((task.get('days') is None and
           task.get('hours') is None) or
          (dt_time > config.now - timedelta(
              days=task.get('days', 60),
              hours=task.get('hours', 0)))):
        if not table_exists(config, task['to']['auth'], config.project,
                            task['to']['dataset'], dt_partition):
          dt_move(config, task, dt_object, dt_partition, jobs)
        else:
          if config.verbose:
            print('DT Partition Exists:', dt_partition)

  for count, job in enumerate(jobs):
    print('Waiting For Job: %d of %d' % (count + 1, len(jobs)))
    job_wait(config, task['to']['auth'], job)
