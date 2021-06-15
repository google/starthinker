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
from starthinker.util.google_api import API_DV360
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.patch import patch_log


def campaign_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Campaigns',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'advertisers.campaigns.list'
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Campaigns',
    'B2:Z'
  )


def campaign_load(config, task):

  # load multiple partners from user defined sheet
  def campaign_load_multiple():
    rows = get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'Advertisers',
        'header':False,
        'range': 'A2:A'
      }
    })

    for row in rows:
      yield from API_DV360(
        config,
        task['auth_dv'],
        iterate=True
      ).advertisers().campaigns().list(
        advertiserId=lookup_id(row[0]),
        filter='entityStatus="ENTITY_STATUS_PAUSED" OR entityStatus="ENTITY_STATUS_ACTIVE" OR entityStatus="ENTITY_STATUS_DRAFT"',
        fields='campaigns.displayName,campaigns.campaignId,campaigns.advertiserId,nextPageToken'
      ).execute()

  # write campaigns to database and sheet
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'DV_Campaigns',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'advertisers.campaigns.list'
      ),
      'format':
      'JSON'
    }},
    campaign_load_multiple()
  )

  # write campaigns to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Campaigns',
      'header':False,
      'range': 'B2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset':task['dataset'],
        'query':"""SELECT
           CONCAT(P.displayName, ' - ', P.partnerId),
           CONCAT(A.displayName, ' - ', A.advertiserId),
           CONCAT(C.displayName, ' - ', C.campaignId),
           C.entityStatus
           FROM `{dataset}.DV_Campaigns` AS C
           LEFT JOIN `{dataset}.DV_Advertisers` AS A
           ON C.advertiserId=A.advertiserId
           LEFT JOIN `{dataset}.DV_Partners` AS P
           ON A.partnerId=P.partnerId
           ORDER BY C.displayName
         """.format(**task),
         'legacy':False
      }}
    )
  )


def campaign_commit(config, task, patches):
  for patch in patches:
    if not patch.get('campaign'):
      continue
    print('API CALL', patch['action'], patch['advertiser'], patch['campaign'])
    try:
      if patch['action'] == 'DELETE':
        response = API_DV360(
          config,
          task['auth_dv']
        ).advertisers().campaigns().delete(**patch['parameters']).execute()
        patch['success'] = response
      elif patch['action'] == 'PATCH':
        response = API_DV360(
          config,
          task['auth_dv']
        ).advertisers().campaigns().patch(**patch['parameters']).execute()
        patch['success'] = response['campaignId']
    except Exception as e:
      patch['error'] = str(e)
    finally:
      patch_log(config, patch)
  patch_log(config, task)
