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
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.insertion_order import insertion_order_commit
from starthinker.task.dv_editor.line_item import line_item_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def bid_strategy_clear(config, task):
  sheets_clear(config, task["auth_sheets"], task["sheet"], "Bid Strategy",
               "A2:Z")


def bid_strategy_load(config, task):

  # write bid_strategy to sheet
  put_rows(
    config,
    task["auth_sheets"],
    {
      "sheets": {
        "sheet": task["sheet"],
        "tab": "Bid Strategy",
        "header":False,
        "range": "A2:U"
      }
    },
    get_rows(
      config,
      task["auth_bigquery"],
      { "bigquery": {
        "dataset": task["dataset"],
        "query": """SELECT * FROM (
          SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
          CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
          CAST(NULL AS STRING) AS LineItem,
          I.bidStrategy.fixedBid.bidAmountMicros / 1000000 AS bidAmountMicros,
          I.bidStrategy.fixedBid.bidAmountMicros / 1000000 AS bidAmountMicros_Edit,
          I.bidStrategy.maximizeSpendAutoBid.performanceGoalType AS maximizeSpendAutoBid_performanceGoalType,
          I.bidStrategy.maximizeSpendAutoBid.performanceGoalType AS maximizeSpendAutoBid_performanceGoalType_Edit,
          I.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS maximizeSpendAutoBid_maxAverageCpmBidAmountMicros,
          I.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS maximizeSpendAutoBid_maxAverageCpmBidAmountMicros_Edit,
          I.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId AS maximizeSpendAutoBid_customBiddingAlgorithmId,
          I.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId AS maximizeSpendAutoBid_customBiddingAlgorithmId_Edit,
          I.bidStrategy.performanceGoalAutoBid.performanceGoalType AS performanceGoalAutoBid_performanceGoalType,
          I.bidStrategy.performanceGoalAutoBid.performanceGoalType AS performanceGoalAutoBid_performanceGoalType_Edit,
          I.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000 AS performanceGoalAutoBid_performanceGoalAmountMicros,
          I.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000 AS performanceGoalAutoBid_performanceGoalAmountMicros_Edit,
          I.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS performanceGoalAutoBid_maxAverageCpmBidAmountMicros,
          I.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS performanceGoalAutoBid_maxAverageCpmBidAmountMicros_Edit,
          I.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId AS performanceGoalAutoBid_customBiddingAlgorithmId,
          I.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId AS performanceGoalAutoBid_customBiddingAlgorithmId_Edit
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
          L.bidStrategy.fixedBid.bidAmountMicros / 1000000 AS bidAmountMicros,
          L.bidStrategy.fixedBid.bidAmountMicros / 1000000 AS bidAmountMicros_Edit,
          L.bidStrategy.maximizeSpendAutoBid.performanceGoalType AS performanceGoalType,
          L.bidStrategy.maximizeSpendAutoBid.performanceGoalType AS performanceGoalType_Edit,
          L.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS maxAverageCpmBidAmountMicros,
          L.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS maxAverageCpmBidAmountMicros_Edit,
          L.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId AS customBiddingAlgorithmId,
          L.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId AS customBiddingAlgorithmId_Edit,
          L.bidStrategy.performanceGoalAutoBid.performanceGoalType AS performanceGoalType,
          L.bidStrategy.performanceGoalAutoBid.performanceGoalType AS performanceGoalType_Edit,
          L.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000 AS performanceGoalAmountMicros,
          L.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000 AS performanceGoalAmountMicros_Edit,
          L.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS maxAverageCpmBidAmountMicros,
          L.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000 AS maxAverageCpmBidAmountMicros_Edit,
          L.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId AS customBiddingAlgorithmId,
          L.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId AS customBiddingAlgorithmId_Edit
        FROM `{dataset}.DV_LineItems` AS L
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON L.campaignId=C.campaignId
        LEFT JOIN `{dataset}.DV_InsertionOrders` AS I
        ON L.insertionOrderId=I.insertionOrderId
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON L.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId )
        ORDER BY InsertionOrder
      """.format(**task),
      "legacy": False
    }}
  ))


