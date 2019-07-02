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

inventoryItemsListResponse_Schema = [
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
        "type": "INT64", 
        "description": "", 
        "name": "orderId"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "PLANNING_PLACEMENT_GROUP_TYPE_PACKAGE, PLANNING_PLACEMENT_GROUP_TYPE_ROADBLOCK", 
          "name": "groupType"
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
          "description": "PLANNING_PLACEMENT_PRICING_TYPE_CLICKS, PLANNING_PLACEMENT_PRICING_TYPE_CPA, PLANNING_PLACEMENT_PRICING_TYPE_CPC, PLANNING_PLACEMENT_PRICING_TYPE_CPM, PLANNING_PLACEMENT_PRICING_TYPE_CPM_ACTIVEVIEW, PLANNING_PLACEMENT_PRICING_TYPE_FLAT_RATE_CLICKS, PLANNING_PLACEMENT_PRICING_TYPE_FLAT_RATE_IMPRESSIONS, PLANNING_PLACEMENT_PRICING_TYPE_IMPRESSIONS", 
          "name": "pricingType"
        }, 
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "rateOrCost"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "DATE", 
              "description": "", 
              "name": "startDate"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "units"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "DATE", 
              "description": "", 
              "name": "endDate"
            }
          ], 
          "type": "RECORD", 
          "name": "flights", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "PLANNING_PLACEMENT_CAP_COST_TYPE_CUMULATIVE, PLANNING_PLACEMENT_CAP_COST_TYPE_MONTHLY, PLANNING_PLACEMENT_CAP_COST_TYPE_NONE", 
          "name": "capCostType"
        }
      ], 
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
        "name": "negotiationChannelId"
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
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "estimatedClickThroughRate"
      }, 
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
        "name": "estimatedConversionRate"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "inPlan", 
        "mode": "NULLABLE"
      }, 
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
        "name": "advertiserId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "siteId"
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
            "name": "linkedPlacementId"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "primary", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "height"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "width"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "PLANNING_PAYMENT_SOURCE_TYPE_AGENCY_PAID, PLANNING_PAYMENT_SOURCE_TYPE_PUBLISHER_PAID", 
            "name": "paymentSourceType"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "APP, APP_INTERSTITIAL, DISPLAY, DISPLAY_INTERSTITIAL, IN_STREAM_AUDIO, IN_STREAM_VIDEO", 
            "name": "compatibility"
          }
        ], 
        "type": "RECORD", 
        "name": "adSlots", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "projectId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "rfpId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "PLANNING_PLACEMENT_TYPE_CREDIT, PLANNING_PLACEMENT_TYPE_REGULAR", 
        "name": "type"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "contentCategoryId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "placementStrategyId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "accountId"
      }
    ], 
    "type": "RECORD", 
    "name": "inventoryItems", 
    "mode": "REPEATED"
  }
]
