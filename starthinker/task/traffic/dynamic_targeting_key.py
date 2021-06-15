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
"""Handles creation and updates of dynamic targeting keys."""

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.store import store


class DynamicTargetingKeyDAO(BaseDAO):
  """Landing page data access object.

  Inherits from BaseDAO and implements dynamic targeting key specific logic for
  creating
  and
  updating dynamic targeting key.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes DynamicTargetingKeyDAO with profile id and authentication scheme."""

    super(DynamicTargetingKeyDAO, self).__init__(config, auth, profile_id, is_admin)

    self._id_field = None
    self._search_field = None
    self._list_name = 'dynamicTargetingKeys'
    self._entity = 'DYNAMIC_TARGETING_KEY'
    self._parent_filter_name = None
    self._parent_filter_field_name = None
    self._parent_dao = None
    self._key_cache = {}

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(DynamicTargetingKeyDAO,
                 self)._api(iterate).dynamicTargetingKeys()

  def _key_exists(self, advertiser_id, key_name):
    cache_key = str(advertiser_id) + key_name

    if not cache_key in self._key_cache:
      keys = self._api().list(
          profileId=self.profile_id,
          advertiserId=advertiser_id,
          names=[key_name]).execute()

      self._key_cache[cache_key] = 'dynamicTargetingKeys' in keys and len(
          keys['dynamicTargetingKeys']) > 0

    return self._key_cache[cache_key]

  def _create_key(self, key_name, object_type, object_id):
    key = {'name': key_name, 'objectId': object_id, 'objectType': object_type}

    self._api().insert(profileId=self.profile_id, body=key).execute()

    if object_type == 'OBJECT_ADVERTISER':
      cache_key = str(object_id) + key_name
      self._key_cache[cache_key] = True

  def process(self, feed_item):
    """Processes a Bulkdozer feed item.

    This method identifies if the dyanmic targeting key already exists in CM, if
    it doesn't it creates it associated with the advertiser, and then inserts an
    association with the identified object.

    Args:
      feed_item: Bulkdozer feed item to process.

    Returns:
      Newly created or updated CM object.
    """
    if feed_item.get(FieldMap.ADVERTISER_ID, None) and feed_item.get(
        FieldMap.DYNAMIC_TARGETING_KEY_NAME, None):
      if not self._key_exists(
          feed_item.get(FieldMap.ADVERTISER_ID, None),
          feed_item.get(FieldMap.DYNAMIC_TARGETING_KEY_NAME, None)):
        self._create_key(
            feed_item.get(FieldMap.DYNAMIC_TARGETING_KEY_NAME, None),
            'OBJECT_ADVERTISER', feed_item.get(FieldMap.ADVERTISER_ID, None))

      object_type = feed_item.get(FieldMap.DYNAMIC_TARGETING_KEY_OBJECT_TYPE, None)
      entity_id = feed_item.get(FieldMap.DYNAMIC_TARGETING_KEY_OBJECT_ID, None)

      if object_type and len(object_type) > 7:
        entity = object_type[7:]
        translated_id = store.translate(entity, entity_id)
        entity_id = translated_id or entity_id

      self._create_key(
          feed_item.get(FieldMap.DYNAMIC_TARGETING_KEY_NAME, None),
          object_type,
          entity_id)

      feed_item[FieldMap.DYNAMIC_TARGETING_KEY_OBJECT_ID] = entity_id

    else:
      raise Exception(
          'Dynamic targeting key, %s and %s are required' %
          (FieldMap.ADVERTISER_ID, FieldMap.DYNAMIC_TARGETING_KEY_NAME))
