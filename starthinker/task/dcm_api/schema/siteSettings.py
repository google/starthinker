###########################################################################
#
#  Copyright 2019 Google Inc.
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

siteSettings_Schema = [
  {
    "type": "BOOLEAN", 
    "name": "activeViewOptOut", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "videoActiveViewOptOutTemplate", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "disableNewCookie", 
    "mode": "NULLABLE"
  }, 
  [
    {
      "type": "BOOLEAN", 
      "name": "includeClickThroughUrls", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "includeClickTracking", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "additionalKeyValues"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "GENERATE_SEPARATE_TAG_FOR_EACH_KEYWORD, IGNORE, PLACEHOLDER_WITH_LIST_OF_KEYWORDS", 
      "name": "keywordOption"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "BOTH, DEFAULT, FLASH, HTML5", 
    "name": "vpaidAdapterChoiceTemplate"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "adBlockingOptOut", 
    "mode": "NULLABLE"
  }
]
