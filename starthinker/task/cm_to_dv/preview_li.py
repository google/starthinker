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
from starthinker.util.google_api import API_DV360
from starthinker.util.sheets import sheets_clear


from starthinker.task.cm_to_dv.log import log_write


def preview_li_clear(config, task):
  sheets_clear(
    task['auth_sheets'],
    task['sheet'],
    'LI Preview',
    'A2:AJ'
  )


def preview_li_load(config, task):

  preview_li_clear(config, task)

  # download LI Rules
  put_rows(
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_LI_Rules",
      "schema": [
        { "name": "CM_Campaign", "type": "STRING" },
        { "name": "DV_Campaign", "type": "STRING" },
        { "name": "Type", "type": "STRING" },
        { "name": "Budget_Allocation", "type": "STRING" },
        { "name": "Pacing_Type", "type": "STRING" },
        { "name": "Pacing_Period", "type": "STRING" },
        { "name": "Pacing_Period_Max_Spend", "type": "INTEGER" },
        { "name": "Pacing_Period_Max_Impressions", "type": "INTEGER" },
        { "name": "Frequency_Cap_Unlimited", "type": "BOOLEAN" },
        { "name": "Frequency_Cap_Time_Unit", "type": "STRING" },
        { "name": "Frequency_Cap_Time_Unit_Count", "type": "INTEGER" },
        { "name": "Frequency_Cap_Max_Impressions", "type": "INTEGER" },
        { "name": "Post_View_Count_Percent", "type": "INTEGER" },
        { "name": "Performance_Goal_Type", "type": "STRING" },
        { "name": "Performance_Goal_Amount", "type": "INTEGER" },
        { "name": "Max_Average_CPM_Amount", "type": "INTEGER" },
        { "name": "Custom_Bidding_Algorithm", "type": "STRING" },
      ],
      "format": "CSV"
    }},
    get_rows(
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "LI Rules",
        "header":False,
        "range": "A2:AQ"
      }}
    )
  )

  # create LI preview ( main logic )
  query_to_view(
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PREVIEW_LI",
    """WITH
      cm AS (
        SELECT
          CM_P.name,
          CM_P.advertiserId,
          CM_C.id AS campaignId,
          CM_C.name AS campaignName,
          CM_P.compatibility,
          CM_PG.pricingSchedule.startDate AS budgetSegmentStartDate,
          CM_PG.pricingSchedule.endDate AS budgetSegmentEndDate,
          NULLIF(CAST(CM_PP.rateOrCostNanos / 1000000000 AS INT64), 0) AS bidAmount,
          CM_PG.name AS ioDisplayName,
          CM_P.name AS liDisplayName
        FROM `{dataset}.CM_PlacementGroups` AS CM_PG, UNNEST(childPlacementIds) AS childPlacementId, UNNEST(CM_PG.pricingSchedule.pricingPeriods) AS CM_PP
        JOIN `{dataset}.CM_Placements` CM_P
        ON childPlacementId = CM_P.id
        JOIN `{dataset}.CM_Campaigns` AS CM_C
        ON CM_P.campaignId = CM_C.id
        JOIN `{dataset}.CM_Sites` AS CM_S
        ON CM_PG.siteId = CM_S.id AND CM_S.name = 'Google DBM'
        WHERE
          pg_ProductCode IS NOT NULL
          AND p_ProductCode IS NOT NULL
      ),

      sheet AS (
        SELECT
          CONCAT(dv_a.displayName, ' - ', dv_a.advertiserid) AS DV_Advertiser,
          sheet.*
        FROM `{dataset}.SHEET_LI_Rules` as sheet
        LEFT JOIN `{dataset}.DV_Campaigns` AS dv_c
        ON CAST(REGEXP_EXTRACT(sheet.DV_Campaign, r' - (\d+)$') AS INT64) = dv_c.campaignId
        LEFT JOIN `{dataset}.DV_Advertisers` AS dv_a
        ON dv_a.advertiserid=dv_c.advertiserId
      ),

      li_flattened AS (
        SELECT
          lineItemId,
          displayName,
          MAX(postViewLookbackWindowDays) AS postViewLookbackWindowDays,
          MAX(postClickLookbackWindowDays) AS postClickLookbackWindowDays,
          ARRAY_TO_STRING(ARRAY_AGG(CAST(floodlightActivityConfig.floodlightActivityId AS STRING) IGNORE NULLS), ",") AS floodlightActivityIds,
          ARRAY_TO_STRING(ARRAY_AGG(CAST(inventorySourceId AS STRING) IGNORE NULLS), ",") AS inventorySourceIds
        FROM `{dataset}.DV_LineItems`
        LEFT JOIN UNNEST(conversionCounting.floodlightActivityConfigs) AS floodlightActivityConfig
        LEFT JOIN UNNEST(inventorySourceIds) AS inventorySourceId
        GROUP BY 1,2
      ),

      io_flattened AS (
        SELECT
          insertionOrderId,
          displayName,
          MIN(DATE(segments.dateRange.startDate.year, segments.dateRange.startDate.month, segments.dateRange.startDate.day)) AS budgetSegmentStartDate,
          MAX(DATE(segments.dateRange.endDate.year, segments.dateRange.endDate.month, segments.dateRange.endDate.day)) AS budgetSegmentEndtDate,
        FROM `{dataset}.DV_InsertionOrders`
        LEFT JOIN UNNEST(budget.budgetSegments) AS segments
        GROUP BY 1,2
      )

      SELECT
        'PREVIEW' AS action,
        sheet.DV_Advertiser,
        sheet.DV_Campaign,
        CONCAT(dv_io.displayName, ' - ', dv_io.insertionOrderId) as DV_InsertionOrder,
        cm.liDisplayName AS displayName,
        sheet.Type AS lineItemType,
        'ENTITY_STATUS_DRAFT' AS entityStatus,
        CAST(NULL AS INT64) AS bidAmount,
        dv_io.budgetSegmentStartDate,
        dv_io.budgetSegmentEndtDate,
        sheet.Budget_Allocation AS lineItemBudgetAllocationType,
        sheet.Pacing_Period AS pacingPeriod,
        sheet.Pacing_Type AS pacingType,
        sheet.Pacing_Period_Max_Spend AS dailyMaxMicros,
        sheet.Pacing_Period_Max_Impressions AS dailyMaxImpressions,
        sheet.Frequency_Cap_Unlimited AS frequencyCapUnlimited,
        sheet.Frequency_Cap_Time_Unit AS frequencyCapTimeUnit,
        sheet.Frequency_Cap_Time_Unit_Count AS frequencyCapTimeUnitCount,
        sheet.Frequency_Cap_Max_Impressions AS frequencyCapMaxImpressions,
        sheet.Post_View_Count_Percent AS postViewCountPercentageMillis,
        90 AS postViewLookbackWindowDays,
        90 AS postClickLookbackWindowDays,
        sheet.Performance_Goal_Type AS biddingStrategyPerformanceGoalType,
        sheet.Performance_Goal_Amount AS performanceGoalAmountMicros,
        sheet.Max_Average_CPM_Amount AS maxAverageCpmBidAmountMicros,
        sheet.Custom_Bidding_Algorithm,
        dv_li.floodlightActivityIds,
        dv_li.inventorySourceIds,
        CAST(NULL AS STRING) AS Partner_Cost_CPM_Fee_Cost_Type,
        CAST(NULL AS STRING) AS Partner_Cost_CPM_Fee_Invoice_Type,
        CAST(NULL AS STRING) AS Partner_Cost_CPM_Fee_Amount,
        CAST(NULL AS STRING) AS Partner_Cost_Media_Fee_Cost_Type,
        CAST(NULL AS STRING) AS Partner_Cost_Media_Fee_Invoice_Type,
        CAST(NULL AS STRING) AS Partner_Cost_Media_Fee_Percent
      FROM sheet
      LEFT JOIN cm
      ON CAST(REGEXP_EXTRACT(sheet.CM_Campaign, r' - (\d+)$') AS INT64) = cm.campaignId
      AND (
        (SPLIT(cm.name,'_')[OFFSET(0)] = 'VID' AND LOWER(SPLIT(sheet.Type , '_')[SAFE_OFFSET(3)]) = 'video')
        OR (NOT SPLIT(cm.name, '_')[OFFSET(0)] = 'VID' AND LOWER(SPLIT(sheet.Type, '_')[SAFE_OFFSET(3)]) = 'display')
      )
      LEFT JOIN io_flattened dv_io
      ON dv_io.displayName = cm.ioDisplayName
      LEFT JOIN li_flattened dv_li
      ON dv_li.displayName = cm.liDisplayName
    """.format(**task),
    legacy=False
  )

  # create audit view
  query_to_view(
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "AUDIT_LI",
    """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
          'LI Rules' AS Operation,
          'Missing Sheet input value.' AS Error,
          'ERROR' AS Severity,
          CAST(NULL AS STRING) AS DV_Advertiser,
          DV_Campaign,
          CAST(NULL AS STRING) AS DV_InsertionOrder,
          CM_Campaign AS DV_LineItem
        FROM `{dataset}.SHEET_LI_Rules`
        WHERE
          CM_Campaign IS NULL
          OR DV_Campaign IS NULL
          OR Type IS NULL
          OR Budget_Allocation IS NULL
          OR Pacing_Period IS NULL
          OR Pacing_Type IS NULL
          OR Pacing_Period_Max_Spend IS NULL
          OR Pacing_Period_Max_Impressions IS NULL
          OR Frequency_Cap_Unlimited IS NULL
          OR Frequency_Cap_Time_Unit IS NULL
          OR Frequency_Cap_Time_Unit_Count IS NULL
          OR Frequency_Cap_Max_Impressions IS NULL
          OR Post_View_Count_Percent IS NULL
          OR Performance_Goal_Type IS NULL
          OR Performance_Goal_Amount IS NULL
          OR Max_Average_CPM_Amount IS NULL
          OR Custom_Bidding_Algorithm IS NULL
      ),

      /* Check if duplicate LI */
      DUPLICATE_ERRORS AS (
        SELECT
          'LI Rules' AS Operation,
          'Duplicate Line Item.' AS Error,
          'WARNING' AS Severity,
           DV_Advertiser,
           DV_Campaign,
           DV_InsertionOrder,
           DV_R.displayName AS DV_LineItem
        FROM
          `{dataset}.PREVIEW_LI` AS DV_R
        LEFT JOIN (
          SELECT
          advertiserId,
          campaignId,
          insertionOrderId,
          displayName
          FROM `{dataset}.DV_LineItems`
          GROUP BY 1,2,3,4
        ) AS DV_LI
        ON DV_R.displayName = DV_LI.displayName
        AND CAST(REGEXP_EXTRACT(DV_R.DV_Campaign, r' - (\d+)$') AS INT64) = DV_LI.campaignId
        AND CAST(REGEXP_EXTRACT(DV_R.DV_InsertionOrder, r' - (\d+)$') AS INT64) = DV_LI.insertionOrderId
      )

      SELECT * FROM INPUT_ERRORS
      UNION ALL
      SELECT * FROM DUPLICATE_ERRORS
    """.format(**task),
    legacy=False
  )

  # write io preview to sheet
  put_rows(
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'LI Preview',
      'header':False,
      'range': 'A2'
    }},
    get_rows(
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
          A.Severity,
          A.Error,
          P.*
          FROM `{dataset}.PREVIEW_LI` AS P
          LEFT JOIN (
            SELECT
              DV_Advertiser,
              DV_Campaign,
              DV_InsertionOrder,
              DV_LineItem,
              CASE
                WHEN 'ERROR' IN UNNEST(ARRAY_AGG(Severity)) THEN 'ERROR'
                WHEN 'WARNING' IN UNNEST(ARRAY_AGG(Severity)) THEN 'WARNING'
                ELSE 'OK'
              END AS Severity,
              ARRAY_TO_STRING(ARRAY_AGG(CONCAT(Severity, ': ', Error)), '\\n') AS Error,
            FROM `{dataset}.AUDIT_LI`
            GROUP BY 1,2,3,4
          ) AS A
          ON P.DV_Advertiser=A.DV_Advertiser
          AND P.DV_Campaign=A.DV_Campaign
          AND P.DV_InsertionOrder=A.DV_InsertionOrder
          AND P.displayName=A.DV_LineItem
        """.format(**task),
      }}
    )
  )


def preview_li_insert(config, task):

  # download IO Inserts
  put_rows(
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_LI_Inserts",
      "schema": [
        { "name": "status", "type": "STRING", "mode": "NULLABLE" },
        { "name": "error", "type": "STRING", "mode": "NULLABLE" },
        { "name": "action", "type": "STRING", "mode": "NULLABLE" },
        { "name": "advertiser", "type": "STRING", "mode": "NULLABLE" },
        { "name": "campaign", "type": "STRING", "mode": "NULLABLE" },
        { "name": "insertionOrder", "type": "STRING", "mode": "NULLABLE" },
        { "name": "displayName", "type": "STRING", "mode": "NULLABLE" },
        { "name": "lineItemType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "entityStatus", "type": "STRING", "mode": "NULLABLE" },
        { "name": "bidAmount", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "budgetSegmentStartDate", "type": "DATE", "mode": "NULLABLE" },
        { "name": "budgetSegmentEndDate", "type": "DATE", "mode": "NULLABLE" },
        { "name": "lineItemBudgetAllocationType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "pacingPeriod", "type": "STRING", "mode": "NULLABLE" },
        { "name": "pacingType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "dailyMaxMicros", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "dailyMaxImpressions", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "frequencyCapUnlimited", "type": "BOOLEAN", "mode": "NULLABLE" },
        { "name": "frequencyCapTimeUnit", "type": "STRING", "mode": "NULLABLE" },
        { "name": "frequencyCapTimeUnitCount", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "frequencyCapMaxImpressions", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "postViewCountPercentageMillis", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "postViewLookbackWindowDays", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "postClickLookbackWindowDays", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "biddingStrategyPerformanceGoalType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "performanceGoalAmountMicros", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "maxAverageCpmBidAmountMicros", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "customBiddingAlgorithm", "type": "STRING", "mode": "NULLABLE" },
        { "name": "floodlightActivityIds", "type": "STRING", "mode": "NULLABLE" },
        { "name": "inventorySourceIds", "type": "STRING", "mode": "NULLABLE" },
        { "name": "partnerCPMFeeCostType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "partnerCPMFeeInvoiceType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "partnerCPMFeeAmount", "type": "FLOAT", "mode": "NULLABLE" },
        { "name": "partnerMediaFeeCostType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "partnerMediaFeeInvoiceType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "partnerMediaFeePercent", "type": "FLOAT", "mode": "NULLABLE" },
      ],
      "format": "CSV"
    }},
    get_rows(
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "LI Preview",
        "header":False,
        "range": "A2:AJ"
      }}
    )
  )

  # create insert view
  query_to_view(
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "INSERT_LI",
    """
      SELECT
        REGEXP_EXTRACT(advertiser, r' - (\d+)$') AS advertiserId,
        STRUCT(
          REGEXP_EXTRACT(advertiser, r' - (\d+)$') AS advertiserId,
          REGEXP_EXTRACT(campaign, r' - (\d+)$') AS campaignId,
          REGEXP_EXTRACT(insertionOrder, r' - (\d+)$') AS insertionOrderId,
          displayName,
          lineItemType,
          entityStatus,
          ARRAY((
            SELECT partnerCost FROM (
              SELECT
              IF(partnerCPMFeeAmount IS NOT NULL,
                STRUCT(
                  'PARTNER_COST_FEE_TYPE_CPM_FEE' AS feeType,
                  partnerCPMFeeCostType AS costType,
                  partnerCPMFeeInvoiceType AS invoiceType,
                  COALESCE(partnerCPMFeeAmount, 0) * 1000000 AS feeAmount
                ), NULL) AS partnerCost
                UNION ALL
                SELECT
              IF(partnerMediaFeePercent IS NOT NULL,
              STRUCT(
                'PARTNER_COST_FEE_TYPE_MEDIA_FEE' AS feeType,
                partnerMediaFeeCostType AS costType,
                partnerMediaFeeInvoiceType AS invoiceType,
                COALESCE(partnerMediaFeePercent, 0) * 1000 AS feePercentageMillis
              ), NULL) AS partnerCost
            ) WHERE partnerCost IS NOT NULL)
          ) AS partnerCosts,
          STRUCT( 'LINE_ITEM_FLIGHT_DATE_TYPE_INHERITED' AS flightDateType ) AS flight,
          STRUCT ( lineItemBudgetAllocationType AS budgetAllocationType ) AS budget,
          STRUCT (
            pacingPeriod,
            pacingType,
            IF(dailyMaxMicros IS NOT NULL, dailyMaxMicros * 1000000, NULL) AS dailyMaxMicros,
            IF(dailyMaxMicros IS NULL, dailyMaxImpressions, NULL) AS dailyMaxImpressions
          ) AS pacing,
          STRUCT ( CAST(frequencyCapUnlimited AS BOOL) AS unlimited,
            frequencyCapTimeUnit AS timeUnit,
            CAST(frequencyCapTimeUnitCount AS INT64) AS timeUnitCount,
            CAST(frequencyCapMaxImpressions AS INT64) AS maxImpressions
          ) AS frequencyCap,
          STRUCT ( 'PARTNER_REVENUE_MODEL_MARKUP_TYPE_TOTAL_MEDIA_COST_MARKUP' AS markupType ) AS partnerRevenueModel,
          STRUCT ( STRUCT ( CAST(bidAmount * 1000000 AS INT64) AS bidAmountMicros ) AS fixedBid ) AS bidStrategy,
          STRUCT(
            postViewCountPercentageMillis AS postViewCountPercentageMillis,
            ARRAY(
              SELECT
                STRUCT(
                  floodlightActivityId,
                  postClickLookbackWindowDays,
                  postViewLookbackWindowDays
                )
                FROM UNNEST(SPLIT(floodlightActivityIds)) AS floodlightActivityId
            ) AS floodlightActivityConfigs
          ) AS conversionCounting
        ) AS body
      FROM `{dataset}.SHEET_LI_Inserts`
      WHERE action = 'INSERT'
    """.format(**task),
    legacy=False
  )

  # write LIs to API
  for row in get_rows(
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"INSERT_LI",
    }},
    as_object=True
  ):
    try:
      response = API_DV360(task['auth_dv']).advertisers().lineItems().create(**row).execute()
      log_write('LI', row, response['lineItemId'], None)
    except Exception as e:
      log_write('LI', row, None, str(e))

  log_write(config)
