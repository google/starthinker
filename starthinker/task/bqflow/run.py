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

from googleapiclient.errors import HttpError

from starthinker.util.bigquery import table_list
from starthinker.util.data import get_rows
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery

from starthinker.task.google_api.run import google_api_build_errors
from starthinker.task.google_api.run import google_api_build_results
from starthinker.task.google_api.run import google_api_execute
from starthinker.task.google_api.run import google_api_initilaize


def build_request(endpoint):
  return {
    "bigquery": {
      "dataset": endpoint['dataset'],
      "table": endpoint['table']
    }
  }


def build_results(config, auth, api_call, endpoint):
  return google_api_build_results(
      config, auth, api_call, {
          'bigquery': {
              'dataset':
                  endpoint['dataset'],
              'table':
                  endpoint['table'].replace('BQFlow__', 'BQFlow__RESULTS__')
          }
      })


def build_errors(config, auth, api_call, endpoint):
  return google_api_build_errors(
      config, auth, api_call, {
          'bigquery': {
              'dataset': endpoint['dataset'],
              'table': endpoint['table'].replace('BQFlow__', 'BQFlow__ERRORS__')
          }
      })


def bqflow(config, task):

  if config.verbose: print('BQFLOW')

  endpoints = []

  # load dataset / table list
  for dataset, table, kind in table_list(config, task['auth'], config.project):
    if table.startswith('BQFlow__') and not table.startswith('BQFlow__RESULTS__') and not table.startswith('BQFlow__ERRORS__'):
      print(table, kind)
      endpoints.append({'dataset': dataset, kind.lower(): table})

  for endpoint in endpoints:
    if 'table' in endpoint:
      _, api, function = endpoint['table'].split('__', 2)
      function = function.replace('__', '.')

      api_call = {
        'auth':'user',
        'api':api,
        'version':Discovery_To_BigQuery.preferred_version(api, task.get('key')),
        'function':function,
      }

      kwargs_list = get_rows(
          config, task['auth'], build_request(endpoint), as_object=True)

      results = build_results(config, task['auth'], api_call, endpoint)
      errors = build_errors(config, task['auth'], api_call, endpoint)

      for kwargs in kwargs_list:
        api_call['kwargs'] = kwargs

        if config.verbose: print('BQFLOW API CALL:', api_call)

        google_api_initilaize(config, api_call)
        google_api_execute(config, task['auth'], api_call, results, errors)
