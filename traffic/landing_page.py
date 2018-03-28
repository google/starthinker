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
from traffic.feed import FieldMap

class LandingPageDAO(BaseDAO):

  def __init__(self, auth, profile_id):
    super(LandingPageDAO, self).__init__(auth, profile_id)

    self._service = self.service.advertiserLandingPages()
    self._id_field = FieldMap.CAMPAIGN_LANDING_PAGE_ID
    self._search_field = FieldMap.CAMPAIGN_LANDING_PAGE_NAME
    self._list_name = 'landingPages'
    self._entity = 'LANDING_PAGE'

  def _process_update(self, item, feed_item):
    item['name'] = feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME]
    item['url'] = feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_URL]

  def _process_new(self, feed_item):
    return {
      'name': feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME],
      'url': feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_URL],
      'advertiserId': feed_item[FieldMap.ADVERTISER_ID]
    }
