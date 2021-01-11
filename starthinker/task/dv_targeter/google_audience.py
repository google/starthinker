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
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear


def google_audience_clear():

  table_create(
    project.task['auth_bigquery'],
    project.id,
    project.task['dataset'],
    'DV_Google_Audiences',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'googleAudiences.list'
    )
  )

  sheets_clear(
    project.task['auth_sheets'],
    project.task['sheet'],
    'Google Audiences',
    'A2:Z'
  )


def google_audience_load():

  # load multiple from user defined sheet
  def load_multiple():
    partners = get_rows(
      project.task['auth_sheets'],
      { 'sheets': {
        'sheet': project.task['sheet'],
        'tab': 'Partners',
        'range': 'A2:A'
      }}
    )

    for partner in partners:
      yield from API_DV360(
        project.task['auth_dv'],
        iterate=True
      ).googleAudiences().list(
        partnerId=lookup_id(partner[0])
      ).execute()

    advertisers = get_rows(
      project.task['auth_sheets'],
      { 'sheets': {
        'sheet': project.task['sheet'],
        'tab': 'Advertisers',
        'range': 'A2:A'
      }}
    )

    for advertiser in advertisers:
      yield from API_DV360(
        project.task['auth_dv'],
        iterate=True
      ).googleAudiences().list(
        advertiserId=lookup_id(advertiser[0])
      ).execute()

  # write inventorys to database and sheet
  put_rows(
    project.task['auth_bigquery'],
    { 'bigquery': {
      'dataset': project.task['dataset'],
      'table': 'DV_Google_Audiences',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'googleAudiences.list'
      ),
      'format': 'JSON'
    }},
    load_multiple()
  )

  # write inventorys to sheet
  rows = get_rows(
    project.task['auth_bigquery'],
    { 'bigquery': {
      'dataset': project.task['dataset'],
      'query': """SELECT
         CONCAT(I.displayName, ' - ', I.googleAudienceId),
         googleAudienceType
         FROM `{dataset}.DV_Google_Audiences` AS I
         GROUP BY 1,2
         ORDER BY 1
      """.format(**project.task),
      'legacy': False
    }}
  )

  put_rows(
    project.task['auth_sheets'],
    { 'sheets': {
      'sheet': project.task['sheet'],
      'tab': 'Google Audiences',
      'range': 'A2'
    }},
    rows
  )