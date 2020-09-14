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

ordersListResponse_Schema = [{
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
        'orders',
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
        'name': 'advertiserId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'approverUserProfileIds',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'buyerInvoiceId',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'buyerOrganizationName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'comments',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name':
            'contacts',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'contactInfo',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'contactName',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'contactTitle',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description':
                'PLANNING_ORDER_CONTACT_BUYER_BILLING_CONTACT, '
                'PLANNING_ORDER_CONTACT_BUYER_CONTACT, '
                'PLANNING_ORDER_CONTACT_SELLER_CONTACT',
            'name':
                'contactType',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description': '',
            'name': 'signatureUserProfileId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }]
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
    }, [{
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
        'description': '',
        'name': 'notes',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'planningTermId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'projectId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'sellerOrderId',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'sellerOrganizationName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'siteId',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'name': 'siteNames',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'subaccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'termsAndConditions',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}]
