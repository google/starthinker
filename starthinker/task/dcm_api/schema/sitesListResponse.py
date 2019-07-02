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

sitesListResponse_Schema = [
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
            "fields": {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "enabledVideoFormats"
            }, 
            "type": "RECORD", 
            "name": "enabledVideoFormats", 
            "mode": "REPEATED"
          }
        ]
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
          "type": "BOOLEAN", 
          "name": "activeViewOptOut", 
          "mode": "NULLABLE"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "videoActiveViewOptOutTemplate", 
          "mode": "NULLABLE"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "disableNewCookie", 
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
          "type": "STRING", 
          "description": "BOTH, DEFAULT, FLASH, HTML5", 
          "name": "vpaidAdapterChoiceTemplate"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "adBlockingOptOut", 
          "mode": "NULLABLE"
        }
      ], 
      {
        "type": "BOOLEAN", 
        "name": "approved", 
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
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "firstName"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "title"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "lastName"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "address"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "email"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "phone"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "SALES_PERSON, TRAFFICKER", 
            "name": "contactType"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "id"
          }
        ], 
        "type": "RECORD", 
        "name": "siteContacts", 
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
      }
    ], 
    "type": "RECORD", 
    "name": "sites", 
    "mode": "REPEATED"
  }
]
