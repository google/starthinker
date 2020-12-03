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
from starthinker.util.google_api import API_DV360
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.patch import patch_clear
from starthinker.task.dv_editor.patch import patch_log
from starthinker.task.dv_editor.patch import patch_masks
from starthinker.task.dv_editor.patch import patch_preview


def line_item_clear():
  table_create(
      project.task["auth_bigquery"],
      project.id,
      project.task["dataset"],
      "DV_LineItems",
      Discovery_To_BigQuery("displayvideo",
                            "v1").method_schema("advertisers.lineItems.list"),
  )

  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Line Items",
               "A2:Z")


def line_item_load():

  # load multiple partners from user defined sheet
  def line_item_load_multiple():
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
          project.task["auth_dv"], iterate=True).advertisers().lineItems().list(
              advertiserId=lookup_id(row[0])).execute()

  # write line_items to database
  put_rows(
      project.task["auth_bigquery"], {
          "bigquery": {
              "dataset":
                  project.task["dataset"],
              "table":
                  "DV_LineItems",
              "schema":
                  Discovery_To_BigQuery(
                      "displayvideo",
                      "v1").method_schema("advertisers.lineItems.list"),
              "format":
                  "JSON"
          }
      }, line_item_load_multiple())

  # write line_items to sheet
  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "query": """SELECT
        CONCAT(P.displayName, ' - ', P.partnerId),
        CONCAT(A.displayName, ' - ', A.advertiserId),
        CONCAT(C.displayName, ' - ', C.campaignId),
        CONCAT(I.displayName, ' - ', I.insertionOrderId),
        CONCAT(L.displayName, ' - ', L.lineItemId),
        'PATCH',
        L.entityStatus,
        ARRAY_TO_STRING(L.warningMessages, '\\n'),

        L.lineItemType,
        L.lineItemType,

        L.flight.flightDateType,
        L.flight.flightDateType,
        CONCAT(L.flight.dateRange.startDate.year, '-', L.flight.dateRange.startDate.month, '-', L.flight.dateRange.startDate.day),
        CONCAT(L.flight.dateRange.startDate.year, '-', L.flight.dateRange.startDate.month, '-', L.flight.dateRange.startDate.day),
        CONCAT(L.flight.dateRange.endDate.year, '-', L.flight.dateRange.endDate.month, '-', L.flight.dateRange.endDate.day),
        CONCAT(L.flight.dateRange.endDate.year, '-', L.flight.dateRange.endDate.month, '-', L.flight.dateRange.endDate.day),
        L.flight.triggerId,
        L.flight.triggerId,

        L.budget.budgetAllocationType,
        L.budget.budgetAllocationType,
        L.budget.budgetUnit,
        L.budget.budgetUnit,
        L.budget.maxAmount / 100000,
        L.budget.maxAmount / 100000,

        L.partnerRevenueModel.markupType,
        L.partnerRevenueModel.markupType,
        CAST(L.partnerRevenueModel.markupAmount AS FLOAT64) / 100000,
        CAST(L.partnerRevenueModel.markupAmount AS FLOAT64) / 100000,

        CAST(L.conversionCounting.postViewCountPercentageMillis AS Float64) / 1000,
        CAST(L.conversionCounting.postViewCountPercentageMillis AS Float64) / 1000,

        L.targetingExpansion.targetingExpansionLevel,
        L.targetingExpansion.targetingExpansionLevel,
        L.targetingExpansion.excludeFirstPartyAudience,
        L.targetingExpansion.excludeFirstPartyAudience,

        FROM `{dataset}.DV_LineItems` AS L
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON L.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON L.advertiserId=C.advertiserId
        LEFT JOIN `{dataset}.DV_InsertionOrders` AS I
        ON L.insertionOrderId=I.insertionOrderId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
      """.format(**project.task),
      "legacy": False
    }}
  )

  put_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Line Items",
      "range": "A2"
    }},
    rows
  )


