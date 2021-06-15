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


def negative_keyword_list_clear(config, task):

  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Negative_Keywod_Lists',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'advertisers.negativeKeywordLists.list'
    )
  )


def negative_keyword_list_load(config, task):

  # load multiple from user defined sheet
  def load_multiple():
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
      ).advertisers().negativeKeywordLists().list(
        advertiserId=lookup_id(advertiser[0])
      ).execute()

  negative_keyword_list_clear(config, task)

  # write to database
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'DV_Negative_Keywod_Lists',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'advertisers.negativeKeywordLists.list'
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
      'tab': 'Targeting Options',
      'header':False,
      'range': 'J2:J'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           CONCAT(A.displayName, ' - ', A.advertiserId, ' > ', L.displayName, ' - ', L.negativeKeywordListId),
           FROM `{dataset}.DV_Negative_Keywod_Lists` AS L
           LEFT JOIN `{dataset}.DV_Advertisers` AS A
           ON L.advertiserId=A.advertiserId
        """.format(**task),
        'legacy': False
      }}
    )
  )
