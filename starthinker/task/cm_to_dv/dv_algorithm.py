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


def dv_algorithm_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Algorithms',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'customBiddingAlgorithms.list'
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'DV Algorithms',
    'B2:D'
  )


def dv_algorithm_load(config, task):

  # load multiple partners from user defined sheet
  def load_multiple():
    for row in get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'DV Partners',
        'header':False,
        'range': 'A2:A'
      }}
    ):
      if row:
        yield from API_DV360(
          config,
          task['auth_dv'],
          iterate=True).customBiddingAlgorithms().list(
          partnerId=lookup_id(row[0])
        ).execute()

  dv_algorithm_clear(config, task)

  # write algorithms to database
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'DV_Algorithms',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'customBiddingAlgorithms.list'
      ),
      'format': 'JSON'
    }},
    load_multiple()
  )

  # write algorithms to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'DV Algorithms',
      'range': 'B2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           CONCAT(P.displayName, ' - ', P.partnerId),
           CONCAT(A.displayName, ' - ', A.advertiserId),
           CONCAT(B.displayName, ' - ', B.customBiddingAlgorithmId),
           B.entityStatus
           FROM `{dataset}.DV_Algorithms` AS B
           LEFT JOIN `{dataset}.DV_Partners` AS P
           ON B.partnerId=P.partnerId
           LEFT JOIN `{dataset}.DV_Advertisers` AS A
           ON B.advertiserId=A.advertiserId
        """.format(**task),
        'legacy': False
      }}
    )
  )
