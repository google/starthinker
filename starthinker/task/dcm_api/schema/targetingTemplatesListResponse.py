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

targetingTemplatesListResponse_Schema = [{
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
        'targetingTemplates',
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
            'name': 'expression',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'subaccountId',
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
        }]
    ]
}]
