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

creativeAssignment_Schema = [
    {
        'name': 'active',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'applyEventTags',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    },
    [{
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
        'name': 'defaultLandingPage',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'landingPageId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'name':
            'companionCreativeOverrides',
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
            'name': 'defaultLandingPage',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'landingPageId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'creativeId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }]
    }, {
        'name':
            'creativeGroupAssignments',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'creativeGroupId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': 'CREATIVE_GROUP_ONE, CREATIVE_GROUP_TWO',
            'name': 'creativeGroupNumber',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'description': '',
        'name': 'creativeId',
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
        'name': 'endTime',
        'type': 'DATETIME',
        'mode': 'NULLABLE'
    }, {
        'name':
            'richMediaExitOverrides',
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
            'name': 'defaultLandingPage',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'landingPageId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'name': 'enabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'exitId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }]
    }, {
        'description': '',
        'name': 'sequence',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'sslCompliant',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'startTime',
        'type': 'DATETIME',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'weight',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }
]
