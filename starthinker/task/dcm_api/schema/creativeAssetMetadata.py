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

creativeAssetMetadata_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
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
    "fields": {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "ADMOB_REFERENCED, ASSET_FORMAT_UNSUPPORTED_DCM, ASSET_INVALID, CLICK_TAG_HARD_CODED, CLICK_TAG_INVALID, CLICK_TAG_IN_GWD, CLICK_TAG_MISSING, CLICK_TAG_MORE_THAN_ONE, CLICK_TAG_NON_TOP_LEVEL, COMPONENT_UNSUPPORTED_DCM, ENABLER_UNSUPPORTED_METHOD_DCM, EXTERNAL_FILE_REFERENCED, FILE_DETAIL_EMPTY, FILE_TYPE_INVALID, GWD_PROPERTIES_INVALID, HTML5_FEATURE_UNSUPPORTED, LINKED_FILE_NOT_FOUND, MAX_FLASH_VERSION_11, MRAID_REFERENCED, NOT_SSL_COMPLIANT, ORPHANED_ASSET, PRIMARY_HTML_MISSING, SVG_INVALID, ZIP_INVALID", 
      "name": "warnedValidationRules"
    }, 
    "type": "RECORD", 
    "name": "warnedValidationRules", 
    "mode": "REPEATED"
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
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }
]
