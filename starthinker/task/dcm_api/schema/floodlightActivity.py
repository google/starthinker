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

floodlightActivity_Schema = [
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
        'description': 'ACTIVE_SERVER_PAGE, COLD_FUSION, JAVASCRIPT, JSP, PHP',
        'name': 'cacheBustingType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ITEMS_SOLD_COUNTING, SESSION_COUNTING, STANDARD_COUNTING, '
            'TRANSACTIONS_COUNTING, UNIQUE_COUNTING',
        'name':
            'countingMethod',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'name':
            'defaultTags',
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
            'description': '',
            'name': 'tag',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'description': '',
        'name': 'expectedUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'floodlightActivityGroupId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'floodlightActivityGroupName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'floodlightActivityGroupTagString',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'COUNTER, SALE',
        'name': 'floodlightActivityGroupType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'floodlightConfigurationId',
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
        'description': 'GLOBAL_SITE_TAG, IFRAME, IMAGE',
        'name': 'floodlightTagType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'hidden',
        'type': 'BOOLEAN',
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
    }, {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'notes',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name':
            'publisherTags',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'name': 'clickThrough',
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
                       'name': 'id',
                       'type': 'INT64',
                       'mode': 'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'name',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }, {
                       'description': '',
                       'name': 'tag',
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
                       'name': 'viewThrough',
                       'type': 'BOOLEAN',
                       'mode': 'NULLABLE'
                   }]
    }, {
        'name': 'secure',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'sslCompliant',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'sslRequired',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'subaccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': 'HTML, XHTML',
        'name': 'tagFormat',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'tagString',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'userDefinedVariableTypes',
        'type': 'STRING',
        'mode': 'REPEATED'
    }
]
