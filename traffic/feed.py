###########################################################################
#
#  Copyright 2017 Google Inc.
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

from util.sheets import sheets_read, sheets_write
import json

class FieldMap:
  AD_ID = 'Ad ID'
  AD_NAME = 'Ad Name'
  AD_START_DATE = 'Ad Start Date'
  AD_END_DATE = 'Ad End Date'
  AD_ACTIVE = 'Ad Active'
  AD_ARCHIVED = 'Ad Archived'
  AD_PRIORITY = 'Ad Priority'

  ADVERTISER_ID = 'Advertiser ID'

  ASSET_SIZE = 'Asset Size'

  CAMPAIGN_ID = 'Campaign ID'
  CAMPAIGN_NAME = 'Campaign Name'
  CAMPAIGN_START_DATE = 'Campaign Start Date'
  CAMPAIGN_END_DATE = 'Campaign End Date'
  CAMPAIGN_LANDING_PAGE_NAME = 'Landing Page Name'
  CAMPAIGN_LANDING_PAGE_URL = 'Default Landing Page'
  CAMPAIGN_LANDING_PAGE_ID = 'Landing Page ID'

  CAMPAIGN_CREATIVE_ASSOCIATION_ID = 'Campaign Creative Association ID'
  CREATIVE_ASSET_BUCKET_NAME = 'Creative Asset Bucket Name'
  CREATIVE_ASSET_ID = 'Creative Asset ID'
  CREATIVE_ASSET_NAME = 'Creative Asset Name'
  CREATIVE_ASSET_FILE_NAME = 'Creative Asset File Name'

  CREATIVE_NAME = 'Creative Name'
  CREATIVE_TYPE = 'Creative Type'
  CREATIVE_ID = 'Creative ID'
  CREATIVE_ROTATION_TYPE = 'Creative Rotation Type'
  CREATIVE_ROTATION_SEQUENCE = 'Creative Rotation Sequence'
  CREATIVE_ROTATION_WEIGHT = 'Creative Rotation Weight'
  CREATIVE_ROTATION_WEIGHT_CALCULATION_STRATEGY = 'Creative Rotation Weight Calculation Strategy'

  PLACEMENT_ID = 'Placement ID'
  PLACEMENT_NAME = 'Placement Name'
  PLACEMENT_START_DATE = 'Placement Start Date'
  PLACEMENT_END_DATE = 'Placement End Date'
  PLACEMENT_TYPE = 'Type'
  PLACEMENT_ARCHIVED = 'Archived'
  PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION = 'Active View and Verification'

  EVENT_TAG_NAME = 'Event Tag Name'
  EVENT_TAG_STATUS = 'Event Tag Status'
  EVENT_TAG_TYPE = 'Event Tag Type'
  EVENT_TAG_URL = 'Event Tag URL'
  EVENT_TAG_ID = 'Event Tag ID'

  SITE_ID = 'Site ID'

  TRANSCODE_ID = 'Transcode ID'
  TRANSCODE_MIN_WIDTH = 'Min Width'
  TRANSCODE_MAX_WIDTH = 'Max Width'
  TRANSCODE_MIN_HEIGHT = 'Min Height'
  TRANSCODE_MAX_HEIGHT = 'Max Height'
  TRANSCODE_MIN_BITRATE = 'Min Bitrate (kbps)'
  TRANSCODE_MAX_BITRATE = 'Max Bitrate (kbps)'
  TRANSCODE_FILE_TYPES = ['THREEGPP', 'FLV', 'MOV', 'MP4', 'WEBM', 'M3U8']

class Feed:

  def __init__(self, auth, trix_id, trix_range):
    self.auth = auth
    self.trix_id = trix_id
    self.trix_range = trix_range

    self.feed = self._feed_to_dict(self._get_feed())

  def update(self):
    new_feed = self._dict_to_feed(self.feed)

    sheets_write(self.auth, self.trix_id, self.trix_range.split('!')[0], self.trix_range.split('!')[1], new_feed)

  def _get_feed(self):
    return sheets_read(self.auth, self.trix_id, self.trix_range.split('!')[0], self.trix_range.split('!')[1])

  def _dict_to_feed(self, feed):
    raw_feed = self._get_feed()

    if not raw_feed:
      return None

    headers = raw_feed[0]

    row = 1

    for item in feed:
      for key in item.keys():
        if key in headers:
          column = headers.index(key)
          raw_feed[row][column] = item[key]

      row += 1

    return raw_feed

  def _feed_to_dict(self, raw_feed):
    if not raw_feed:
      return None

    result = []

    header = raw_feed[0]

    for line in raw_feed[1:]:
      if line and line[0]:
        i = 0
        item = {}
        while i < len(line):
          item[header[i]] = line[i].strip()
          i += 1

        result.append(item)
      else:
        break

    return result
