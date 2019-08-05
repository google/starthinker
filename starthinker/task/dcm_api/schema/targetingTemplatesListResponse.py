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

targetingTemplatesListResponse_Schema = [
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
        {
          "type": "BOOLEAN", 
          "name": "userLocalTime", 
          "mode": "NULLABLE"
        }, 
        {
          "type": "INT64", 
          "name": "hoursOfDay", 
          "mode": "REPEATED"
        }, 
        {
          "type": "STRING", 
          "name": "daysOfWeek", 
          "mode": "REPEATED"
        }
      ], 
      [
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
          "name": "platformTypes", 
          "mode": "REPEATED"
        }, 
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "majorVersion"
            }, 
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
              "name": "name"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "id"
            }, 
            [
              {
                "type": "BOOLEAN", 
                "name": "mobile", 
                "mode": "NULLABLE"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "INT64", 
                "description": "", 
                "name": "dartId"
              }, 
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
                "name": "name"
              }, 
              {
                "type": "BOOLEAN", 
                "name": "desktop", 
                "mode": "NULLABLE"
              }
            ], 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "minorVersion"
            }
          ], 
          "type": "RECORD", 
          "name": "operatingSystemVersions", 
          "mode": "REPEATED"
        }, 
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "majorVersion"
            }, 
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
              "name": "name"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "browserVersionId"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dartId"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "minorVersion"
            }
          ], 
          "type": "RECORD", 
          "name": "browsers", 
          "mode": "REPEATED"
        }, 
        {
          "fields": [
            {
              "type": "BOOLEAN", 
              "name": "mobile", 
              "mode": "NULLABLE"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dartId"
            }, 
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
              "name": "name"
            }, 
            {
              "type": "BOOLEAN", 
              "name": "desktop", 
              "mode": "NULLABLE"
            }
          ], 
          "type": "RECORD", 
          "name": "operatingSystems", 
          "mode": "REPEATED"
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
              "name": "countryDartId"
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
              "name": "countryCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "name"
            }
          ], 
          "type": "RECORD", 
          "name": "mobileCarriers", 
          "mode": "REPEATED"
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
          "name": "connectionTypes", 
          "mode": "REPEATED"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "expression"
        }
      ], 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "expression"
        }
      ], 
      [
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "languageCode"
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
          "name": "languages", 
          "mode": "REPEATED"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "advertiserId"
      }, 
      [
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dartId"
            }, 
            {
              "type": "BOOLEAN", 
              "name": "sslEnabled", 
              "mode": "NULLABLE"
            }, 
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
              "name": "countryCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "name"
            }
          ], 
          "type": "RECORD", 
          "name": "countries", 
          "mode": "REPEATED"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "excludeCountries", 
          "mode": "NULLABLE"
        }, 
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "countryDartId"
            }, 
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
              "name": "code"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "id"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "countryCode"
            }
          ], 
          "type": "RECORD", 
          "name": "postalCodes", 
          "mode": "REPEATED"
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
              "name": "countryDartId"
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
              "name": "countryCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "regionCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dartId"
            }
          ], 
          "type": "RECORD", 
          "name": "regions", 
          "mode": "REPEATED"
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
              "name": "countryDartId"
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
              "name": "countryCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "metroCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "regionCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "metroDmaId"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dartId"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "regionDartId"
            }
          ], 
          "type": "RECORD", 
          "name": "cities", 
          "mode": "REPEATED"
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
              "name": "countryDartId"
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
              "name": "countryCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "metroCode"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dmaId"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "dartId"
            }
          ], 
          "type": "RECORD", 
          "name": "metros", 
          "mode": "REPEATED"
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
    "name": "targetingTemplates", 
    "mode": "REPEATED"
  }
]
