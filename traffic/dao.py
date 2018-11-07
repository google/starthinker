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
"""Module that centralizes all CM data access.

"""

import json
import re
import time
import traceback
import datetime

from apiclient import http
from util.auth import get_service
from traffic.store import store
from traffic.logger import logger


class BaseDAO(object):
  """Parent class to all data access objects.

  Centralizes all common logic to all classes that access CM to create or update
  entities.
  """
  """Version of the CM API to use."""
  API_VERSION = 'v3.2'

  def __init__(self, auth, profile_id):
    """Initializes the object with a specific CM profile ID and an authorization scheme.

    """
    self.service = get_service('dfareporting', self.API_VERSION, auth)
    self.profile_id = profile_id
    self._entity = 'UNDEFINED'
    self._metrics = {}

  def _clean(self, item):
    """Removes null keys from the item.

    An absent key and a null key mean different things in certain contexts for
    CM, this method cleans up objects before sending to the CM API by removing
    any null keys.

    Args:
      item: The CM object to clean.
    """
    # Write code here to remove all null fields from item
    null_keys = []
    for key in item:
      if item[key] == None:
        null_keys.append(key)

    for key in null_keys:
      del item[key]

    return item

  def _get(self, feed_item):
    """Fetches an item from CM.

    Args:
      feed_item: Feed item from Bulkdozer feed representing the item to fetch
        from CM.
    """
    return self._retry(
        self._service.get(
            profileId=self.profile_id, id=feed_item[self._id_field]))

  def get(self, feed_item):
    """Retrieves an item.

    Items could be retrieved from a in memory cache in case it has already been
    retrieved within the current execution. Also, this method is capable of
    translating 'ext' placeholder IDs with concrete CM ids.

    Args:
      feed_item: Feed item from the Bulkdozer feed representing the item to
        retrieve.

    Returns:
      The CM object that represents the identified entity.
    """
    result = None

    # If the id field is provided, and it is not blank
    if self._id_field and feed_item.get(self._id_field, None):
      # If it starts with ext this is a mapping id, and it should be fecthed
      # from the cache
      id_value = feed_item.get(self._id_field, None)

      if id_value and type(id_value) in (str, unicode) and id_value.startswith('ext'):
        dcm_id = store.translate(self._entity, id_value)
        if dcm_id:
          feed_item[self._id_field] = dcm_id
          result = self._get(feed_item)
        else:
          result = store.get(self._entity, id_value)
      else:
        # Otherwise use the ID to fetch it from DCM
        result = self._get(feed_item)
    # If no ID field was provided, check if a search field was, if so try to
    # search for the object
    elif self._search_field and self._search_field in feed_item and len(
        feed_item[self._search_field]) > 0:
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
    """Inserts a new item into CM.

    Args:
      item: The CM object to insert.
      feed_item: The feed item from the Bulkdozer feed representing the item to
        insert.

    Returns:
      The CM object representing the item inserted.
    """
    return self._retry(
        self._service.insert(profileId=self.profile_id, body=item))

  def _update(self, item, feed_item):
    """Updates a new item in CM.

    Args:
      item: The CM object to update.
      feed_item: The feed item from the Bulkdozer feed representing the item to
        update.
    """
    self._retry(self._service.update(profileId=self.profile_id, body=item))

  def start_timer(self, name):
    self._metrics[name] = datetime.datetime.now()

  def end_timer(self, name):
    if name in self._metrics:
      delta = datetime.datetime.now() - self._metrics[name]
      print '%s: %d.%d' % (name, delta.seconds, delta.microseconds / 1000)

  def process(self, feed_item):
    """Processes a Bulkdozer feed item.

    This method identifies if the item needs to be inserted or updated, cleans
    it, performs the CM operations required, and update the feed item with newly
    created ids and name lookups so that the feed can be updated.

    Args:
      feed_item: Bulkdozer feed item to process.

    Returns:
      Newly created or updated CM object.
    """
    item = self.get(feed_item)

    if item:
      self._process_update(item, feed_item)

      self._clean(item)

      self._update(item, feed_item)
    else:
      new_item = self._process_new(feed_item)

      self._clean(new_item)

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
    """Provides an opportunity for sub classes to perform any required operations after the item has been processed.

    Args:
      feed_item: The Bulkdozer feed item that was processed.
      item: The CM object resulting from the process operation.
    """
    pass

  def _retry(self, job, retries=10, wait=30):
    """Handles required logic to ensure robust interactions with the CM API.

    Analyzes errors to determine if retries are appropriate, performs retries,
    and exponential backoff.

    Args:
      job: The API function to execute.
      retries: Optional, defaults to 10. The number of retries before failing.
      wait: Optional, defaults to 30. The number of seconds to wait between
        retries. This number is doubled at each retry (a.k.a. exponential
        backoff).
    """
    try:
      data = job.execute()
      return data
    except http.HttpError, e:
      stack = traceback.format_exc()
      print stack

      msg = str(e)
      match = re.search(r'"(.*)"', msg)

      if e.resp.status in [403, 429, 500, 503]:
        if retries > 0:
          time.sleep(wait)
          return self._retry(job, retries - 1, wait * 2)
        else:
          if match:
            raise Exception('ERROR: %s' % match.group(1))
          else:
            logger.log(msg)

      raise
