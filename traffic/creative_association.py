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
from traffic.feed import FieldMap
from traffic.campaign import CampaignDAO
from traffic.creative import CreativeDAO


class CreativeAssociationDAO(BaseDAO):

  def __init__(self, auth, profile_id):
    super(CreativeAssociationDAO, self).__init__(auth, profile_id)

    self._service = self.service.campaignCreativeAssociations()
    self._id_field = FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID

    self.campaign_dao = CampaignDAO(auth, profile_id)
    self.creative_dao = CreativeDAO(auth, profile_id)

  def get(self, feed_item):
    return None

  def process(self, feed_item):

    if feed_item[FieldMap.
                 CREATIVE_ID] and feed_item[FieldMap.
                                            CAMPAIGN_ID] and not feed_item[FieldMap.
                                                                           CAMPAIGN_CREATIVE_ASSOCIATION_ID]:
      campaign = self.campaign_dao.get(feed_item)
      creative = self.creative_dao.get(feed_item)

      association = {'creativeId': creative['id']}

      result = self._retry(
          self._service.insert(
              profileId=self.profile_id,
              campaignId=campaign['id'],
              body=association))

      feed_item[FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID] = '%s|%s' % (
        campaign['id'], creative['id'])

      return result
