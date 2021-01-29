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
from starthinker.util.project import project
from starthinker.util.sheets import sheets_clear

SCHEMA_PREVIEW = [
  { 'name': 'Operation', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Layer', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Partner', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Advertiser', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Line_Item', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Parameters', 'type': 'STRING', 'mode': 'NULLABLE' },
]

SCHEMA_LOG = [
  { 'name': 'Layer', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Partner', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Advertiser', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Line_Item', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Parameters', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Status', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Error', 'type': 'STRING', 'mode': 'NULLABLE' },
]

BUFFER_ERROR = []
BUFFER_SUCCESS = []
BUFFER_LENGTH = 10


def edit_clear():

  table_create(
    project.task['auth_bigquery'],
    project.id,
    project.task['dataset'],
    'EDIT_Preview',
    SCHEMA_PREVIEW
  )

  table_create(project.task['auth_bigquery'],
    project.id,
    project.task['dataset'],
    'EDIT_Log',
    SCHEMA_LOG
  )

  sheets_clear(project.task['auth_sheets'],
    project.task['sheet'],
    'Preview',
    'A2:Z'
  )

  sheets_clear(project.task['auth_sheets'],
    project.task['sheet'],
    'Error',
    'A2:Z'
  )

  sheets_clear(project.task['auth_sheets'],
    project.task['sheet'],
    'Success',
    'A2:Z'
  )


def edit_log(edit=None):
  global BUFFER_SUCCESS
  global BUFFER_ERROR

  def _edit_write(rows, kind):
    if not rows:
      return

    rows = [(
      p['layer'],
      p.get('partner'),
      p.get('advertiser'),
      p.get('line_item'),
      json.dumps(p.get('parameters', {}), indent=2),
      kind,
      p[kind.lower()
    ]) for p in rows]

    put_rows(
      project.task['auth_bigquery'],
      { 'bigquery': {
        'dataset': project.task['dataset'],
        'table': 'EDIT_Log',
        'schema': SCHEMA_LOG,
        'disposition': 'WRITE_APPEND',
        'format': 'CSV'
      }},
      rows
    )

    put_rows(
      project.task['auth_sheets'],
      { 'sheets': {
        'sheet': project.task['sheet'],
        'tab': kind.title(),
        'range': 'A2',
        'append': True
      }},
      rows
    )

  if edit and 'success' in edit:
    BUFFER_SUCCESS.append(edit)
    print('SUCCESS:', edit['success'])
  elif edit and 'error' in edit:
    BUFFER_ERROR.append(edit)
    print('ERROR:', edit['error'])

  if len(BUFFER_SUCCESS) > BUFFER_LENGTH or edit is None:
    _edit_write(BUFFER_SUCCESS, 'SUCCESS')
    BUFFER_SUCCESS = []

  if len(BUFFER_ERROR) > BUFFER_LENGTH or edit is None:
    _edit_write(BUFFER_ERROR, 'ERROR')
    BUFFER_ERROR = []


def edit_preview(edits):
  if edits:
    rows = [(
      p['layer'],
      p.get('partner'),
      p.get('advertiser'),
      p.get('line_item'),
      json.dumps(p.get('parameters', {}), indent=2)
    ) for p in edits]

    put_rows(
      project.task['auth_bigquery'],
      { 'bigquery': {
        'dataset': project.task['dataset'],
        'table': 'EDIT_Preview',
        'schema': SCHEMA_PREVIEW,
        'disposition': 'WRITE_APPEND',
        'format': 'CSV'
        }
      },
      rows
    )

    put_rows(
      project.task['auth_sheets'],
      { 'sheets': {
        'sheet': project.task['sheet'],
        'tab': 'Preview',
        'range': 'A2',
      }},
      rows
    )
