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

creativeAssetMetadata_Schema = [
    [{
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'AUDIO, FLASH, HTML, HTML_IMAGE, IMAGE, VIDEO',
        'name': 'type',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'name':
            'clickTags',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [[{
            'description': '',
            'name': 'computedClickThroughUrl',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'customClickThroughUrl',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'landingPageId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'eventName',
            'type': 'STRING',
            'mode': 'NULLABLE'
        },
                   {
                       'description': '',
                       'name': 'name',
                       'type': 'STRING',
                       'mode': 'NULLABLE'
                   }]
    }, {
        'name': 'detectedFeatures',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'id',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
        'description': '',
        'name': 'dimensionName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'etag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
        'name': 'matchType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'warnedValidationRules',
        'type': 'STRING',
        'mode': 'REPEATED'
    }
]
