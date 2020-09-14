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

sitesListResponse_Schema = [{
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
        'sites',
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
            'name': 'approved',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
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
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name':
                'siteContacts',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
                'description': '',
                'name': 'address',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': 'SALES_PERSON, TRAFFICKER',
                'name': 'contactType',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'email',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'firstName',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'id',
                'type': 'INT64',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'lastName',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'phone',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'title',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }]
        },
        [{
            'name': 'activeViewOptOut',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name': 'adBlockingOptOut',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name': 'disableNewCookie',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
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
             'name': 'videoActiveViewOptOutTemplate',
             'type': 'BOOLEAN',
             'mode': 'NULLABLE'
         }, {
             'description': 'BOTH, DEFAULT, FLASH, HTML5',
             'name': 'vpaidAdapterChoiceTemplate',
             'type': 'STRING',
             'mode': 'NULLABLE'
         }], {
             'description': '',
             'name': 'subaccountId',
             'type': 'INT64',
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
         }]]
    ]
}]
