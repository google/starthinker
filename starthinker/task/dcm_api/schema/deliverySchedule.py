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

deliverySchedule_Schema = [[{
    'description': '',
    'name': 'duration',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'impressions',
    'type': 'INT64',
    'mode': 'NULLABLE'
}], {
    'name': 'hardCutoff',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'impressionRatio',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description':
        'AD_PRIORITY_01, AD_PRIORITY_02, AD_PRIORITY_03, AD_PRIORITY_04, '
        'AD_PRIORITY_05, AD_PRIORITY_06, AD_PRIORITY_07, AD_PRIORITY_08, '
        'AD_PRIORITY_09, AD_PRIORITY_10, AD_PRIORITY_11, AD_PRIORITY_12, '
        'AD_PRIORITY_13, AD_PRIORITY_14, AD_PRIORITY_15, AD_PRIORITY_16',
    'name':
        'priority',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}]
