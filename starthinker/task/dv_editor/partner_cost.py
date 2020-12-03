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
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.insertion_order import insertion_order_commit
from starthinker.task.dv_editor.line_item import line_item_commit
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def partner_cost_clear():
  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Partner Costs",
               "A2:Z")


def partner_cost_load():

  # write partner_costs to sheet
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
         PC.costType,
         PC.costType,
         PC.feeType,
         PC.feeType,
         PC.invoiceType,
         PC.invoiceType,
         PC.feeAmount / 100000,
         PC.feeAmount / 100000,
         PC.feePercentageMillis / 1000,
         PC.feePercentageMillis / 1000
       FROM `{dataset}.DV_InsertionOrders` AS I, UNNEST(partnerCosts) AS PC
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
         PC.costType,
         PC.costType,
         PC.feeType,
         PC.feeType,
         PC.invoiceType,
         PC.invoiceType,
         PC.feeAmount / 100000,
         PC.feeAmount / 100000,
         PC.feePercentageMillis / 1000,
         PC.feePercentageMillis / 1000
       FROM `{dataset}.DV_LineItems` AS L, UNNEST(partnerCosts) AS PC
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
              "tab": "Partner Costs",
              "range": "A2"
          }
      }, rows)


def partner_cost_audit():
  rows = get_rows(
      project.task["auth_sheets"], {
          "sheets": {
              "sheet": project.task["sheet"],
              "tab": "Partner Costs",
              "range": "A2:Z"
          }
      })

  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset": project.task["dataset"],
              "table": "SHEET_PartnerCosts",
              "schema": [
                  { "name": "Partner", "type": "STRING" },
                  { "name": "Advertiser", "type": "STRING" },
                  { "name": "Campaign", "type": "STRING" },
                  { "name": "Insertion_Order", "type": "STRING" },
                  { "name": "Line_Item", "type": "STRING" },
                  { "name": "Cost_Type", "type": "STRING" },
                  { "name": "Cost_Type_Edit", "type": "STRING" },
                  { "name": "Fee_Type", "type": "STRING" },
                  { "name": "Fee_Type_Edit", "type": "STRING" },
                  { "name": "Invoice_Type", "type": "STRING" },
                  { "name": "Invoice_Type_Edit", "type": "STRING" },
                  { "name": "Fee_Amount", "type": "FLOAT" },
                  { "name": "Fee_Amount_Edit", "type": "FLOAT" },
                  { "name": "Fee_Percent", "type": "FLOAT" },
                  { "name": "Fee_Percent_Edit", "type": "FLOAT" },
              ],
              "format": "CSV"
          }
      }, rows)

  query_to_view(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "AUDIT_PartnerCosts",
      """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Partner Costs' AS Operation,
            CASE
              WHEN Cost_Type_Edit IS NULL THEN 'Missing Cost Type.'
              WHEN Fee_Type_Edit IS NULL THEN 'Missing Fee Type.'
              WHEN Invoice_Type_Edit IS NULL THEN 'Missing Invoice Type.'
              WHEN Fee_Amount_Edit IS NULL THEN 'Missing Fee Amount.'
              WHEN Fee_Percent_Edit IS NULL THEN 'Missing Fee Percent.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Line_Item, Insertion_Order, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_PartnerCosts`
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
    "PATCH_PartnerCosts",
    """SELECT *
      FROM `{dataset}.SHEET_PartnerCosts`
      WHERE (
        REGEXP_CONTAINS(Insertion_Order, r" - (\d+)$")
        OR REGEXP_CONTAINS(Line_Item, r" - (\d+)$")
      )
      AND Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_PartnerCosts` WHERE Severity='ERROR')
      AND Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_PartnerCosts` WHERE Severity='ERROR')
    """.format(**project.task),
    legacy=False
  )


def partner_cost_patch(commit=False):
  patches = {}
  changed = set()

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"PATCH_PartnerCosts",
    }},
    as_object=True
  )

  for row in rows:

    lookup = row['Line_Item'] or row['Insertion_Order']

    patches.setdefault(
        lookup, {
            "operation": "Partner Costs",
            "action": "PATCH",
            "partner": row['Partner'],
            "advertiser": row['Advertiser'],
            "campaign": row['Campaign'],
            "parameters": {
                "advertiserId": lookup_id(row['Advertiser']),
                "body": {
                    "partnerCosts": []
                }
            }
        })

    if row['Line_Item']:
      patches[lookup]["line_item"] = row['Line_Item']
      patches[lookup]["parameters"]["lineItemId"] = lookup_id(row['Line_Item'])
    else:
      patches[lookup]["insertion_order"] = row['Insertion_Order']
      patches[lookup]["parameters"]["insertionOrderId"] = lookup_id(row['Insertion_Order'])

    patches[lookup]["parameters"]["body"]["partnerCosts"].append({
        "costType": row['Cost_Type_Edit'],
        "feeType": row['Fee_Type_Edit'],
        "invoiceType": row['Invoice_Type_Edit'],
        "feeAmount": int(float(row['Fee_Amount_Edit']) * 100000) if row['Fee_Amount_Edit'] else None,
        "feePercentageMillis": int(float(row['Fee_Percent_Edit']) * 1000) if row['Fee_Percent_Edit'] else None
    })

    if row['Cost_Type'] != row['Cost_Type_Edit'] \
      or row['Fee_Type'] != row['Fee_Type_Edit'] \
      or row['Invoice_Type'] != row['Invoice_Type_Edit'] \
      or row['Fee_Amount'] != row['Fee_Amount_Edit'] \
      or row['Fee_Percent'] != row['Fee_Percent_Edit']:
      changed.add(lookup)

  # Remove any patches where partner costs have not changed
  for pc in list(patches.keys()):
    if pc not in changed:
      del patches[pc]
  patches = list(patches.values())

  patch_masks(patches)

  if commit:
    insertion_order_commit(patches)
    line_item_commit(patches)
  else:
    patch_preview(patches)
