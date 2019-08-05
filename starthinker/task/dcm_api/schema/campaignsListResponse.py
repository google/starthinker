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

campaignsListResponse_Schema = [
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
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "clickThroughUrlSuffix"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "overrideInheritedSuffix", 
          "mode": "NULLABLE"
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
        "name": "defaultLandingPageId"
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
        "fields": [
          {
            "type": "BOOLEAN", 
            "name": "enabled", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "id"
          }
        ], 
        "type": "RECORD", 
        "name": "eventTagOverrides", 
        "mode": "REPEATED"
      }, 
      [
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "floodlightActivityId"
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
              "name": "weight"
            }
          ], 
          "type": "RECORD", 
          "name": "optimizationActivitys", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "CLICK, POST_CLICK, POST_CLICK_AND_IMPRESSION, POST_IMPRESSION, VIDEO_COMPLETION", 
          "name": "optimizationModel"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "id"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
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
        "type": "STRING", 
        "name": "traffickerEmails", 
        "mode": "REPEATED"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "archived", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "externalId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "advertiserGroupId"
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
        "name": "billingInvoiceCode"
      }, 
      {
        "type": "INT64", 
        "name": "creativeGroupIds", 
        "mode": "REPEATED"
      }, 
      {
        "fields": [
          {
            "fields": [
              {
                "mode": "NULLABLE", 
                "type": "INT64", 
                "description": "", 
                "name": "floodlightActivityId"
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
                "name": "weight"
              }
            ], 
            "type": "RECORD", 
            "name": "optimizationActivitys", 
            "mode": "REPEATED"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "CLICK, POST_CLICK, POST_CLICK_AND_IMPRESSION, POST_IMPRESSION, VIDEO_COMPLETION", 
            "name": "optimizationModel"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "id"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }
        ], 
        "type": "RECORD", 
        "name": "additionalCreativeOptimizationConfigurations", 
        "mode": "REPEATED"
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
          "type": "BOOLEAN", 
          "name": "overrideInheritedEventTag", 
          "mode": "NULLABLE"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "defaultClickThroughEventTagId"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "creativeBundleId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "clickThroughUrl"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "enabled", 
          "mode": "NULLABLE"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "overrideClickThroughUrl", 
          "mode": "NULLABLE"
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
      {
        "type": "BOOLEAN", 
        "name": "nielsenOcrEnabled", 
        "mode": "NULLABLE"
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
        "fields": [
          {
            "fields": [
              {
                "mode": "NULLABLE", 
                "type": "INT64", 
                "description": "", 
                "name": "allocation"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "INT64", 
                "description": "", 
                "name": "id"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "STRING", 
                "description": "", 
                "name": "name"
              }
            ], 
            "type": "RECORD", 
            "name": "audienceSegments", 
            "mode": "REPEATED"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "id"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }
        ], 
        "type": "RECORD", 
        "name": "audienceSegmentGroups", 
        "mode": "REPEATED"
      }
    ], 
    "type": "RECORD", 
    "name": "campaigns", 
    "mode": "REPEATED"
  }, 
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
  }
]
