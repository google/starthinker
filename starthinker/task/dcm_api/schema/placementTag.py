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

placementTag_Schema = [{
    'description': '',
    'name': 'placementId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'name':
        'tagDatas',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description': '',
        'name': 'adId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'clickTag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'creativeId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'PLACEMENT_TAG_CLICK_COMMANDS, PLACEMENT_TAG_IFRAME_ILAYER, '
            'PLACEMENT_TAG_IFRAME_JAVASCRIPT, '
            'PLACEMENT_TAG_IFRAME_JAVASCRIPT_LEGACY, '
            'PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH, '
            'PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH_VAST_3, '
            'PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH_VAST_4, '
            'PLACEMENT_TAG_INTERNAL_REDIRECT, '
            'PLACEMENT_TAG_INTERSTITIAL_IFRAME_JAVASCRIPT, '
            'PLACEMENT_TAG_INTERSTITIAL_IFRAME_JAVASCRIPT_LEGACY, '
            'PLACEMENT_TAG_INTERSTITIAL_INTERNAL_REDIRECT, '
            'PLACEMENT_TAG_INTERSTITIAL_JAVASCRIPT, '
            'PLACEMENT_TAG_INTERSTITIAL_JAVASCRIPT_LEGACY, '
            'PLACEMENT_TAG_JAVASCRIPT, PLACEMENT_TAG_JAVASCRIPT_LEGACY, '
            'PLACEMENT_TAG_STANDARD, PLACEMENT_TAG_TRACKING, '
            'PLACEMENT_TAG_TRACKING_IFRAME, PLACEMENT_TAG_TRACKING_JAVASCRIPT',
        'name':
            'format',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'impressionTag',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}]
