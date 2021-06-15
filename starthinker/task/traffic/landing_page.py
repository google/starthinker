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
"""Handles creation and updates of landing pages."""

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap


class LandingPageDAO(BaseDAO):
  """Landing page data access object.

  Inherits from BaseDAO and implements landing page specific logic for creating
  and
  updating landing pages.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes LandingPageDAO with profile id and authentication scheme."""

    super(LandingPageDAO, self).__init__(config, auth, profile_id, is_admin)

    self._id_field = FieldMap.CAMPAIGN_LANDING_PAGE_ID
    self._search_field = FieldMap.CAMPAIGN_LANDING_PAGE_NAME
    self._list_name = 'landingPages'
    self._entity = 'LANDING_PAGE'
    self._parent_filter_name = 'advertiserIds'
    self._parent_filter_field_name = FieldMap.ADVERTISER_ID
    self._parent_dao = None

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(LandingPageDAO, self)._api(iterate).advertiserLandingPages()

  def _process_update(self, item, feed_item):
    """Updates an landing page based on the values from the feed.

    Args:
      item: Object representing the landing page to be updated, this object is
        updated directly.
      feed_item: Feed item representing landing page values from the Bulkdozer
        feed.
    """

    item['name'] = feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_NAME, None)
    item['url'] = feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_URL, None)

  def _process_new(self, feed_item):
    """Creates a new landing page DCM object from a feed item representing a landing page from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the landing page from the Bulkdozer
        feed.

    Returns:
      An landing page object ready to be inserted in DCM through the API.

    """
    return {
        'name': feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_NAME, None),
        'url': feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_URL, None),
        'advertiserId': feed_item.get(FieldMap.ADVERTISER_ID, None)
    }
