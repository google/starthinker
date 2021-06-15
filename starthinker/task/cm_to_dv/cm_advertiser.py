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
from starthinker.util.cm import get_profile_for_api
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear


def cm_advertiser_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'CM_Advertisers',
    Discovery_To_BigQuery(
      'dfareporting',
      'v3.4'
    ).method_schema(
      'advertisers.list',
      iterate=True
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'CM Advertisers',
    'B2:D'
  )


def cm_advertiser_load(config, task):

  # load multiple partners from user defined sheet
  def load_multiple():
    for row in get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'CM Accounts',
        'header':False,
        'range': 'A2:A'
      }}
    ):
      if row:
        account_id = lookup_id(row[0])
        is_superuser, profile_id = get_profile_for_api(config, task['auth_cm'], account_id)
        kwargs = { 'profileId': profile_id, 'accountId': account_id } if is_superuser else { 'profileId': profile_id }
        yield from API_DCM(
          config,
          task['auth_cm'],
          iterate=True,
          internal=is_superuser
        ).advertisers().list( **kwargs).execute()

  cm_advertiser_clear(config, task)

  # write advertisers to database
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'CM_Advertisers',
      'schema': Discovery_To_BigQuery(
        'dfareporting',
        'v3.4'
      ).method_schema(
        'advertisers.list',
        iterate=True
      ),
      'format':'JSON'
    }},
    load_multiple()
  )

  # write advertisers to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'CM Advertisers',
      'header':False,
      'range': 'B2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': '''SELECT
          CONCAT(AC.name, ' - ', AC.id),
          CONCAT(AD.name, ' - ', AD.id),
          AD.status
          FROM `{dataset}.CM_Advertisers` AS AD
          LEFT JOIN `{dataset}.CM_Accounts` AS AC
          ON AD.accountId=AC.id
        '''.format(**task),
        'legacy': False
      }}
    )
  )
