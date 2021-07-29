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
from starthinker.task.dv_editor.campaign import campaign_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def frequency_cap_clear(config, task):
  sheets_clear(config, task["auth_sheets"], task["sheet"], "Frequency Caps",
               "A2:Z")


def frequency_cap_load(config, task):

  # write frequency_caps to sheet
  put_rows(
    config,
    task["auth_sheets"],
    {
      "sheets": {
        "sheet": task["sheet"],
        "tab": "Frequency Caps",
        "header":False,
        "range": "A2"
      }
    },
    get_rows(
      config,
      task["auth_bigquery"],
      { "bigquery": {
        "dataset":task["dataset"],
        "query":"""SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
          CAST(NULL AS STRING) AS InsertionOrder,
          CAST(NULL AS STRING) AS LineItem,
          IFNULL(C.frequencyCap.unlimited, FALSE) AS unlimited,
          IFNULL(C.frequencyCap.unlimited, FALSE) AS unlimited_Edit,
          C.frequencyCap.timeUnit AS timeUnit,
          C.frequencyCap.timeUnit AS timeUnit_Edit,
          C.frequencyCap.timeUnitCount AS timeUnitCount,
          C.frequencyCap.timeUnitCount AS timeUnitCount_Edit,
          C.frequencyCap.maxImpressions AS maxImpressions,
          C.frequencyCap.maxImpressions AS maxImpressions_Edit
        FROM `{dataset}.DV_Campaigns` AS C
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON C.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
        UNION ALL
        SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
          CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
          CAST(NULL AS STRING) AS LineItem,
          IFNULL(I.frequencyCap.unlimited, FALSE) AS unlimited,
          IFNULL(I.frequencyCap.unlimited, FALSE) AS unlimited_Edit,
          I.frequencyCap.timeUnit AS timeUnit,
          I.frequencyCap.timeUnit AS timeUnit_Edit,
          I.frequencyCap.timeUnitCount AS timeUnitCount,
          I.frequencyCap.timeUnitCount AS timeUnitCount_Edit,
          I.frequencyCap.maxImpressions AS maxImpressions,
          I.frequencyCap.maxImpressions AS maxImpressions_Edit
        FROM `{dataset}.DV_InsertionOrders` AS I
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON I.campaignId=C.campaignId
      LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON I.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
        UNION ALL
        SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
          CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
          CONCAT(L.displayName, ' - ', L.lineItemId) AS LineItem,
          IFNULL(L.frequencyCap.unlimited, FALSE) AS unlimited,
          IFNULL(L.frequencyCap.unlimited, FALSE) AS unlimited_Edit,
          L.frequencyCap.timeUnit AS timeUnit,
          L.frequencyCap.timeUnit AS timeUnit_Edit,
          L.frequencyCap.timeUnitCount AS timeUnitCount,
          L.frequencyCap.timeUnitCount AS timeUnitCount_Edit,
          L.frequencyCap.maxImpressions AS maxImpressions,
          L.frequencyCap.maxImpressions AS maxImpressions_Edit
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
      "legacy": False
    }}
  ))


def frequency_cap_audit(config, task):
  rows = get_rows(
      config,
      task["auth_sheets"], {
          "sheets": {
              "sheet": task["sheet"],
              "tab": "Frequency Caps",
              "header":False,
              "range": "A2:M"
          }
      })

  put_rows(
      config,
      task["auth_bigquery"], {
          "bigquery": {
              "dataset": task["dataset"],
              "table": "SHEET_FrequencyCaps",
              "schema": [
                  { "name": "Partner", "type": "STRING" },
                  { "name": "Advertiser", "type": "STRING" },
                  { "name": "Campaign", "type": "STRING" },
                  { "name": "Insertion_Order", "type": "STRING" },
                  { "name": "Line_Item", "type": "STRING" },
                  { "name": "Unlimited", "type": "BOOLEAN" },
                  { "name": "Unlimited_Edit", "type": "BOOLEAN" },
                  { "name": "Time_Unit", "type": "STRING" },
                  { "name": "Time_Unit_Edit", "type": "STRING" },
                  { "name": "Time_Count", "type": "INTEGER" },
                  { "name": "Time_Count_Edit", "type": "INTEGER" },
                  { "name": "Max_impressions", "type": "INTEGER" },
                  { "name": "Max_impressions_Edit", "type": "INTEGER" },
              ],
              "format": "CSV"
          }
      }, rows)

  query_to_view(
      config,
      task["auth_bigquery"],
      config.project,
      task["dataset"],
      "AUDIT_FrequencyCaps",
      """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Frequency Caps' AS Operation,
            CASE WHEN Unlimited_Edit IS TRUE THEN
              CASE WHEN Time_Unit_Edit IS NOT NULL OR Time_Count_Edit IS NOT NULL OR Max_Impressions_Edit IS NOT NULL THEN 'Time Unit and the Other Options are Mutually Exclusive.'
              ELSE NULL
             END
            ELSE
              IF(Time_Unit_Edit IS NULL OR Time_Count_Edit IS NULL OR Max_Impressions_Edit IS NULL, 'If Time Unit is FALSE, the other options are required.', NULL)
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Line_Item, Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_FrequencyCaps`
        )
        WHERE
          Error IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      ;
    """.format(**task),
      legacy=False)

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PATCH_FrequencyCaps",
    """SELECT *
      FROM `{dataset}.SHEET_FrequencyCaps`
      WHERE Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_FrequencyCaps` WHERE Severity='ERROR')
      AND Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_FrequencyCaps` WHERE Severity='ERROR')
      AND Campaign NOT IN (SELECT Id FROM `{dataset}.AUDIT_FrequencyCaps` WHERE Severity='ERROR')
    """.format(**task),
    legacy=False
  )


def frequency_cap_patch(config, task, commit=False):
  patches = []

  rows = get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"PATCH_FrequencyCaps",
    }},
    as_object=True
  )

  for row in rows:

    frequency_cap = {}

    if row['Unlimited'] != row['Unlimited_Edit']:
      frequency_cap.setdefault("frequencyCap", {})
      frequency_cap["frequencyCap"]["unlimited"] = row['Unlimited_Edit']
    if row['Time_Unit'] != row['Time_Unit_Edit']:
      frequency_cap.setdefault("frequencyCap", {})
      frequency_cap["frequencyCap"]["timeUnit"] = row['Time_Unit_Edit']
    if row['Time_Count'] != row['Time_Count_Edit']:
      frequency_cap.setdefault("frequencyCap", {})
      frequency_cap["frequencyCap"]["timeUnitCount"] = row['Time_Count_Edit']
    if row['Max_impressions'] != row['Max_impressions_Edit']:
      frequency_cap.setdefault("frequencyCap", {})
      frequency_cap["frequencyCap"]["maxImpressions"] = row['Max_impressions_Edit']

    if frequency_cap:
      patch = {
          "operation": "Frequency Caps",
          "action": "PATCH",
          "partner": row['Partner'],
          "advertiser": row['Advertiser'],
          "parameters": {
              "advertiserId": lookup_id(row['Advertiser']),
              "body": frequency_cap
          }
      }

      if row['Line_Item']:
        patch["line_item"] = row['Line_Item']
        patch["parameters"]["lineItemId"] = lookup_id(row['Line_Item'])
      elif row['Insertion_Order']:
        patch["insertion_order"] = row['Insertion_Order']
        patch["parameters"]["insertionOrderId"] = lookup_id(row['Insertion_Order'])
      else:
        patch["campaign"] = row['Campaign']
        patch["parameters"]["campaignId"] = lookup_id(row['Campaign'])

      patches.append(patch)

  patch_masks(patches)
  patch_preview(config, task, patches)

  if commit:
    insertion_order_commit(config, task, patches)
    line_item_commit(config, task, patches)
    campaign_commit(config, task, patches)
