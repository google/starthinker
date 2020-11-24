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

from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.dcm import get_profile_for_api
from starthinker.util.google_api import API
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project


ERROR_SCHEMA = [
  { 'name': 'Error', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'Parameters', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [
    { 'name': 'Key', 'type': 'STRING', 'mode': 'NULLABLE' },
    { 'name': 'Value', 'type': 'STRING', 'mode': 'NULLABLE' },
  ]}
]


def google_api_initilaize(api_call, alias=None):

  if api_call['function'].endswith('list') or alias == 'list':
    api_call['iterate'] = True

  if api_call['api'] == 'dfareporting':
    is_superuser, profile_id = get_profile_for_api(
        api_call['auth'], api_call['kwargs']['accountId'])

    api_call['kwargs']['profileId'] = profile_id

    if is_superuser:
      from starthinker.util.dcm.internalv33_uri import URI as DCM_URI
      api_call['version'] = 'internalv3.3'
      api_call['uri'] = DCM_URI
    else:
      del api_call['kwargs']['accountId']


def google_api_build_results(auth, api_call, results):
  if 'bigquery' in results:
    results['bigquery']['schema'] = Discovery_To_BigQuery(
        api_call['api'],
        api_call['version'],
        api_call.get('key', None),
    ).method_schema(api_call['function'])

    #TODO: Fix format to sometimes be CSV, probably refactor BigQuery to
    # determine format based on rows or schema
    results['bigquery']['format'] = 'JSON'
    results['bigquery']['skip_rows'] = 0
    results['bigquery']['disposition'] = 'WRITE_TRUNCATE'

    table_create(
        results['bigquery'].get('auth', auth),
        project.id,
        results['bigquery']['dataset'],
        results['bigquery']['table'],
        results['bigquery']['schema'],
        overwrite=False)

  return results


def google_api_build_errors(auth, api_call, errors):
  if 'bigquery' in errors:
    errors['bigquery']['schema'] = ERROR_SCHEMA
    errors['bigquery']['format'] = 'JSON'
    errors['bigquery']['skip_rows'] = 0
    errors['bigquery']['disposition'] = 'WRITE_TRUNCATE'

    table_create(
        errors['bigquery'].get('auth', auth),
        project.id,
        errors['bigquery']['dataset'],
        errors['bigquery']['table'],
        errors['bigquery']['schema'],
        overwrite=False)

  return errors


def google_api_execute(auth, api_call, results, errors):
  try:
    rows = API(api_call).execute()

    if results:
      # check if single object needs conversion to rows
      if isinstance(rows, dict):
        rows = [rows]
      rows = map(lambda r: Discovery_To_BigQuery.clean(r), rows)
      put_rows(auth, results, rows)

      if 'bigquery' in results:
        results['bigquery']['disposition'] = 'WRITE_APPEND'

  except HttpError as e:

    if errors:
      rows = [{
          'Error':
              str(e),
          'Parameters': [{
              'Key': k,
              'Value': str(v)
          } for k, v in api_call['kwargs'].items()]
      }]
      put_rows(auth, errors, rows)

      if 'bigquery' in errors:
        errors['bigquery']['disposition'] = 'WRITE_APPEND'

    else:
      raise e


@project.from_parameters
def google_api():

  if project.verbose:
    print('GOOGLE_API', project.task['api'], project.task['version'],
          project.task['function'])

  api_call = {
      'auth': project.task['auth'],
      'api': project.task['api'],
      'version': project.task['version'],
      'function': project.task['function'],
      'iterate': project.task.get('iterate', False),
      'key': project.key,
      'headers': project.task.get('headers'),
  }

  results = google_api_build_results(
    project.task['auth'],
    api_call,
    project.task.get('results', {})
  )

  errors = google_api_build_errors(
    project.task['auth'],
    api_call,
    project.task.get('errors', {})
  )

  if 'kwargs' in project.task:
    kwargs_list = project.task['kwargs'] if isinstance(
        project.task['kwargs'], (list, tuple)) else [project.task['kwargs']]
  elif 'kwargs_remote' in project.task:
    kwargs_list = get_rows(
        project.task['auth'], project.task['kwargs_remote'], as_object=True)
  else:
    kwargs_list = [{}]

  for kwargs in kwargs_list:

    api_call['kwargs'] = kwargs

    google_api_initilaize(api_call, project.task.get('alias'))

    google_api_execute(project.task['auth'], api_call, results, errors)


if __name__ == '__main__':
  google_api()
