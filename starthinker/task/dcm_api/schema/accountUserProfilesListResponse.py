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

accountUserProfilesListResponse_Schema = [{
    'name':
        'accountUserProfiles',
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
            'name': 'active',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'objectIds',
            'type': 'INT64',
            'mode': 'REPEATED'
        }, {
            'description': 'ALL, ASSIGNED, NONE',
            'name': 'status',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }],
        [{
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'objectIds',
            'type': 'INT64',
            'mode': 'REPEATED'
        }, {
            'description': 'ALL, ASSIGNED, NONE',
            'name': 'status',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'comments',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'email',
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
            'name': 'locale',
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
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'objectIds',
            'type': 'INT64',
            'mode': 'REPEATED'
        }, {
            'description': 'ALL, ASSIGNED, NONE',
            'name': 'status',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'subaccountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description':
                'EXTERNAL_TRAFFICKER, INTERNAL_NON_TRAFFICKER, '
                'INTERNAL_TRAFFICKER',
            'name':
                'traffickerType',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description':
                'INTERNAL_ADMINISTRATOR, NORMAL_USER, READ_ONLY_SUPER_USER, '
                'SUPER_USER',
            'name':
                'userAccessType',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        },
        [{
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'name': 'objectIds',
            'type': 'INT64',
            'mode': 'REPEATED'
        }, {
            'description': 'ALL, ASSIGNED, NONE',
            'name': 'status',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'userRoleId',
            'type': 'INT64',
            'mode': 'NULLABLE'
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
