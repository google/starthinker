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

""" Recipe handler for "conversion_upload" task.

Reads a source and performs a conversion upload into CM360.
Leverages get_rows and put_rows JSON pattern for IO. See docs.
For sample use see scripts/cm360_conversion_upload_from_*.json.
"""


from starthinker.util.cm import conversions_upload
from starthinker.util.data import get_rows


def conversion_upload(config, task):
  """Entry point for conversion_upload task, which uploads conversins to CM360.

  Prints sucess or failure to STDOUT.
  Currently only does batchInsert, not batchUpdate.
  """

  rows = get_rows(
    config,
    task['auth'],
    task['from'],
    as_object=False
  )

  if config.verbose:
    print('CONVERSION UPLOAD')

  statuses = conversions_upload(
    config,
    task['auth'],
    task['account_id'],
    task['activity_id'],
    task['conversion_type'], rows,
    task['encryptionInfo']
  )

  has_rows = False
  for status in statuses:
    has_rows = True
    if 'errors' in status:
      if config.verbose:
        print( 'ERROR:', status['conversion']['ordinal'], '\n'.join([e['message'] for e in status['errors']]))
    else:
      if config.verbose:
        print('OK:', status['conversion']['ordinal'])

  if not has_rows:
    if config.verbose:
      print('NO ROWS')