def line_item_audit():

  rows = get_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Line Items",
      "range": "A2:Z"
    }}
  )

  put_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table": "SHEET_LineItems",
      "schema": [
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "Campaign", "type": "STRING" },
        { "name": "Insertion_Order", "type": "STRING" },
        { "name": "Line_Item", "type": "STRING" },
        { "name": "Action", "type": "STRING" },
        { "name": "Status", "type": "STRING" },
        { "name": "Warning", "type": "STRING" },
        { "name": "Line_Item_Type", "type": "STRING" },
        { "name": "Line_Item_Type_Edit", "type": "STRING" },
        { "name": "Flight_Data_Type", "type": "STRING" },
        { "name": "Flight_Data_Type_Edit", "type": "STRING" },
        { "name": "Flight_Start_Date", "type": "STRING" },
        { "name": "Flight_Start_Date_Edit", "type": "STRING" },
        { "name": "Flight_End_Date", "type": "STRING" },
        { "name": "Flight_End_Date_Edit", "type": "STRING" },
        { "name": "Flight_Trigger", "type": "STRING" },
        { "name": "Flight_Trigger_Edit", "type": "STRING" },
        { "name": "Budget_Allocation_Type", "type": "STRING" },
        { "name": "Budget_Allocation_Type_Edit", "type": "STRING" },
        { "name": "Budget_Unit", "type": "STRING" },
        { "name": "Budget_Unit_Edit", "type": "STRING" },
        { "name": "Budget_Max", "type": "FLOAT" },
        { "name": "Budget_Max_Edit", "type": "FLOAT" },
        { "name": "Partner_Revenue_Model", "type": "STRING" },
        { "name": "Partner_Revenue_Model_Edit", "type": "STRING" },
        { "name": "Partner_Markup", "type": "FLOAT" },
        { "name": "Partner_Markup_Edit", "type": "FLOAT" },
        { "name": "Conversion_Percent", "type": "FLOAT" },
        { "name": "Conversion_Percent_Edit", "type": "FLOAT" },
        { "name": "Targeting_Expansion_Level", "type": "STRING" },
        { "name": "Targeting_Expansion_Level_Edit", "type": "STRING" },
        { "name": "Exclude_1P", "type": "STRING" },
        { "name": "Exclude_1P_Edit", "type": "STRING" },
      ],
      "format": "CSV"
    }},
    rows
  )

  # Create Insert View
  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "INSERT_LineItems",
    """SELECT
      REGEXP_EXTRACT(S_LI.Advertiser, r' - (\d+)$') AS advertiserId,
      REGEXP_EXTRACT(S_LI.Campaign, r' - (\d+)$') AS campaignId,
      REGEXP_EXTRACT(S_LI.Insertion_Order, r' - (\d+)$') AS insertionOrderId,
      S_LI.Line_Item AS displayName,
      S_LI.Line_Item_Type_Edit AS lineItemType,
      'ENTITY_STATUS_DRAFT' AS entityStatus,
      STRUCT(
        S_PC.Cost_Type_Edit As costType,
        S_PC.Fee_Type_Edit As feeType,
        S_PC.Invoice_Type_Edit AS invoiceType,
        S_PC.Fee_Amount_Edit AS feeAmount,
        S_PC.Fee_Percent_Edit * 1000 AS feePercentageMillis
      ) AS partnerCosts,
      STRUCT(
        S_LI.Flight_Data_Type_Edit AS flightDateType,
        STRUCT (
          STRUCT (
            EXTRACT(YEAR FROM CAST(S_LI.Flight_Start_Date_Edit AS Date)) AS year,
            EXTRACT(MONTH FROM CAST(S_LI.Flight_Start_Date_Edit AS DATE)) AS month,
            EXTRACT(DAY FROM CAST(S_LI.Flight_Start_Date_Edit AS DATE)) AS day
          ) AS startDate,
          STRUCT (
            EXTRACT(YEAR FROM CAST(S_LI.Flight_End_Date_Edit AS Date)) AS year,
            EXTRACT(MONTH FROM CAST(S_LI.Flight_End_Date_Edit AS DATE)) AS month,
            EXTRACT(DAY FROM CAST(S_LI.Flight_End_Date_Edit AS DATE)) AS day
          ) AS endDate
        ) AS dateRange,
        S_LI.Flight_Trigger_Edit AS triggerId
      ) AS flight,
      STRUCT(
        S_LI.Budget_Allocation_Type_Edit AS budgetAllocationType,
        S_LI.Budget_Unit_Edit AS budgetUnit,
        S_LI.Budget_Max_Edit * 100000 AS maxAmount
      ) AS budget,
      STRUCT(
        S_P.Period_Edit As pacingPeriod,
        S_P.Type_Edit As pacingType,
        S_P.Daily_Budget_Edit AS dailyMaxMicros,
        S_P.Daily_Impressions_Edit AS dailyMaxImpressions
      ) AS pacing,
      STRUCT(
        S_FC.Unlimited_Edit AS unlimited,
        S_FC.Time_Unit_Edit AS timeUnit,
        S_FC.Time_Count_Edit AS timeUnitCount,
        S_FC.Max_impressions_Edit AS maxImpressions
      ) AS frequencyCap,
      STRUCT(
        S_LI.Partner_Revenue_Model_Edit AS markupType,
        S_LI.Partner_Markup_Edit * 100000 AS markupAmount
      ) AS partnerRevenueModel,
      STRUCT(
        S_LI. Conversion_Percent_Edit * 1000 AS postViewCountPercentageMillis,
        [] AS floodlightActivityConfigs
      ) AS conversionCounting,
      STRUCT(
        IF(S_BS.Fixed_Bid_Edit IS NOT NULL,
          STRUCT(
            S_BS.Fixed_Bid_Edit * 100000 AS bidAmountMicros
          ),
          NULL
        ) AS fixedBid,
        IF(S_BS.Auto_Bid_Goal_Edit IS NOT NULL,
          STRUCT(
            S_BS.Auto_Bid_Goal_Edit AS performanceGoalType,
            S_BS.Auto_Bid_Amount_Edit * 100000 AS maxAverageCpmBidAmountMicros,
            S_BS.Auto_Bid_Algorithm_Edit AS customBiddingAlgorithmId
          ),
          NULL
        ) AS maximizeSpendAutoBid,
        IF(S_BS.Performance_Goal_Type_Edit IS NOT NULL,
          STRUCT(
            S_BS.Performance_Goal_Type_Edit AS performanceGoalType,
            S_BS.Performance_Goal_Amount_Edit * 100000 AS performanceGoalAmountMicros,
            S_BS.Performance_Goal_Average_CPM_Bid_Edit * 100000 AS maxAverageCpmBidAmountMicros,
            S_BS.Performance_Goal_Algorithm_Edit AS customBiddingAlgorithmId
          ),
          NULL
        ) AS performanceGoalAutoBid
      )
      AS bidStrategy,
      STRUCT(
        S_ID.Integration_Code_Edit AS integrationCode,
        S_ID.Details_Edit AS details
      ) AS integrationDetails,
      STRUCT(
        S_LI.Targeting_Expansion_Level_Edit AS targetingExpansionLevel,
        S_LI.Exclude_1P_Edit AS excludeFirstPartyAudience
      ) AS targetingExpansion
    FROM `{dataset}.SHEET_LineItems` AS S_LI
    LEFT JOIN `{dataset}.SHEET_PartnerCosts` AS S_PC ON S_LI.Line_Item=S_PC.Line_Item
    LEFT JOIN `{dataset}.SHEET_Pacing` AS S_P ON S_LI.Line_Item=S_P.Line_Item
    LEFT JOIN `{dataset}.SHEET_FrequencyCaps` AS S_FC ON S_LI.Line_Item=S_FC.Line_Item
    LEFT JOIN `{dataset}.SHEET_IntegrationDetails` AS S_ID ON S_LI.Line_Item=S_ID.Line_Item
    LEFT JOIN `{dataset}.SHEET_BidStrategy` AS S_BS ON S_LI.Line_Item=S_BS.Line_Item
    LEFT JOIN `{dataset}.DV_LineItems` AS DV_LI ON S_LI.Line_Item=DV_LI.displayName
    WHERE S_LI.Action="INSERT"
    AND DV_LI IS NULL
    """.format(**project.task),
    legacy=False
  )

  # Create Audit View
  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "AUDIT_LineItems",
    """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
        *
        FROM (
          SELECT
            'Line Item' AS Operation,
            CASE
              WHEN Budget_Allocation_Type_Edit IS NULL THEN 'Missing Budget Allocation Type.'
              WHEN Budget_Unit_Edit IS NULL THEN 'Missing Budget Unit.'
              WHEN Budget_Max_Edit IS NULL THEN 'Missing Budget Max.'
              WHEN Partner_Revenue_Model_Edit IS NULL THEN 'Missing Partner Revenue Model.'
            ELSE
              NULL
            END AS Error,
            'ERROR' AS Severity,
          COALESCE(Line_Item, 'BLANK') AS Id
        FROM
          `{dataset}.SHEET_LineItems`
        )
        WHERE
          Error IS NOT NULL
      ),
      /* Check duplicate inserts */
      DUPLICATE_ERRORS AS (
        SELECT
          'Line Item' AS Operation,
          'Duplicate Line Item name, insert will be ignored.' AS Error,
          'WARNING' AS Severity,
          COALESCE(S_LI.Line_Item, 'BLANK') AS Id
        FROM `{dataset}.SHEET_LineItems` As S_LI
        LEFT JOIN `{dataset}.DV_LineItems` AS DV_LI ON S_LI.Line_Item=DV_LI.displayName
        WHERE S_LI.Action="INSERT"
        AND DV_LI IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      UNION ALL
      SELECT * FROM DUPLICATE_ERRORS
    """.format(**project.task),
    legacy=False
  )

  query_to_view(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "PATCH_LineItems",
    """SELECT *
      FROM `{dataset}.SHEET_LineItems`
      WHERE Line_Item NOT IN (SELECT Id FROM `{dataset}.AUDIT_LineItems` WHERE Severity='ERROR')
    """.format(**project.task),
    legacy=False
  )


