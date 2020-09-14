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

encryptionInfo_Schema = [{
    'description': '',
    'name': 'encryptionEntityId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description':
        'ADWORDS_CUSTOMER, DBM_ADVERTISER, DBM_PARTNER, DCM_ACCOUNT, '
        'DCM_ADVERTISER, DFP_NETWORK_CODE, ENCRYPTION_ENTITY_TYPE_UNKNOWN',
    'name':
        'encryptionEntityType',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': 'AD_SERVING, DATA_TRANSFER, ENCRYPTION_SCOPE_UNKNOWN',
    'name': 'encryptionSource',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