def bid_strategy_audit(config, task):
  rows = get_rows(
      config,
      task["auth_sheets"], {
          "sheets": {
              "sheet": task["sheet"],
              "tab": "Bid Strategy",
              "header":False,
              "range": "A2:U"
          }
      })

  put_rows(
      config,
      task["auth_bigquery"], {
          "bigquery": {
              "dataset": task["dataset"],
              "table": "SHEET_BidStrategy",
              "schema": [
                  { "name": "Partner", "type": "STRING" },
                  { "name": "Advertiser", "type": "STRING" },
                  { "name": "Campaign", "type": "STRING" },
                  { "name": "Insertion_Order", "type": "STRING" },
                  { "name": "Line_Item", "type": "STRING" },
                  { "name": "Fixed_Bid", "type": "FLOAT" },
                  { "name": "Fixed_Bid_Edit", "type": "FLOAT" },
                  { "name": "Auto_Bid_Goal", "type": "STRING" },
                  { "name": "Auto_Bid_Goal_Edit", "type": "STRING" },
                  { "name": "Auto_Bid_Amount", "type": "FLOAT" },
                  { "name": "Auto_Bid_Amount_Edit", "type": "FLOAT" },
                  { "name": "Auto_Bid_Algorithm", "type": "STRING" },
                  { "name": "Auto_Bid_Algorithm_Edit", "type": "STRING" },
                  { "name": "Performance_Goal_Type", "type": "STRING" },
                  { "name": "Performance_Goal_Type_Edit", "type": "STRING" },
                  { "name": "Performance_Goal_Amount", "type": "FLOAT" },
                  { "name": "Performance_Goal_Amount_Edit", "type": "FLOAT" },
                  { "name": "Performance_Goal_Average_CPM_Bid", "type": "FLOAT" },
                  { "name": "Performance_Goal_Average_CPM_Bid_Edit", "type": "FLOAT" },
                  { "name": "Performance_Goal_Algorithm", "type": "STRING" },
                  { "name": "Performance_Goal_Algorithm_Edit", "type": "STRING" },
              ],
              "format": "CSV"
          }
      }, rows)

  query_to_view(
      config,
      task["auth_bigquery"],
      config.project,
      task["dataset"],
      "AUDIT_BidStrategy",
      """WITH
        /* Check if sheet values are set */ INPUT_ERRORS AS (
        SELECT
          *
        FROM (
          SELECT
            'Bid Strategy' AS Operation,
            CASE
              WHEN Insertion_Order IS NOT NULL AND Line_Item IS NOT NULL THEN
                CASE
                  WHEN Fixed_Bid_Edit IS NOT NULL AND Auto_Bid_Goal_Edit IS NULL AND Auto_Bid_Algorithm_Edit IS NOT NULL THEN 'Both Fixed Bid and Bid Algorithm exist.'
                  WHEN Fixed_Bid_Edit IS NULL AND Auto_Bid_Goal_Edit IS NOT NULL AND Auto_Bid_Algorithm_Edit IS NOT NULL THEN 'Both Bid Goal and Bid Algorithm exist.'
                  WHEN Fixed_Bid_Edit IS NOT NULL AND Auto_Bid_Goal_Edit IS NOT NULL AND Auto_Bid_Algorithm_Edit IS NULL THEN 'Both Fixed Bid and Bid Goal exist.'
                  WHEN Fixed_Bid_Edit IS NOT NULL AND Auto_Bid_Goal_Edit IS NOT NULL AND Auto_Bid_Algorithm_Edit IS NOT NULL THEN 'All bid fields exist.'
                  ELSE NULL
                END
            ELSE
            NULL
          END
            AS Error,
            'ERROR' AS Severity,
            COALESCE(Line_Item,
              Insertion_Order,
              'BLANK') AS Id
          FROM
            `{dataset}.SHEET_BidStrategy` )
        WHERE
          Error IS NOT NULL )
      SELECT
        *
      FROM
        INPUT_ERRORS ;
    """.format(**task),
      legacy=False)

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PATCH_BidStrategy",
    """SELECT *
      FROM `{dataset}.SHEET_BidStrategy`
      WHERE (
        REGEXP_CONTAINS(Insertion_Order, r" - (\d+)$")
        OR REGEXP_CONTAINS(Line_Item, r" - (\d+)$")
      )
      AND Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_BidStrategy` WHERE Severity='ERROR')
      AND Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_BidStrategy` WHERE Severity='ERROR')
    """.format(**task),
    legacy=False
  )


