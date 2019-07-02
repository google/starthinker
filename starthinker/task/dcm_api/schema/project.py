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

project_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "DATE", 
    "description": "", 
    "name": "startDate"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetCpmNanos"
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
    "description": "", 
    "name": "clientBillingCode"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "overview"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetCpaNanos"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "advertiserId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetImpressions"
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
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetCpcNanos"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetCpmActiveViewNanos"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetClicks"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "PLANNING_AUDIENCE_GENDER_FEMALE, PLANNING_AUDIENCE_GENDER_MALE", 
    "name": "audienceGender"
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
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "time"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "budget"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "PLANNING_AUDIENCE_AGE_18_24, PLANNING_AUDIENCE_AGE_25_34, PLANNING_AUDIENCE_AGE_35_44, PLANNING_AUDIENCE_AGE_45_54, PLANNING_AUDIENCE_AGE_55_64, PLANNING_AUDIENCE_AGE_65_OR_MORE, PLANNING_AUDIENCE_AGE_UNKNOWN", 
    "name": "audienceAgeGroup"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetConversions"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "clientName"
  }
]
