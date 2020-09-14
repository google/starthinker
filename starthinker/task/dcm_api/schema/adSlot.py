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

adSlot_Schema = [{
    'description': '',
    'name': 'comment',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description':
        'APP, APP_INTERSTITIAL, DISPLAY, DISPLAY_INTERSTITIAL, '
        'IN_STREAM_AUDIO, IN_STREAM_VIDEO',
    'name':
        'compatibility',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': '',
    'name': 'height',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'linkedPlacementId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'name',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description':
        'PLANNING_PAYMENT_SOURCE_TYPE_AGENCY_PAID, '
        'PLANNING_PAYMENT_SOURCE_TYPE_PUBLISHER_PAID',
    'name':
        'paymentSourceType',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'name': 'primary',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'width',
    'type': 'INT64',
    'mode': 'NULLABLE'
}]
