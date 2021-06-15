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


def preview_io_clear(config, task):
  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'IO Preview',
    'A2:AC'
  )


def preview_io_load(config, task):

  preview_io_clear(config, task)

  # download IO rules
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_IO_Rules",
      "schema": [
        { "name": "CM_Campaign", "type": "STRING" },
        { "name": "DV_Campaign", "type": "STRING" },
        { "name": "Pacing_Period", "type": "STRING" },
        { "name": "Pacing_Type", "type": "STRING" },
        { "name": "Frequency_Cap_Unlimited", "type": "BOOLEAN" },
        { "name": "Frequency_Cap_Time_Unit", "type": "STRING" },
        { "name": "Frequency_Cap_Time_Unit_Count", "type": "INTEGER" },
        { "name": "Frequency_Cap_Max_Impressions", "type": "INTEGER" },
        { "name": "Performance_Goal_Type", "type": "STRING" },
        { "name": "Budget_Unit", "type": "STRING" },
        { "name": "Budget_Automation_Type", "type": "STRING" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "IO Rules",
        "header":False,
        "range": "A2:K"
      }}
    )
  )

  # create IO preview (main logic)
  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "PREVIEW_IO",
    """WITH
      cm AS (
        SELECT
          CM_C.id AS campaignId,
          NULLIF(CAST(CM_PP.rateOrCostNanos / 1000000000 AS INT64), 0) AS performanceGoalAmount,
          CM_PG.pricingSchedule.startDate AS budgetSegmentStartDate,
          CM_PG.pricingSchedule.endDate AS budgetSegmentEndDate,
          CM_PG.name AS displayName
        FROM `{dataset}.CM_Advertisers` AS CM_A
        LEFT JOIN `{dataset}.CM_Campaigns` AS CM_C
        ON CM_A.Id = CM_C.advertiserId
        LEFT JOIN `{dataset}.CM_Sites` AS CM_S
        ON CM_S.name = 'Google DBM'
        LEFT JOIN `{dataset}.CM_PlacementGroups` CM_PG
        ON CM_PG.advertiserId = CM_C.advertiserId
        AND CM_PG.campaignId = CM_C.Id
        AND CM_PG.siteId = CM_S.id,
        UNNEST(pricingSchedule.pricingPeriods) AS CM_PP
      )

      SELECT
        'PREVIEW' AS action,
        CONCAT(dv_a.displayName, ' - ', dv_a.advertiserId) as DV_Advertiser,
        sheet.DV_Campaign AS DV_Campaign,
        cm.displayName,
        sheet.Pacing_Period AS pacingPeriod,
        sheet.Pacing_Type AS pacingType,
        CAST(NULL AS INT64) AS dailyMaxMicros,
        CAST(NULL AS INT64) dailyMaxImpressions,
        sheet.Frequency_Cap_Unlimited AS frequencyCapUnlimited,
        sheet.Frequency_Cap_Time_Unit AS frequencyCapTimeUnit,
        sheet.Frequency_Cap_Time_Unit_Count AS frequencyCapTimeUnitCount,
        sheet.Frequency_Cap_Max_Impressions AS frequencyCapMaxImpressions,
        sheet.Performance_Goal_Type AS performanceGoalType,
        cm.performanceGoalAmount AS performanceGoalAmount,
        CAST(NULL AS INT64) AS performanceGoalPercentageMicros,
        CAST(NULL AS STRING) AS performanceGoalString,
        sheet.Budget_Unit AS budgetUnit,
        CAST(NULL AS STRING) AS budgetAutomationType,
        CAST(NULL AS INT64) AS budgetSegmentAmount,
        CAST(NULL AS STRING) AS budgetSegmentDescription,
        cm.budgetSegmentStartDate AS budgetSegmentStartDate,
        cm.budgetSegmentEndDate AS budgetSegmentEndDate,
        CAST(NULL AS INT64) AS budgetSegmentCampaignBudgetId,
        0 AS biddingStrategyFixedBid,
        CAST(NULL AS STRING) AS integrationCode,
        CAST(NULL AS STRING) AS integrationDetails
      FROM `{dataset}.SHEET_IO_Rules` as sheet
      LEFT JOIN cm
      ON CAST(REGEXP_EXTRACT(sheet.CM_Campaign, r' - (\d+)$') AS INT64) = cm.campaignId
      LEFT JOIN `{dataset}.DV_Campaigns` AS dv_c
      ON CAST(REGEXP_EXTRACT(sheet.DV_Campaign, r' - (\d+)$') AS INT64) = dv_c.campaignId
      LEFT JOIN `{dataset}.DV_Advertisers` AS dv_a
      ON dv_c.advertiserId = dv_a.advertiserId
    """.format(**task),
    legacy=False
  )

  # create audits
  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "AUDIT_IO",
    """WITH
      /* Check if sheet values are set */
      INPUT_ERRORS AS (
        SELECT
          'IO Rules' AS Operation,
          'Missing Sheet input value.' AS Error,
          'ERROR' AS Severity,
          DV_Advertiser,
          DV_Campaign,
          displayName AS DV_InsertionOrder,
          CAST(NULL AS STRING) AS DV_LineItem
        FROM `{dataset}.PREVIEW_IO`
        WHERE
          displayName IS NULL
          OR pacingPeriod IS NULL
          OR pacingType IS NULL
          OR (dailyMaxMicros IS NULL AND dailyMaxImpressions IS NULL)
          OR frequencyCapUnlimited IS NULL
          OR frequencyCapTimeUnitCount IS NULL
          OR frequencyCapMaxImpressions IS NULL
          OR performanceGoalType IS NULL
          OR (performanceGoalAmount IS NULL AND performanceGoalPercentageMicros IS NULL)
          OR performanceGoalString IS NULL
          OR budgetUnit IS NULL
          OR budgetAutomationType IS NULL
          OR budgetSegmentAmount IS NULL
          OR budgetSegmentStartDate IS NULL
          OR budgetSegmentEndDate IS NULL
          OR biddingStrategyFixedBid IS NULL
      ),

      /* Check if duplicate IO */
      DUPLICATE_ERRORS AS (
        SELECT
          'IO Rules' AS Operation,
          'Duplicate Insertion Order.' AS Error,
          'WARNING' AS Severity,
            DV_R.DV_Advertiser AS DV_Advertiser,
            DV_R.DV_Campaign AS DV_Campaign,
            DV_R.displayName AS DV_InsertionOrder,
            CAST(NULL AS STRING) AS DV_LineItem
        FROM
          `{dataset}.PREVIEW_IO` AS DV_R
        LEFT JOIN (
          SELECT DISTINCT(displayName)
          FROM `{dataset}.DV_InsertionOrders` ) AS DV_IO
        ON DV_R.displayName = DV_IO.displayName
      ),

      /* Check if budget segments are current */
      SEGMENT_ERRORS AS (
        SELECT *
        FROM (
          SELECT
            'IO Rules' AS Operation,
            CASE
              WHEN CAST(budgetSegmentAmount AS INT64) > 1 THEN 'Segment has excessive spend.'
              WHEN budgetSegmentStartDate IS NULL THEN 'Segment missing start date.'
              WHEN budgetSegmentEndDate IS NULL THEN 'Segment missing end date.'
              WHEN CAST(budgetSegmentStartDate AS DATE) < CURRENT_DATE() THEN 'Segment starts in the past.'
              WHEN CAST(budgetSegmentEndDate AS DATE) < CURRENT_DATE() THEN 'Segment ends in the past.'
            ELSE
            NULL
          END
            AS Error,
            'ERROR' AS Severity,
            DV_Advertiser,
            DV_Campaign,
            displayName AS DV_InsertionOrder,
            CAST(NULL AS STRING) AS DV_LineItem
          FROM `{dataset}.PREVIEW_IO`
        )
        WHERE Error IS NOT NULL
      )

      SELECT * FROM INPUT_ERRORS
      UNION ALL
      SELECT * FROM DUPLICATE_ERRORS
      UNION ALL
      SELECT * FROM SEGMENT_ERRORS

    """.format(**task),
    legacy=False
  )

  # write io preview to sheet with audits
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'IO Preview',
      'header':False,
      'range': 'A2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
          A.Severity,
          A.Error,
          P.*
          FROM `{dataset}.PREVIEW_IO` AS P
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
            FROM `{dataset}.AUDIT_IO`
            GROUP BY 1,2,3,4
          ) AS A
          ON P.DV_Advertiser=A.DV_Advertiser
          AND P.DV_Campaign=A.DV_Campaign
          AND P.displayName=A.DV_InsertionOrder
        """.format(**task),
      }}
    )
  )

def preview_io_insert(config, task):

  # download IO Inserts
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_IO_Inserts",
      "schema": [
        { "name": "status", "type": "STRING", "mode": "NULLABLE" },
        { "name": "error", "type": "STRING", "mode": "NULLABLE" },
        { "name": "action", "type": "STRING", "mode": "NULLABLE" },
        { "name": "advertiser", "type": "STRING", "mode": "NULLABLE" },
        { "name": "campaign", "type": "STRING", "mode": "NULLABLE" },
        { "name": "displayName", "type": "STRING", "mode": "NULLABLE" },
        { "name": "pacingPeriod", "type": "STRING", "mode": "NULLABLE" },
        { "name": "pacingType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "dailyMaxMicros", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "dailyMaxImpressions", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "frequencyCapUnlimited", "type": "BOOLEAN", "mode": "NULLABLE" },
        { "name": "frequencyCapTimeUnit", "type": "STRING", "mode": "NULLABLE" },
        { "name": "frequencyCapTimeUnitCount", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "frequencyCapMaxImpressions", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "performanceGoalType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "performanceGoalAmount", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "performanceGoalPercentageMicros", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "performanceGoalString", "type": "STRING", "mode": "NULLABLE" },
        { "name": "budgetUnit", "type": "STRING", "mode": "NULLABLE" },
        { "name": "budgetAutomationType", "type": "STRING", "mode": "NULLABLE" },
        { "name": "budgetSegmentAmount", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "budgetSegmentDescription", "type": "STRING", "mode": "NULLABLE" },
        { "name": "budgetSegmentStartDate", "type": "DATE", "mode": "NULLABLE" },
        { "name": "budgetSegmentEndDate", "type": "DATE", "mode": "NULLABLE" },
        { "name": "budgetSegmentCampaignBudgetId", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "biddingStrategyFixedBid", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "integrationCode", "type": "STRING", "mode": "NULLABLE" },
        { "name": "integrationDetails", "type": "STRING", "mode": "NULLABLE" }
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "IO Preview",
        "header":False,
        "range": "A2:AC"
      }}
    )
  )

  # create insert view
  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "INSERT_IO",
    """
      SELECT
        REGEXP_EXTRACT(advertiser, r' - (\d+)$') AS advertiserId,
        STRUCT(
          REGEXP_EXTRACT(advertiser, r' - (\d+)$') AS advertiserId,
          REGEXP_EXTRACT(campaign, r' - (\d+)$') AS campaignId,
          displayName,
          'ENTITY_STATUS_DRAFT' AS entityStatus,
          STRUCT(
            pacingPeriod,
            pacingType,
            IF(dailyMaxMicros IS NOT NULL,  dailyMaxMicros * 1000000, NULL) AS dailyMaxMicros,
            IF(dailyMaxMicros IS NULL, dailyMaxImpressions, NULL) AS dailyMaxImpressions
          ) AS pacing,
          STRUCT(
            CAST(frequencyCapUnlimited AS bool) AS unlimited,
            frequencyCapTimeUnit AS timeUnit,
            frequencyCapTimeUnitCount AS timeUnitCount,
            frequencyCapMaxImpressions AS maxImpressions
          ) AS frequencyCap,
          STRUCT(
            performanceGoalType,
            CAST(NULLIF(CAST(performanceGoalAmount AS INT64) * 1000000, 0) AS STRING) AS performanceGoalAmountMicros
          ) AS performanceGoal,
          STRUCT(
            budgetUnit,
            budgetAutomationType AS automationType,
            [
              STRUCT(
                IF(
                  budgetSegmentAmount IS NOT NULL,
                  budgetSegmentAmount * 1000000,
                  NULL
                ) AS budgetAmountMicros,
                budgetSegmentDescription AS description,
                STRUCT(
                  STRUCT(
                    EXTRACT(YEAR FROM budgetSegmentStartDate) AS year,
                    EXTRACT(MONTH FROM budgetSegmentStartDate) AS month,
                    EXTRACT(DAY FROM budgetSegmentStartDate) AS day
                  ) AS startDate,
                  STRUCT(
                    EXTRACT(YEAR FROM budgetSegmentEndDate) AS year,
                    EXTRACT(MONTH FROM budgetSegmentEndDate) AS month,
                    EXTRACT(DAY FROM budgetSegmentEndDate) AS day
                  ) AS endDate
                ) AS dateRange,
                budgetSegmentCampaignBudgetId AS campaignBudgetId
              )
            ] AS budgetSegments
          ) AS budget,
          STRUCT(
            STRUCT(
              NULLIF(biddingStrategyFixedBid * 1000000, 0) AS bidAmountMicros
            ) AS fixedBid
          ) AS bidStrategy
        ) AS body
      FROM `{dataset}.SHEET_IO_Inserts`
      WHERE action = 'INSERT'
    """.format(**task),
    legacy=False
  )

  # write IOs to API
  for row in get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"INSERT_IO",
    }},
    as_object=True
  ):
    try:
      response = API_DV360(config, task['auth_dv']).advertisers().insertionOrders().create(**row).execute()
      log_write('IO', row, response['insertionOrderId'], None)
    except Exception as e:
      log_write('IO', row, None, str(e))

  log_write(config)
