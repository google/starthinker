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

IO_WRITE = """SELECT
  COALESCE(CONCAT(name, ' - ', accountId), Rules.Cm_Campaign) AS displayName,
  '' AS entityStatus, /* ENUM: ENTITY_STATUS_DRAFT, ENTITY_STATUS_ACTIVE */
  STRUCT(
    COALESCE(Rules.Pacing_Period, 'ERROR') As pacingPeriod,
    COALESCE(Rules.Pacing_Type, 'ERROR') As pacingType,
    "" AS dailyMaxMicros,
    "" AS dailyMaxImpressions
  ) AS pacing,
  STRUCT(
    true AS unlimited,
    "" AS timeUnit,
    0 AS timeUnitCount,
    0 AS maxImpressions
  ) AS frequencyCap,
  STRUCT(
    "" AS performanceGoalType,
    "" AS performanceGoalAmountMicros,
    "" AS performanceGoalPercentageMicros,
    "" AS performanceGoalString
  ) AS performanceGoal,
  STRUCT(
    "" AS budgetUnit,
    "" AS automationType,
    [
      STRUCT(
       "" AS budgetAmountMicros,
       "" AS description,
       STRUCT (
         STRUCT (
           2020 AS year,
           10 AS month,
           3 AS day
         ) AS startDate,
         STRUCT (
           2020 AS year,
           10 AS month,
           3 AS day
         ) AS endDate
       ) AS dateRange
      )
    ] AS budgetSegments
  ) AS budget,
  STRUCT(
    STRUCT(
      "" AS bidAmountMicros
    ) AS fixedBid,
    STRUCT(
     "" AS performanceGoalType,
     "" AS maxAverageCpmBidAmountMicros,
     "" AS customBiddingAlgorithmId
    ) AS maximizeSpendAutoBid,
    STRUCT(
      "" AS performanceGoalType,
      "" AS performanceGoalAmountMicros,
      "" AS maxAverageCpmBidAmountMicros,
      "" AS customBiddingAlgorithmId
    ) AS performanceGoalAutoBid
  ) AS biddingStrategy
FROM `kenjora-161023.BB_Demo.Rules` As Rules
LEFT JOIN `kenjora-161023.BB_Demo.CM_Campaigns` As CM
ON Rules.Cm_Campaign=CM.name;
"""
