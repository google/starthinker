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
"""Handles creation and updates of creative assets."""

import os
import json
import mimetypes
from io import BytesIO

from starthinker.config import BUFFER_SCALE
from starthinker.util.storage import object_get, object_get_chunks, MediaIoBaseUpload
from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.store import store

CHUNKSIZE = int(200 * 1024000 *
                BUFFER_SCALE)  # scale is controlled in config.py


class CreativeAssetDAO(BaseDAO):
  """Creative asset data access object.

  Inherits from BaseDAO and implements ad specific logic for creating and
  updating ads.
  """

  def __init__(self, config, auth, profile_id, is_admin, gc_project):
    """Initializes CreativeAssetDAO with profile id and authentication scheme."""
    super(CreativeAssetDAO, self).__init__(config, auth, profile_id, is_admin)

    self._entity = 'CREATIVE_ASSET'
    self.gc_project = gc_project
    self._list_name = ''
    self._id_field = FieldMap.CREATIVE_ASSET_ID
    self._search_field = None
    self.config = config
    self.auth = auth

    self._parent_filter_name = None
    self._parent_filter_field_name = None

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(CreativeAssetDAO, self)._api(iterate).creativeAssets()

  def pre_fetch(self, feed):
    """Pre-fetches all required items to be update into the cache.

    This increases performance for update operations.

    Args:
      feed: List of feed items to retrieve
    """
    pass

  def _process_update(self, item, feed_item):
    """Handles updates to the creative asset object.

    Since creative assets are read only in DCM, there is nothing to do here,
    this method is mandatory as it is invoked by the BaseDAO class.

    Args:
      item: The creative asset DCM object being updated.
      feed_item: The feed item representing the creative asset from the
        Bulkdozer feed.
    """
    pass

  def _insert(self, new_item, feed_item):
    """Handles the upload of creative assets to DCM and the creation of the associated entity.

    This method makes a call to the DCM API to create a new entity.

    Args:
      new_item: The item to insert into DCM.
      feed_item: The feed item representing the creative asset from the
        Bulkdozer feed.

    Returns:
      The newly created item in DCM.
    """
    filename = feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None)

    file_buffer = object_get(
        self.config,
        'user',
        '%s:%s' % (feed_item.get(FieldMap.CREATIVE_ASSET_BUCKET_NAME, None), filename))

    file_mime = mimetypes.guess_type(filename, strict=False)[0]

    media = MediaIoBaseUpload(
        BytesIO(file_buffer),
        mimetype=file_mime,
        chunksize=CHUNKSIZE,
        resumable=True)

    result = self._api().insert(
        profileId=self.profile_id,
        advertiserId=feed_item.get(FieldMap.ADVERTISER_ID, None),
        media_body=media,
        body=new_item).execute()

    return result

  def _get(self, feed_item):
    """Retrieves an item from DCM or the local cache.

    Args:
      feed_item: The feed item representing the creative asset from the
        Bulkdozer feed.

    Returns:
      Instance of the DCM object either from the API or from the local cache.
    """
    result = store.get(self._entity,
                       feed_item.get(FieldMap.CREATIVE_ASSET_ID, None))

    if not result:
      result = {
          'id': feed_item.get(FieldMap.CREATIVE_ASSET_ID, None),
          'assetIdentifier': {
              'name': feed_item.get(FieldMap.CREATIVE_ASSET_NAME, None),
              'type': feed_item.get(FieldMap.CREATIVE_TYPE, None)
          }
      }

      store.set(self._entity, [feed_item.get(FieldMap.CREATIVE_ASSET_ID, None)],
                result)

    return result

  def _update(self, item, feed_item):
    """Performs an update in DCM.

    Since this method is not allowed for creative assets because those cannot be
    updated, this method reimplements _update from BaseDAO but doesn't do
    anything to prevent an error.

    Args:
      item: The item to update in DCM.
      feed_item: The feed item representing the creative asset in the Bulkdozer
        feed.
    """
    pass

  def _process_new(self, feed_item):
    """Creates a new creative asset DCM object from a feed item representing a creative asset from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the creative asset from the Bulkdozer
        feed.

    Returns:
      A creative asset object ready to be inserted in DCM through the API.

    """
    return {
        'assetIdentifier': {
            'name': feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None),
            'type': feed_item.get(FieldMap.CREATIVE_TYPE, None)
        }
    }

  def _post_process(self, feed_item, item):
    """Maps ids and names of related entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    creative asset feed.

    Args:
      feed_item: Feed item representing the creative asset from the Bulkdozer
        feed.
      item: The DCM creative asset being updated or created.
    """
    if item['assetIdentifier']['name']:
      feed_item[FieldMap.CREATIVE_ASSET_NAME] = item['assetIdentifier']['name']

  def get_identifier(self, association, feed):
    asset_ids = (association.get(FieldMap.CREATIVE_ASSET_ID, None),
                 store.translate(self._entity,
                                 association[FieldMap.CREATIVE_ASSET_ID]))

    for creative_asset in feed.feed:
      if creative_asset[FieldMap.CREATIVE_ASSET_ID] in asset_ids or str(
          creative_asset[FieldMap.CREATIVE_ASSET_ID]) in asset_ids:
        return {
            'name': creative_asset.get(FieldMap.CREATIVE_ASSET_NAME, None),
            'type': creative_asset.get(FieldMap.CREATIVE_TYPE, None)
        }

    return None

  def get_backup_identifier(self, association, feed):

    asset_ids = (association.get(FieldMap.CREATIVE_BACKUP_ASSET_ID, None),
                 store.translate(
                     self._entity,
                     association[FieldMap.CREATIVE_BACKUP_ASSET_ID]))

    for creative_asset in feed.feed:
      if creative_asset[FieldMap.CREATIVE_ASSET_ID] in asset_ids or str(
          creative_asset[FieldMap.CREATIVE_ASSET_ID]) in asset_ids:
        return {
            'name': creative_asset.get(FieldMap.CREATIVE_ASSET_NAME, None),
            'type': creative_asset.get(FieldMap.CREATIVE_TYPE, None)
        }

    return None
