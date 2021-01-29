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

from starthinker.util.bigquery import query_to_view
from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.project import project
from starthinker.util.sheets import sheets_clear

SCHEMA_PREVIEW = [
    {
        'name': 'Operation',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Action',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Partner',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Advertiser',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Campaign',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Insertion_Order',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Line_Item',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Parameters',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
]

SCHEMA_LOG = [
    {
        'name': 'Operation',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Action',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Partner',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Advertiser',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Campaign',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Insertion_Order',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Line_Item',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Parameters',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Status',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    {
        'name': 'Error',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
]

BUFFER_ERROR = []
BUFFER_SUCCESS = []
BUFFER_LENGTH = 10


def patch_clear():

  table_create(project.task['auth_bigquery'], project.id,
               project.task['dataset'], 'PATCH_Preview', SCHEMA_PREVIEW)

  table_create(project.task['auth_bigquery'], project.id,
               project.task['dataset'], 'PATCH_Log', SCHEMA_LOG)

  sheets_clear(project.task['auth_sheets'], project.task['sheet'], 'Preview', 'A2:Z')

  sheets_clear(project.task['auth_sheets'], project.task['sheet'], 'Error', 'A2:Z')

  sheets_clear(project.task['auth_sheets'], project.task['sheet'], 'Success', 'A2:Z')


def patch_mask(patch):

  def _patch_mask(body):
    mask = set()
    if isinstance(body, dict):
      for parent, value in body.items():
        children = _patch_mask(value)
        if children:
          for child in children:
            mask.add(parent + '.' + child)
        else:
          mask.add(parent)
    elif isinstance(body, (list, tuple)):
      for value in body:
        mask.update(_patch_mask(value))
    return list(mask)

  mask = ','.join(_patch_mask(patch['parameters'].get('body')))
  if mask:
    patch['parameters']['updateMask'] = mask

  return patch


def patch_masks(patches):
  for patch in patches:
    patch_mask(patch)


def patch_log(patch=None):
  global BUFFER_SUCCESS
  global BUFFER_ERROR

  def _patch_write(rows, kind):
    if not rows:
      return

    rows = [(p['operation'], p['action'], p.get('partner'), p.get('advertiser'),
             p.get('campaign'), p.get('insertion_order'), p.get('line_item'),
             json.dumps(p.get('parameters', {}),
                        indent=2), kind, p[kind.lower()]) for p in rows]

    put_rows(
        project.task['auth_bigquery'], {
            'bigquery': {
                'dataset': project.task['dataset'],
                'table': 'PATCH_Log',
                'schema': SCHEMA_LOG,
                'disposition': 'WRITE_APPEND',
                'format': 'CSV'
            }
        }, rows)

    put_rows(
        project.task['auth_sheets'], {
            'sheets': {
                'sheet': project.task['sheet'],
                'tab': kind.title(),
                'range': 'A2',
                'append': True
            }
        }, rows)

  if patch and 'success' in patch:
    BUFFER_SUCCESS.append(patch)
    print('SUCCESS:', patch['success'])
  elif patch and 'error' in patch:
    BUFFER_ERROR.append(patch)
    print('ERROR:', patch['error'])

  if len(BUFFER_SUCCESS) > BUFFER_LENGTH or patch is None:
    _patch_write(BUFFER_SUCCESS, 'SUCCESS')
    BUFFER_SUCCESS = []

  if len(BUFFER_ERROR) > BUFFER_LENGTH or patch is None:
    _patch_write(BUFFER_ERROR, 'ERROR')
    BUFFER_ERROR = []


def patch_preview(patches):
  if patches:
    rows = [(p['operation'], p['action'], p.get('partner'), p.get('advertiser'),
             p.get('campaign'), p.get('insertion_order'), p.get('line_item'),
             json.dumps(p.get('parameters', {}), indent=2)) for p in patches]

    put_rows(
        project.task['auth_bigquery'], {
            'bigquery': {
                'dataset': project.task['dataset'],
                'table': 'PATCH_Preview',
                'schema': SCHEMA_PREVIEW,
                'disposition': 'WRITE_APPEND',
                'format': 'CSV'
            }
        }, rows)

    put_rows(
        project.task['auth_sheets'], {
            'sheets': {
                'sheet': project.task['sheet'],
                'tab': 'Preview',
                'range': 'A2',
            }
        }, rows)
