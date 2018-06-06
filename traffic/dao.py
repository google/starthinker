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
import time
import traceback

from apiclient import http
from util.auth import get_service
from traffic.store import store
from traffic.logger import logger

class BaseDAO(object):

  API_VERSION = 'v3.0'

  def __init__(self, auth, profile_id):
    self.service = get_service('dfareporting', self.API_VERSION, auth)
    self.profile_id = profile_id
    self._entity = 'UNDEFINED'

  def _get(self, feed_item):
    return self._retry(
        self._service.get(
            profileId=self.profile_id, id=feed_item[self._id_field]))

  def get(self, feed_item):
    result = None

    # If the id field is provided, and it is not blank
    if self._id_field and len(feed_item.get(self._id_field, '')) > 0:
      # If it starts with ext this is a mapping id, and it should be fecthed
      # from the cache
      if feed_item[self._id_field].startswith('ext'):
        dcm_id = store.translate(self._entity, feed_item[self._id_field])
        if dcm_id:
          feed_item[self._id_field] = dcm_id
          result = self._get(feed_item)
        else:
          result = store.get(self._entity, feed_item[self._id_field])
      else:
        # Otherwise use the ID to fetch it from DCM
        result = self._get(feed_item)
    # If no ID field was provided, check if a search field was, if so try to
    # search for the object
    elif self._search_field and self._search_field in feed_item and len(feed_item[self._search_field]) > 0:
      result = store.get(self._entity, feed_item[self._search_field])
      if not result:
        item_list = self._retry(
            self._service.list(
                profileId=self.profile_id,
                searchString=feed_item[self._search_field]))

        # If there is more than 1 item that matches the search, we can't
        # reliably select which one should be used, so throw an exception
        if item_list and len(item_list[self._list_name]) > 1:
          raise Exception('More than one item found with the provided name: %s'
                          % feed_item[self._search_field])
        if item_list and len(item_list[self._list_name]) == 1:
          result = item_list[self._list_name][0]

    # If an item was found, add it to the cache
    if result:
      keys = []
      if self._id_field and self._id_field in feed_item:
        keys.append(feed_item[self._id_field])

      if 'id' in result:
        keys.append(result['id'])

      if self._search_field and self._search_field in feed_item:
        keys.append(feed_item[self._search_field])

      store.set(self._entity, keys, result)

    return result

  def _insert(self, item, feed_item):
    return self._retry(
        self._service.insert(profileId=self.profile_id, body=item))

  def _update(self, item, feed_item):
    self._retry(self._service.update(profileId=self.profile_id, body=item))

  def process(self, feed_item):
    item = self.get(feed_item)

    if item:
      self._process_update(item, feed_item)
      self._update(item, feed_item)
    else:
      new_item = self._process_new(feed_item)
      item = self._insert(new_item, feed_item)

      if self._id_field and feed_item.get(self._id_field, '').startswith('ext'):
        store.map(self._entity, feed_item.get(self._id_field), item['id'])
        store.set(self._entity, [feed_item[self._id_field]], item)

    if item:
      feed_item[self._id_field] = item['id']
      store.set(self._entity, [item['id']], item)

    self._post_process(feed_item, item)

    return item

  def _post_process(self, feed_item, item):
    pass

  def _retry(self, job, retries=10, wait=30):
    try:
      data = job.execute()
      return data
    except http.HttpError, e:
      msg = traceback.format_exc()
      print msg
      logger.log(msg)
      if e.resp.status in [403, 429, 500, 503]:
        if retries > 0:
          time.sleep(wait)
          return self._retry(job, retries - 1, wait * 2)
        else:
          raise
