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

campaignsListResponse_Schema = [{
    'name':
        'campaigns',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [
        {
            'description': '',
            'name': 'accountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'clickThroughUrl',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'creativeBundleId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'name': 'enabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        },
         {
             'name': 'overrideClickThroughUrl',
             'type': 'BOOLEAN',
             'mode': 'NULLABLE'
         }], {
             'name':
                 'additionalCreativeOptimizationConfigurations',
             'type':
                 'RECORD',
             'mode':
                 'REPEATED',
             'fields': [{
                 'description': '',
                 'name': 'id',
                 'type': 'INT64',
                 'mode': 'NULLABLE'
             }, {
                 'description': '',
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
                 'fields': [
                     {
                         'description': '',
                         'name': 'floodlightActivityId',
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
                         'description':
                             'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
                         'name':
                             'matchType',
                         'type':
                             'STRING',
                         'mode':
                             'NULLABLE'
                     }, {
                         'description': '',
                         'name': 'value',
                         'type': 'STRING',
                         'mode': 'NULLABLE'
                     }], {
                         'description': '',
                         'name': 'weight',
                         'type': 'INT64',
                         'mode': 'NULLABLE'
                     }
                 ]
             }, {
                 'description':
                     'CLICK, POST_CLICK, POST_CLICK_AND_IMPRESSION, '
                     'POST_IMPRESSION, VIDEO_COMPLETION',
                 'name':
                     'optimizationModel',
                 'type':
                     'STRING',
                 'mode':
                     'NULLABLE'
             }]
         }, {
             'description': '',
             'name': 'advertiserGroupId',
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
                    'description': '',
                    'name': 'allocation',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'id',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'name',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }]
            }, {
                'description': '',
                'name': 'id',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'name',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }]
        }, {
            'description': '',
            'name': 'billingInvoiceCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'clickThroughUrlSuffix',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'overrideInheritedSuffix',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'comment',
            'type': 'STRING',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'time',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'name': 'creativeGroupIds',
            'type': 'INT64',
            'mode': 'REPEATED'
        },
        [{
            'description': '',
            'name': 'id',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
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
            'fields': [
                {
                    'description': '',
                    'name': 'floodlightActivityId',
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
                    'description':
                        'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
                    'name':
                        'matchType',
                    'type':
                        'STRING',
                    'mode':
                        'NULLABLE'
                }, {
                    'description': '',
                    'name': 'value',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }], {
                    'description': '',
                    'name': 'weight',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }
            ]
        }, {
            'description':
                'CLICK, POST_CLICK, POST_CLICK_AND_IMPRESSION, '
                'POST_IMPRESSION, VIDEO_COMPLETION',
            'name':
                'optimizationModel',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }],
        [{
            'description': '',
            'name': 'defaultClickThroughEventTagId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'name': 'overrideInheritedEventTag',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'defaultLandingPageId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'endDate',
            'type': 'DATE',
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
                'description': '',
                'name': 'id',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }]
        }, {
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
        },
        [{
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
            'name': 'nielsenOcrEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'startDate',
            'type': 'DATE',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'subaccountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'name': 'traffickerEmails',
            'type': 'STRING',
            'mode': 'REPEATED'
        }
    ]
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'nextPageToken',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
