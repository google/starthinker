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

import json

from traffic.dao import BaseDAO
from traffic.campaign import CampaignDAO
from traffic.video_format import VideoFormatDAO
from traffic.feed import FieldMap


class PlacementDAO(BaseDAO):

  cache = {}

  def __init__(self, auth, profile_id):
    super(PlacementDAO, self).__init__(auth, profile_id)

    self._entity = 'PLACEMENT'

    self.campaign_dao = CampaignDAO(auth, profile_id)
    self.video_format_dao = VideoFormatDAO(auth, profile_id)

    self._service = self.service.placements()
    self._id_field = FieldMap.PLACEMENT_ID
    self._search_field = FieldMap.PLACEMENT_NAME

    self._list_name = 'placements'

    self.cache = PlacementDAO.cache

  def _process_update(self, item, feed_item):
    campaign = self.campaign_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    item['pricingSchedule']['startDate'] = feed_item[
        FieldMap.PLACEMENT_START_DATE]
    item['pricingSchedule']['endDate'] = feed_item[FieldMap.PLACEMENT_END_DATE]
    item['pricingSchedule']['pricingPeriods'][0]['startDate'] = feed_item[
        FieldMap.PLACEMENT_START_DATE]
    item['pricingSchedule']['pricingPeriods'][0]['endDate'] = feed_item[
        FieldMap.PLACEMENT_END_DATE]
    item['name'] = feed_item[FieldMap.PLACEMENT_NAME]
    item['archived'] = feed_item[FieldMap.PLACEMENT_ARCHIVED]

    self._process_transcode(item, feed_item)

  def _process_transcode(self, item, feed_item):
    if 'transcode_config' in feed_item:
      if not 'videoSettings' in item:
        item['videoSettings'] = {}

      if not 'transcodeSettings' in item['videoSettings']:
        item['videoSettings']['transcodeSettings'] = {}

      item['videoSettings']['transcodeSettings'][
          'enabledVideoFormats'] = self.video_format_dao.translate_transcode_config(
              feed_item['transcode_config'])

  def _process_new(self, feed_item):

    campaign = self.campaign_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    result = {
        'name': feed_item[FieldMap.PLACEMENT_NAME],
        'campaignId': campaign['id'],
        'archived': feed_item[FieldMap.PLACEMENT_ARCHIVED],
        'siteId': feed_item[FieldMap.SITE_ID],
        'paymentSource': 'PLACEMENT_AGENCY_PAID',
        'pricingSchedule': {
            'startDate':
                feed_item[FieldMap.PLACEMENT_START_DATE],
            'endDate':
                feed_item[FieldMap.PLACEMENT_END_DATE],
            'pricingType':
                'PRICING_TYPE_CPM',
            'pricingPeriods': [{
                'startDate': feed_item[FieldMap.PLACEMENT_START_DATE],
                'endDate': feed_item[FieldMap.PLACEMENT_END_DATE]
            }]
        }
    }

    if feed_item[FieldMap.PLACEMENT_TYPE] == 'VIDEO' or feed_item[FieldMap.PLACEMENT_TYPE] == 'IN_STREAM_VIDEO':
      result['compatibility'] = 'IN_STREAM_VIDEO'
      result['size'] = {'width': '0', 'height': '0'}
      result['tagFormats'] = ['PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH']
    else:
      result['compatibility'] = 'DISPLAY'
      width, height = feed_item[FieldMap.ASSET_SIZE].strip().lower().split('x')
      sizes = self.get_sizes(int(width), int(height))['sizes']
      if sizes:
        result['size'] = {'id': sizes[0]['id']}
      else:
        result['size'] = {'width': int(width), 'height': int(height)}

      result['tagFormats'] = [
          'PLACEMENT_TAG_STANDARD', 'PLACEMENT_TAG_JAVASCRIPT',
          'PLACEMENT_TAG_IFRAME_JAVASCRIPT', 'PLACEMENT_TAG_IFRAME_ILAYER',
          'PLACEMENT_TAG_INTERNAL_REDIRECT', 'PLACEMENT_TAG_TRACKING',
          'PLACEMENT_TAG_TRACKING_IFRAME', 'PLACEMENT_TAG_TRACKING_JAVASCRIPT'
      ]

    self._process_transcode(result, feed_item)

    return result

  def map_placement_transcode_configs(self, placement_feed,
                                      transcode_configs_feed):
    for placement in placement_feed:
      for transcode_config in transcode_configs_feed:
        if placement[FieldMap.TRANSCODE_ID] == transcode_config[
            FieldMap.TRANSCODE_ID]:
          placement['transcode_config'] = transcode_config
          break
