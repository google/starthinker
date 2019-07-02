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

targetableRemarketingList_Schema = [
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
