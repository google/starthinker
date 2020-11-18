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
from starthinker.util.google_api import API_DV360
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_sheets.patch import patch_clear
from starthinker.task.dv_sheets.patch import patch_log
from starthinker.task.dv_sheets.patch import patch_masks
from starthinker.task.dv_sheets.patch import patch_preview


def insertion_order_clear():
  table_create(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "DV_InsertionOrders",
      Discovery_To_BigQuery(
          "displayvideo",
          "v1").method_schema("advertisers.insertionOrders.list"),
  )

  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Insertion Orders",
               "A2:Z")


def insertion_order_load():

  # load multiple partners from user defined sheet
  def insertion_order_load_multiple():
    rows = get_rows(
        project.task["auth_sheets"], {
            "sheets": {
                "sheet": project.task["sheet"],
                "tab": "Advertisers",
                "range": "A2:A"
            }
        })

    for row in rows:
      yield from API_DV360(
          project.task["auth_dv"],
          iterate=True).advertisers().insertionOrders().list(
              advertiserId=lookup_id(row[0])).execute()

  # write insertion orders to database and sheet
  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset":
                  project.task["dataset"],
              "table":
                  "DV_InsertionOrders",
              "schema":
                  Discovery_To_BigQuery(
                      "displayvideo",
                      "v1").method_schema("advertisers.insertionOrders.list"),
              "format":
                  "JSON"
          }
      }, insertion_order_load_multiple())

  # write insertion orders to sheet
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
         'PATCH',
         I.entityStatus,
         I.displayName,
         I.displayName,
         I.budget.budgetUnit,
         I.budget.budgetUnit,
         I.budget.automationType,
         I.budget.automationType,
         I.performanceGoal.performanceGoalType,
         I.performanceGoal.performanceGoalType,
         I.performanceGoal.performanceGoalAmountMicros / 1000000,
         I.performanceGoal.performanceGoalAmountMicros / 1000000,
         I.performanceGoal.performanceGoalPercentageMicros / 1000000,
         I.performanceGoal.performanceGoalPercentageMicros / 1000000,
         I.performanceGoal.performanceGoalString,
         I.performanceGoal.performanceGoalString
         FROM `{dataset}.DV_InsertionOrders` AS I
         LEFT JOIN `{dataset}.DV_Campaigns` AS C
         ON I.campaignId=C.campaignId
         LEFT JOIN `{dataset}.DV_Advertisers` AS A
         ON I.advertiserId=A.advertiserId
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
              "tab": "Insertion Orders",
              "range": "A2"
          }
      }, rows)


def insertion_order_audit():

  # Move Insertion Order To BigQuery
  rows = get_rows(
      project.task["auth_sheets"], {
          "sheets": {
              "sheet": project.task["sheet"],
              "tab": "Insertion Orders",
              "range": "A2:Z"
          }
      })

  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset": project.task["dataset"],
              "table": "SHEET_InsertionOrders",
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
                      "name": "Action",
                      "type": "STRING"
                  },
                  {
                      "name": "Status",
                      "type": "STRING"
                  },
                  {
                      "name": "Name",
                      "type": "STRING"
                  },
                  {
                      "name": "Name_Edit",
                      "type": "STRING"
                  },
                  {
                      "name": "Budget_Unit",
                      "type": "STRING"
                  },
                  {
                      "name": "Budget_Unit_Edit",
                      "type": "STRING"
                  },
                  {
                      "name": "Budget_Automation",
                      "type": "STRING"
                  },
                  {
                      "name": "Budget_Automation_Edit",
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
                      "name": "Performance_Goal_Percent",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Performance_Goal_Percent_Edit",
                      "type": "FLOAT"
                  },
                  {
                      "name": "Performance_Goal_String",
                      "type": "STRING"
                  },
                  {
                      "name": "Performance_Goal_String_Edit",
                      "type": "STRING"
                  },
              ],
              "format": "CSV"
          }
      }, rows)

  # Create Audit View And Write To Sheets
  query_to_view(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "AUDIT_InsertionOrders",
      """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Insertion Order' AS Operation,
            CASE
              WHEN Name_Edit IS NULL THEN 'Missing Name.'
              WHEN Budget_Unit_Edit IS NULL THEN 'Missing Budget Unit.'
              WHEN Budget_Automation_Edit IS NULL THEN 'Missing Budget Automation.'
              WHEN Performance_Goal_Type_Edit IS NULL THEN 'Missing Goal Type.'
              WHEN Performance_Goal_Amount_Edit IS NULL
              AND Performance_Goal_Percent_Edit IS NULL
              AND Performance_Goal_String_Edit IS NULL THEN 'Missing Goal Amount / Percent / String.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_InsertionOrders`
        )
        WHERE
          Error IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      ;
    """.format(**project.task),
      legacy=False)


def insertion_order_patch(commit=False):

  patches = []

  rows = get_rows(
      project.task["auth_sheets"], {
          "sheets": {
              "sheet": project.task["sheet"],
              "tab": "Insertion Orders",
              "range": "A2:Z"
          }
      })

  rows = rows_pad(rows, 20, "")

  for row in rows:
    if row[4] == "DELETE":
      patches.append({
          "operation": "Insertion Orders",
          "action": "DELETE",
          "partner": row[0],
          "advertiser": row[1],
          "campaign": row[2],
          "insertion_order": row[3],
          "parameters": {
              "advertiserId": lookup_id(row[1]),
              "insertionOrderId": lookup_id(row[3])
          }
      })

    elif row[4] == "PATCH":
      insertion_order = {}

      if row[6] != row[7]:
        insertion_order["displayName"] = row[7]
      if row[8] != row[9]:
        insertion_order.setdefault("budget", {})
        insertion_order["budget"]["budgetUnit"] = row[9]
      if row[10] != row[11]:
        insertion_order.setdefault("budget", {})
        insertion_order["budget"]["automationType"] = row[11]
      if row[12] != row[13]:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalType"] = row[13]
      if row[14] != row[15]:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalAmountMicros"] = int(
            float(row[15]) * 1000000)
      if row[16] != row[17]:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"][
            "performanceGoalPercentageMicros"] = int(float(row[15]) * 1000000)
      if row[18] != row[19]:
        insertion_order.setdefault("performanceGoal", {})
        insertion_order["performanceGoal"]["performanceGoalString"] = row[15]

      if insertion_order:
        patches.append({
            "operation": "Insertion Orders",
            "action": "PATCH",
            "partner": row[0],
            "advertiser": row[1],
            "campaign": row[2],
            "insertion_order": row[3],
            "parameters": {
                "advertiserId": lookup_id(row[1]),
                "insertionOrderId": lookup_id(row[3]),
                "body": insertion_order
            }
        })

  patch_masks(patches)

  if commit:
    insertion_order_commit(patches)
  else:
    patch_preview(patches)


def insertion_order_commit(patches):
  for patch in patches:
    if not patch.get("insertion_order"):
      continue
    print("API INSERTION ORDER:", patch["action"], patch["insertion_order"])
    try:
      if patch["action"] == "DELETE":
        response = API_DV360(
            project.task["auth_dv"]).advertisers().insertionOrders().delete(
                **patch["parameters"]).execute()
        patch["success"] = response
      elif patch["action"] == "PATCH":
        response = API_DV360(
            project.task["auth_dv"]).advertisers().insertionOrders().patch(
                **patch["parameters"]).execute()
        patch["success"] = response["insertionOrderId"]
    except Exception as e:
      patch["error"] = str(e)
    finally:
      patch_log(patch)
  patch_log()
