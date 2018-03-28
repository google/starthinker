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

import os
import json
from apiclient import http

from traffic.dao import BaseDAO
from traffic.feed import FieldMap
from traffic.store import store
from util.storage import object_download


class CreativeAssetDAO(BaseDAO):

  def __init__(self, auth, profile_id, gc_project):
    super(CreativeAssetDAO, self).__init__(auth, profile_id)

    self._entity = 'CREATIVE_ASSET'
    self._service = self.service.creativeAssets()
    self.gc_project = gc_project
    self._list_name = ''
    self._id_field = FieldMap.CREATIVE_ASSET_ID
    self._search_field = None

  def _process_update(self, item, feed_item):
    pass

  def _insert(self, new_item, feed_item):
    local_file = os.path.join('/tmp',
                              feed_item[FieldMap.CREATIVE_ASSET_FILE_NAME])

    self._download_from_gcs(feed_item[FieldMap.CREATIVE_ASSET_BUCKET_NAME],
                            feed_item[FieldMap.CREATIVE_ASSET_FILE_NAME],
                            local_file)

    media = http.MediaFileUpload(local_file)

    if not media.mimetype():
      mimetype = 'application/zip' if asset_type == 'HTML' else 'application/octet-stream'
      media = http.MediaFileUpload(asset_file, mimetype)

    result = self._retry(
        self._service.insert(
            profileId=self.profile_id,
            advertiserId=feed_item[FieldMap.ADVERTISER_ID],
            media_body=media,
            body=new_item))

    os.remove(local_file)

    return result

  def _get(self, feed_item):
    result = store.get(self._entity, feed_item[FieldMap.CREATIVE_ASSET_ID])

    if not result:
      result = {
          'id': feed_item[FieldMap.CREATIVE_ASSET_ID],
          'assetIdentifier': {
              'name': feed_item[FieldMap.CREATIVE_ASSET_NAME],
              'type': feed_item[FieldMap.CREATIVE_TYPE]
          }
      }

      store.set(self._entity, feed_item[FieldMap.CREATIVE_ASSET_ID], result)

    return result

  def _update(self, item, feed_item):
    pass

  def _process_new(self, feed_item):
    return {
        'assetIdentifier': {
            'name': feed_item[FieldMap.CREATIVE_ASSET_FILE_NAME],
            'type': feed_item[FieldMap.CREATIVE_TYPE]
        }
    }

  def _post_process(self, feed_item, item):
    if item['assetIdentifier']['name']:
      feed_item[FieldMap.CREATIVE_ASSET_NAME] = item['assetIdentifier']['name']

  def _download_from_gcs(self, bucket, object_name, local_file):
    object_download(self.gc_project, bucket, object_name, local_file)
