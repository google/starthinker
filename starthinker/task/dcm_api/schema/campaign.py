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

campaign_Schema = [{
    'name': 'externalId',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'billingInvoiceCode',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'additionalCreativeOptimizationConfigurations',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name':
            'optimizationActivitys',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'name':
                'floodlightActivityIdDimensionValue',
            'type':
                'RECORD',
            'mode':
                'NULLABLE',
            'fields': [{
                'name': 'value',
                'type': 'INTEGER',
                'mode': 'NULLABLE'
            }, {
                'name': 'etag',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'name': 'kind',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'name': 'dimensionName',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }]
        }, {
            'name': 'weight',
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }, {
            'name': 'floodlightActivityId',
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }]
    }, {
        'name': 'optimizationModel',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'advertiserGroupId',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name':
        'audienceSegmentGroups',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'name':
            'audienceSegments',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'allocation',
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }, {
            'name': 'id',
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }]
    }, {
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'comment',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'archived',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'name': 'subaccountId',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name':
        'adBlockingConfiguration',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'name': 'creativeBundleId',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'clickThroughUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'overrideClickThroughUrl',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'enabled',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'nielsenOcrEnabled',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'name': 'lastModifiedInfo',
    'type': 'RECORD',
    'mode': 'NULLABLE',
    'fields': [{
        'name': 'time',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'creativeGroupIds',
    'type': 'INTEGER',
    'mode': 'REPEATED'
}, {
    'name':
        'advertiserIdDimensionValue',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'name': 'value',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}, {
    'name':
        'idDimensionValue',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'name': 'value',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'createInfo',
    'type': 'RECORD',
    'mode': 'NULLABLE',
    'fields': [{
        'name': 'time',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'creativeOptimizationConfiguration',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'name':
            'optimizationActivitys',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'name':
                'floodlightActivityIdDimensionValue',
            'type':
                'RECORD',
            'mode':
                'NULLABLE',
            'fields': [{
                'name': 'value',
                'type': 'INTEGER',
                'mode': 'NULLABLE'
            }, {
                'name': 'etag',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'name': 'kind',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'name': 'dimensionName',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }]
        }, {
            'name': 'weight',
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }, {
            'name': 'floodlightActivityId',
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }]
    }, {
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'optimizationModel',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'endDate',
    'type': 'DATE',
    'mode': 'NULLABLE',
    'description': '%E4Y-%m-%d'
}, {
    'name': 'defaultLandingPageId',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name':
        'defaultClickThroughEventTagProperties',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'name': 'defaultClickThroughEventTagId',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'overrideInheritedEventTag',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }]
}, {
    'name':
        'clickThroughUrlSuffixProperties',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'name': 'clickThroughUrlSuffix',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'overrideInheritedSuffix',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'advertiserId',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'startDate',
    'type': 'DATE',
    'mode': 'NULLABLE',
    'description': '%E4Y-%m-%d'
}, {
    'name': 'name',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'accountId',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name':
        'eventTagOverrides',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'name': 'enabled',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}]
