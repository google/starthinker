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

creativeAsset_Schema = [
    {
        'name': 'actionScript3',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'active',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name':
            'additionalSizes',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
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
        }]
    }, {
        'description':
            'ALIGNMENT_BOTTOM, ALIGNMENT_LEFT, ALIGNMENT_RIGHT, ALIGNMENT_TOP',
        'name':
            'alignment',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
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
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': 'AUDIO, FLASH, HTML, HTML_IMAGE, IMAGE, VIDEO',
        'name': 'type',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'audioBitRate',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'audioSampleRate',
        'type': 'INT64',
        'mode': 'NULLABLE'
    },
    [{
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
     }], {
         'description': '',
         'name': 'bitRate',
         'type': 'INT64',
         'mode': 'NULLABLE'
     },
    {
        'description':
            'CHILD_ASSET_TYPE_DATA, CHILD_ASSET_TYPE_FLASH, '
            'CHILD_ASSET_TYPE_IMAGE, CHILD_ASSET_TYPE_VIDEO',
        'name':
            'childAssetType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    },
    [{
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
    }], {
        'name': 'companionCreativeIds',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'customStartTimeValue',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'detectedFeatures',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'description':
            'ASSET_DISPLAY_TYPE_BACKDROP, ASSET_DISPLAY_TYPE_EXPANDING, '
            'ASSET_DISPLAY_TYPE_FLASH_IN_FLASH, '
            'ASSET_DISPLAY_TYPE_FLASH_IN_FLASH_EXPANDING, '
            'ASSET_DISPLAY_TYPE_FLOATING, ASSET_DISPLAY_TYPE_INPAGE, '
            'ASSET_DISPLAY_TYPE_OVERLAY, ASSET_DISPLAY_TYPE_PEEL_DOWN, '
            'ASSET_DISPLAY_TYPE_VPAID_LINEAR, '
            'ASSET_DISPLAY_TYPE_VPAID_NON_LINEAR',
        'name':
            'displayType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'duration',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ASSET_DURATION_TYPE_AUTO, ASSET_DURATION_TYPE_CUSTOM, '
            'ASSET_DURATION_TYPE_NONE',
        'name':
            'durationType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    },
    [{
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
    }], {
        'description': '',
        'name': 'fileSize',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'flashVersion',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'frameRate',
        'type': 'FLOAT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'hideFlashObjects',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'hideSelectionBoxes',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'horizontallyLocked',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
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
        'name': 'mediaDuration',
        'type': 'FLOAT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'mimeType',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
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
        'description': 'LANDSCAPE, PORTRAIT, SQUARE',
        'name': 'orientation',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'originalBackup',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'politeLoad',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    },
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
        'description':
            'OFFSET_UNIT_PERCENT, OFFSET_UNIT_PIXEL, '
            'OFFSET_UNIT_PIXEL_FROM_CENTER',
        'name':
            'positionLeftUnit',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description':
            'OFFSET_UNIT_PERCENT, OFFSET_UNIT_PIXEL, '
            'OFFSET_UNIT_PIXEL_FROM_CENTER',
        'name':
            'positionTopUnit',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'progressiveServingUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'pushdown',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'pushdownDuration',
        'type': 'FLOAT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ADDITIONAL_FLASH, ADDITIONAL_IMAGE, ALTERNATE_VIDEO, '
            'BACKUP_IMAGE, OTHER, PARENT_AUDIO, PARENT_VIDEO, PRIMARY, '
            'TRANSCODED_AUDIO, TRANSCODED_VIDEO',
        'name':
            'role',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    },
    [{
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
    }], {
        'name': 'sslCompliant',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ASSET_START_TIME_TYPE_CUSTOM, ASSET_START_TIME_TYPE_NONE',
        'name':
            'startTimeType',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'streamingServingUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'transparency',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'verticallyLocked',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': 'OPAQUE, TRANSPARENT, WINDOW',
        'name': 'windowMode',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'zIndex',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'zipFilename',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'zipFilesize',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }
]
