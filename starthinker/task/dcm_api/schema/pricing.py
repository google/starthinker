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

pricing_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "PLANNING_PLACEMENT_GROUP_TYPE_PACKAGE, PLANNING_PLACEMENT_GROUP_TYPE_ROADBLOCK", 
    "name": "groupType"
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
    "description": "PLANNING_PLACEMENT_PRICING_TYPE_CLICKS, PLANNING_PLACEMENT_PRICING_TYPE_CPA, PLANNING_PLACEMENT_PRICING_TYPE_CPC, PLANNING_PLACEMENT_PRICING_TYPE_CPM, PLANNING_PLACEMENT_PRICING_TYPE_CPM_ACTIVEVIEW, PLANNING_PLACEMENT_PRICING_TYPE_FLAT_RATE_CLICKS, PLANNING_PLACEMENT_PRICING_TYPE_FLAT_RATE_IMPRESSIONS, PLANNING_PLACEMENT_PRICING_TYPE_IMPRESSIONS", 
    "name": "pricingType"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "rateOrCost"
      }, 
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
        "name": "units"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "DATE", 
        "description": "", 
        "name": "endDate"
      }
    ], 
    "type": "RECORD", 
    "name": "flights", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "PLANNING_PLACEMENT_CAP_COST_TYPE_CUMULATIVE, PLANNING_PLACEMENT_CAP_COST_TYPE_MONTHLY, PLANNING_PLACEMENT_CAP_COST_TYPE_NONE", 
    "name": "capCostType"
  }
]
