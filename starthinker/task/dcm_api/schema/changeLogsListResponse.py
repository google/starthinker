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

changeLogsListResponse_Schema = [{
    'name':
        'changeLogs',
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
        'description': '',
        'name': 'action',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'changeTime',
        'type': 'DATETIME',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'fieldName',
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
        'name': 'newValue',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'objectId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'objectType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'oldValue',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'subaccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'transactionId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'userProfileId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'userProfileName',
        'type': 'STRING',
        'mode': 'NULLABLE'
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
