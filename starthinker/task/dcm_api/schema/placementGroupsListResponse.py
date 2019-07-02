###########################################################################
#
#  Copyright 2019 Google Inc.
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

placementGroupsListResponse_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "nextPageToken"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "comment"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "primaryPlacementId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "campaignId"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "advertiserId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "directorySiteId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "PLACEMENT_PACKAGE, PLACEMENT_ROADBLOCK", 
        "name": "placementGroupType"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "id"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "accountId"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "archived", 
        "mode": "NULLABLE"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "childPlacementIds"
        }, 
        "type": "RECORD", 
        "name": "childPlacementIds", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "contentCategoryId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "externalId"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "time"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "siteId"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "placementStrategyId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "subaccountId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "name"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "time"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "startDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "endDate"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "flighted", 
          "mode": "NULLABLE"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "disregardOverdelivery", 
          "mode": "NULLABLE"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "CAP_COST_CUMULATIVE, CAP_COST_MONTHLY, CAP_COST_NONE", 
          "name": "capCostOption"
        }, 
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "units"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "rateOrCostNanos"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "DATE", 
              "description": "", 
              "name": "startDate"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "DATE", 
              "description": "", 
              "name": "endDate"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "pricingComment"
            }
          ], 
          "type": "RECORD", 
          "name": "pricingPeriods", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "PRICING_TYPE_CPA, PRICING_TYPE_CPC, PRICING_TYPE_CPM, PRICING_TYPE_CPM_ACTIVEVIEW, PRICING_TYPE_FLAT_RATE_CLICKS, PRICING_TYPE_FLAT_RATE_IMPRESSIONS", 
          "name": "pricingType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "testingStartDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "floodlightActivityId"
        }
      ]
    ], 
    "type": "RECORD", 
    "name": "placementGroups", 
    "mode": "REPEATED"
  }
]
