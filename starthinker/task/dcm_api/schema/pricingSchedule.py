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

pricingSchedule_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "DATE", 
    "description": "", 
    "name": "startDate"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "DATE", 
    "description": "", 
    "name": "endDate"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "flighted", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "disregardOverdelivery", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CAP_COST_CUMULATIVE, CAP_COST_MONTHLY, CAP_COST_NONE", 
    "name": "capCostOption"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "units"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "rateOrCostNanos"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "DATE", 
        "description": "", 
        "name": "startDate"
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
        "name": "pricingComment"
      }
    ], 
    "type": "RECORD", 
    "name": "pricingPeriods", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "PRICING_TYPE_CPA, PRICING_TYPE_CPC, PRICING_TYPE_CPM, PRICING_TYPE_CPM_ACTIVEVIEW, PRICING_TYPE_FLAT_RATE_CLICKS, PRICING_TYPE_FLAT_RATE_IMPRESSIONS", 
    "name": "pricingType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "DATE", 
    "description": "", 
    "name": "testingStartDate"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "floodlightActivityId"
  }
]
