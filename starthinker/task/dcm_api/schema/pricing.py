###########################################################################
#
#  Copyright 2020 Google LLC
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

pricing_Schema = [{
    'description':
        'PLANNING_PLACEMENT_CAP_COST_TYPE_CUMULATIVE, '
        'PLANNING_PLACEMENT_CAP_COST_TYPE_MONTHLY, '
        'PLANNING_PLACEMENT_CAP_COST_TYPE_NONE',
    'name':
        'capCostType',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': '',
    'name': 'endDate',
    'type': 'DATE',
    'mode': 'NULLABLE'
}, {
    'name':
        'flights',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description': '',
        'name': 'endDate',
        'type': 'DATE',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'rateOrCost',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'startDate',
        'type': 'DATE',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'units',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }]
}, {
    'description':
        'PLANNING_PLACEMENT_GROUP_TYPE_PACKAGE, '
        'PLANNING_PLACEMENT_GROUP_TYPE_ROADBLOCK',
    'name':
        'groupType',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description':
        'PLANNING_PLACEMENT_PRICING_TYPE_CLICKS, '
        'PLANNING_PLACEMENT_PRICING_TYPE_CPA, '
        'PLANNING_PLACEMENT_PRICING_TYPE_CPC, '
        'PLANNING_PLACEMENT_PRICING_TYPE_CPM, '
        'PLANNING_PLACEMENT_PRICING_TYPE_CPM_ACTIVEVIEW, '
        'PLANNING_PLACEMENT_PRICING_TYPE_FLAT_RATE_CLICKS, '
        'PLANNING_PLACEMENT_PRICING_TYPE_FLAT_RATE_IMPRESSIONS, '
        'PLANNING_PLACEMENT_PRICING_TYPE_IMPRESSIONS',
    'name':
        'pricingType',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': '',
    'name': 'startDate',
    'type': 'DATE',
    'mode': 'NULLABLE'
}]
