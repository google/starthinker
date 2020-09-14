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

ad_Schema = [
    {
        'description': '',
        'name': 'accountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'active',
        'type': 'BOOLEAN',
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
        'name': 'audienceSegmentId',
        'type': 'INT64',
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
    }],
    [{
        'description': '',
        'name': 'computedClickThroughUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'customClickThroughUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'defaultLandingPage',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'landingPageId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }],
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
        'name': 'comments',
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
    }, [{
        'description': '',
        'name': 'time',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'name':
            'creativeGroupAssignments',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'creativeGroupId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': 'CREATIVE_GROUP_ONE, CREATIVE_GROUP_TWO',
            'name': 'creativeGroupNumber',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    },
    [{
        'name':
            'creativeAssignments',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [
            {
                'name': 'active',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            }, {
                'name': 'applyEventTags',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            },
            [{
                'description': '',
                'name': 'computedClickThroughUrl',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'customClickThroughUrl',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'name': 'defaultLandingPage',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'landingPageId',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }], {
                'name':
                    'companionCreativeOverrides',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [[{
                    'description': '',
                    'name': 'computedClickThroughUrl',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'customClickThroughUrl',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'defaultLandingPage',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'landingPageId',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }], {
                    'description': '',
                    'name': 'creativeId',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }]
            }, {
                'name':
                    'creativeGroupAssignments',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [{
                    'description': '',
                    'name': 'creativeGroupId',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'description': 'CREATIVE_GROUP_ONE, CREATIVE_GROUP_TWO',
                    'name': 'creativeGroupNumber',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }]
            }, {
                'description': '',
                'name': 'creativeId',
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
                'name': 'endTime',
                'type': 'DATETIME',
                'mode': 'NULLABLE'
            }, {
                'name':
                    'richMediaExitOverrides',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [[{
                    'description': '',
                    'name': 'computedClickThroughUrl',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'customClickThroughUrl',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'defaultLandingPage',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'landingPageId',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }], {
                    'name': 'enabled',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'exitId',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }]
            }, {
                'description': '',
                'name': 'sequence',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }, {
                'name': 'sslCompliant',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'startTime',
                'type': 'DATETIME',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'weight',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }
        ]
    }, {
        'description': '',
        'name': 'creativeOptimizationConfigurationId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'CREATIVE_ROTATION_TYPE_RANDOM, CREATIVE_ROTATION_TYPE_SEQUENTIAL',
        'name':
            'type',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description':
            'WEIGHT_STRATEGY_CUSTOM, WEIGHT_STRATEGY_EQUAL, '
            'WEIGHT_STRATEGY_HIGHEST_CTR, WEIGHT_STRATEGY_OPTIMIZED',
        'name':
            'weightCalculationStrategy',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }],
    [{
        'name': 'daysOfWeek',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'name': 'hoursOfDay',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'name': 'userLocalTime',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
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
    }],
    [[{
        'description': '',
        'name': 'duration',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'impressions',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'name': 'hardCutoff',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'impressionRatio',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'AD_PRIORITY_01, AD_PRIORITY_02, AD_PRIORITY_03, AD_PRIORITY_04, '
            'AD_PRIORITY_05, AD_PRIORITY_06, AD_PRIORITY_07, AD_PRIORITY_08, '
            'AD_PRIORITY_09, AD_PRIORITY_10, AD_PRIORITY_11, AD_PRIORITY_12, '
            'AD_PRIORITY_13, AD_PRIORITY_14, AD_PRIORITY_15, AD_PRIORITY_16',
        'name':
            'priority',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }], {
        'name': 'dynamicClickTracker',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'endTime',
        'type': 'DATETIME',
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
    },
    [{
        'name':
            'cities',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'countryCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'countryDartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'dartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'metroCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'metroDmaId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'regionCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'regionDartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'countries',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'countryCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'dartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'sslEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }]
    }, {
        'name': 'excludeCountries',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name':
            'metros',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'countryCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'countryDartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'dartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'dmaId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'metroCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'postalCodes',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'code',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'countryCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'countryDartId',
            'type': 'INT64',
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
        }]
    }, {
        'name':
            'regions',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'countryCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'countryDartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'dartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'regionCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }], {
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
    }],
    [{
        'description': '',
        'name': 'expression',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    [{
        'name':
            'languages',
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
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'languageCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }],
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
        'name':
            'placementAssignments',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'name': 'active',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'placementId',
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
                       'name': 'sslRequired',
                       'type': 'BOOLEAN',
                       'mode': 'NULLABLE'
                   }]
    },
    [{
        'description': '',
        'name': 'expression',
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
        'name': 'sslCompliant',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'sslRequired',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'startTime',
        'type': 'DATETIME',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'subaccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetingTemplateId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'name':
            'browsers',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'browserVersionId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'dartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'majorVersion',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'minorVersion',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'connectionTypes',
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
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'mobileCarriers',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'countryCode',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'countryDartId',
            'type': 'INT64',
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
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'operatingSystemVersions',
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
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'majorVersion',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'minorVersion',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        },
                   [{
                       'description': '',
                       'name': 'dartId',
                       'type': 'INT64',
                       'mode': 'NULLABLE'
                   }, {
                       'name': 'desktop',
                       'type': 'BOOLEAN',
                       'mode': 'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'kind',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }, {
                       'name': 'mobile',
                       'type': 'BOOLEAN',
                       'mode': 'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'name',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }]]
    }, {
        'name':
            'operatingSystems',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'dartId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'name': 'desktop',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'mobile',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'platformTypes',
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
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }], {
        'description':
            'AD_SERVING_CLICK_TRACKER, AD_SERVING_DEFAULT_AD, '
            'AD_SERVING_STANDARD_AD, AD_SERVING_TRACKING',
        'name':
            'type',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }
]
