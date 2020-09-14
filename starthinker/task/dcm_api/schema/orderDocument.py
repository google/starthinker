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

orderDocument_Schema = [{
    'description': '',
    'name': 'accountId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'advertiserId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'amendedOrderDocumentId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'name': 'approvedByUserProfileIds',
    'type': 'INT64',
    'mode': 'REPEATED'
}, {
    'name': 'cancelled',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, [{
    'description': '',
    'name': 'time',
    'type': 'INT64',
    'mode': 'NULLABLE'
}], {
    'description': '',
    'name': 'effectiveDate',
    'type': 'DATE',
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
    'name': 'lastSentRecipients',
    'type': 'STRING',
    'mode': 'REPEATED'
}, {
    'description': '',
    'name': 'lastSentTime',
    'type': 'DATETIME',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'orderId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'projectId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'name': 'signed',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'subaccountId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'title',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description':
        'PLANNING_ORDER_TYPE_CHANGE_ORDER, PLANNING_ORDER_TYPE_INSERTION_ORDER',
    'name':
        'type',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}]
