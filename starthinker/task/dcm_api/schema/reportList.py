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

reportList_Schema = [{
    'description': '',
    'name': 'etag',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'items',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description': '',
        'name': 'accountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name':
            'criteria',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [[{
            'name':
                'filters',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
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
            }]
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'metricNames',
            'type': 'STRING',
            'mode': 'REPEATED'
        }],
                   [{
                       'name':
                           'filteredEventIds',
                       'type':
                           'RECORD',
                       'mode':
                           'REPEATED',
                       'fields': [{
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
                       }]
                   }, {
                       'description': '',
                       'name': 'kind',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }],
                   [{
                       'description': '',
                       'name': 'endDate',
                       'type': 'DATE',
                       'mode': 'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'kind',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }, {
                       'description':
                           'LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, '
                           'LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, '
                           'LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, '
                           'PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, '
                           'QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, '
                           'YEAR_TO_DATE, YESTERDAY',
                       'name':
                           'relativeDateRange',
                       'type':
                           'STRING',
                       'mode':
                           'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'startDate',
                       'type': 'DATE',
                       'mode': 'NULLABLE'
                   }], {
                       'name':
                           'dimensionFilters',
                       'type':
                           'RECORD',
                       'mode':
                           'REPEATED',
                       'fields': [{
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
                       }]
                   }, {
                       'name':
                           'dimensions',
                       'type':
                           'RECORD',
                       'mode':
                           'REPEATED',
                       'fields': [{
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
                           'description': 'ASCENDING, DESCENDING',
                           'name': 'sortOrder',
                           'type': 'STRING',
                           'mode': 'NULLABLE'
                       }]
                   }, {
                       'name': 'metricNames',
                       'type': 'STRING',
                       'mode': 'REPEATED'
                   }]
    }, {
        'name':
            'crossDimensionReachCriteria',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name':
                    'breakdown',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'description': '',
                        'name': 'kind',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'name',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': 'ASCENDING, DESCENDING',
                        'name': 'sortOrder',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    }
                ]
            },
            [{
                'description':
                    '',
                'name': 'endDate',
                'type': 'DATE',
                'mode': 'NULLABLE'
            }, {
                'description':
                    '',
                'name':
                    'kind',
                'type':
                    'STRING',
                'mode': 'NULLABLE'
            }, {
                'description':
                    'LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, '
                    'LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, '
                    'MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, '
                    'PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, '
                    'WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY',
                'name':
                    'relativeDateRange',
                'type':
                    'STRING',
                'mode':
                    'NULLABLE'
            }, {
                'description': '',
                'name': 'startDate',
                'type': 'DATE',
                'mode': 'NULLABLE'
            }], {
                'description':
                    'ADVERTISER, CAMPAIGN, SITE_BY_ADVERTISER, SITE_BY_CAMPAIGN',
                'name':
                    'dimension',
                'type':
                    'STRING',
                'mode':
                    'NULLABLE'
            }, {
                'name':
                    'dimensionFilters',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [{
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
                }]
            }, {
                'name': 'metricNames',
                'type': 'STRING',
                'mode': 'REPEATED'
            }, {
                'name': 'overlapMetricNames',
                'type': 'STRING',
                'mode': 'REPEATED'
            }, {
                'name': 'pivoted',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE'
            }
        ]
    }, {
        'name':
            'delivery',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [{
            'name': 'emailOwner',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': 'ATTACHMENT, LINK',
            'name': 'emailOwnerDeliveryType',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'message',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name':
                'recipients',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
                'description': 'ATTACHMENT, LINK',
                'name': 'deliveryType',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'email',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'kind',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }]
        }]
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'fileName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name':
            'floodlightCriteria',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name':
                    'customRichMediaEvents',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'description': '',
                        'name': 'dimensionName',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'etag',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'id',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'kind',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description':
                            'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
                        'name':
                            'matchType',
                        'type':
                            'STRING',
                        'mode':
                            'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'value',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    }
                ]
            },
            [{
                'description':
                    '',
                'name': 'endDate',
                'type': 'DATE',
                'mode': 'NULLABLE'
            }, {
                'description':
                    '',
                'name':
                    'kind',
                'type':
                    'STRING',
                'mode': 'NULLABLE'
            }, {
                'description':
                    'LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, '
                    'LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, '
                    'MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, '
                    'PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, '
                    'WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY',
                'name':
                    'relativeDateRange',
                'type':
                    'STRING',
                'mode':
                    'NULLABLE'
            }, {
                'description': '',
                'name': 'startDate',
                'type': 'DATE',
                'mode': 'NULLABLE'
            }], {
                'name':
                    'dimensionFilters',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [{
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
                }]
            }, {
                'name':
                    'dimensions',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [{
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
                    'description': 'ASCENDING, DESCENDING',
                    'name': 'sortOrder',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }]
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
                'name': 'metricNames',
                'type': 'STRING',
                'mode': 'REPEATED'
            }, {
                'name':
                    'reportProperties',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [{
                    'name': 'includeAttributedIPConversions',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'includeUnattributedCookieConversions',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'includeUnattributedIPConversions',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }]
            }
        ]
    }, {
        'description': 'CSV, EXCEL',
        'name': 'format',
        'type': 'STRING',
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
        'name': 'lastModifiedTime',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'ownerProfileId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name':
            'pathToConversionCriteria',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name':
                    'activityFilters',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'description': '',
                        'name': 'dimensionName',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'etag',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'id',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'kind',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    },
                    {
                        'description':
                            'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
                        'name':
                            'matchType',
                        'type':
                            'STRING',
                        'mode':
                            'NULLABLE'
                    },
                    {
                        'description': '',
                        'name': 'value',
                        'type': 'STRING',
                        'mode': 'NULLABLE'
                    }
                ]
            }, {
                'name':
                    'conversionDimensions',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields':
                    [
                        {
                            'description': '',
                            'name': 'kind',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': '',
                            'name': 'name',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': 'ASCENDING, DESCENDING',
                            'name': 'sortOrder',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        }
                    ]
            }, {
                'name':
                    'customFloodlightVariables',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields':
                    [
                        {
                            'description': '',
                            'name': 'kind',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': '',
                            'name': 'name',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': 'ASCENDING, DESCENDING',
                            'name': 'sortOrder',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        }
                    ]
            }, {
                'name':
                    'customRichMediaEvents',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields':
                    [
                        {
                            'description': '',
                            'name': 'dimensionName',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': '',
                            'name': 'etag',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': '',
                            'name': 'id',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description': '',
                            'name': 'kind',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                        {
                            'description':
                                'BEGINS_WITH, CONTAINS, EXACT, '
                                'WILDCARD_EXPRESSION',
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
                        }
                    ]
            },
            [{
                'description':
                    '',
                'name': 'endDate',
                'type': 'DATE',
                'mode': 'NULLABLE'
            }, {
                'description':
                    '',
                'name':
                    'kind',
                'type':
                    'STRING',
                'mode': 'NULLABLE'
            }, {
                'description':
                    'LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, '
                    'LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, '
                    'MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, '
                    'PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, '
                    'WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY',
                'name':
                    'relativeDateRange',
                'type':
                    'STRING',
                'mode':
                    'NULLABLE'
            }, {
                'description': '',
                'name': 'startDate',
                'type': 'DATE',
                'mode': 'NULLABLE'
            }],
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
                'name': 'metricNames',
                'type': 'STRING',
                'mode': 'REPEATED'
            }, {
                'name':
                    'perInteractionDimensions',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [{
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
                    'description': 'ASCENDING, DESCENDING',
                    'name': 'sortOrder',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }]
            }, {
                'name':
                    'reportProperties',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [{
                    'description': '',
                    'name': 'clicksLookbackWindow',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'impressionsLookbackWindow',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'includeAttributedIPConversions',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'includeUnattributedCookieConversions',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'includeUnattributedIPConversions',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'maximumClickInteractions',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'maximumImpressionInteractions',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'maximumInteractionGap',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'pivotOnInteractionPath',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }]
            }
        ]
    }, {
        'name':
            'reachCriteria',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [[{
            'name':
                'filters',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
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
            }]
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'metricNames',
            'type': 'STRING',
            'mode': 'REPEATED'
        }],
                   [{
                       'name':
                           'filteredEventIds',
                       'type':
                           'RECORD',
                       'mode':
                           'REPEATED',
                       'fields': [{
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
                       }]
                   }, {
                       'description': '',
                       'name': 'kind',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }],
                   [{
                       'description': '',
                       'name': 'endDate',
                       'type': 'DATE',
                       'mode': 'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'kind',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }, {
                       'description':
                           'LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, '
                           'LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, '
                           'LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, '
                           'PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, '
                           'QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, '
                           'YEAR_TO_DATE, YESTERDAY',
                       'name':
                           'relativeDateRange',
                       'type':
                           'STRING',
                       'mode':
                           'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'startDate',
                       'type': 'DATE',
                       'mode': 'NULLABLE'
                   }], {
                       'name':
                           'dimensionFilters',
                       'type':
                           'RECORD',
                       'mode':
                           'REPEATED',
                       'fields': [{
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
                       }]
                   }, {
                       'name':
                           'dimensions',
                       'type':
                           'RECORD',
                       'mode':
                           'REPEATED',
                       'fields': [{
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
                           'description': 'ASCENDING, DESCENDING',
                           'name': 'sortOrder',
                           'type': 'STRING',
                           'mode': 'NULLABLE'
                       }]
                   }, {
                       'name': 'enableAllDimensionCombinations',
                       'type': 'BOOLEAN',
                       'mode': 'NULLABLE'
                   }, {
                       'name': 'metricNames',
                       'type': 'STRING',
                       'mode': 'REPEATED'
                   }, {
                       'name': 'reachByFrequencyMetricNames',
                       'type': 'STRING',
                       'mode': 'REPEATED'
                   }]
    }, {
        'name':
            'schedule',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [{
            'name': 'active',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'every',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'expirationDate',
            'type': 'DATE',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'repeats',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'repeatsOnWeekDays',
            'type': 'STRING',
            'mode': 'REPEATED'
        }, {
            'description': 'DAY_OF_MONTH, WEEK_OF_MONTH',
            'name': 'runsOnDayOfMonth',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'startDate',
            'type': 'DATE',
            'mode': 'NULLABLE'
        }]
    }, {
        'description': '',
        'name': 'subAccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'CROSS_DIMENSION_REACH, FLOODLIGHT, PATH_TO_CONVERSION, REACH, '
            'STANDARD',
        'name':
            'type',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }]
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
