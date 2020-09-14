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

userRolePermissionsListResponse_Schema = [{
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'userRolePermissions',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description':
            'ACCOUNT_ALWAYS, ACCOUNT_BY_DEFAULT, NOT_AVAILABLE_BY_DEFAULT, '
            'SUBACCOUNT_AND_ACCOUNT_ALWAYS, SUBACCOUNT_AND_ACCOUNT_BY_DEFAULT',
        'name':
            'availability',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
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
        'description': '',
        'name': 'permissionGroupId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }]
}]
