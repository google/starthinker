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

creativeAssetSelection_Schema = [{
    'description': '',
    'name': 'defaultAssetId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'name':
        'rules',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description': '',
        'name': 'assetId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetingTemplateId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }]
}]
