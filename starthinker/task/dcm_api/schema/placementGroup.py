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

placementGroup_Schema = [
    {
        'description': '',
        'name': 'accountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'advertiserId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'name': 'archived',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'campaignId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'name': 'childPlacementIds',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'comment',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'contentCategoryId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, [{
        'description': '',
        'name': 'time',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'directorySiteId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'externalId',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, [{
        'description': '',
        'name': 'time',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'PLACEMENT_PACKAGE, PLACEMENT_ROADBLOCK',
        'name': 'placementGroupType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'placementStrategyId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': 'CAP_COST_CUMULATIVE, CAP_COST_MONTHLY, CAP_COST_NONE',
        'name': 'capCostOption',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'disregardOverdelivery',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'endDate',
        'type': 'DATE',
        'mode': 'NULLABLE'
    }, {
        'name': 'flighted',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'floodlightActivityId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name':
            'pricingPeriods',
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
            'name': 'pricingComment',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'rateOrCostNanos',
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
            'PRICING_TYPE_CPA, PRICING_TYPE_CPC, PRICING_TYPE_CPM, '
            'PRICING_TYPE_CPM_ACTIVEVIEW, PRICING_TYPE_FLAT_RATE_CLICKS, '
            'PRICING_TYPE_FLAT_RATE_IMPRESSIONS',
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
    }, {
        'description': '',
        'name': 'testingStartDate',
        'type': 'DATE',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'primaryPlacementId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'siteId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'subaccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }
]
