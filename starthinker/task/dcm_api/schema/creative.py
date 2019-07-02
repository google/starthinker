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

creative_Schema = [
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "url"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "CLICK_TRACKING, IMPRESSION, RICH_MEDIA_BACKUP_IMPRESSION, RICH_MEDIA_IMPRESSION, RICH_MEDIA_RM_IMPRESSION, SURVEY, VIDEO_COMPLETE, VIDEO_CUSTOM, VIDEO_FIRST_QUARTILE, VIDEO_FULLSCREEN, VIDEO_MIDPOINT, VIDEO_MUTE, VIDEO_PAUSE, VIDEO_PROGRESS, VIDEO_REWIND, VIDEO_SKIP, VIDEO_START, VIDEO_STOP, VIDEO_THIRD_QUARTILE", 
        "name": "thirdPartyUrlType"
      }
    ], 
    "type": "RECORD", 
    "name": "thirdPartyUrls", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ARTWORK_TYPE_FLASH, ARTWORK_TYPE_HTML5, ARTWORK_TYPE_IMAGE, ARTWORK_TYPE_MIXED", 
    "name": "artworkType"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "latestTraffickedCreativeId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "advertiserId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "requiredFlashPluginVersion"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "thirdPartyBackupImageImpressionsUrl"
  }, 
  {
    "fields": [
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
    "type": "RECORD", 
    "name": "timerCustomEvents", 
    "mode": "REPEATED"
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
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "windowHeight"
    }, 
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
      "name": "windowWidth"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "CENTERED, DISTANCE_FROM_TOP_LEFT_CORNER", 
      "name": "positionOption"
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
    "name": "dynamicAssetSelection", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "offsetPercentage"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "offsetSeconds"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "accountId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "studioTraffickedCreativeId"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "archived", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "overrideCss"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CREATIVE_AUTHORING_SOURCE_DBM, CREATIVE_AUTHORING_SOURCE_DCM, CREATIVE_AUTHORING_SOURCE_STUDIO", 
    "name": "authoringSource"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "requiredFlashVersion"
  }, 
  {
    "fields": [
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
    "type": "RECORD", 
    "name": "exitCustomEvents", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "renderingId"
  }, 
  {
    "fields": [
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
    "type": "RECORD", 
    "name": "counterCustomEvents", 
    "mode": "REPEATED"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "offsetPercentage"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "offsetSeconds"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "backupImageReportingLabel"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "version"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "creativeFieldId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "creativeFieldValueId"
      }
    ], 
    "type": "RECORD", 
    "name": "creativeFieldAssignments", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "backgroundColor"
  }, 
  {
    "fields": {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "customKeyValues"
    }, 
    "type": "RECORD", 
    "name": "customKeyValues", 
    "mode": "REPEATED"
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
    "type": "STRING", 
    "description": "BRAND_SAFE_DEFAULT_INSTREAM_VIDEO, CUSTOM_DISPLAY, CUSTOM_DISPLAY_INTERSTITIAL, DISPLAY, DISPLAY_IMAGE_GALLERY, DISPLAY_REDIRECT, FLASH_INPAGE, HTML5_BANNER, IMAGE, INSTREAM_AUDIO, INSTREAM_VIDEO, INSTREAM_VIDEO_REDIRECT, INTERNAL_REDIRECT, INTERSTITIAL_INTERNAL_REDIRECT, RICH_MEDIA_DISPLAY_BANNER, RICH_MEDIA_DISPLAY_EXPANDING, RICH_MEDIA_DISPLAY_INTERSTITIAL, RICH_MEDIA_DISPLAY_MULTI_FLOATING_INTERSTITIAL, RICH_MEDIA_IM_EXPAND, RICH_MEDIA_INPAGE_FLOATING, RICH_MEDIA_MOBILE_IN_APP, RICH_MEDIA_PEEL_DOWN, TRACKING_TEXT, VPAID_LINEAR_VIDEO, VPAID_NON_LINEAR_VIDEO", 
    "name": "type"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "totalFileSize"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "FLOAT64", 
    "description": "", 
    "name": "mediaDuration"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "thirdPartyRichMediaImpressionsUrl"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "studioAdvertiserId"
  }, 
  {
    "fields": [
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
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "APPLICATION_CACHE, AUDIO, CANVAS, CANVAS_TEXT, CSS_ANIMATIONS, CSS_BACKGROUND_SIZE, CSS_BORDER_IMAGE, CSS_BORDER_RADIUS, CSS_BOX_SHADOW, CSS_COLUMNS, CSS_FLEX_BOX, CSS_FONT_FACE, CSS_GENERATED_CONTENT, CSS_GRADIENTS, CSS_HSLA, CSS_MULTIPLE_BGS, CSS_OPACITY, CSS_REFLECTIONS, CSS_RGBA, CSS_TEXT_SHADOW, CSS_TRANSFORMS, CSS_TRANSFORMS3D, CSS_TRANSITIONS, DRAG_AND_DROP, GEO_LOCATION, HASH_CHANGE, HISTORY, INDEXED_DB, INLINE_SVG, INPUT_ATTR_AUTOCOMPLETE, INPUT_ATTR_AUTOFOCUS, INPUT_ATTR_LIST, INPUT_ATTR_MAX, INPUT_ATTR_MIN, INPUT_ATTR_MULTIPLE, INPUT_ATTR_PATTERN, INPUT_ATTR_PLACEHOLDER, INPUT_ATTR_REQUIRED, INPUT_ATTR_STEP, INPUT_TYPE_COLOR, INPUT_TYPE_DATE, INPUT_TYPE_DATETIME, INPUT_TYPE_DATETIME_LOCAL, INPUT_TYPE_EMAIL, INPUT_TYPE_MONTH, INPUT_TYPE_NUMBER, INPUT_TYPE_RANGE, INPUT_TYPE_SEARCH, INPUT_TYPE_TEL, INPUT_TYPE_TIME, INPUT_TYPE_URL, INPUT_TYPE_WEEK, LOCAL_STORAGE, POST_MESSAGE, SESSION_STORAGE, SMIL, SVG_CLIP_PATHS, SVG_FE_IMAGE, SVG_FILTERS, SVG_HREF, TOUCH, VIDEO, WEBGL, WEB_SOCKETS, WEB_SQL_DATABASE, WEB_WORKERS", 
          "name": "detectedFeatures"
        }, 
        "type": "RECORD", 
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
        "fields": {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "companionCreativeIds"
        }, 
        "type": "RECORD", 
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
    ], 
    "type": "RECORD", 
    "name": "creativeAssets", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "redirectUrl"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "autoAdvanceImages", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "htmlCodeLocked", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "convertFlashToHtml5", 
    "mode": "NULLABLE"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "eventName"
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
        "name": "name"
      }
    ], 
    "type": "RECORD", 
    "name": "clickTags", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "commercialId"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "active", 
    "mode": "NULLABLE"
  }, 
  {
    "fields": {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "APP, APP_INTERSTITIAL, DISPLAY, DISPLAY_INTERSTITIAL, IN_STREAM_AUDIO, IN_STREAM_VIDEO", 
      "name": "compatibility"
    }, 
    "type": "RECORD", 
    "name": "compatibility", 
    "mode": "REPEATED"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "AD_ID.ORG, CLEARCAST, DCM, OTHER", 
      "name": "registry"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "value"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "adParameters"
  }, 
  {
    "fields": {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "adTagKeys"
    }, 
    "type": "RECORD", 
    "name": "adTagKeys", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "subaccountId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "name"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "sslOverride", 
    "mode": "NULLABLE"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "time"
    }
  ], 
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
    "type": "BOOLEAN", 
    "name": "sslCompliant", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "studioCreativeId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "NINJA, SWIFFY", 
    "name": "authoringTool"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "allowScriptAccess", 
    "mode": "NULLABLE"
  }, 
  {
    "fields": {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "companionCreatives"
    }, 
    "type": "RECORD", 
    "name": "companionCreatives", 
    "mode": "REPEATED"
  }, 
  [
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "assetId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "targetingTemplateId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "rules", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "defaultAssetId"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "htmlCode"
  }, 
  {
    "fields": {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "APPLICATION_CACHE, AUDIO, CANVAS, CANVAS_TEXT, CSS_ANIMATIONS, CSS_BACKGROUND_SIZE, CSS_BORDER_IMAGE, CSS_BORDER_RADIUS, CSS_BOX_SHADOW, CSS_COLUMNS, CSS_FLEX_BOX, CSS_FONT_FACE, CSS_GENERATED_CONTENT, CSS_GRADIENTS, CSS_HSLA, CSS_MULTIPLE_BGS, CSS_OPACITY, CSS_REFLECTIONS, CSS_RGBA, CSS_TEXT_SHADOW, CSS_TRANSFORMS, CSS_TRANSFORMS3D, CSS_TRANSITIONS, DRAG_AND_DROP, GEO_LOCATION, HASH_CHANGE, HISTORY, INDEXED_DB, INLINE_SVG, INPUT_ATTR_AUTOCOMPLETE, INPUT_ATTR_AUTOFOCUS, INPUT_ATTR_LIST, INPUT_ATTR_MAX, INPUT_ATTR_MIN, INPUT_ATTR_MULTIPLE, INPUT_ATTR_PATTERN, INPUT_ATTR_PLACEHOLDER, INPUT_ATTR_REQUIRED, INPUT_ATTR_STEP, INPUT_TYPE_COLOR, INPUT_TYPE_DATE, INPUT_TYPE_DATETIME, INPUT_TYPE_DATETIME_LOCAL, INPUT_TYPE_EMAIL, INPUT_TYPE_MONTH, INPUT_TYPE_NUMBER, INPUT_TYPE_RANGE, INPUT_TYPE_SEARCH, INPUT_TYPE_TEL, INPUT_TYPE_TIME, INPUT_TYPE_URL, INPUT_TYPE_WEEK, LOCAL_STORAGE, POST_MESSAGE, SESSION_STORAGE, SMIL, SVG_CLIP_PATHS, SVG_FE_IMAGE, SVG_FILTERS, SVG_HREF, TOUCH, VIDEO, WEBGL, WEB_SOCKETS, WEB_SQL_DATABASE, WEB_WORKERS", 
      "name": "backupImageFeatures"
    }, 
    "type": "RECORD", 
    "name": "backupImageFeatures", 
    "mode": "REPEATED"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "customHtml"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "CURRENT_WINDOW, CUSTOM, NEW_WINDOW", 
      "name": "targetWindowOption"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "mediaDescription"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "skippable", 
    "mode": "NULLABLE"
  }
]
