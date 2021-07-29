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
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def partner_cost_clear(config, task):
  sheets_clear(
    config,
    task["auth_sheets"],
    task["sheet"],
    "Partner Costs",
    "A2:Z"
  )


def partner_cost_load(config, task):

  # write partner_costs to sheet
  put_rows(
    config,
    task["auth_sheets"],
    { "sheets": {
      "sheet": task["sheet"],
      "tab": "Partner Costs",
      "header":False,
      "range": "A2"
    }},
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
           CONCAT(REGEXP_REPLACE(PC.feeType, r'^PARTNER_COST_FEE_TYPE_(.*)_FEE', '\\\\1'),' ', ROW_NUMBER() OVER (PARTITION BY I.insertionOrderId, PC.feeType ORDER BY PO)) AS Index,
           PC.costType AS costType,
           PC.costType AS costType_Edit,
           PC.feeType AS feeType,
           PC.feeType AS feeType_Edit,
           PC.invoiceType AS invoiceType,
           PC.invoiceType AS invoiceType_Edit,
           PC.feeAmount / 1000000 AS feeAmount,
           PC.feeAmount / 1000000 AS feeAmount_Edit,
           PC.feePercentageMillis / 1000 AS feePercentageMillis,
           PC.feePercentageMillis / 1000 AS feePercentageMillis_Edit
         FROM `{dataset}.DV_InsertionOrders` AS I, UNNEST(partnerCosts) AS PC WITH OFFSET AS PO
         LEFT JOIN `{dataset}.DV_Campaigns` AS C
         ON I.campaignId=C.campaignId
         LEFT JOIN `{dataset}.DV_Advertisers` AS A
         ON I.advertiserId=A.advertiserId
         LEFT JOIN `{dataset}.DV_Partners` AS P
         ON A.partnerId=P.partnerId
         UNION ALL
         SELECT
           CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,
           CONCAT(A.displayName, ' - ', A.advertiserId) AS Adveriser,
           CONCAT(C.displayName, ' - ', C.campaignId) AS Campaign,
           CONCAT(I.displayName, ' - ', I.insertionOrderId) AS InsertionOrder,
           CONCAT(L.displayName, ' - ', L.lineItemId) AS LineItem,
           CONCAT(REGEXP_REPLACE(PC.feeType, r'^PARTNER_COST_FEE_TYPE_(.*)_FEE', '\\\\1'),' ', ROW_NUMBER() OVER (PARTITION BY L.lineItemId, PC.feeType ORDER BY PO)) AS Index,
           PC.costType AS costType,
           PC.costType AS costType_Edit,
           PC.feeType AS feeType,
           PC.feeType AS feeType_Edit,
           PC.invoiceType AS invoiceType,
           PC.invoiceType AS invoiceType_Edit,
           PC.feeAmount / 1000000 AS feeAmount,
           PC.feeAmount / 1000000 AS feeAmount_Edit,
           PC.feePercentageMillis / 1000 AS feePercentageMillis,
           PC.feePercentageMillis / 1000 AS feePercentageMillis_Edit
         FROM `{dataset}.DV_LineItems` AS L, UNNEST(partnerCosts) AS PC WITH OFFSET AS PO
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
        "legacy":False
      }}
    )
  )


def partner_cost_audit(config, task):
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_PartnerCosts",
      "schema": [
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "Campaign", "type": "STRING" },
        { "name": "Insertion_Order", "type": "STRING" },
        { "name": "Line_Item", "type": "STRING" },
        { "name": "Label", "type": "STRING" },
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
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Partner Costs",
        "header":False,
        "range": "A2:P"
      }}
    )
  )

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "AUDIT_PartnerCosts",
    """WITH
      /* Check if sheet values are set */ INPUT_ERRORS AS (
      SELECT
        *
      FROM (
        SELECT
          'Partner Costs' AS Operation,
          CASE
            WHEN Cost_Type_Edit IS NULL THEN 'Missing Cost Type.'
            WHEN Fee_Type_Edit IS NULL THEN 'Missing Fee Type.'
            WHEN Invoice_Type_Edit IS NULL THEN 'Missing Invoice Type.'
            WHEN Fee_Amount_Edit IS NULL
          AND Fee_Percent_Edit IS NULL THEN 'You must select a Fee Amount OR Fee Percent'
          ELSE IF
          (Fee_Amount_Edit IS NOT NULL
            AND Fee_Percent_Edit IS NOT NULL,
            'You must select a Fee Amount OR Fee Percent, not both',
            NULL)
        END
          AS Error,
          'ERROR' AS Severity,
          COALESCE(Line_Item,
            Insertion_Order,
            'BLANK') AS Id
        FROM
          `{dataset}.SHEET_PartnerCosts` )
      WHERE
        Error IS NOT NULL )
    SELECT
      *
    FROM
      INPUT_ERRORS ;
    """.format(**task),
    legacy=False
  )

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PATCH_PartnerCosts",
    """SELECT *
      FROM `{dataset}.SHEET_PartnerCosts`
      WHERE (
        REGEXP_CONTAINS(Insertion_Order, r" - (\d+)$")
        OR REGEXP_CONTAINS(Line_Item, r" - (\d+)$")
      )
      AND Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_PartnerCosts` WHERE Severity='ERROR')
      AND Insertion_Order NOT IN (SELECT Id FROM `{dataset}.AUDIT_PartnerCosts` WHERE Severity='ERROR')
      ORDER BY Insertion_Order, Line_Item, Label
    """.format(**task),
    legacy=False
  )


def partner_cost_patch(config, task, commit=False):
  patches = {}
  changed = set()

  rows = get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"PATCH_PartnerCosts",
    }},
    as_object=True
  )

  for row in rows:

    lookup = row['Line_Item'] or row['Insertion_Order']

    patches.setdefault(
      lookup,
      { "operation": "Partner Costs",
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
      }
    )

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
  patch_preview(config, task, patches)

  if commit:
    insertion_order_commit(config, task, patches)
    line_item_commit(config, task, patches)
