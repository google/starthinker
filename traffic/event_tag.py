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
from traffic.campaign import CampaignDAO
from traffic.feed import FieldMap

class EventTagDAO(BaseDAO):

  def __init__(self, auth, profile_id):
    super(EventTagDAO, self).__init__(auth, profile_id)

    self._id_field = FieldMap.EVENT_TAG_ID

    # This causes the dao to search event tag by name, but 
    # to do so it is required to pass campaign or advertiser id
    # self._search_field = FieldMap.EVENT_TAG_NAME
    self._search_field = None

    self._list_name = 'eventTags'
    self._entity = 'EVENT_TAGS'
    self._campaign_dao = CampaignDAO(auth, profile_id)
    self._service = self.service.eventTags()

  def _process_update(self, item, feed_item):
    item['name'] = feed_item[FieldMap.EVENT_TAG_NAME]
    item['status'] = feed_item[FieldMap.EVENT_TAG_STATUS]
    item['type'] = feed_item[FieldMap.EVENT_TAG_TYPE]
    item['url'] = feed_item[FieldMap.EVENT_TAG_URL]

  def _process_new(self, feed_item):
    campaign = self._campaign_dao.get(feed_item)

    return {
      'advertiserId': feed_item[FieldMap.ADVERTISER_ID],
      'campaignId': campaign.get('id', None) if campaign else None,
      'enabledByDefault': feed_item.get(FieldMap.EVENT_TAG_ENABLED_BY_DEFAULT, False),
      'name': feed_item[FieldMap.EVENT_TAG_NAME],
      'status': feed_item[FieldMap.EVENT_TAG_STATUS],
      'type': feed_item[FieldMap.EVENT_TAG_TYPE],
      'url': feed_item[FieldMap.EVENT_TAG_URL]
    }

  def _post_process(self, feed_item, item):
    campaign = self._campaign_dao.get(feed_item)

    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']
    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
