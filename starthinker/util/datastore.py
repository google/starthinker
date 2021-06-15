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
"""Simple datastor implentation for storing key/value pairs quickly.

Datastore concepts similar to a database:
- Namespace is like database name.
- Kind is like database table.
- Key is like a primary key.
- Data is like a row or record passed in as a dictionary )

Use cases:

Quickly store a dictionary of data for lookup from different machines.
More specific logging, where key is object ID.

"""

import datetime

from starthinker.util.google_api import API_Datastore


def _datastore_p_to_v(properties):
  """Very simple conversion from datastore types to python types.

  Handles
    - nullValue
    - stringValue
    - integerValue
    - doubleValue
    - booleanValue
    - timestampValue

  Omitted For Simplicity ( add as needed )
    - keyValue
    - entityValue
    - blobValue
    - geoPointValue
    - arrayValue

  """

  v = {}

  for p, d in properties.items():
    for dk, dv in d.items():
      if dk.endswith('Value'):
        if dk == 'nullValue':
          v[p] = dv
        elif dk == 'stringValue':
          v[p] = dv
        elif dk == 'integerValue':
          v[p] = int(dv)
        elif dk == 'doubleValue':
          v[p] = float(dv)
        elif dk == 'booleanValue':
          v[p] = bool(dv)
        elif dk == 'timestampValue':
          v[p] = datetime.datetime.strptime(dv + 'UTC',
                                            '%Y-%m-%dT%H:%M:%S.%fZ%Z')
        else:
          raise Exception(
              'No mapping from python to datastore for type of: %s' % k)

  return v


def _datastore_path(path):
  return '.'.join([p['name'] for p in path])


def _datastore_v_to_p(values):
  """Very simple conversion from datastore types to python types.

  Handles
    - nullValue
    - stringValue
    - integerValue
    - doubleValue
    - booleanValue
    - timestampValue

  Omitted For Simplicity ( add as needed )
    - keyValue
    - entityValue
    - blobValue
    - geoPointValue
    - arrayValue

  """

  p = {}

  for k, v in values.items():
    if v is None:
      p[k] = {'nullValue': v}
    elif isinstance(v, str):
      p[k] = {'stringValue': v, 'excludeFromIndexes': True}
    elif isinstance(v, int):
      p[k] = {'integerValue': v, 'excludeFromIndexes': True}
    elif isinstance(v, float):
      p[k] = {'doubleValue': v, 'excludeFromIndexes': True}
    elif isinstance(v, bool):
      p[k] = {'booleanValue': v, 'excludeFromIndexes': True}
    elif isinstance(v, datetime.datetime):
      p[k] = {
          'timestampValue': v.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          'excludeFromIndexes': True
      }
    else:
      raise Exception('No mapping from python to datastore for type of: %s' % k)

  return p


def datastore_write(config, auth, project_id, namespace, kind, key, values):
  """Writes a single row to datastore.

  For simplicity this is designed to store a single dictionary of values.

  Args
    - namespace (string): database
    - kind (string): table
    - key (string): primary key used for lookup
    - values (dictionary): record

  """

  body = {
      'mode':
          'NON_TRANSACTIONAL',
      'mutations': [{
          'upsert': {
              'key': {
                  'path': [{
                      'kind': kind,
                      'name': key
                  }],
                  'partitionId': {
                      'projectId': project_id,
                      'namespaceId': namespace
                  }
              },
              'properties': _datastore_v_to_p(values)
          }
      }]
  }

  API_Datastore(config, auth).projects().commit(
      projectId=project.id, body=body).execute()


def datastore_read(config, auth, project_id, namespace, kind, key):
  """Reads records from datastore based on supplied keys.

  Works on a single key, or an array of keys. Returns an iterator
  of tuples that can be cast to a list or a string:

  Sample usage:
    lookup_items = dict(datastore_read, "user", "some_project",
    "some_namespace", "some_kind", "some_key"))
    sort_items = list(datastore_read, "user", "some_project", "some_namespace",
    "some_kind", "some_key"))

  Args
    - namespace (string): database
    - kind (string): table
    - key (string or list): primary keys used for lookup

  Returns
    - key (string), values (dict): tuple iterator, even if single result
  """

  #response = API_Datastore(config, auth).projects().beginTransaction(
  #  projectId=project_id,
  #  body={
  #    "transactionOptions": { "readOnly":{} }
  #  }
  #).execute()

  # if single key givem turn it into a list
  if isinstance(key, str):
    key = [key]

  body = {
      'readOptions': {
          'readConsistency': 'STRONG'
      },
      'keys': [{
          'path': [{
              'kind': kind,
              'name': k
          }],
          'partitionId': {
              'projectId': project_id,
              'namespaceId': namespace
          }
      } for k in key]
  }

  response = API_Datastore(config, auth).projects().lookup(
      projectId=project.id, body=body).execute()

  # ignore missing, just do found for simplicity
  for e in response.get('found', []):
    yield _datastore_path(e['entity']['key']['path']), _datastore_p_to_v(
        e['entity']['properties'])


def datastore_list(config, auth, project_id, namespace, kind):
  """Reads all records from a datastore.

  Simplified query implementation that fetches all records. Designed for small
  non relational
  work.

  Sample usage:
    lookup_items = dict(datastore_list, "user", "some_project",
    "some_namespace", "some_kind"))
    sort_items = list(datastore_list, "user", "some_project", "some_namespace",
    "some_kind"))

  Args
    - namespace (string): database
    - kind (string): table

  Returns
    - key (string), values (dict): tuple iterator

  """

  body = {
      'partitionId': {
          'projectId': project_id,
          'namespaceId': namespace
      },
      'readOptions': {},
      'query': {
          'kind': [{
              'name': kind
          }]
      }
  }

  response = {'batch': {'moreResults': '', 'endCursor': None}}

  while response['batch']['moreResults'] != 'NO_MORE_RESULTS':
    body['query']['startCursor'] = response['batch']['endCursor']
    response = API_Datastore(config, auth).projects().runQuery(
        projectId=project.id, body=body).execute()

    for e in response['batch'].get('entityResults', []):
      yield _datastore_path(e['entity']['key']['path']), _datastore_p_to_v(
          e['entity']['properties'])
