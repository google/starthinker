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
"""Manages id maps and caching.

  Id mapping is important because if an execution fails, the context of maps of
  ext ids and concrete CM ids is lost, the Store maintains a persistent map that
  can be referenced througout an execution allowing for successful retries.

  Caching is important for performance reasons, and to reduce the number of
  calls to the CM API.
"""

#import json

#from starthinker.util.sheets import sheets_read, sheets_write, sheets_clear


class Store(object):
  """Class that handles interaction with the Store."""

  def __init__(self):
    """Initializes the store.

    Since this is a sigleton, before the fist usage the trix id and auth scheme
    must be set.
    """
    self._store = {}
    self._id_map = {}


#    self.trix_id = None
#    self.auth = None

#  def load_id_map(self):
#    """Loads the ID map from the Bulkdozer feed into the object.
#
#    """
#    if self.trix_id:
#      data = sheets_read(self.auth, self.trix_id, 'Store', 'A1:Z1')
#      content = ''
#      if data and data[0]:
#        for cell in data[0]:
#          content += cell
#
#        self._id_map = json.loads(content)
#      else:
#        self._id_map = {}

#  def save_id_map(self):
#    """Saves the ID map into the Bulkdozer feed.
#
#    """
#    if self.trix_id:
#      columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']
#
#      data = json.dumps(self._id_map)
#      data = [data[start:start+49999] for start in range(0, len(data), 49999)]
#      sheets_write(self.auth, self.trix_id, 'Store', 'A:' + columns[len(data) + 1], [data])

#  def clear(self):
#    """Clears the store in the Bulkdozer feed.
#
#    """
#    if self.trix_id:
#      sheets_clear(self.auth, self.trix_id, 'Store', 'A1:Z1')
#
#    self._store = {}
#    self._id_map = {}

  def map(self, entity, ext_id, dcm_id):
    """Maps a CM id and an ext id for an entity.

    Args:
      entity: The name of the entity for which the ID relates.
      ext_id: Placeholder ext id.
      dcm_id: Real CM id of the object.
    """
    if not entity in self._id_map:
      self._id_map[entity] = {}

    self._id_map[entity][ext_id] = dcm_id
    self._id_map[entity][dcm_id] = ext_id

  def translate(self, entity, identifier):
    """Given an id, returns its counterpart.

    ext id to cm id and vice versa.

    Args:
      entity: The name of the entity for which the ID relates.
      identifier: Ext id or actual CM id to map.
    """
    if entity in self._id_map and identifier in self._id_map[entity]:
      return self._id_map[entity][identifier]

    return None

  def set(self, entity, keys, item):
    """Sets an item in the cache.

    Args:
      entity: The name of the entity cache to use.
      keys: The keys to set this item to. Typically this will contain the ext id
        and the actual CM id.
      item: The item to cache.
    """
    if not entity in self._store:
      self._store[entity] = {}

    for key in keys:
      self._store[entity][str(key)] = item

  def get(self, entity, key):
    """Gets and item from the cache.

    Args:
      entity: The entity cache to use.
      key: The key to use to lookup the cached item.
    """
    if entity in self._store:
      return self._store[entity].get(str(key))

    return None

store = Store()
