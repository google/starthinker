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

creativeCustomEvent_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "TARGET_BLANK, TARGET_PARENT, TARGET_POPUP, TARGET_SELF, TARGET_TOP", 
    "name": "targetType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ARTWORK_TYPE_FLASH, ARTWORK_TYPE_HTML5, ARTWORK_TYPE_IMAGE, ARTWORK_TYPE_MIXED", 
    "name": "artworkType"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "computedClickThroughUrl"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "customClickThroughUrl"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "landingPageId"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "videoReportingId"
  }, 
  [
    {
      "type": "BOOLEAN", 
      "name": "showStatusBar", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "showScrollBar", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "showAddressBar", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "showMenuBar", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "title"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "showToolBar", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "CENTER, COORDINATES", 
      "name": "positionType"
    }, 
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "top"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "left"
      }
    ], 
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "width"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "iab", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "id"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "height"
      }
    ]
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "advertiserCustomEventId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "artworkLabel"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ADVERTISER_EVENT_COUNTER, ADVERTISER_EVENT_EXIT, ADVERTISER_EVENT_TIMER", 
    "name": "advertiserCustomEventType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "advertiserCustomEventName"
  }
]
