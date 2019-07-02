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

listPopulationRule_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "floodlightActivityName"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "floodlightActivityId"
  }, 
  {
    "fields": [
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "remarketingListId"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "contains", 
            "mode": "NULLABLE"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "negation", 
            "mode": "NULLABLE"
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
            "name": "variableFriendlyName"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "NUM_EQUALS, NUM_GREATER_THAN, NUM_GREATER_THAN_EQUAL, NUM_LESS_THAN, NUM_LESS_THAN_EQUAL, STRING_CONTAINS, STRING_EQUALS", 
            "name": "operator"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "CUSTOM_VARIABLE_TERM, LIST_MEMBERSHIP_TERM, REFERRER_TERM", 
            "name": "type"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "variableName"
          }
        ], 
        "type": "RECORD", 
        "name": "terms", 
        "mode": "REPEATED"
      }
    ], 
    "type": "RECORD", 
    "name": "listPopulationClauses", 
    "mode": "REPEATED"
  }
]
