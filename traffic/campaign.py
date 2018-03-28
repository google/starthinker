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

from traffic.dao import BaseDAO
from traffic.landing_page import LandingPageDAO
from traffic.feed import FieldMap
from traffic.store import store

class CampaignDAO(BaseDAO):

  def __init__(self, auth, profile_id):
    super(CampaignDAO, self).__init__(auth, profile_id)

    self.landing_page_dao = LandingPageDAO(auth, profile_id)
    self._id_field = FieldMap.CAMPAIGN_ID
    self._search_field = FieldMap.CAMPAIGN_NAME
    self._list_name = 'campaigns'
    self._entity = 'CAMPAIGN'
    self._service = self.service.campaigns()

  def _process_update(self, item, feed_item):
    lp = self.landing_page_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_ID] = lp['id']
    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME] = lp['name']

    item['startDate'] = feed_item[FieldMap.CAMPAIGN_START_DATE]
    item['endDate'] = feed_item[FieldMap.CAMPAIGN_END_DATE]
    item['name'] = feed_item[FieldMap.CAMPAIGN_NAME]
    item['defaultLandingPageId'] = lp['id']

  def _process_new(self, feed_item):
    lp = self.landing_page_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_ID] = lp['id']
    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME] = lp['name']

    return {
      'advertiserId': feed_item[FieldMap.ADVERTISER_ID],
      'name': feed_item[FieldMap.CAMPAIGN_NAME],
      'startDate': feed_item[FieldMap.CAMPAIGN_START_DATE],
      'endDate': feed_item[FieldMap.CAMPAIGN_END_DATE],
      'defaultLandingPageId': lp['id']
    }