def line_item_patch(commit=False):

  def date_edited(value):
    y, m, d = value.split("-")
    return {"year": y, "month": m, "day": d}

  patches = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"PATCH_LineItems",
    }},
    as_object=True
  )

  for row in rows:

    if row['Action'] == "DELETE":
      patches.append({
        "operation": "Line Items",
        "action": "DELETE",
        "partner": row['Partner'],
        "advertiser": row['Advertiser'],
        "campaign": row['Campaign'],
        "line_item": row['Line_Item'],
        "parameters": {
          "advertiserId": lookup_id(row['Advertiser']),
          "lineItemId": lookup_id(row['Line_Item'])
        }
      })

    elif row['Action'] == "PATCH":
      line_item = {}

      if row['Line_Item_Type'] != row['Line_Item_Type_Edit']:
        line_item["lineItemType"] = row['Line_Item_Type_Edit']

      if row['Flight_Data_Type'] != row['Flight_Data_Type_Edit']:
        line_item.setdefault("flight", {})
        line_item["flight"]["flightDateType"] = row['Flight_Data_Type_Edit']

      if row['Flight_Start_Date'] != row['Flight_Start_Date_Edit']:
        line_item.setdefault("flight", {}).setdefault("dateRange", {})
        line_item["flight"]["dateRange"]["startDate"] = date_edited(row['Flight_Start_Date_Edit'])

      if row['Flight_End_Date'] != row['Flight_End_Date_Edit']:
        line_item.setdefault("flight", {}).setdefault("endDate", {})
        line_item["flight"]["dateRange"]["endDate"] = date_edited(row['Flight_End_Date_Edit'])

      if row['Flight_Trigger'] != row['Flight_Trigger_Edit']:
        line_item.setdefault("flight", {})
        line_item["flight"]["triggerId"] = row['Flight_Trigger_Edit']

      if row['Budget_Allocation_Type'] != row['Budget_Allocation_Type_Edit']:
        line_item.setdefault("budget", {})
        line_item["budget"]["budgetAllocationType"] = row['Budget_Allocation_Type_Edit']

      if row['Budget_Unit'] != row['Budget_Unit_Edit']:
        line_item.setdefault("budget", {})
        line_item["budget"]["budgetUnit"] = row['Budget_Unit_Edit']

      if row['Budget_Max'] != row['Budget_Max_Edit']:
        line_item.setdefault("budget", {})
        line_item["budget"]["maxAmount"] = int(
          float(row['Budget_Max_Edit']) * 100000
        )

      if row['Partner_Revenue_Model'] != row['Partner_Revenue_Model_Edit']:
        line_item.setdefault("partnerRevenueModel", {})
        line_item["partnerRevenueModel"]["markupType"] = row['Partner_Revenue_Model_Edit']

      if row['Partner_Markup'] != row['Partner_Markup_Edit']:
        line_item.setdefault("partnerRevenueModel", {})
        line_item["partnerRevenueModel"]["markupAmount"] = int(
          float(row['Partner_Markup_Edit']) * 100000
        )

      if row['Conversion_Percent'] != row['Conversion_Percent_Edit']:
        line_item.setdefault("conversionCounting", {})
        line_item["conversionCounting"]["postViewCountPercentageMillis"] = int(
          float(row['Conversion_Percent_Edit']) * 1000
        )

      if row['Targeting_Expansion_Level'] != row['Targeting_Expansion_Level_Edit']:
        line_item.setdefault("targetingExpansion", {})
        line_item["targetingExpansion"]["targetingExpansionLevel"] = row['Targeting_Expansion_Level_Edit']

      if row['Exclude_1P'] != row['Exclude_1P_Edit']:
        line_item.setdefault("targetingExpansion", {})
        line_item["targetingExpansion"]["excludeFirstPartyAudience"] = row['Exclude_1P_Edit']

      if line_item:
        patches.append({
          "operation": "Line Items",
          "action": "PATCH",
          "partner": row['Partner'],
          "advertiser": row['Advertiser'],
          "campaign": row['Campaign'],
          "line_item": row['Line_Item'],
          "parameters": {
            "advertiserId": lookup_id(row['Advertiser']),
            "lineItemId": lookup_id(row['Line_Item']),
            "body": line_item
          }
        })

  patch_masks(patches)

  if commit:
    line_item_commit(patches)
  else:
    patch_preview(patches)


