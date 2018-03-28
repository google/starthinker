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
from traffic.creative_assets import CreativeAssetDAO


class CreativeDAO(BaseDAO):

  def __init__(self, auth, profile_id):
    super(CreativeDAO, self).__init__(auth, profile_id)

    self._entity = 'CREATIVE'
    self._service = self.service.creatives()
    self._id_field = FieldMap.CREATIVE_ID
    self._search_field = FieldMap.CREATIVE_NAME
    self._list_name = 'creatives'

    self.creative_asset_dao = CreativeAssetDAO(auth, profile_id, None)

  def map_creative_and_association_feeds(self, creative_feed,
                                         creative_association_feed):
    for creative in creative_feed:
      creative['associations'] = [
          association for association in creative_association_feed
          if association[FieldMap.CREATIVE_ID] == creative[FieldMap.CREATIVE_ID]
      ]

  def _process_update(self, item, feed_item):
    item['name'] = feed_item[FieldMap.CREATIVE_NAME]

  def _process_new(self, feed_item):
    creative = {
        'advertiserId': feed_item[FieldMap.ADVERTISER_ID],
        'name': feed_item[FieldMap.CREATIVE_NAME],
        'active': True
    }

    if feed_item[FieldMap.CREATIVE_TYPE] == 'VIDEO':
      creative['type'] = 'INSTREAM_VIDEO'

      for association in feed_item.get('associations', []):
        identifier = self.creative_asset_dao.get(association)['assetIdentifier']

        creative['creativeAssets'] = [{
            'assetIdentifier': identifier,
            'role': 'PARENT_VIDEO'
        }]

      del creative['active']
    else:
      raise Exception('Only video is supported at the moment!')
    # (mauriciod@): I didn't pull the display creative stuff from jeltz in here,
    # because I am splitting things up differently, and the backup image will
    # have to be uploaded in the creative_assets dao

    return creative

  def _post_process(self, feed_item, new_item):
    for association in feed_item.get('associations', []):
      association[FieldMap.CREATIVE_ID] = self.get(association)['id']
      association[FieldMap.CREATIVE_ASSET_ID] = self.creative_asset_dao.get(association)['id']
