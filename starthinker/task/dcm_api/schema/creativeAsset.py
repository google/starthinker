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

creativeAsset_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "mimeType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ARTWORK_TYPE_FLASH, ARTWORK_TYPE_HTML5, ARTWORK_TYPE_IMAGE, ARTWORK_TYPE_MIXED", 
    "name": "artworkType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "OFFSET_UNIT_PERCENT, OFFSET_UNIT_PIXEL, OFFSET_UNIT_PIXEL_FROM_CENTER", 
    "name": "positionLeftUnit"
  }, 
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
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "audioSampleRate"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "FLOAT64", 
    "description": "", 
    "name": "frameRate"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "flashVersion"
  }, 
  {
    "fields": [
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
    ], 
    "type": "RECORD", 
    "name": "additionalSizes", 
    "mode": "REPEATED"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "hideFlashObjects", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "STRING", 
    "name": "detectedFeatures", 
    "mode": "REPEATED"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "originalBackup", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "duration"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "OFFSET_UNIT_PERCENT, OFFSET_UNIT_PIXEL, OFFSET_UNIT_PIXEL_FROM_CENTER", 
    "name": "positionTopUnit"
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
    "description": "ALIGNMENT_BOTTOM, ALIGNMENT_LEFT, ALIGNMENT_RIGHT, ALIGNMENT_TOP", 
    "name": "alignment"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "LANDSCAPE, PORTRAIT, SQUARE", 
    "name": "orientation"
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
  {
    "type": "BOOLEAN", 
    "name": "politeLoad", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "horizontallyLocked", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ASSET_START_TIME_TYPE_CUSTOM, ASSET_START_TIME_TYPE_NONE", 
    "name": "startTimeType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ASSET_DISPLAY_TYPE_BACKDROP, ASSET_DISPLAY_TYPE_EXPANDING, ASSET_DISPLAY_TYPE_FLASH_IN_FLASH, ASSET_DISPLAY_TYPE_FLASH_IN_FLASH_EXPANDING, ASSET_DISPLAY_TYPE_FLOATING, ASSET_DISPLAY_TYPE_INPAGE, ASSET_DISPLAY_TYPE_OVERLAY, ASSET_DISPLAY_TYPE_PEEL_DOWN, ASSET_DISPLAY_TYPE_VPAID_LINEAR, ASSET_DISPLAY_TYPE_VPAID_NON_LINEAR", 
    "name": "displayType"
  }, 
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
  ], 
  {
    "type": "BOOLEAN", 
    "name": "verticallyLocked", 
    "mode": "NULLABLE"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "value"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "dimensionName"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "etag"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
      "name": "matchType"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "id"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ADDITIONAL_FLASH, ADDITIONAL_IMAGE, ALTERNATE_VIDEO, BACKUP_IMAGE, OTHER, PARENT_AUDIO, PARENT_VIDEO, PRIMARY, TRANSCODED_AUDIO, TRANSCODED_VIDEO", 
    "name": "role"
  }, 
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
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "bitRate"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "OPAQUE, TRANSPARENT, WINDOW", 
    "name": "windowMode"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "audioBitRate"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "pushdown", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "progressiveServingUrl"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ASSET_DURATION_TYPE_AUTO, ASSET_DURATION_TYPE_CUSTOM, ASSET_DURATION_TYPE_NONE", 
    "name": "durationType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "zIndex"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "fileSize"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "zipFilename"
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
  {
    "type": "BOOLEAN", 
    "name": "active", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "INT64", 
    "name": "companionCreativeIds", 
    "mode": "REPEATED"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "hideSelectionBoxes", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "streamingServingUrl"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "zipFilesize"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CHILD_ASSET_TYPE_DATA, CHILD_ASSET_TYPE_FLASH, CHILD_ASSET_TYPE_IMAGE, CHILD_ASSET_TYPE_VIDEO", 
    "name": "childAssetType"
  }, 
  [
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
  ], 
  {
    "type": "BOOLEAN", 
    "name": "actionScript3", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "FLOAT64", 
    "description": "", 
    "name": "pushdownDuration"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "AUDIO, FLASH, HTML, HTML_IMAGE, IMAGE, VIDEO", 
      "name": "type"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "name"
    }
  ], 
  {
    "type": "BOOLEAN", 
    "name": "transparency", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "sslCompliant", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "FLOAT64", 
    "description": "", 
    "name": "mediaDuration"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "customStartTimeValue"
  }
]
