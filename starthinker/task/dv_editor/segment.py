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
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.insertion_order import insertion_order_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def segment_clear(config, task):
  sheets_clear(
    config,
    task["auth_sheets"],
    task["sheet"],
    "Segments",
    "A2:Z"
  )


def segment_load(config, task):

  # write segments to sheet
  put_rows(
    config,
    task["auth_sheets"],
    { "sheets": {
      "sheet": task["sheet"],
      "tab": "Segments",
      "header":False,
      "range": "A2"
    }},
    get_rows(
      config,
      task["auth_bigquery"],
      { "bigquery": {
        "dataset": task["dataset"],
        "query": """SELECT
          CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
          CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,
          CONCAT(C.displayName, ' - ', C.campaignId) AS Camapign,
          CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
          'PATCH' AS Action,
          CONCAT(BS.dateRange.startDate.year, '-', BS.dateRange.startDate.month, '-', BS.dateRange.startDate.day) AS startDate,
          CONCAT(BS.dateRange.startDate.year, '-', BS.dateRange.startDate.month, '-', BS.dateRange.startDate.day) AS startDate_Edit,
          CONCAT(BS.dateRange.endDate.year, '-', BS.dateRange.endDate.month, '-', BS.dateRange.endDate.day) AS endDate,
          CONCAT(BS.dateRange.endDate.year, '-', BS.dateRange.endDate.month, '-', BS.dateRange.endDate.day) AS endDate_Edit,
          BS.budgetAmountMicros / 1000000 AS budgetAmountMicros,
          BS.budgetAmountMicros / 1000000 AS budgetAmountMicros_Edit,
          BS.description AS description,
          BS.description AS description_Edit
          FROM `{dataset}.DV_InsertionOrders` AS I, UNNEST( budget.budgetSegments) AS BS
          LEFT JOIN `{dataset}.DV_Campaigns` AS C
          ON I.campaignId=C.campaignId
          LEFT JOIN `{dataset}.DV_Advertisers` AS A
          ON I.advertiserId=A.advertiserId
          LEFT JOIN `{dataset}.DV_Partners` AS P
          ON A.partnerId=P.partnerId
          ORDER BY I.displayName
        """.format(**task),
        "legacy":False
      }}
    )
  )


def segment_audit(config, task):

  # Move Segments To BigQuery
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Segments",
      "schema": [
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "Campaign", "type": "STRING" },
        { "name": "Insertion_Order", "type": "STRING" },
        { "name": "Action", "type": "STRING" },
        { "name": "Start_Date", "type": "STRING" },
        { "name": "Start_Date_Edit", "type": "STRING" },
        { "name": "End_Date", "type": "STRING" },
        { "name": "End_Date_Edit", "type": "STRING" },
        { "name": "Budget", "type": "FLOAT" },
        { "name": "Budget_Edit", "type": "FLOAT" },
        { "name": "Description", "type": "STRING" },
        { "name": "Description_Edit", "type": "STRING" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Segments",
        "header":False,
        "range": "A2:M"
      }}
    )
  )

  # Create Audit View And Write To Sheets
  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "AUDIT_Segments",
    """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Segment' AS Operation,
            CASE
              WHEN Start_Date_Edit IS NULL THEN 'Missing Start Date.'
              WHEN End_Date_Edit IS NULL THEN 'Missing End Date .'
              WHEN Budget_Edit IS NULL THEN 'Missing Budget.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_Segments`
        )
        WHERE
          Error IS NOT NULL
      ),

      /* Check if duplicate Segments */
      DUPLICATE_ERRORS AS (
        SELECT
          'Segment' AS Operation,
          'Duplicate Segment.' AS Error,
          'WARNING' AS Severity,
          COALESCE(Insertion_Order, 'BLANK') AS Id
        FROM (
          SELECT Insertion_Order, Start_Date_Edit, End_Date_Edit, COUNT(*) AS count
          FROM `{dataset}.SHEET_Segments`
          GROUP BY 1, 2, 3
          HAVING count > 1
        )
      ),

      /* Check if budget segments are current */
      SEGMENT_ERRORS AS (
        SELECT
          *
        FROM (
          SELECT
            'Segments' AS Operation,
            CASE
              WHEN SAFE_CAST(Budget_Edit AS FLOAT64) > 1000000 THEN 'Segment has excessive spend.'
              WHEN SAFE_CAST(Start_Date AS DATE) != SAFE_CAST(Start_Date_Edit AS DATE) AND SAFE_CAST(Start_Date_Edit AS DATE) < CURRENT_DATE() THEN 'Segment starts in past.'
              WHEN SAFE_CAST(End_Date AS DATE) != SAFE_CAST(End_Date_Edit AS DATE) AND SAFE_CAST(End_Date_Edit AS DATE) < CURRENT_DATE() THEN 'Segment ends in past.'
            ELSE
            NULL
          END
            AS Error,
            'ERROR' AS Severity,
            COALESCE(Insertion_Order, 'BLANK') AS Id
          FROM
            `{dataset}.SHEET_Segments`
          )
        WHERE
          Error IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      UNION ALL
      SELECT * FROM DUPLICATE_ERRORS
      UNION ALL
      SELECT * FROM SEGMENT_ERRORS
      ;
    """.format(**task),
    legacy=False
  )

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PATCH_Segments",
    """SELECT *
      FROM `{dataset}.SHEET_Segments`
      WHERE Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_Segments` WHERE Severity='ERROR')
    """.format(**task),
    legacy=False
  )


def segment_patch(config, task, commit=False):

  def date_edited(value):
    y, m, d = value.split("-")
    return {"year": y, "month": m, "day": d}

  patches = {}
  changed = set()

  rows = get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"PATCH_Segments",
    }},
    as_object=True
  )

  # Build list of segements skipping only deletes, track changes
  for row in rows:

    patches.setdefault(
      row["Insertion_Order"],
      { "operation": "Segments",
        "action": "PATCH",
        "partner": row["Partner"],
        "advertiser": row["Advertiser"],
        "campaign": row["Campaign"],
        "insertion_order": row["Insertion_Order"],
        "parameters": {
          "advertiserId": lookup_id(row["Advertiser"]),
          "insertionOrderId": lookup_id(row["Insertion_Order"]),
          "body": {
            "budget": {
              "budgetSegments": []
            }
          }
        }
      }
    )

    if row['Action'] == "DELETE":
      changed.add(row["Insertion_Order"])
    else:
      patches[row["Insertion_Order"]]["parameters"]["body"]["budget"]["budgetSegments"].append({
        "dateRange": {
          "startDate": date_edited(row["Start_Date_Edit"]),
          "endDate": date_edited(row["End_Date_Edit"])
        },
        "budgetAmountMicros": float(row["Budget_Edit"]) * 1000000,
        "description": row["Description_Edit"]
      })

      if (row['Action'] == "INSERT"
        or row["Start_Date"] != row["Start_Date_Edit"]
        or row["End_Date"] != row["End_Date_Edit"]
        or row["Budget"] != row["Budget_Edit"]
        or row["Description"] != row["Description_Edit"]
      ):
        changed.add(row["Insertion_Order"])

  # Remove any patches where segments have not changed
  for io in list(patches.keys()):
    if io not in changed:
      del patches[io]
  patches = list(patches.values())

  patch_masks(patches)
  patch_preview(config, task, patches)

  if commit:
    insertion_order_commit(config, task, patches)
