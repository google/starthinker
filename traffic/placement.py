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
"""Handles creation and updates of Placements.

"""

import json

from traffic.dao import BaseDAO
from traffic.campaign import CampaignDAO
from traffic.video_format import VideoFormatDAO
from traffic.feed import FieldMap
from dateutil import parser
from class_extensions import StringExtensions


class PlacementDAO(BaseDAO):
  """Placement data access object.

  Inherits from BaseDAO and implements placement specific logic for creating and
  updating placement.
  """

  cache = {}

  def __init__(self, auth, profile_id):
    """Initializes PlacementDAO with profile id and authentication scheme."""
    super(PlacementDAO, self).__init__(auth, profile_id)

    self._entity = 'PLACEMENT'

    self.campaign_dao = CampaignDAO(auth, profile_id)
    self.video_format_dao = VideoFormatDAO(auth, profile_id)

    self._service = self.service.placements()
    self._id_field = FieldMap.PLACEMENT_ID
    self._search_field = FieldMap.PLACEMENT_NAME

    self._list_name = 'placements'

    self.cache = PlacementDAO.cache

  def _process_active_view_and_verification(self, placement, feed_item):
    """Updates / creates active view and verification settings.

    This method updates the CM item by setting or creating active view and
    verification settings based on the Bulkdozer feed configurations.

    Args:
      placement: The CM placement object to be updated.
      feed_item: The Bulkdozer feed item with the configurations.

    Raises:
      Exception: In case the values for active view and verification enumeration
      is invalid.
    """

    if FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION in feed_item:
      if feed_item.get(FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION, None) == 'ON':
        placement['vpaidAdapterChoice'] = 'HTML5'
        placement['videoActiveViewOptOut'] = False
      elif feed_item.get(FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION, None) == 'OFF':
        placement['vpaidAdapterChoice'] = 'DEFAULT'
        placement['videoActiveViewOptOut'] = True
      elif feed_item[
          FieldMap.
          PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION] == 'LET_DCM_DECIDE' or feed_item[
              FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION] == '':
        placement['vpaidAdapterChoice'] = 'DEFAULT'
        placement['videoActiveViewOptOut'] = False
      else:
        raise Exception(
            '%s is not a valid value for the placement Active View and Verification field'
            % feed_item.get(FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION, None))

  def _process_pricing_schedule(self, item, feed_item):
    """Updates / creates pricing schedule settings.

    This method updates the CM item with pricing schedule based on
    configurations from the Bulkdozer feed.

    Args:
      item: the CM placement object to update.
      feed_item: The Bulkdozer feed item representing the settings to define.
    """
    if 'pricing_schedule' in feed_item:

      if not 'pricingSchedule' in item:
        item['pricingSchedule'] = {}

      item['pricingSchedule']['pricingPeriods'] = []

      for pricing_schedule in feed_item['pricing_schedule']:
        item['pricingSchedule']['pricingPeriods'].append({
            'endDate':
                pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_END),
            'startDate':
                pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_START),
            'rateOrCostNanos':
                float(pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_RATE)) *
                1000000000,
            'units':
                pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_UNITS),
        })

  def _process_update(self, item, feed_item):
    """Updates an placement based on the values from the feed.

    Args:
      item: Object representing the placement to be updated, this object is
        updated directly.
      feed_item: Feed item representing placement values from the Bulkdozer
        feed.
    """

    if feed_item.get(FieldMap.CAMPAIGN_ID, '') == '':
      feed_item[FieldMap.CAMPAIGN_ID] = item['campaignId']

    campaign = self.campaign_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    item['pricingSchedule']['startDate'] = (StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_START_DATE, None)) 
        if feed_item.get(FieldMap.PLACEMENT_START_DATE, '')
        else item['pricingSchedule']['startDate'])

    item['pricingSchedule']['endDate'] = (StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_END_DATE, None)) 
      if feed_item.get(FieldMap.PLACEMENT_END_DATE, '') 
      else item['pricingSchedule']['endDate'])

    item['pricingSchedule']['pricingType'] = feed_item.get(
        FieldMap.PLACEMENT_PRICING_SCHEDULE_COST_STRUCTURE,
        None) if feed_item.get(
            FieldMap.PLACEMENT_PRICING_SCHEDULE_COST_STRUCTURE,
            '') else item['pricingSchedule']['pricingType']

    item['name'] = feed_item.get(FieldMap.PLACEMENT_NAME,
                                 None) if feed_item.get(FieldMap.PLACEMENT_NAME,
                                                        '') else item['name']
    item['archived'] = feed_item.get(
        FieldMap.PLACEMENT_ARCHIVED, None) if feed_item.get(
            FieldMap.PLACEMENT_ARCHIVED, '') else item['archived']
    item['adBlockingOptOut'] = feed_item.get(FieldMap.PLACEMENT_AD_BLOCKING,
                                             False)

    self._process_transcode(item, feed_item)
    self._process_active_view_and_verification(item, feed_item)
    self._process_pricing_schedule(item, feed_item)

  def _process_transcode(self, item, feed_item):
    """Updates / creates transcode configuration for the placement.

    This method updates the CM placement object with transcoding configuration
    from the feed.

    Args:
      item: The CM placement object to update.
      feed_item: The Bulkdozer feed item with the transcode configurations.
    """
    if 'transcode_config' in feed_item:

      if not 'videoSettings' in item:
        item['videoSettings'] = {}

      if not 'transcodeSettings' in item['videoSettings']:
        item['videoSettings']['transcodeSettings'] = {}

      item['videoSettings']['transcodeSettings'][
          'enabledVideoFormats'] = self.video_format_dao.translate_transcode_config(
              feed_item['transcode_config'])

      if not item['videoSettings']['transcodeSettings']['enabledVideoFormats']:
        raise Exception(
            'Specified transcode profile did not match any placement level transcode settings in Campaign Manager'
        )

  def get_sizes(self, width, height):
    """Retrieves a creative sizes from DCM.

    Args:
      width: width of the creative.
      height: height of the creative.
      retry_count: how many times the api call should be
        retried in case of an api related error that is not
        a client error.

    Returns:
      The sizes object from DCM.
    """
    # TODO (mauriciod): this could potentially be in a separate SizesDAO,
    # but since we don't use it anywhere else it is probably fine.
    # May need to do it in case it becomes necessary for other entities when
    # we implement display
    return self._retry(self.service.sizes().list(
        profileId=self.profile_id, height=height, width=width))

  def _process_new(self, feed_item):
    """Creates a new placement DCM object from a feed item representing an placement from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the placement from the Bulkdozer feed.

    Returns:
      An placement object ready to be inserted in DCM through the API.

    """
    campaign = self.campaign_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    result = {
        'name':
            feed_item.get(FieldMap.PLACEMENT_NAME, None),
        'adBlockingOptOut':
            feed_item.get(FieldMap.PLACEMENT_AD_BLOCKING, False),
        'campaignId':
            campaign['id'],
        'archived':
            feed_item.get(FieldMap.PLACEMENT_ARCHIVED, None),
        'siteId':
            feed_item.get(FieldMap.SITE_ID, None),
        'paymentSource':
            'PLACEMENT_AGENCY_PAID',
        'pricingSchedule': {
            'startDate':
                StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_START_DATE, None)),
            'endDate':
                StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_END_DATE, None)),
            'pricingType':
                'PRICING_TYPE_CPM',
            'pricingPeriods': [{
                'startDate':
                    feed_item.get(FieldMap.PLACEMENT_START_DATE, None),
                'endDate':
                    feed_item.get(FieldMap.PLACEMENT_END_DATE, None)
            }]
        }
    }

    self._process_active_view_and_verification(result, feed_item)

    if feed_item.get(FieldMap.PLACEMENT_TYPE, None) == 'VIDEO' or feed_item[
        FieldMap.PLACEMENT_TYPE] == 'IN_STREAM_VIDEO':
      result['compatibility'] = 'IN_STREAM_VIDEO'
      result['size'] = {'width': '0', 'height': '0'}
      result['tagFormats'] = ['PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH']
    else:
      result['compatibility'] = 'DISPLAY'
      width, height = feed_item.get(FieldMap.ASSET_SIZE,
                                    '0x0').strip().lower().split('x')
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
    self._process_pricing_schedule(result, feed_item)

    return result

  def map_placement_transcode_configs(
      self, placement_feed, transcode_configs_feed, pricing_schedule_feed):
    """Maps sub feeds with the parent feed based on placement id.

    Args:
      placement_feed: Bulkdozer feed representing the placements configurations.
      trascode_configs_feed: Bulkdozer feed representing the transcode configs.
      pricing_schedule_feed: Bulkdozer feed representing the pricing schedules.
    """

    for placement in placement_feed:
      placement['pricing_schedule'] = []

      for pricing_schedule in pricing_schedule_feed:
        if placement.get(FieldMap.PLACEMENT_ID,
                         '') == pricing_schedule.get(FieldMap.PLACEMENT_ID, None):
          placement['pricing_schedule'].append(pricing_schedule)

      transcode_id = placement.get(FieldMap.TRANSCODE_ID, '')
      if transcode_id:
        for transcode_config in transcode_configs_feed:
          if transcode_id == transcode_config.get(FieldMap.TRANSCODE_ID, None):
            placement['transcode_config'] = transcode_config
            break
