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


def partner_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Partners',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'partners.list'
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Partners',
    'B2:D'
  )


def partner_load(config, task):

  partner_clear(config, task)

  # write partners to BQ
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'DV_Partners',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema('partners.list'),
      'format':
      'JSON'
    }},
    API_DV360(
      config,
      task['auth_dv'],
      iterate=True
    ).partners().list(
      filter='entityStatus="ENTITY_STATUS_ACTIVE"'
    ).execute()
  )

  # write partners to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Partners',
      'header':False,
      'range': 'B2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': "SELECT CONCAT(displayName, ' - ', partnerId), entityStatus  FROM `%s.DV_Partners`" % task['dataset'],
        'legacy': False
      }}
    )
  )
