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

remarketingList_Schema = [
  [
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
    "name": "description"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "listSize"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "lifeSpan"
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
    "name": "advertiserId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "REMARKETING_LIST_SOURCE_ADX, REMARKETING_LIST_SOURCE_DBM, REMARKETING_LIST_SOURCE_DFA, REMARKETING_LIST_SOURCE_DFP, REMARKETING_LIST_SOURCE_DMP, REMARKETING_LIST_SOURCE_GA, REMARKETING_LIST_SOURCE_GPLUS, REMARKETING_LIST_SOURCE_OTHER, REMARKETING_LIST_SOURCE_PLAY_STORE, REMARKETING_LIST_SOURCE_XFP, REMARKETING_LIST_SOURCE_YOUTUBE", 
    "name": "listSource"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "active", 
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
]
