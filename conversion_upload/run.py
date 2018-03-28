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
from util.dcm import conversions_upload
from util.bigquery import query_to_rows
from util.sheets import sheets_read

def conversion_upload():
  if project.verbose: print 'CONVERSION UPLOAD'

  rows = []

  # pull from bigquery if specified
  if project.task['bigquery']['dataset']:
    rows.extend(query_to_rows(
      project.task['auth'],
      project.id,
      project.task['bigquery']['dataset'],
      'SELECT * FROM %s' % project.task['bigquery']['table']
    ))

  # pull from sheets if specified
  if project.task['sheets']['url']:
    rows.extend(sheets_read(
      project.task['auth'], 
      project.task['sheets']['url'], 
      project.task['sheets']['tab'], 
      project.task['sheets']['range']
    ))

  # write to account
  if rows:
    if project.verbose: print 'WRITING ROWS', len(rows)
    conversions_upload(
      project.task['auth'], 
      project.task['account_id'], 
      project.task['activity_id'], 
      project.task['conversion_type'], 
      rows, 
      project.task['encryptionInfo']
    )
  else:
    if project.verbose: print 'NO ROWS'


if __name__ == "__main__":
  project.load('conversion_upload')
  conversion_upload()
