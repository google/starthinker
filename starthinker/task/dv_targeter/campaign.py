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


def campaign_load(config, task):

  # load multiple partners from user defined sheet
  def campaign_load_multiple():
    for row in get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'Advertisers',
        'header':False,
        'range': 'A2:A'
      }}
    ):
      if row:
        yield from API_DV360(
          config,
          task['auth_dv'],
          iterate=True
        ).advertisers().campaigns().list(
          advertiserId=lookup_id(row[0]),
          filter='entityStatus="ENTITY_STATUS_PAUSED" OR entityStatus="ENTITY_STATUS_ACTIVE" OR entityStatus="ENTITY_STATUS_DRAFT"',
          fields='campaigns.displayName,campaigns.campaignId,campaigns.advertiserId,nextPageToken'
        ).execute()

  campaign_clear(config, task)

  # write to database
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
      'format': 'JSON'
    }},
    campaign_load_multiple()
  )
