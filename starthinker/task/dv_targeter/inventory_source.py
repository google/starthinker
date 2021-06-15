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


def inventory_source_clear(config, task):

  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Inventory_Sources',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'inventorySources.list'
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Inventory Sources',
    'A2:Z'
  )


def inventory_source_load(config, task):

  # load multiple from user defined sheet
  def load_multiple():
    partners = get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'Partners',
        'header':False,
        'range': 'A2:A'
      }}
    )

    for partner in partners:
      yield from API_DV360(
        config,
        task['auth_dv'],
        iterate=True
      ).inventorySources().list(
        partnerId=lookup_id(partner[0])
      ).execute()

    advertisers = get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'Advertisers',
        'header':False,
        'range': 'A2:A'
      }}
    )

    for advertiser in advertisers:
      yield from API_DV360(
        config,
        task['auth_dv'],
        iterate=True
      ).inventorySources().list(
        advertiserId=lookup_id(advertiser[0])
      ).execute()

  inventory_source_clear(config, task)

  # write to database
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'DV_Inventory_Sources',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'inventorySources.list'
      ),
      'format': 'JSON'
    }},
    load_multiple()
  )

  # write to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Inventory Sources',
      'header':False,
      'range': 'A2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           CONCAT(I.displayName, ' - ', I.inventorySourceId),
           inventorySourceType,
           status.entityStatus,
           status.sellerStatus,
           status.configStatus,
           exchange,
           publisherName,
           dealId
           FROM `{dataset}.DV_Inventory_Sources` AS I
           GROUP BY 1,2,3,4,5,6,7,8
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )
