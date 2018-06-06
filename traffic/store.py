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

from util.sheets import sheets_read, sheets_write


class Store(object):

  def __init__(self):
    self._store = {}
    self._id_map = {}

    self.trix_id = None
    self.auth = None

  def load_id_map(self):
    if self.trix_id:
      data = sheets_read(self.auth, self.trix_id, 'Store', 'A1')
      if data and data[0]:
        self._id_map = json.loads(data[0][0])
      else:
        self._id_map = {}

  def _save_id_map(self):
    if self.trix_id:
      sheets_write(self.auth, self.trix_id, 'Store', 'A1', [[json.dumps(self._id_map)]])

  def map(self, entity, ext_id, dcm_id):
    if not entity in self._id_map:
      self._id_map[entity] = {}

    self._id_map[entity][ext_id] = dcm_id
    self._id_map[entity][dcm_id] = ext_id
    self._save_id_map()

  def translate(self, entity, identifier):
    if entity in self._id_map and identifier in self._id_map[entity]:
      return self._id_map[entity][identifier]

    return None

  def set(self, entity, keys, item):
    if not entity in self._store:
      self._store[entity] = {}

    for key in keys:
      self._store[entity][key] = item

  def get(self, entity, key):
    if entity in self._store:
      return self._store[entity].get(key)

    return None


store = Store()
