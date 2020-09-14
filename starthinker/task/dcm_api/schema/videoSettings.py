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

videoSettings_Schema = [[{
    'name': 'companionsDisabled',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'name':
        'enabledSizes',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description': '',
        'name': 'height',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'iab',
        'type': 'BOOLEAN',
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
        'name': 'width',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }]
}, {
    'name': 'imageOnly',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}], {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': 'ANY, LANDSCAPE, PORTRAIT',
    'name': 'orientation',
    'type': 'STRING',
    'mode': 'NULLABLE'
},
                        [{
                            'description': '',
                            'name': 'kind',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        },
                         [{
                             'description': '',
                             'name': 'offsetPercentage',
                             'type': 'INT64',
                             'mode': 'NULLABLE'
                         }, {
                             'description': '',
                             'name': 'offsetSeconds',
                             'type': 'INT64',
                             'mode': 'NULLABLE'
                         }],
                         [{
                             'description': '',
                             'name': 'offsetPercentage',
                             'type': 'INT64',
                             'mode': 'NULLABLE'
                         }, {
                             'description': '',
                             'name': 'offsetSeconds',
                             'type': 'INT64',
                             'mode': 'NULLABLE'
                         }], {
                             'name': 'skippable',
                             'type': 'BOOLEAN',
                             'mode': 'NULLABLE'
                         }],
                        [{
                            'name': 'enabledVideoFormats',
                            'type': 'INT64',
                            'mode': 'REPEATED'
                        }, {
                            'description': '',
                            'name': 'kind',
                            'type': 'STRING',
                            'mode': 'NULLABLE'
                        }]]
