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

import json
from urllib import request
from googleapiclient.schema import Schemas


def discovery_type(object):

  # https://developers.google.com/discovery/v1/type-format
  # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types

  t = object.get('type')
  f = object.get('format')

  if t == 'any':
    return 'STRING'
  elif t == 'array':
    return 'REPEATED'
  elif t == 'boolean':
    return 'BOOLEAN'
  elif t == 'integer':
    return 'INT64'
  elif t == 'number':
    if f == 'double':
      return 'NUMBER'
    else:
      return 'FLOAT'
  elif t == 'object':
    return 'STRUCT'
  elif t == 'string':
    if f == 'byte':
      return 'BYTES'
    elif f == 'date':
      return 'DATE'
    elif f == 'date-time':
      return 'DATETIME'
    elif f == 'int64':
      return 'INT64'
    elif f == 'uint64':
      return 'INT64'
    else:
      return 'STRING'
  else:
    return 'STRING'


def discovery_download(api, version):
  return json.load(
      request.urlopen('https://%s.googleapis.com/$discovery/rest?version=%s' %
                      (api, version)))


def discovery_schema(api,
                     version,
                     resource,
                     api_schema=None,
                     object_schema=None):

  if not resource:
    return None

  if not api_schema:
    api_document = discovery_download(api, version)
    api_schema = Schemas(api_document)

  if not object_schema:
    object_schema = api_schema.get(resource)['properties']

  bigquery_schema = []

  for key, value in object_schema.items():

    if '$ref' in value:
      bigquery_schema.append({
          'name': key,
          'type': 'RECORD',
          'mode': 'NULLABLE',
          'fields': discovery_schema(api, version, value['$ref'], api_schema)
      })

    else:

      if value['type'] == 'array':

        if '$ref' in value['items']:
          bigquery_schema.append({
              'name':
                  key,
              'type':
                  'RECORD',
              'mode':
                  'REPEATED',
              'fields':
                  discovery_schema(api, version, value['items']['$ref'],
                                   api_schema)
          })

        else:
          bigquery_schema.append({
              'description': ', '.join(value['items'].get('enum', [])),
              'name': key,
              'type': discovery_type(value['items']),
              'mode': 'REPEATED',
          })

      else:
        bigquery_schema.append({
            'description': ', '.join(value.get('enum', [])),
            'name': key,
            'type': discovery_type(value),
            'mode': 'NULLABLE'
        })

  return bigquery_schema


#x = discovery_schema('displayvideo', 'v1', 'Advertiser')
#print(json.dumps(x, indent=2))
