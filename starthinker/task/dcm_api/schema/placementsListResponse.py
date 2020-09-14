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

placementsListResponse_Schema = [{
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'nextPageToken',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'placements',
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
        }, {
            'name': 'adBlockingOptOut',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name':
                'additionalSizes',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
                'description': '',
                'name': 'height',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }, {
                'name': 'iab',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            },
                       {
                           'description': '',
                           'name': 'id',
                           'type': 'INT64',
                           'mode': 'NULLABLE'
                       }, {
                           'description': '',
                           'name': 'kind',
                           'type': 'STRING',
                           'mode': 'NULLABLE'
                       }, {
                           'description': '',
                           'name': 'width',
                           'type': 'INT64',
                           'mode': 'NULLABLE'
                       }]
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
            'description': '',
            'name': 'comment',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description':
                'APP, APP_INTERSTITIAL, DISPLAY, DISPLAY_INTERSTITIAL, '
                'IN_STREAM_AUDIO, IN_STREAM_VIDEO',
            'name':
                'compatibility',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description': '',
            'name': 'contentCategoryId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        },
        [{
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
            'name': 'keyName',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
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
        }],
        [{
            'description': '',
            'name': 'clickDuration',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'postImpressionActivitiesDuration',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'paymentApproved',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': 'PLACEMENT_AGENCY_PAID, PLACEMENT_PUBLISHER_PAID',
            'name': 'paymentSource',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'placementGroupId',
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
            'name': 'placementStrategyId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        },
        [{
            'description':
                'CAP_COST_CUMULATIVE, CAP_COST_MONTHLY, CAP_COST_NONE',
            'name':
                'capCostOption',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
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
            'name': 'primary',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'time',
            'type': 'INT64',
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
        }],
        [{
            'description': '',
            'name': 'height',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'name': 'iab',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'id',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'width',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'name': 'sslRequired',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description':
                'ACKNOWLEDGE_ACCEPTANCE, ACKNOWLEDGE_REJECTION, DRAFT, '
                'PAYMENT_ACCEPTED, PAYMENT_REJECTED, PENDING_REVIEW',
            'name':
                'status',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description': '',
            'name': 'subaccountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'name': 'tagFormats',
            'type': 'STRING',
            'mode': 'REPEATED'
        },
        [{
            'description': '',
            'name': 'additionalKeyValues',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'includeClickThroughUrls',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name': 'includeClickTracking',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description':
                'GENERATE_SEPARATE_TAG_FOR_EACH_KEYWORD, IGNORE, '
                'PLACEHOLDER_WITH_LIST_OF_KEYWORDS',
            'name':
                'keywordOption',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }], {
            'name': 'videoActiveViewOptOut',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        },
        [[{
            'name': 'companionsDisabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name':
                'enabledSizes',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
                'description': '',
                'name': 'height',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }, {
                'name': 'iab',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'id',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'kind',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'width',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }]
        }, {
            'name': 'imageOnly',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': 'ANY, LANDSCAPE, PORTRAIT',
            'name': 'orientation',
            'type': 'STRING',
            'mode': 'NULLABLE'
        },
         [{
             'description': '',
             'name': 'kind',
             'type': 'STRING',
             'mode': 'NULLABLE'
         },
          [{
              'description': '',
              'name': 'offsetPercentage',
              'type': 'INT64',
              'mode': 'NULLABLE'
          }, {
              'description': '',
              'name': 'offsetSeconds',
              'type': 'INT64',
              'mode': 'NULLABLE'
          }],
          [{
              'description': '',
              'name': 'offsetPercentage',
              'type': 'INT64',
              'mode': 'NULLABLE'
          }, {
              'description': '',
              'name': 'offsetSeconds',
              'type': 'INT64',
              'mode': 'NULLABLE'
          }], {
              'name': 'skippable',
              'type': 'BOOLEAN',
              'mode': 'NULLABLE'
          }],
         [{
             'name': 'enabledVideoFormats',
             'type': 'INT64',
             'mode': 'REPEATED'
         }, {
             'description': '',
             'name': 'kind',
             'type': 'STRING',
             'mode': 'NULLABLE'
         }]], {
             'description': 'BOTH, DEFAULT, FLASH, HTML5',
             'name': 'vpaidAdapterChoice',
             'type': 'STRING',
             'mode': 'NULLABLE'
         }
    ]
}]
