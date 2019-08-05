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

floodlightActivitiesListResponse_Schema = [
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
        "name": "tagString"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "secure", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "floodlightActivityGroupName"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "advertiserId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "HTML, XHTML", 
        "name": "tagFormat"
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
        "name": "floodlightActivityGroupId"
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
        "name": "floodlightActivityGroupTagString"
      }, 
      {
        "fields": [
          {
            "type": "BOOLEAN", 
            "name": "viewThrough", 
            "mode": "NULLABLE"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "clickThrough", 
            "mode": "NULLABLE"
          }, 
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
              "name": "tag"
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
          ]
        ], 
        "type": "RECORD", 
        "name": "publisherTags", 
        "mode": "REPEATED"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "sslCompliant", 
        "mode": "NULLABLE"
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
      {
        "type": "BOOLEAN", 
        "name": "hidden", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "accountId"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "sslRequired", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "GLOBAL_SITE_TAG, IFRAME, IMAGE", 
        "name": "floodlightTagType"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "expectedUrl"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "ACTIVE_SERVER_PAGE, COLD_FUSION, JAVASCRIPT, JSP, PHP", 
        "name": "cacheBustingType"
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
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "notes"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "floodlightConfigurationId"
      }, 
      {
        "type": "STRING", 
        "name": "userDefinedVariableTypes", 
        "mode": "REPEATED"
      }, 
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "tag"
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
        "name": "defaultTags", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "ITEMS_SOLD_COUNTING, SESSION_COUNTING, STANDARD_COUNTING, TRANSACTIONS_COUNTING, UNIQUE_COUNTING", 
        "name": "countingMethod"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "COUNTER, SALE", 
        "name": "floodlightActivityGroupType"
      }
    ], 
    "type": "RECORD", 
    "name": "floodlightActivities", 
    "mode": "REPEATED"
  }
]
