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

import json

from starthinker.util.bigquery import table_create
from starthinker.util.data import put_rows
from starthinker.util.sheets import sheets_clear


SCHEMA_LOG = [
  { 'name': 'Operation', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Advertiser', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Campaign', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Name', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Parameters', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Success', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Error', 'type': 'STRING', 'mode': 'NULLABLE' },
]

BUFFER_LOG = []
BUFFER_LENGTH = 10


def log_clear(config, task):

  table_create(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "INSERT_Log",
    SCHEMA_LOG
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Log',
    'A2:Z'
  )

def log_write(operation=None, parameters=None, success=None, error=None):
  global BUFFER_LOG

  if operation:
    BUFFER_LOG.append({
      'operation':operation,
      'parameters':parameters,
      'success':success,
      'error':error
    })

  if len(BUFFER_LOG) > 0 and (not operation or len(BUFFER_LOG) > BUFFER_LENGTH):
    rows = [(
      log['operation'],
      log['parameters']['body']['advertiserId'],
      log['parameters']['body']['campaignId'],
      log['parameters']['body']['displayName'],
      json.dumps(log['parameters'], indent=2),
      log['success'],
      log['error'],
    ) for log in BUFFER_LOG]

    put_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'table': 'INSERT_Log',
        'schema': SCHEMA_LOG,
        'disposition': 'WRITE_APPEND',
        'format': 'CSV'
      }},
      rows
    )

    put_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'Log',
        'header':False,
        'range': 'A2',
        'append': True
      }},
      rows
    )

    BUFFER_LOG = []
