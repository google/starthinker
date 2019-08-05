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

placement_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "comment"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "videoActiveViewOptOut", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "campaignId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "PLACEMENT_AGENCY_PAID, PLACEMENT_PUBLISHER_PAID", 
    "name": "paymentSource"
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
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "width"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "iab", 
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
        "name": "height"
      }
    ], 
    "type": "RECORD", 
    "name": "additionalSizes", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "keyName"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "directorySiteId"
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
  [
    [
      {
        "type": "BOOLEAN", 
        "name": "skippable", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "offsetPercentage"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "offsetSeconds"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "offsetPercentage"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "offsetSeconds"
        }
      ]
    ], 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "companionsDisabled", 
        "mode": "NULLABLE"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "imageOnly", 
        "mode": "NULLABLE"
      }, 
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "width"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "kind"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "iab", 
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
            "name": "height"
          }
        ], 
        "type": "RECORD", 
        "name": "enabledSizes", 
        "mode": "REPEATED"
      }
    ], 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "ANY, LANDSCAPE, PORTRAIT", 
      "name": "orientation"
    }, 
    [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "type": "INT64", 
        "name": "enabledVideoFormats", 
        "mode": "REPEATED"
      }
    ]
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
    "type": "STRING", 
    "name": "tagFormats", 
    "mode": "REPEATED"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "paymentApproved", 
    "mode": "NULLABLE"
  }, 
  [
    {
      "type": "BOOLEAN", 
      "name": "includeClickThroughUrls", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "includeClickTracking", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "additionalKeyValues"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "GENERATE_SEPARATE_TAG_FOR_EACH_KEYWORD, IGNORE, PLACEHOLDER_WITH_LIST_OF_KEYWORDS", 
      "name": "keywordOption"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "contentCategoryId"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "adBlockingOptOut", 
    "mode": "NULLABLE"
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
      "type": "INT64", 
      "description": "", 
      "name": "width"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "iab", 
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
      "name": "height"
    }
  ], 
  {
    "type": "BOOLEAN", 
    "name": "sslRequired", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ACKNOWLEDGE_ACCEPTANCE, ACKNOWLEDGE_REJECTION, DRAFT, PAYMENT_ACCEPTED, PAYMENT_REJECTED, PENDING_REVIEW", 
    "name": "status"
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
    "type": "BOOLEAN", 
    "name": "primary", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "placementGroupId"
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
    "type": "STRING", 
    "description": "APP, APP_INTERSTITIAL, DISPLAY, DISPLAY_INTERSTITIAL, IN_STREAM_AUDIO, IN_STREAM_VIDEO", 
    "name": "compatibility"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "placementStrategyId"
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
      "name": "clickDuration"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "postImpressionActivitiesDuration"
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
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "BOTH, DEFAULT, FLASH, HTML5", 
    "name": "vpaidAdapterChoice"
  }
]
