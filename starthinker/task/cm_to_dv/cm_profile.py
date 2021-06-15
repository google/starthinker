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


from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_DCM
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.sheets import sheets_clear


def cm_profile_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'CM_Profiles',
    Discovery_To_BigQuery(
      'dfareporting',
      'v3.4'
    ).method_schema(
      'userProfiles.list',
      iterate=True
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'CM Profiles',
    'B2:E'
  )


def cm_profile_load(config, task):

  cm_profile_clear(config, task)

  # write accounts to BQ
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'CM_Profiles',
      'schema': Discovery_To_BigQuery(
        'dfareporting',
        'v3.4'
      ).method_schema('userProfiles.list', iterate=True),
      'format':'JSON'
    }},
    API_DCM(config, task['auth_cm'], iterate=True).userProfiles().list().execute()
  )

  # write accounts to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'CM Profiles',
      'header':False,
      'range': 'B2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': "SELECT CONCAT(accountName, ' - ', accountId), CONCAT(subAccountName, ' - ', subAccountId), profileId, userName FROM `%s.CM_Profiles`" % task['dataset'],
        'legacy': False
      }}
    )
  )
