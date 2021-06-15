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


def patch_clear(config, task):

  table_create(config, task['auth_bigquery'], config.project,
               task['dataset'], 'PATCH_Preview', SCHEMA_PREVIEW)

  table_create(config, task['auth_bigquery'], config.project,
               task['dataset'], 'PATCH_Log', SCHEMA_LOG)

  sheets_clear(config, task['auth_sheets'], task['sheet'], 'Preview', 'A2:Z')

  sheets_clear(config, task['auth_sheets'], task['sheet'], 'Error', 'A2:Z')

  sheets_clear(config, task['auth_sheets'], task['sheet'], 'Success', 'A2:Z')


def patch_mask(patch:dict) -> dict:
  """Adds an update mask to a patch based on keys in patch.

  Operates under assumption that all fields prsent in update will be updated.
  Immediately wraps a nested function to perform actual patch logic using generator.

  Args:
    patch: {
      "operation": IGNORED,
      "action": IGNORED,
      "partner": IGNORED,
      "advertiser": IGNORED,
      "campaign": IGNORED,
      "parameters": {
        "body": { PATCH IS CONSTRUCTED FROM THIS }
      }
    }

  Returns:
    Patch with ['parameters']['updateMask'] added.

  """

  def _patch_mask(body:dict) -> list:
    """Loop through dictionary defining API body and create patch mask on keys.

    Each patch mask has format parent.child repreated. Each leaf has a full path
    describing the patch. Exceptions are budgetSegments, and partnerCosts which
    are lists with an order and changed at the parent level not the leaves.

    Args:
      body: Any REST API call dictionary, defined by API endpoint.

    Returns:
      A list of strings representing full path to each leaf key.

    """

    mask = set()
    if isinstance(body, dict):
      for parent, value in body.items():
        children = _patch_mask(value)
        if children and parent not in ('budgetSegments', 'partnerCosts'):
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


def patch_masks(patches:dict) -> None:
  """Wraps patch mask function for list of patches.

  Modifies in place. Executes patch_mask for multiple patches.

  Args:
    patches: A list of patch objects to annotate.

  """

  for patch in patches:
    patch_mask(patch)


def patch_log(config, task, patch=None):
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
        config,
        task['auth_bigquery'], {
            'bigquery': {
                'dataset': task['dataset'],
                'table': 'PATCH_Log',
                'schema': SCHEMA_LOG,
                'disposition': 'WRITE_APPEND',
                'format': 'CSV'
            }
        }, rows)

    put_rows(
        config,
        task['auth_sheets'], {
            'sheets': {
                'sheet': task['sheet'],
                'tab': kind.title(),
                'header':False,
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


def patch_preview(config, task, patches):
  if patches:
    rows = [(p['operation'], p['action'], p.get('partner'), p.get('advertiser'),
             p.get('campaign'), p.get('insertion_order'), p.get('line_item'),
             json.dumps(p.get('parameters', {}), indent=2)) for p in patches]

    put_rows(
        config,
        task['auth_bigquery'], {
            'bigquery': {
                'dataset': task['dataset'],
                'table': 'PATCH_Preview',
                'schema': SCHEMA_PREVIEW,
                'disposition': 'WRITE_APPEND',
                'format': 'CSV'
            }
        }, rows)

    put_rows(
        config,
        task['auth_sheets'], {
            'sheets': {
                'sheet': task['sheet'],
                'tab': 'Preview',
                'header':False,
                'range': 'A2',
            }
        }, rows)
