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
"""Module that centralizes all CM data access."""

from starthinker.util.google_api import API_DCM
from starthinker.task.traffic.store import store


class BaseDAO(object):
  """Parent class to all data access objects.

  Centralizes all common logic to all classes that access CM to create or update
  entities.
  """

  def __init__(self, config, auth, profile_id, is_admin=False):
    """Initializes the object with a specific CM profile ID and an authorization scheme."""
    self.config = config
    self.auth = auth
    self.is_admin = is_admin
    self.profile_id = profile_id
    self._entity = 'UNDEFINED'
    self._metrics = {}

  def _api(self, iterate=False):
    """Returns an DCM API instance.

    Must be overloaded by one of the derived classes and extended for
    specific endpoint.
    """
    return API_DCM(self.config, self.auth, iterate, self.is_admin)

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

    if 'adBlockingOptOut' in item and not item['adBlockingOptOut']:
      item['adBlockingOptOut'] = False

    return item

  def _get(self, feed_item):
    """Fetches an item from CM.

    Args:
      feed_item: Feed item from Bulkdozer feed representing the item to fetch
        from CM.
    """
    #print('hitting the api to get %s, %s' % (self._entity, feed_item[self._id_field]))
    return self._api().get(
        profileId=self.profile_id, id=feed_item[self._id_field]).execute()

  def get(self, feed_item, required=False, column_name=None):
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
    keys = []
    id_value = feed_item.get(self._id_field,
                             None) if column_name == None else feed_item.get(
                                 column_name, None)

    if not id_value and self._search_field and feed_item.get(
        self._search_field, None):
      store_key = feed_item[self._search_field]

      if self._parent_filter_name:
        if feed_item.get(self._parent_filter_field_name, None):
          store_key = str(feed_item.get(self._parent_filter_field_name,
                                        None)) + store_key

      result = store.get(self._entity, store_key)

      if not result:
        result, key = self._get_by_name(feed_item)
        keys.append(key)

      if not result and required:
        raise Exception('ERROR: Could not find %s with name %s' %
                        (self._entity, feed_item[self._search_field]))
    elif id_value:
      if isinstance(id_value, str) and id_value.startswith('ext'):
        keys.append(id_value)
        id_value = store.translate(self._entity, id_value)

        if id_value and not column_name:
          feed_item[self._id_field] = id_value

        elif id_value and column_name:
          feed_item[column_name] = id_value

      if id_value:
        keys.append(id_value)
        result = store.get(self._entity, id_value)

        if not result:
          result = self._get(feed_item)

        if not result and required:
          raise Exception('ERROR: Could not find %s with id %s' %
                          (self._entity, id_value))

    store.set(self._entity, keys, result)

    return result

  def _get_base_search_args(self, search_string):
    return {
        'profileId': self.profile_id,
        'searchString': search_string,
        'sortField': 'NAME',
        'maxResults': 2
    }

  def _get_by_name(self, feed_item):
    """Searches CM for an item of name defined in the search field of the DAO class.

    If more than one item is returned an error is raised, e.g. if there are more
    than one item with the same name.

    Args:
      feed_item: The Bulkdozer feed item with the name to search for.

    Returns:
      If found, the CM entity object that matches the search string.
    """
    key = ''
    if self._search_field:
      key = feed_item[self._search_field].strip()

      search_string = feed_item[self._search_field].strip()
      args = self._get_base_search_args(search_string)

      if self._parent_filter_name:
        if feed_item.get(self._parent_filter_field_name, None):
          args[self._parent_filter_name] = feed_item.get(
              self._parent_filter_field_name, None)
        elif self._parent_dao:
          parent = self._parent_dao.get(feed_item, required=True)
          if parent:
            args[self._parent_filter_name] = parent.get('id', None)

        key = str(args.get(self._parent_filter_name, '')) + key

      print('hitting the api to search for %s, %s' %
            (self._entity, search_string))
      search_result = self._api().list(**args).execute()

      items = search_result[self._list_name]

      if items and len(items) > 0:
        item = items[0]

        if search_string == item['name']:
          if len(items) > 1 and items[1]['name'] == search_string:
            raise Exception('ERROR: More than one item found with %s %s' %
                            (self._search_field, feed_item[self._search_field]))
          else:
            return item, key

    return None, key

  def _insert(self, item, feed_item):
    """Inserts a new item into CM.

    Args:
      item: The CM object to insert.
      feed_item: The feed item from the Bulkdozer feed representing the item to
        insert.

    Returns:
      The CM object representing the item inserted.
    """
    #print('ITEM', item)
    return self._api().insert(profileId=self.profile_id, body=item).execute()

  def _update(self, item, feed_item):
    """Updates a new item in CM.

    Args:
      item: The CM object to update.
      feed_item: The feed item from the Bulkdozer feed representing the item to
        update.
    """
    #print('ITEM', item)
    self._api().update(profileId=self.profile_id, body=item).execute()

  def pre_fetch(self, feed):
    """Pre-fetches all required items to be update into the cache.

    This increases performance for update operations.

    Args:
      feed: List of feed items to retrieve
    """
    if hasattr(self, '_list_name') and self._list_name and self._id_field:
      print('pre fetching %s' % self._list_name)
      ids = [
          feed_item[self._id_field]
          for feed_item in feed
          if isinstance(feed_item[self._id_field], int)
      ]

      if ids:
        for i in range(0, len(ids), 500):
          results = self._api(iterate=True).list(
              profileId=self.profile_id, ids=ids[i:i + 500]).execute()
          for item in results:
            store.set(self._entity, [item['id']], item)

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

      if self._search_field and feed_item.get(self._search_field, ''):
        store.map(self._entity, feed_item.get(self._search_field), item['id'])
        store.set(self._entity, [feed_item[self._search_field]], item)

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
