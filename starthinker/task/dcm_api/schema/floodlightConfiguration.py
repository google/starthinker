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

floodlightConfiguration_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "EXCLUDE_NATURAL_SEARCH_CONVERSION_ATTRIBUTION, INCLUDE_NATURAL_SEARCH_CONVERSION_ATTRIBUTION, INCLUDE_NATURAL_SEARCH_TIERED_CONVERSION_ATTRIBUTION", 
    "name": "naturalSearchConversionAttributionOption"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "exposureToConversionEnabled", 
    "mode": "NULLABLE"
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
      "type": "BOOLEAN", 
      "name": "dynamicTagEnabled", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "imageTagEnabled", 
      "mode": "NULLABLE"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "MONDAY, SUNDAY", 
    "name": "firstDayOfWeek"
  }, 
  [
    {
      "type": "BOOLEAN", 
      "name": "omnitureCostDataEnabled", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "omnitureIntegrationEnabled", 
      "mode": "NULLABLE"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "subaccountId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "advertiserId"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "analyticsDataSharingEnabled", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "inAppAttributionTrackingEnabled", 
    "mode": "NULLABLE"
  }, 
  {
    "fields": [
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
        "name": "value"
      }
    ], 
    "type": "RECORD", 
    "name": "thirdPartyAuthenticationTokens", 
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
    "name": "accountId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "NUMBER, STRING", 
        "name": "dataType"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "reportName"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "U1, U10, U100, U11, U12, U13, U14, U15, U16, U17, U18, U19, U2, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U3, U30, U31, U32, U33, U34, U35, U36, U37, U38, U39, U4, U40, U41, U42, U43, U44, U45, U46, U47, U48, U49, U5, U50, U51, U52, U53, U54, U55, U56, U57, U58, U59, U6, U60, U61, U62, U63, U64, U65, U66, U67, U68, U69, U7, U70, U71, U72, U73, U74, U75, U76, U77, U78, U79, U8, U80, U81, U82, U83, U84, U85, U86, U87, U88, U89, U9, U90, U91, U92, U93, U94, U95, U96, U97, U98, U99", 
        "name": "variableType"
      }
    ], 
    "type": "RECORD", 
    "name": "userDefinedVariableConfigurations", 
    "mode": "REPEATED"
  }, 
  [
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "timePercent"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "timeMillis"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "viewabilityPercent"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "audible", 
        "mode": "NULLABLE"
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
      "type": "STRING", 
      "description": "", 
      "name": "name"
    }
  ]
]
