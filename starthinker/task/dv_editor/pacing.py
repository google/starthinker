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
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.insertion_order import insertion_order_commit
from starthinker.task.dv_editor.line_item import line_item_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def pacing_clear():
  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Pacing", "A2:Z")


def pacing_load():

  # write pacings to sheet
  rows = get_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset":
                  project.task["dataset"],
              "query":
                  """SELECT
         CONCAT(P.displayName, ' - ', P.partnerId),
         CONCAT(A.displayName, ' - ', A.advertiserId),
         CONCAT(C.displayName, ' - ', C.campaignId),
         CONCAT(I.displayName, ' - ', I.insertionOrderId),
         NULL,
         I.pacing.pacingPeriod,
         I.pacing.pacingPeriod,
         I.pacing.pacingType,
         I.pacing.pacingType,
         CAST(I.pacing.dailyMaxMicros AS INT64) / 100000,
         CAST(I.pacing.dailyMaxMicros AS INT64) / 100000,
         I.pacing.dailyMaxImpressions,
         I.pacing.dailyMaxImpressions
       FROM `{dataset}.DV_InsertionOrders` AS I
       LEFT JOIN `{dataset}.DV_Campaigns` AS C
       ON I.campaignId=C.campaignId
       LEFT JOIN `{dataset}.DV_Advertisers` AS A
       ON I.advertiserId=A.advertiserId
       LEFT JOIN `{dataset}.DV_Partners` AS P
       ON A.partnerId=P.partnerId
       UNION ALL
       SELECT
         CONCAT(P.displayName, ' - ', P.partnerId),
         CONCAT(A.displayName, ' - ', A.advertiserId),
         CONCAT(C.displayName, ' - ', C.campaignId),
         CONCAT(I.displayName, ' - ', I.insertionOrderId),
         CONCAT(L.displayName, ' - ', L.lineItemId),
         L.pacing.pacingPeriod,
         L.pacing.pacingPeriod,
         L.pacing.pacingType,
         L.pacing.pacingType,
         CAST(L.pacing.dailyMaxMicros AS INT64) / 100000,
         CAST(L.pacing.dailyMaxMicros AS INT64) / 100000,
         L.pacing.dailyMaxImpressions,
         L.pacing.dailyMaxImpressions
       FROM `{dataset}.DV_LineItems` AS L
       LEFT JOIN `{dataset}.DV_Campaigns` AS C
       ON L.campaignId=C.campaignId
       LEFT JOIN `{dataset}.DV_InsertionOrders` AS I
       ON L.insertionOrderId=I.insertionOrderId
       LEFT JOIN `{dataset}.DV_Advertisers` AS A
       ON L.advertiserId=A.advertiserId
       LEFT JOIN `{dataset}.DV_Partners` AS P
       ON A.partnerId=P.partnerId
       """.format(**project.task),
              "legacy":
                  False
          }
      })

  put_rows(project.task["auth_sheets"], {
      "sheets": {
          "sheet": project.task["sheet"],
          "tab": "Pacing",
          "range": "A2"
      }
  }, rows)


def pacing_audit():
  rows = get_rows(project.task["auth_sheets"], {
      "sheets": {
          "sheet": project.task["sheet"],
          "tab": "Pacing",
          "range": "A2:Z"
      }
  })

  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset": project.task["dataset"],
              "table": "SHEET_Pacing",
              "schema": [
                  { "name": "Partner", "type": "STRING" },
                  { "name": "Advertiser", "type": "STRING" },
                  { "name": "Campaign", "type": "STRING" },
                  { "name": "Insertion_Order", "type": "STRING" },
                  { "name": "Line_Item", "type": "STRING" },
                  { "name": "Period", "type": "STRING" },
                  { "name": "Period_Edit", "type": "STRING" },
                  { "name": "Type", "type": "STRING" },
                  { "name": "Type_Edit", "type": "STRING" },
                  { "name": "Daily_Budget", "type": "FLOAT" },
                  { "name": "Daily_Budget_Edit", "type": "FLOAT" },
                  { "name": "Daily_Impressions", "type": "INTEGER" },
                  { "name": "Daily_Impressions_Edit", "type": "INTEGER" },
              ],
              "format": "CSV"
          }
      }, rows)

  query_to_view(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "AUDIT_Pacing",
      """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Pacing' AS Operation,
            CASE
              WHEN Period_Edit IS NULL THEN 'Missing Period.'
              WHEN Type_Edit IS NULL THEN 'Missing Type.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Line_Item, Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_Pacing`
        )
        WHERE
          Error IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      ;
    """.format(**project.task),
      legacy=False)

  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "PATCH_Pacing",
    """SELECT *
      FROM `{dataset}.SHEET_Pacing`
      WHERE (
        REGEXP_CONTAINS(Insertion_Order, r" - (\d+)$")
        OR REGEXP_CONTAINS(Line_Item, r" - (\d+)$")
      )
      AND Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_Pacing` WHERE Severity='ERROR')
      AND Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_Pacing` WHERE Severity='ERROR')
    """.format(**project.task),
    legacy=False
  )


def pacing_patch(commit=False):

  patches = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"PATCH_Pacing",
    }},
    as_object=True
  )

  for row in rows:

    pacing = {}

    if row['Period'] != row['Period_Edit']:
      pacing.setdefault("pacing", {})
      pacing["pacing"]["pacingPeriod"] = row['Period_Edit']

    if row['Type'] != row['Type_Edit']:
      pacing.setdefault("pacing", {})
      pacing["pacing"]["pacingType"] = row['Type_Edit']

    if row['Daily_Budget'] != row['Daily_Budget_Edit']:
      pacing.setdefault("pacing", {})
      pacing["pacing"]["dailyMaxMicros"] = int(float(row['Daily_Budget_Edit']) * 100000)

    if row['Daily_Impressions'] != row['Daily_Impressions_Edit']:
      pacing.setdefault("pacing", {})
      pacing["pacing"]["dailyMaxImpressions"] = row['Daily_Impressions_Edit']

    if pacing:
      patch = {
          "operation": "Pacing",
          "action": "PATCH",
          "partner": row['Partner'],
          "advertiser": row['Advertiser'],
          "campaign": row['Campaign'],
          "parameters": {
              "advertiserId": lookup_id(row['Advertiser']),
              "body": pacing
          }
      }

      if row['Line_Item']:
        patch["line_item"] = row['Line_Item']
        patch["parameters"]["lineItemId"] = lookup_id(row['Line_Item'])
      else:
        patch["insertion_order"] = row['Insertion_Order']
        patch["parameters"]["insertionOrderId"] = lookup_id(row['Insertion_Order'])

      patches.append(patch)

  patch_masks(patches)

  if commit:
    insertion_order_commit(patches)
    line_item_commit(patches)
  else:
    patch_preview(patches)
