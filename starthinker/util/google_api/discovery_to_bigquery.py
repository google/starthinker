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
import re
from urllib import request

from googleapiclient.schema import Schemas

DATETIME_RE = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}:\d{2}\.?\d+Z')
DESCRIPTION_LENGTH = 1024
RECURSION_DEPTH = 5


class Discovery_To_BigQuery():

  def __init__(self, api, version, key=None, recursion_depth=RECURSION_DEPTH):
    self.key = key or ''
    self.recursion_depth = recursion_depth
    api_url = 'https://%s.googleapis.com/$discovery/rest?version=%s&key=%s' % (
        api, version, self.key)
    print('DISCOVERY FETCH:', api_url)
    self.api_document = json.load(request.urlopen(api_url))

  @staticmethod
  def preferred_version(api_name, key=None):
    api_url = 'https://discovery.googleapis.com/discovery/v1/apis?name=%s&key=%s&preferred=true' % (
        api_name, key or '')
    print(api_url)
    api_info = json.load(request.urlopen(api_url))
    return api_info['items'][0]['version']

  @staticmethod
  def clean(struct):
    if isinstance(struct, dict):
      for key, value in struct.items():
        if isinstance(value, str) and DATETIME_RE.match(value):
          struct[key] = struct[key].replace('.000Z', 'Z')
        else:
          Discovery_To_BigQuery.clean(value)
    elif isinstance(struct, list):
      for index, value in enumerate(struct):
        if isinstance(value, str) and DATETIME_RE.match(value):
          struct[index] = struct[index].replace('.000Z', 'Z')
        else:
          Discovery_To_BigQuery.clean(value)
    return struct

  def to_type(self, entry):

    # https://developers.google.com/discovery/v1/type-format
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types

    t = entry.get('type')
    f = entry.get('format')

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


  def to_schema(self, entry, parents={}):
    bigquery_schema = []

    for key, value in entry.items():

      if '$ref' in value:
        parents.setdefault(value['$ref'], 0)
        if parents[value['$ref']] < self.recursion_depth:
          parents[value['$ref']] += 1
          bigquery_schema.append({
              'name':
                  key,
              'type':
                  'RECORD',
              'mode':
                  'NULLABLE',
              'fields':
                  self.to_schema(
                      self.api_document['schemas'][value['$ref']]['properties'],
                      parents)
          })
        parents[value['$ref']] -= 1

      else:

        if value['type'] == 'array':

          if '$ref' in value['items']:
            parents.setdefault(value['items']['$ref'], 0)
            if parents[value['items']['$ref']] < self.recursion_depth:
              parents[value['items']['$ref']] += 1
              bigquery_schema.append({
                  'name':
                      key,
                  'type':
                      'RECORD',
                  'mode':
                      'REPEATED',
                  'fields':
                      self.to_schema(
                          self.api_document['schemas'][value['items']['$ref']]
                          ['properties'], parents)
              })
              parents[value['items']['$ref']] -= 1

          else:
            bigquery_schema.append({
                'description': (', '.join(value['items'].get('enum', [])))
                               [:DESCRIPTION_LENGTH],
                'name':
                    key,
                'type':
                    self.to_type(value['items']),
                'mode':
                    'REPEATED',
            })

        else:
          bigquery_schema.append({
              'description': (', '.join(value.get('enum', [])))
                             [:DESCRIPTION_LENGTH],
              'name':
                  key,
              'type':
                  self.to_type(value),
              'mode':
                  'NULLABLE'
          })

    return bigquery_schema


  def resource_schema(self, resource):
    entry = self.api_document['schemas'][resource]['properties']
    return self.to_schema(entry)


  def method_schema(self, method):
    endpoint, method = method.rsplit('.', 1)
    resource = self.api_document

    for e in endpoint.split('.'):
      resource = resource['resources'][e]
    resource = resource['methods'][method]['response']['$ref']

    # get schema
    properties = self.api_document['schemas'][resource]['properties']
    schema = self.to_schema(properties)

    # List responses wrap their items in a paginated response object
    # Unroll it to return item schema instead of repsonse schema
    if 'List' in resource and resource.endswith('Response'):
      for entry in schema:
        if entry['type'] == 'RECORD':
          return entry['fields']
        elif entry['mode'] == 'REPEATED':
          entry['mode'] = 'NULLABLE'
          return [entry]
      # raise exception after checking all fields for a list
      raise ('Unahandled discovery schema.')
    else:
      return schema


#x = Discovery_To_BigQuery('displayvideo', 'v1').resource_schema('Advertiser')
#x = Discovery_To_BigQuery('dfareporting', 'v3.4').method_schema('sites', 'list')
#print(json.dumps(x, indent=2))
