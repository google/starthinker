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

thirdPartyTrackingUrl_Schema = [{
    'description':
        'CLICK_TRACKING, IMPRESSION, RICH_MEDIA_BACKUP_IMPRESSION, '
        'RICH_MEDIA_IMPRESSION, RICH_MEDIA_RM_IMPRESSION, SURVEY, '
        'VIDEO_COMPLETE, VIDEO_CUSTOM, VIDEO_FIRST_QUARTILE, VIDEO_FULLSCREEN,'
        ' VIDEO_MIDPOINT, VIDEO_MUTE, VIDEO_PAUSE, VIDEO_PROGRESS, '
        'VIDEO_REWIND, VIDEO_SKIP, VIDEO_START, VIDEO_STOP, '
        'VIDEO_THIRD_QUARTILE',
    'name':
        'thirdPartyUrlType',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': '',
    'name': 'url',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
