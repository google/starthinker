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
from starthinker.util.csv import rows_pad
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_sheets.insertion_order import insertion_order_commit
from starthinker.task.dv_sheets.line_item import line_item_commit
from starthinker.task.dv_sheets.patch import patch_masks
from starthinker.task.dv_sheets.patch import patch_preview


def bid_strategy_clear():
  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Bid Strategy",
               "A2:Z")


def bid_strategy_load():

  # write bid_strategy to sheet
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
         I.bidStrategy.fixedBid.bidAmountMicros / 1000000,
         I.bidStrategy.fixedBid.bidAmountMicros / 1000000,
         I.bidStrategy.maximizeSpendAutoBid.performanceGoalType,
         I.bidStrategy.maximizeSpendAutoBid.performanceGoalType,
         I.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         I.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         I.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId,
         I.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId,
         I.bidStrategy.performanceGoalAutoBid.performanceGoalType,
         I.bidStrategy.performanceGoalAutoBid.performanceGoalType,
         I.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000,
         I.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000,
         I.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         I.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         I.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId,
         I.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId
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
         L.bidStrategy.fixedBid.bidAmountMicros / 1000000,
         L.bidStrategy.fixedBid.bidAmountMicros / 1000000,
         L.bidStrategy.maximizeSpendAutoBid.performanceGoalType,
         L.bidStrategy.maximizeSpendAutoBid.performanceGoalType,
         L.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         L.bidStrategy.maximizeSpendAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         L.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId,
         L.bidStrategy.maximizeSpendAutoBid.customBiddingAlgorithmId,
         L.bidStrategy.performanceGoalAutoBid.performanceGoalType,
         L.bidStrategy.performanceGoalAutoBid.performanceGoalType,
         L.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000,
         L.bidStrategy.performanceGoalAutoBid.performanceGoalAmountMicros / 1000000,
         L.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         L.bidStrategy.performanceGoalAutoBid.maxAverageCpmBidAmountMicros / 1000000,
         L.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId,
         L.bidStrategy.performanceGoalAutoBid.customBiddingAlgorithmId
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

  put_rows(
      project.task["auth_sheets"], {
          "sheets": {
              "sheet": project.task["sheet"],
              "tab": "Bid Strategy",
              "range": "A2"
          }
      }, rows)


def bid_strategy_audit():
  rows = get_rows(
      project.task["auth_sheets"], {
          "sheets": {
              "sheet": project.task["sheet"],
              "tab": "Bid Strategy",
              "range": "A2:Z"
          }
      })

  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset": project.task["dataset"],
              "table": "SHEET_BidStrategy",
              "schema": [
                  {
                      "name": "Partner",
                      "type": "STRING"
                  },
                  {
                      "name": "Advertiser",
                      "type": "STRING"
                  },
                  {
                      "name": "Campaign",
                      "type": "STRING"
                  },
                  {
                      "name": "Insertion_Order",
                      "type": "STRING"
                  },
                  {
                      "name": "Line_Item",
                      "type": "STRING"
                  },
                  {
                      "name": "Fixed_Bid",
                      "type": "STRING"
                  },
                  {
                      "name": "Fixed_Bid_Edit",
                      "type": "STRING"
                  },
                  {
                      "name": "Auto_Bid_Goal",
                      "type": "STRING"
                  },
                  {
                      "name": "Auto_Bid_Goal_Edit",
                      "type": "STRING"
                  },
                  {
                      "name": "Auto_Bid_Amount",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Auto_Bid_Amount_Edit",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Auto_Bid_Algorithm",
                      "type": "STRING"
                  },
                  {
                      "name": "Auto_Bid_Algorithm_Edit",
                      "type": "STRING"
                  },
                  {
                      "name": "Performance_Goal_Type",
                      "type": "STRING"
                  },
                  {
                      "name": "Performance_Goal_Type_Edit",
                      "type": "STRING"
                  },
                  {
                      "name": "Performance_Goal_Amount",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Performance_Goal_Amount_Edit",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Performance_Goal_Average_CPM_Bid",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Performance_Goal_Average_CPM_Bid_Edit",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Performance_Goal_Algorithm",
                      "type": "STRING"
                  },
                  {
                      "name": "Performance_Goal_Algorithm_Edit",
                      "type": "STRING"
                  },
              ],
              "format": "CSV"
          }
      }, rows)

  query_to_view(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "AUDIT_BidStrategy",
      """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Bid Strategy' AS Operation,
            CASE
              WHEN Fixed_Bid_Edit IS NULL THEN 'Missing Fixed Bid.'
              WHEN Auto_Bid_Goal_Edit IS NULL THEN 'Missing Auto Bid Goal.'
              WHEN Auto_Bid_Algorithm_Edit IS NULL THEN 'Missing Auto Bid Algorithm.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Line_Item, Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_BidStrategy`
        )
        WHERE
          Error IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      ;
    """.format(**project.task),
      legacy=False)


def bid_strategy_patch(commit=False):
  patches = []

  rows = get_rows(
      project.task["auth_sheets"], {
          "sheets": {
              "sheet": project.task["sheet"],
              "tab": "Bid Strategy",
              "range": "A2:Z"
          }
      })

  rows = rows_pad(rows, 21, "")

  for row in rows:
    bid_strategy = {}

    if row[5] != row[6]:
      bid_strategy.setdefault("bidStrategy", {"fixedBid": {}})
      bid_strategy["bidStrategy"]["fixedBid"]["bidAmountMicros"] = int(
          float(row[6]) * 1000000)
    if row[7] != row[8]:
      bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
      bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
          "performanceGoalType"] = row[8]
    if row[9] != row[10]:
      bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
      bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
          "maxAverageCpmBidAmountMicros"] = int(float(row[10]) * 1000000)
    if row[11] != row[12]:
      bid_strategy.setdefault("bidStrategy", {"maximizeSpendAutoBid": {}})
      bid_strategy["bidStrategy"]["maximizeSpendAutoBid"][
          "customBiddingAlgorithmId"] = row[12]
    if row[13] != row[14]:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "performanceGoalType"] = row[14]
    if row[15] != row[16]:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "performanceGoalAmountMicros"] = int(float(row[16]) * 1000000)
    if row[17] != row[18]:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "maxAverageCpmBidAmountMicros"] = int(float(row[18]) * 1000000)
    if row[19] != row[20]:
      bid_strategy.setdefault("bidStrategy", {"performanceGoalAutoBid": {}})
      bid_strategy["bidStrategy"]["performanceGoalAutoBid"][
          "customBiddingAlgorithmId"] = row[20]

    if bid_strategy:
      patch = {
          "operation": "Bid Strategy",
          "action": "PATCH",
          "partner": row[0],
          "advertiser": row[1],
          "campaign": row[2],
          "parameters": {
              "advertiserId": lookup_id(row[1]),
              "body": bid_strategy
          }
      }

      if row[4]:
        patch["line_item"] = row[4]
        patch["parameters"]["lineItemId"] = lookup_id(row[4])
      else:
        patch["insertion_order"] = row[3]
        patch["parameters"]["insertionOrderId"] = lookup_id(row[3])

      patches.append(patch)

  patch_masks(patches)

  if commit:
    insertion_order_commit(patches)
    line_item_commit(patches)
  else:
    patch_preview(patches)
