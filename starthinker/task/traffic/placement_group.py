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
"""Handles creation and updates of placement groups."""

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.campaign import CampaignDAO
from starthinker.task.traffic.feed import FieldMap


class PlacementGroupDAO(BaseDAO):
  """Placement group data access object.

  Inherits from BaseDAO and implements placement group specific logic for
  creating
  and
  updating placement group.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes PlacementGroupDAO with profile id and authentication scheme."""

    super(PlacementGroupDAO, self).__init__(config, auth, profile_id, is_admin)

    self.campaign_dao = CampaignDAO(config, auth, profile_id, is_admin)

    self._id_field = FieldMap.PLACEMENT_GROUP_ID
    self._search_field = FieldMap.PLACEMENT_GROUP_NAME
    self._list_name = 'placementGroups'
    self._entity = 'PLACEMENT_GROUP'

    self._parent_filter_name = 'campaignIds'
    self._parent_filter_field_name = FieldMap.CAMPAIGN_ID
    self._parent_dao = self.campaign_dao

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(PlacementGroupDAO, self)._api(iterate).placementGroups()

  def _process_update(self, item, feed_item):
    """Updates a placement group based on the values from the feed.

    Args:
      item: Object representing the placement group to be updated, this object
        is updated directly.
      feed_item: Feed item representing placement group values from the
        Bulkdozer feed.
    """
    campaign = self.campaign_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    item['name'] = feed_item.get(FieldMap.PLACEMENT_GROUP_NAME, None)
    item['placementGroupType'] = feed_item.get(FieldMap.PLACEMENT_GROUP_TYPE,
                                               None)
    item['pricingSchedule']['startDate'] = feed_item.get(
        FieldMap.PLACEMENT_GROUP_START_DATE, None)
    item['pricingSchedule']['endDate'] = feed_item.get(
        FieldMap.PLACEMENT_GROUP_END_DATE, None)
    item['pricingSchedule']['pricingType'] = feed_item.get(
        FieldMap.PLACEMENT_GROUP_PRICING_TYPE, None)

  def _process_new(self, feed_item):
    """Creates a new placement group DCM object from a feed item representing a placement group from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the placement group from the Bulkdozer
        feed.

    Returns:
      A placement group object ready to be inserted in DCM through the API.

    """
    campaign = self.campaign_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    return {
        'advertiserId':
            feed_item.get(FieldMap.ADVERTISER_ID, None),
        'campaignId':
            campaign['id'] if campaign else None,
        'siteId':
            feed_item.get(FieldMap.SITE_ID, None),
        'name':
            feed_item.get(FieldMap.PLACEMENT_GROUP_NAME, None),
        'placementGroupType':
            feed_item.get(FieldMap.PLACEMENT_GROUP_TYPE, None),
        'pricingSchedule': {
            'startDate':
                feed_item.get(FieldMap.PLACEMENT_GROUP_START_DATE, None),
            'endDate':
                feed_item.get(FieldMap.PLACEMENT_GROUP_END_DATE, None),
            'pricingType':
                feed_item.get(FieldMap.PLACEMENT_GROUP_PRICING_TYPE, None)
        }
    }
