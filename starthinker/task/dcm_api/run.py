###########################################################################
# 
#  Copyright 2019 Google Inc.
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

import re

from starthinker.util.project import project
from starthinker.util.google_api import API_DCM
from starthinker.util.data import put_rows, get_rows
from starthinker.util.dcm import get_profile_for_api
#from starthinker.util.regexp import epoch_to_datetime
from starthinker.task.dcm_api.schema.lookup import DCM_Schema_Lookup


RE_DATETIME = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}:\d{2}\.?\d+Z')


def bigquery_clean(struct):
  if isinstance(struct, dict):
    for key, value in struct.items():
      if isinstance(value, str) and RE_DATETIME.match(value):
        struct[key] =  struct[key].replace('.000Z', '.0000')
      else:
        bigquery_clean(value)
  elif isinstance(struct, list):
    for index, value in enumerate(struct):
      if isinstance(value, str) and RE_DATETIME.match(value):
        struct[index] = struct[index].replace('.000Z', '.0000')
      else:
        bigquery_clean(value)
  return  struct


def row_clean(structs):
  for struct in structs:
    yield bigquery_clean(struct) 


def put_data(kind, schema, row_format='CSV'):

  out = {}

  if 'dataset' in project.task['out']:
    out["bigquery"] = {
      "dataset": project.task['out']['dataset'],
      "table": kind,
      "schema": schema,
      "skip_rows": 0,
      "format":row_format,
    }

  if 'sheet' in project.task:
    out["sheets"] = {
      "url":project.task['out']['sheet'],
      "tab":kind,
      "range":"A1:A1",
      "delete": True
    }

  return out


def dcm_api_list(endpoint):
  accounts = set(get_rows("user", project.task['accounts']))
  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for item in API_DCM(project.task['auth'], iterate=True, internal=is_superuser).call(endpoint).list(**kwargs).execute():
      yield item


@project.from_parameters
def dcm_api():
  if project.verbose: print('DCM API')

  if isinstance(project.task['endpoints'], str): project.task['endpoints'] = [project.task['endpoints']]

  for endpoint in project.task['endpoints']:
    schema = DCM_Schema_Lookup[endpoint]
    rows = dcm_api_list(endpoint)
    rows = row_clean(rows)
    put_rows(
      project.task['out']['auth'], 
      put_data('CM_%s' % endpoint.title(), schema, 'JSON'),
      rows
    )

if __name__ == "__main__":
  dcm_api()
