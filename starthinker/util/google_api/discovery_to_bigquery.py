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


class Discovery_To_BigQuery():

  def __init__(self, api, version):
    api_url = 'https://%s.googleapis.com/$discovery/rest?version=%s' % (api, version)
    print('DISCOVERY FETCH:', api_url)
    self.api_document = json.load(request.urlopen(api_url))

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


  def to_schema(self, entry):
    bigquery_schema = []

    for key, value in entry.items():

      if '$ref' in value:
        bigquery_schema.append({
            'name': key,
            'type': 'RECORD',
            'mode': 'NULLABLE',
            'fields': self.to_schema(self.api_document['schemas'][value['$ref']]['properties'])
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
                    'fields': self.to_schema(self.api_document['schemas'][value['items']['$ref']]['properties'])
            })

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

    # List responses wrap their items in a paginated response object
    # Unroll it to return item schema instead of repsonse schema
    if 'List' in resource and resource.endswith('Response'):
      resource = self.api_document['schemas'][resource]['properties'][
          endpoint.split('.')[-1]]['items']['$ref']

    return self.resource_schema(resource)


#x = Discovery_To_BigQuery('displayvideo', 'v1').resource_schema('Advertiser')
#x = Discovery_To_BigQuery('dfareporting', 'v3.4').method_schema('sites', 'list')
#print(json.dumps(x, indent=2))
