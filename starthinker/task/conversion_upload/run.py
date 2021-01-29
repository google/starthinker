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

import io

from starthinker.util.project import project
from starthinker.util.dcm import conversions_upload
from starthinker.util.bigquery import query_to_rows
from starthinker.util.sheets import sheets_read
from starthinker.util.csv import csv_to_rows

# Possible CSV headers to ignore
CSV_HEADERS = ['user_id', 'encrypted_user_id']


def conversions_download():
  if project.verbose:
    print('CONVERSION DOWNLOAD')

  # pull from bigquery if specified
  if 'bigquery' in project.task:
    if project.verbose:
      print('READING BIGQUERY')
    rows = query_to_rows(
        project.task['auth'],
        project.id,
        project.task['bigquery']['dataset'],
        'SELECT * FROM %s' % project.task['bigquery']['table'],
        legacy=project.task['bigquery'].get('legacy', True))
    for row in rows:
      yield row

  # pull from sheets if specified
  if 'sheets' in project.task:
    if project.verbose:
      print('READING SHEET')
    rows = sheets_read(project.task['auth'], project.task['sheets']['url'],
                       project.task['sheets']['tab'],
                       project.task['sheets']['range'])
    for row in rows:
      yield row

  # pull from csv if specified
  if 'csv' in project.task:
    if project.verbose:
      print('READING CSV FILE')
    with io.open(project.task['csv']['file']) as f:
      for row in csv_to_rows(f):
        if row[0] not in CSV_HEADERS:
          yield row


@project.from_parameters
def conversion_upload():

  rows = conversions_download()

  if project.verbose:
    print('CONVERSION UPLOAD')

  statuses = conversions_upload(project.task['auth'],
                                project.task['account_id'],
                                project.task['activity_id'],
                                project.task['conversion_type'], rows,
                                project.task['encryptionInfo'])

  has_rows = False
  for status in statuses:
    has_rows = True
    if 'errors' in status:
      if project.verbose:
        print('ERROR:', status['conversion']['ordinal'],
              '\n'.join([e['message'] for e in status['errors']]))
    else:
      if project.verbose:
        print('OK:', status['conversion']['ordinal'])

  if not has_rows:
    if project.verbose:
      print('NO ROWS')


if __name__ == '__main__':
  conversion_upload()