def bid_strategy_patch(config, task, commit=False):
  patches = []

  rows = get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"PATCH_BidStrategy",
    }},
    as_object=True
  )

  for row in rows:

    bid_strategy = {}

    # If we are trying to switch from fixed bid to another bid type
    if row['Fixed_Bid_Edit'] is None and row['Fixed_Bid'] is not None:
      # If we switched from fixed to goal
      if row['Auto_Bid_Goal'] != row['Auto_Bid_Goal_Edit']:
        if config.verbose:
          print("Switching from Fixed Bid to Auto Bid Goal.")
        bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
        bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
          "performanceGoalType"] = row['Auto_Bid_Goal_Edit']
      # If we switched from fixed to algorithm
      elif row['Auto_Bid_Algorithm'] != row['Auto_Bid_Algorithm_Edit']:
        if config.verbose:
          print("Switching from Fixed Bid to Bid Algorithm.")
        bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
        bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
          "customBiddingAlgorithmId"] = row['Auto_Bid_Algorithm_Edit']

    elif row['Fixed_Bid'] != row['Fixed_Bid_Edit']:
      bid_strategy.setdefault("bidStrategy", {"fixedBid": {}})
      bid_strategy["bidStrategy"]["fixedBid"]["bidAmountMicros"] = int(
        float(row['Fixed_Bid_Edit']) * 100000
      )

    if row['Auto_Bid_Goal'] != row['Auto_Bid_Goal_Edit']:
      bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
      bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
       "performanceGoalType"] = row['Auto_Bid_Goal_Edit']

    if row['Auto_Bid_Amount'] != row['Auto_Bid_Amount_Edit']:
      bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
      bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
        "maxAverageCpmBidAmountMicros"] = int(float(row['Auto_Bid_Amount_Edit']) * 100000)

    if row['Auto_Bid_Algorithm'] != row['Auto_Bid_Algorithm_Edit']:
      bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
      bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
        "customBiddingAlgorithmId"] = row['Auto_Bid_Algorithm_Edit']

    if row['Performance_Goal_Type'] != row['Performance_Goal_Type_Edit']:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "performanceGoalType"] = row['Performance_Goal_Type_Edit']

    if row['Performance_Goal_Amount'] != row['Performance_Goal_Amount_Edit']:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "performanceGoalAmountMicros"] = int(float(row['Performance_Goal_Amount_Edit']) * 100000)

    if row['Performance_Goal_Average_CPM_Bid'] != row['Performance_Goal_Average_CPM_Bid_Edit']:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "maxAverageCpmBidAmountMicros"] = int(float(row['Performance_Goal_Average_CPM_Bid_Edit']) * 100000)

    if row['Performance_Goal_Algorithm'] != row['Performance_Goal_Algorithm_Edit']:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "customBiddingAlgorithmId"] = row['Performance_Goal_Algorithm_Edit']

    if bid_strategy:
      patch = {
          "operation": "Bid Strategy",
          "action": "PATCH",
          "partner": row['Partner'],
          "advertiser": row['Advertiser'],
          "campaign": row['Campaign'],
          "parameters": {
              "advertiserId": lookup_id(row['Advertiser']),
              "body": bid_strategy
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
  patch_preview(config, task, patches)

  if commit:
    insertion_order_commit(config, task, patches)
    line_item_commit(config, task, patches)
