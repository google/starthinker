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
"""Handles creation and updates of Ads."""

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.landing_page import LandingPageDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.store import store
from starthinker.task.traffic.class_extensions import StringExtensions


class CampaignDAO(BaseDAO):
  """Campaign data access object.

  Inherits from BaseDAO and implements campaign specific logic for creating and
  updating campaigns.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes CampaignDAO with profile id and authentication scheme."""
    super(CampaignDAO, self).__init__(config, auth, profile_id, is_admin)

    self.landing_page_dao = LandingPageDAO(config, auth, profile_id, is_admin)
    self._id_field = FieldMap.CAMPAIGN_ID
    self._search_field = FieldMap.CAMPAIGN_NAME
    self._list_name = 'campaigns'

    self._parent_filter_name = None
    self._parent_filter_field_name = None

    self._entity = 'CAMPAIGN'

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(CampaignDAO, self)._api(iterate).campaigns()

  def _process_update(self, item, feed_item):
    """Updates a campaign based on the values from the feed.

    Args:
      item: Object representing the campaign to be updated, this object is
        updated directly.
      feed_item: Feed item representing campaign values from the Bulkdozer feed.
    """
    lp = self.landing_page_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_ID] = lp['id']
    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME] = lp['name']

    item['startDate'] = StringExtensions.convertDateTimeStrToDateStr(
        feed_item.get(FieldMap.CAMPAIGN_START_DATE, None))
    item['endDate'] = StringExtensions.convertDateTimeStrToDateStr(
        feed_item.get(FieldMap.CAMPAIGN_END_DATE, None))
    item['name'] = feed_item.get(FieldMap.CAMPAIGN_NAME, None)
    item['defaultLandingPageId'] = lp['id']

  def _process_new(self, feed_item):
    """Creates a new campaign DCM object from a feed item representing a campaign from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the campaign from the Bulkdozer feed.

    Returns:
      A campaign object ready to be inserted in DCM through the API.

    """
    lp = self.landing_page_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_ID] = lp['id']
    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME] = lp['name']

    return {
        'advertiserId':
            feed_item.get(FieldMap.ADVERTISER_ID, None),
        'name':
            feed_item.get(FieldMap.CAMPAIGN_NAME, None),
        'startDate':
            StringExtensions.convertDateTimeStrToDateStr(
                feed_item.get(FieldMap.CAMPAIGN_START_DATE, None)),
        'endDate':
            StringExtensions.convertDateTimeStrToDateStr(
                feed_item.get(FieldMap.CAMPAIGN_END_DATE, None)),
        'defaultLandingPageId':
            lp['id']
    }
