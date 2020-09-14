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

eventTagsListResponse_Schema = [{
    'name':
        'eventTags',
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
        }], {
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
            'name': 'enabledByDefault',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name': 'excludeFromAdxRequests',
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
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': 'BLACKLIST, WHITELIST',
            'name': 'siteFilterType',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'siteIds',
            'type': 'INT64',
            'mode': 'REPEATED'
        }, {
            'name': 'sslCompliant',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': 'DISABLED, ENABLED',
            'name': 'status',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'subaccountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description':
                'CLICK_THROUGH_EVENT_TAG, IMPRESSION_IMAGE_EVENT_TAG, '
                'IMPRESSION_JAVASCRIPT_EVENT_TAG',
            'name':
                'type',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description': '',
            'name': 'url',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'urlEscapeLevels',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }
    ]
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
