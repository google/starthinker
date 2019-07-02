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

creativeRotation_Schema = [
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "weight"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "sequence"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "applyEventTags", 
        "mode": "NULLABLE"
      }, 
      {
        "fields": [
          [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "computedClickThroughUrl"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "customClickThroughUrl"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "landingPageId"
            }, 
            {
              "type": "BOOLEAN", 
              "name": "defaultLandingPage", 
              "mode": "NULLABLE"
            }
          ], 
          {
            "type": "BOOLEAN", 
            "name": "enabled", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "exitId"
          }
        ], 
        "type": "RECORD", 
        "name": "richMediaExitOverrides", 
        "mode": "REPEATED"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "sslCompliant", 
        "mode": "NULLABLE"
      }, 
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "CREATIVE_GROUP_ONE, CREATIVE_GROUP_TWO", 
            "name": "creativeGroupNumber"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "creativeGroupId"
          }
        ], 
        "type": "RECORD", 
        "name": "creativeGroupAssignments", 
        "mode": "REPEATED"
      }, 
      {
        "fields": [
          [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "computedClickThroughUrl"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "customClickThroughUrl"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "landingPageId"
            }, 
            {
              "type": "BOOLEAN", 
              "name": "defaultLandingPage", 
              "mode": "NULLABLE"
            }
          ], 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "creativeId"
          }
        ], 
        "type": "RECORD", 
        "name": "companionCreativeOverrides", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "DATETIME", 
        "description": "", 
        "name": "startTime"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "computedClickThroughUrl"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "customClickThroughUrl"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "landingPageId"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "defaultLandingPage", 
          "mode": "NULLABLE"
        }
      ], 
      {
        "type": "BOOLEAN", 
        "name": "active", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "creativeId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "DATETIME", 
        "description": "", 
        "name": "endTime"
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
    "name": "creativeAssignments", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "WEIGHT_STRATEGY_CUSTOM, WEIGHT_STRATEGY_EQUAL, WEIGHT_STRATEGY_HIGHEST_CTR, WEIGHT_STRATEGY_OPTIMIZED", 
    "name": "weightCalculationStrategy"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "creativeOptimizationConfigurationId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CREATIVE_ROTATION_TYPE_RANDOM, CREATIVE_ROTATION_TYPE_SEQUENTIAL", 
    "name": "type"
  }
]