def line_item_insert(commit=False):
  inserts = []

  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table":"INSERT_LineItems",
    }},
    as_object=True
  )

  for row in rows:
    inserts.append({
      "operation": "Line Items",
      "action": "INSERT",
      "partner": None,
      "advertiser": row['advertiserId'],
      "campaign": row['campaignId'],
      "line_item": row['displayName'],
      "parameters": {
        "advertiserId": row['advertiserId'],
        "body":row
      }
    })

  if commit:
    line_item_commit(inserts)
  else:
    patch_preview(inserts)


def line_item_commit(patches):
  for patch in patches:
    if not patch.get("line_item"):
      continue
    print("API LINE ITEM:", patch["action"], patch["line_item"])
    try:
      if patch["action"] == "DELETE":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().lineItems().delete(
          **patch["parameters"]
        ).execute()
        patch["success"] = response
      elif patch["action"] == "PATCH":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().lineItems().patch(
          **patch["parameters"]
        ).execute()
        patch["success"] = response["lineItemId"]
      elif patch["action"] == "INSERT":
        response = API_DV360(
          project.task["auth_dv"]
        ).advertisers().lineItems().create(
          **patch["parameters"]
        ).execute()
        patch["success"] = response["lineItemId"]
    except Exception as e:
      patch["error"] = str(e)
    finally:
      patch_log(patch)
  patch_log()
