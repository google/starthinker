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
"""Handles creation and updates of creative asset association."""

import json

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.campaign import CampaignDAO
from starthinker.task.traffic.creative import CreativeDAO


class CreativeAssociationDAO(BaseDAO):
  """Creative Association data access object.

  Inherits from BaseDAO and implements creative association specific logic for
  creating and
  updating creative association.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes CreativeAssociationDAO with profile id and authentication scheme."""
    super(CreativeAssociationDAO, self).__init__(config, auth, profile_id, is_admin)

    self.config = config
    self._id_field = FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID

    self.campaign_dao = CampaignDAO(config, auth, profile_id, is_admin)
    self.creative_dao = CreativeDAO(config, auth, profile_id, is_admin)

    self._parent_filter_name = None
    self._parent_filter_field_name = None

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(CreativeAssociationDAO,
                 self)._api(iterate).campaignCreativeAssociations()

  def get(self, feed_item):
    """It is not possible to retrieve creative associations from DCM,

    and they are read-only, so the get method just returns None,
    it does this to avoid errors when this is invoked polimorfically.

    For more information on the get method, refer to BaseDAO.

    Args:
      feed_item: Feed item representing the creative association from the
        Bulkdozer feed.

    Returns:
      None.
    """
    return None

  def process(self, feed_item):
    """Processes a feed item by creating the creative association in DCM.

    Args:
      feed_item: Feed item representing the creative association from the
        Bulkdozer feed.

    Returns:
      The newly created object from DCM.
    """
    if not feed_item.get(FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID, None):
      campaign = self.campaign_dao.get(feed_item, required=True)
      creative = self.creative_dao.get(feed_item, required=True)

      if campaign and creative:
        if campaign:
          feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
          feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

        association = {'creativeId': creative['id']}

        result = self._api().insert(
            profileId=self.profile_id,
            campaignId=campaign['id'],
            body=association).execute()

        feed_item[FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID] = '%s|%s' % (
            campaign['id'], creative['id'])

        return result

    return None
