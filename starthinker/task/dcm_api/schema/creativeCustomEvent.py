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

creativeCustomEvent_Schema = [
    {
        'description': '',
        'name': 'advertiserCustomEventId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'advertiserCustomEventName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ADVERTISER_EVENT_COUNTER, ADVERTISER_EVENT_EXIT, '
            'ADVERTISER_EVENT_TIMER',
        'name':
            'advertiserCustomEventType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'artworkLabel',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ARTWORK_TYPE_FLASH, ARTWORK_TYPE_HTML5, ARTWORK_TYPE_IMAGE, '
            'ARTWORK_TYPE_MIXED',
        'name':
            'artworkType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
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
        'description': '',
        'name': 'landingPageId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'id',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [[{
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
    }],
     [{
         'description': '',
         'name': 'left',
         'type': 'INT64',
         'mode': 'NULLABLE'
     }, {
         'description': '',
         'name': 'top',
         'type': 'INT64',
         'mode': 'NULLABLE'
     }], {
         'description': 'CENTER, COORDINATES',
         'name': 'positionType',
         'type': 'STRING',
         'mode': 'NULLABLE'
     }, {
         'name': 'showAddressBar',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'showMenuBar',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'showScrollBar',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'showStatusBar',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'showToolBar',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'description': '',
         'name': 'title',
         'type': 'STRING',
         'mode': 'NULLABLE'
     }],
    {
        'description':
            'TARGET_BLANK, TARGET_PARENT, TARGET_POPUP, TARGET_SELF, TARGET_TOP',
        'name':
            'targetType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'videoReportingId',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }
]
