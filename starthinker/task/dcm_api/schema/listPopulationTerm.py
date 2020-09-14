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

listPopulationTerm_Schema = [{
    'name': 'contains',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'name': 'negation',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'description':
        'NUM_EQUALS, NUM_GREATER_THAN, NUM_GREATER_THAN_EQUAL, NUM_LESS_THAN, '
        'NUM_LESS_THAN_EQUAL, STRING_CONTAINS, STRING_EQUALS',
    'name':
        'operator',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': '',
    'name': 'remarketingListId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': 'CUSTOM_VARIABLE_TERM, LIST_MEMBERSHIP_TERM, REFERRER_TERM',
    'name': 'type',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'value',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'variableFriendlyName',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'variableName',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
