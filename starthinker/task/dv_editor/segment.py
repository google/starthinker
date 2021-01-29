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

from starthinker.task.dv_editor.insertion_order import insertion_order_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def segment_clear():
  sheets_clear(
    project.task["auth_sheets"],
    project.task["sheet"],
    "Segments",
    "A2:Z"
  )


def segment_load():

  # write segments to sheet
  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "query": """SELECT
        CONCAT(P.displayName, ' - ', P.partnerId),
        CONCAT(A.displayName, ' - ', A.advertiserId),
        CONCAT(C.displayName, ' - ', C.campaignId),
        CONCAT(I.displayName, ' - ', I.insertionOrderId),
        'PATCH',
        CONCAT(BS.dateRange.startDate.year, '-', BS.dateRange.startDate.month, '-', BS.dateRange.startDate.day),
        CONCAT(BS.dateRange.startDate.year, '-', BS.dateRange.startDate.month, '-', BS.dateRange.startDate.day),
        CONCAT(BS.dateRange.endDate.year, '-', BS.dateRange.endDate.month, '-', BS.dateRange.endDate.day),
        CONCAT(BS.dateRange.endDate.year, '-', BS.dateRange.endDate.month, '-', BS.dateRange.endDate.day),
        BS.budgetAmountMicros / 100000,
        BS.budgetAmountMicros / 100000,
        BS.description,
        BS.description
        FROM `{dataset}.DV_InsertionOrders` AS I, UNNEST( budget.budgetSegments) AS BS
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON I.campaignId=C.campaignId
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON I.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
      """.format(**project.task),
      "legacy":False
    }}
  )

  put_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Segments",
      "range": "A2"
    }},
    rows
  )


def segment_audit():

  # Move Segments To BigQuery
  rows = get_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Segments",
      "range": "A2:M"
    }}
  )

  put_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
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
    rows
  )

  # Create Audit View And Write To Sheets
  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
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
              WHEN SAFE_CAST(Budget_Edit AS FLOAT64) > 1000 THEN 'Segment has excessive spend.'
              WHEN SAFE_CAST(Start_Date AS DATE) < CURRENT_DATE() THEN 'Segment starts in past.'
              WHEN SAFE_CAST(End_Date AS DATE) < CURRENT_DATE() THEN 'Segment ends in past.'
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
    """.format(**project.task),
    legacy=False
  )


def segment_patch(commit=False):

  def date_edited(value):
    y, m, d = value.split("-")
    return {"year": y, "month": m, "day": d}

  patches = {}
  changed = set()

  rows = get_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Segments",
      "range": "A2:Z"
    }}
  )

  rows = rows_pad(rows, 13, "")

  # Build list of segements skipping only deletes, track changes
  for row in rows:

    # inserts do not have an ID, skip them
    if not lookup_id(row[3]): continue

    patches.setdefault(
      row[3],
      { "operation": "Segments",
        "action": "PATCH",
        "partner": row[0],
        "advertiser": row[1],
        "campaign": row[2],
        "insertion_order": row[3],
        "parameters": {
          "advertiserId": lookup_id(row[1]),
          "insertionOrderId": lookup_id(row[3]),
          "body": {
            "budget": {
              "budgetSegments": []
            }
          }
        }
      }
    )

    if row[4] == "DELETE":
      changed.add(row[3])
    else:
      patches[row[3]]["parameters"]["body"]["budget"]["budgetSegments"].append({
        "dateRange": {
          "startDate": date_edited(row[6]),
          "endDate": date_edited(row[8])
        },
        "budgetAmountMicros": float(row[10]) * 100000,
        "description": row[12]
      })

      if row[5] != row[6] or row[7] != row[8] or row[9] != row[10] or row[11] != row[12]:
        changed.add(row[3])

  # Remove any patches where segments have not changed
  for io in list(patches.keys()):
    if io not in changed:
      del patches[io]
  patches = list(patches.values())

  patch_masks(patches)
  patch_preview(patches)

  if commit:
    insertion_order_commit(patches)
