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

from starthinker.util.bigquery import query_to_view
from starthinker.util.csv import rows_pad
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.line_item import line_item_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def line_item_map_clear(config, task):
  sheets_clear(config, task['auth_sheets'], task['sheet'], 'Line Items Map',
               'A2:Z')


def line_item_map_load(config, task):
  pass


def line_item_map_audit(config, task):
  rows = get_rows(
      config,
      task['auth_sheets'], {
          'sheets': {
              'sheet': task['sheet'],
              'tab': 'Line Items Map',
              'header':False,
              'range': 'A2:Z'
          }
      })

  put_rows(
      config,
      task['auth_bigquery'], {
          'bigquery': {
              'dataset': task['dataset'],
              'table': 'SHEET_LineItemMaps',
              'schema': [{
                  'name': 'Action',
                  'type': 'STRING'
              }, {
                  'name': 'Line_Item',
                  'type': 'STRING'
              }, {
                  'name': 'Creative',
                  'type': 'STRING'
              }],
              'format': 'CSV'
          }
      }, rows)

  query_to_view(
      config,
      task['auth_bigquery'],
      config.project,
      task['dataset'],
      'AUDIT_LineItemMaps',
      """WITH
      LINEITEM_ERRORS AS (
      SELECT
        'Line Items Map' AS Operation,
        'Missing Line Item.' AS Error,
        'ERROR' AS Severity,
        COALESCE(Line_Item, 'BLANK') AS Id
      FROM
        `{dataset}.SHEET_LineItemMaps` AS M
      LEFT JOIN
        `{dataset}.DV_LineItems` AS L
      ON
        M.Line_Item=CONCAT(L.displayName, ' - ', L.lineItemId)
      WHERE L IS NULL
      ),
      CREATIVE_ERRORS AS (
      SELECT
        'Line Items Map' AS Operation,
        'Missing Line Item.' AS Error,
        'ERROR' AS Severity,
        COALESCE(Line_Item, 'BLANK') AS Id
      FROM
        `{dataset}.SHEET_LineItemMaps` AS M
      LEFT JOIN
        `{dataset}.DV_Creatives` AS C
      ON
        M.Line_Item=CONCAT(C.displayName, ' - ', C.creativeId)
      WHERE C IS NULL
      )
      SELECT * FROM LINEITEM_ERRORS
      UNION ALL
      SELECT * FROM CREATIVE_ERRORS
      ;
    """.format(**task),
      legacy=False)


def line_item_map_patch(config, task, commit=False):
  patches = {}
  changed = set()

  rows = get_rows(
      config,
      task['auth_bigquery'], {
          'bigquery': {
              'dataset':
                  task['dataset'],
              'query':
                  """SELECT advertiserId, lineItemId, creativeIds FROM `{dataset}.DV_LineItems`
      """.format(**task),
              'as_object':
                  True,
              'legacy':
                  False
          }
      })

  for row in rows:
    patches[str(row['lineItemId'])] = {
        'operation': 'Line Items Map',
        'action': 'PATCH',
        'parameters': {
            'advertiserId': str(row['advertiserId']),
            'lineItemId': str(row['lineItemId']),
            'body': {
                'creativeIds': [str(c) for c in row['creativeIds']]
            }
        }
    }

  rows = get_rows(
      config,
      task['auth_sheets'], {
          'sheets': {
              'sheet': task['sheet'],
              'tab': 'Line Items Map',
              'header':False,
              'range': 'A2:Z'
          }
      })

  rows = rows_pad(rows, 3, '')

  for row in rows:
    lineitem_id = lookup_id(row[1])
    creative_id = lookup_id(row[2])
    if lineitem_id in patches:
      if row[0] == 'ADD' and creative_id not in patches[lineitem_id][
          'parameters']['body']['creativeIds']:
        patches[lineitem_id]['line_item'] = row[1]
        patches[lineitem_id]['parameters']['body']['creativeIds'].append(
            creative_id)
        changed.add(lineitem_id)
      if row[0] == 'REMOVE' and creative_id in patches[lineitem_id][
          'parameters']['body']['creativeIds']:
        patches[lineitem_id]['line_item'] = row[1]
        patches[lineitem_id]['parameters']['body']['creativeIds'].remove(
            creative_id)
        changed.add(lineitem_id)

  # Remove any patches where creatives have not changed
  for li in list(patches.keys()):
    if li not in changed:
      del patches[li]
  patches = list(patches.values())

  patch_masks(patches)
  patch_preview(config, task, patches)

  if commit:
    line_item_commit(config, task, patches)
