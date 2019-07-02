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

creativeOptimizationConfiguration_Schema = [
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
]
