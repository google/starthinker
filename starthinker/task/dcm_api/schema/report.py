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

report_Schema = [
  {
    "fields": [
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
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "conversionDimensions", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metricNames"
        }, 
        "type": "RECORD", 
        "name": "metricNames", 
        "mode": "REPEATED"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "startDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
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
          "description": "LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY", 
          "name": "relativeDateRange"
        }
      ], 
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "clicksLookbackWindow"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "pivotOnInteractionPath", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "impressionsLookbackWindow"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "includeUnattributedIPConversions", 
            "mode": "NULLABLE"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "includeUnattributedCookieConversions", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "maximumInteractionGap"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "includeAttributedIPConversions", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "maximumClickInteractions"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "maximumImpressionInteractions"
          }
        ], 
        "type": "RECORD", 
        "name": "reportProperties", 
        "mode": "REQUIRED"
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
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "perInteractionDimensions", 
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
        "type": "RECORD", 
        "name": "activityFilters", 
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
        "type": "RECORD", 
        "name": "customRichMediaEvents", 
        "mode": "REPEATED"
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
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "customFloodlightVariables", 
        "mode": "REPEATED"
      }
    ], 
    "type": "RECORD", 
    "name": "pathToConversionCriteria", 
    "mode": "REQUIRED"
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
    "name": "subAccountId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "name"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "DATE", 
        "description": "", 
        "name": "startDate"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "DAY_OF_MONTH, WEEK_OF_MONTH", 
        "name": "runsOnDayOfMonth"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "every"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "DATE", 
        "description": "", 
        "name": "expirationDate"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "active", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "repeats"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "FRIDAY, MONDAY, SATURDAY, SUNDAY, THURSDAY, TUESDAY, WEDNESDAY", 
          "name": "repeatsOnWeekDays"
        }, 
        "type": "RECORD", 
        "name": "repeatsOnWeekDays", 
        "mode": "REPEATED"
      }
    ], 
    "type": "RECORD", 
    "name": "schedule", 
    "mode": "REQUIRED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CSV, EXCEL", 
    "name": "format"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "ownerProfileId"
  }, 
  {
    "fields": [
      [
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
          "type": "RECORD", 
          "name": "filters", 
          "mode": "REPEATED"
        }, 
        {
          "fields": {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "metricNames"
          }, 
          "type": "RECORD", 
          "name": "metricNames", 
          "mode": "REPEATED"
        }
      ], 
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
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "dimensions", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metricNames"
        }, 
        "type": "RECORD", 
        "name": "metricNames", 
        "mode": "REPEATED"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "startDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
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
          "description": "LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY", 
          "name": "relativeDateRange"
        }
      ], 
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
        "type": "RECORD", 
        "name": "dimensionFilters", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "reachByFrequencyMetricNames"
        }, 
        "type": "RECORD", 
        "name": "reachByFrequencyMetricNames", 
        "mode": "REPEATED"
      }, 
      [
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
          "type": "RECORD", 
          "name": "filteredEventIds", 
          "mode": "REPEATED"
        }
      ], 
      {
        "type": "BOOLEAN", 
        "name": "enableAllDimensionCombinations", 
        "mode": "NULLABLE"
      }
    ], 
    "type": "RECORD", 
    "name": "reachCriteria", 
    "mode": "REQUIRED"
  }, 
  {
    "fields": [
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
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "dimensions", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metricNames"
        }, 
        "type": "RECORD", 
        "name": "metricNames", 
        "mode": "REPEATED"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "startDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
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
          "description": "LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY", 
          "name": "relativeDateRange"
        }
      ], 
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
        "type": "RECORD", 
        "name": "dimensionFilters", 
        "mode": "REPEATED"
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
        "type": "RECORD", 
        "name": "customRichMediaEvents", 
        "mode": "REPEATED"
      }, 
      {
        "fields": [
          {
            "type": "BOOLEAN", 
            "name": "includeUnattributedIPConversions", 
            "mode": "NULLABLE"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "includeUnattributedCookieConversions", 
            "mode": "NULLABLE"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "includeAttributedIPConversions", 
            "mode": "NULLABLE"
          }
        ], 
        "type": "RECORD", 
        "name": "reportProperties", 
        "mode": "REQUIRED"
      }
    ], 
    "type": "RECORD", 
    "name": "floodlightCriteria", 
    "mode": "REQUIRED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "fileName"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "message"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "ATTACHMENT, LINK", 
        "name": "emailOwnerDeliveryType"
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
            "type": "STRING", 
            "description": "ATTACHMENT, LINK", 
            "name": "deliveryType"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "email"
          }
        ], 
        "type": "RECORD", 
        "name": "recipients", 
        "mode": "REPEATED"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "emailOwner", 
        "mode": "NULLABLE"
      }
    ], 
    "type": "RECORD", 
    "name": "delivery", 
    "mode": "REQUIRED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "etag"
  }, 
  {
    "fields": [
      [
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
          "type": "RECORD", 
          "name": "filters", 
          "mode": "REPEATED"
        }, 
        {
          "fields": {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "metricNames"
          }, 
          "type": "RECORD", 
          "name": "metricNames", 
          "mode": "REPEATED"
        }
      ], 
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
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "dimensions", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metricNames"
        }, 
        "type": "RECORD", 
        "name": "metricNames", 
        "mode": "REPEATED"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "startDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
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
          "description": "LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY", 
          "name": "relativeDateRange"
        }
      ], 
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
        "type": "RECORD", 
        "name": "dimensionFilters", 
        "mode": "REPEATED"
      }, 
      [
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
          "type": "RECORD", 
          "name": "filteredEventIds", 
          "mode": "REPEATED"
        }
      ]
    ], 
    "type": "RECORD", 
    "name": "criteria", 
    "mode": "REQUIRED"
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
    "name": "lastModifiedTime"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CROSS_DIMENSION_REACH, FLOODLIGHT, PATH_TO_CONVERSION, REACH, STANDARD", 
    "name": "type"
  }, 
  {
    "fields": [
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
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ASCENDING, DESCENDING", 
            "name": "sortOrder"
          }
        ], 
        "type": "RECORD", 
        "name": "breakdown", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "overlapMetricNames"
        }, 
        "type": "RECORD", 
        "name": "overlapMetricNames", 
        "mode": "REPEATED"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metricNames"
        }, 
        "type": "RECORD", 
        "name": "metricNames", 
        "mode": "REPEATED"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "DATE", 
          "description": "", 
          "name": "startDate"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
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
          "description": "LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY", 
          "name": "relativeDateRange"
        }
      ], 
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
        "type": "RECORD", 
        "name": "dimensionFilters", 
        "mode": "REPEATED"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "pivoted", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "ADVERTISER, CAMPAIGN, SITE_BY_ADVERTISER, SITE_BY_CAMPAIGN", 
        "name": "dimension"
      }
    ], 
    "type": "RECORD", 
    "name": "crossDimensionReachCriteria", 
    "mode": "REQUIRED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "accountId"
  }
]
