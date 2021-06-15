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
from starthinker.task.traffic.campaign import CampaignDAO
from starthinker.task.traffic.feed import FieldMap


class EventTagDAO(BaseDAO):
  """Event Tag data access object.

  Inherits from BaseDAO and implements Event Tag specific logic for creating and
  updating Event Tags.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes EventTagDAO with profile id and authentication scheme."""
    super(EventTagDAO, self).__init__(config, auth, profile_id, is_admin)

    self._id_field = FieldMap.EVENT_TAG_ID

    # This causes the dao to search event tag by name, but
    # to do so it is required to pass campaign or advertiser id
    # self._search_field = FieldMap.EVENT_TAG_NAME
    #self._search_field = FieldMap.EVENT_TAG_NAME
    self._search_field = None

    self._list_name = 'eventTags'
    self._entity = 'EVENT_TAGS'
    self._parent_filter_name = 'advertiserId'
    self._parent_dao = None
    self._parent_filter_field_name = FieldMap.ADVERTISER_ID
    self._campaign_dao = CampaignDAO(config, auth, profile_id, is_admin)

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(EventTagDAO, self)._api(iterate).eventTags()

  def pre_fetch(self, feed):
    """Pre-fetches all required items to be update into the cache.

    This increases performance for update operations.

    Args:
      feed: List of feed items to retrieve
    """
    pass

  def _get_base_search_args(self, search_string):
    return {
        'profileId': self.profile_id,
        'searchString': search_string,
        'sortField': 'NAME'
    }

  def _process_update(self, item, feed_item):
    """Processes the update of an Event Tag

    Args:
      item: Object representing the event tag to be updated, this object is
        updated directly.
      feed_item: Feed item representing event tag values from the Bulkdozer
        feed.
    """
    item['name'] = feed_item.get(FieldMap.EVENT_TAG_NAME, None)
    item['status'] = feed_item.get(FieldMap.EVENT_TAG_STATUS, None)
    item['type'] = feed_item.get(FieldMap.EVENT_TAG_TYPE, None)
    item['url'] = feed_item.get(FieldMap.EVENT_TAG_URL, None)

  def _process_new(self, feed_item):
    """Creates a new event tag DCM object from a feed item representing a event tag from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the event tag from the Bulkdozer feed.

    Returns:
      A event tag object ready to be inserted in DCM through the API.

    """
    campaign = self._campaign_dao.get(feed_item, required=True)

    return {
        'advertiserId':
            feed_item.get(FieldMap.ADVERTISER_ID, None),
        'campaignId':
            campaign.get('id', None) if campaign else None,
        'enabledByDefault':
            feed_item.get(FieldMap.EVENT_TAG_ENABLED_BY_DEFAULT, False),
        'name':
            feed_item.get(FieldMap.EVENT_TAG_NAME, None),
        'status':
            feed_item.get(FieldMap.EVENT_TAG_STATUS, None),
        'type':
            feed_item.get(FieldMap.EVENT_TAG_TYPE, None),
        'url':
            feed_item.get(FieldMap.EVENT_TAG_URL, None)
    }

  def _post_process(self, feed_item, item):
    """Updates the feed item with ids and names of related object so those can be updated in the Bulkdozer feed.

    Args:
      feed_item: The Bulkdozer feed item.
      item: The CM newly created or updated object.
    """
    campaign = self._campaign_dao.get(feed_item, required=True)

    if campaign:
      feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']
      feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
