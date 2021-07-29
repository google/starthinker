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
from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.insertion_order import insertion_order_commit
from starthinker.task.dv_editor.line_item import line_item_commit
from starthinker.task.dv_editor.advertiser import advertiser_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def integration_detail_clear(config, task):
  sheets_clear(config, task["auth_sheets"], task["sheet"],
               "Integration Details", "A2:Z")


def integration_detail_load(config, task):

  # write integration_details to sheet
  put_rows(
    config,
    task["auth_sheets"],
    {
      "sheets": {
        "sheet": task["sheet"],
        "tab": "Integration Details",
        "range": "A2"
      }
    },
    get_rows(
      config,
      task["auth_bigquery"],
      { "bigquery": {
        "dataset":task["dataset"],
        "query":"""SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) Advertiser,
          CAST(NULL AS STRING) Campaign,
          CAST(NULL AS STRING) InsertionOrder,
          CAST(NULL AS STRING) LineItem,
          A.integrationDetails.integrationCode AS integrationCode,
          A.integrationDetails.integrationCode AS integrationCode_Edit,
          A.integrationDetails.details AS details,
          A.integrationDetails.details AS details_Edit
        FROM `{dataset}.DV_Advertisers` AS A
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
        UNION ALL
        SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
          CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
          CAST(NULL AS STRING) AS LineItem,
          I.integrationDetails.integrationCode AS integrationCode,
          I.integrationDetails.integrationCode AS integrationCode_Edit,
          I.integrationDetails.details AS details,
          I.integrationDetails.details AS details_Edit
        FROM `{dataset}.DV_InsertionOrders` AS I
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON I.campaignId=C.campaignId
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON I.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
        UNION ALL
        SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner ,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
          CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
          CONCAT(L.displayName, ' - ', L.lineItemId) AS LineItem,
          L.integrationDetails.integrationCode AS integrationCode,
          L.integrationDetails.integrationCode AS integrationCode_Edit,
          L.integrationDetails.details AS details,
          L.integrationDetails.details AS details_Edit
        FROM `{dataset}.DV_LineItems` AS L
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON L.campaignId=C.campaignId
        LEFT JOIN `{dataset}.DV_InsertionOrders` AS I
        ON L.insertionOrderId=I.insertionOrderId
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON L.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
        """.format(**task),
        "legacy":False
      }}
    )
  )


def integration_detail_audit(config, task):
  rows = get_rows(
      config,
      task["auth_sheets"], {
          "sheets": {
              "sheet": task["sheet"],
              "tab": "Integration Details",
              "range": "A2:I"
          }
      })

  put_rows(
      config,
      task["auth_bigquery"], {
          "bigquery": {
              "dataset": task["dataset"],
              "table": "SHEET_IntegrationDetails",
              "schema": [
                  { "name": "Partner", "type": "STRING" },
                  { "name": "Advertiser", "type": "STRING" },
                  { "name": "Campaign", "type": "STRING" },
                  { "name": "Insertion_Order", "type": "STRING" },
                  { "name": "Line_Item", "type": "STRING" },
                  { "name": "Integration_Code", "type": "STRING" },
                  { "name": "Integration_Code_Edit", "type": "STRING" },
                  { "name": "Details", "type": "STRING" },
                  { "name": "Details_Edit", "type": "STRING" },
              ],
              "format": "CSV"
          }
      }, rows)

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "AUDIT_IntegrationDetails",
    """WITH
      /* Check if advertiser values are set */
      INPUT_ERRORS AS (
        SELECT
          'Integration Details' AS Operation,
          'Missing Advertiser.' AS Error,
          'ERROR' AS Severity,
          COALESCE(Line_Item, Insertion_Order, Advertiser, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_IntegrationDetails`
        WHERE Advertiser IS NULL
      )

      SELECT * FROM INPUT_ERRORS
    """.format(**task),
    legacy=False
  )

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PATCH_IntegrationDetails",
    """SELECT *
      FROM `{dataset}.SHEET_IntegrationDetails`
      WHERE Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_IntegrationDetails` WHERE Severity='ERROR')
      AND Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_IntegrationDetails` WHERE Severity='ERROR')
      AND Campaign NOT IN (SELECT Id FROM `{dataset}.AUDIT_IntegrationDetails` WHERE Severity='ERROR')
    """.format(**task),
    legacy=False
  )


def integration_detail_patch(config, task, commit=False):
  patches = []

  rows = get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"PATCH_IntegrationDetails",
    }},
    as_object=True
  )

  for row in rows:

    integration_details = {}

    if row['Integration_Code'] != row['Integration_Code_Edit']:
      integration_details.setdefault("integrationDetails", {})
      integration_details["integrationDetails"]["integrationCode"] = row['Integration_Code_Edit']
    if row['Details'] != row['Details_Edit']:
      integration_details.setdefault("integrationDetails", {})
      integration_details["integrationDetails"]["details"] = row['Details_Edit']

    if integration_details:
      patch = {
          "operation": "Pacing",
          "action": "PATCH",
          "partner": row['Partner'],
          "parameters": {
              "advertiserId": lookup_id(row['Advertiser']),
              "body": integration_details
          }
      }

      if row['Line_Item']:
        patch["line_item"] = row['Line_Item']
        patch["parameters"]["lineItemId"] = lookup_id(row['Line_Item'])

      elif row['Insertion_Order']:
        patch["insertion_order"] = row['Insertion_Order']
        patch["parameters"]["insertionOrderId"] = lookup_id(row['Insertion_Order'])

      else:
        patch["advertiser"] = row['Advertiser']
        patch["parameters"]["advertiserId"] = lookup_id(row['Advertiser'])

      patches.append(patch)

  patch_masks(patches)
  patch_preview(config, task, patches)

  if commit:
    insertion_order_commit(config, task, patches)
    line_item_commit(config, task, patches)
    advertiser_commit(config, task, patches)
