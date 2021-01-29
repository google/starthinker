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


def channel_clear():

  table_create(
    project.task['auth_bigquery'],
    project.id,
    project.task['dataset'],
    'DV_Channels',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'advertisers.channels.list'
    )
  )


def channel_load():

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
      ).partners().channels().list(
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
      ).advertisers().channels().list(
        advertiserId=lookup_id(advertiser[0])
      ).execute()

  # write channels to database
  put_rows(
    project.task['auth_bigquery'],
    { 'bigquery': {
      'dataset': project.task['dataset'],
      'table': 'DV_Channels',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'advertisers.channels.list'
      ),
      'format': 'JSON'
    }},
    load_multiple()
  )

  # write channels to sheet
  put_rows(
    project.task['auth_sheets'],
    { 'sheets': {
      'sheet': project.task['sheet'],
      'tab': 'Targeting Options',
      'range': 'I2'
    }},
    get_rows(
      project.task['auth_bigquery'],
      { 'bigquery': {
        'dataset': project.task['dataset'],
        'query': """SELECT
           CASE
             WHEN C.partnerId IS NOT NULL THEN CONCAT('PARTNER: ', P.displayName, ' - ', P.partnerId, ' > ', C.displayName, ' - ', C.channelId)
             ELSE CONCAT('ADVERTISER: ', A.displayName, ' - ', A.advertiserId, ' > ', C.displayName, ' - ', C.channelId)
           END
           FROM `{dataset}.DV_Channels` AS C
           LEFT JOIN `{dataset}.DV_Partners` AS P
           ON C.partnerId=P.partnerId
           LEFT JOIN `{dataset}.DV_Advertisers` AS A
           ON C.advertiserId=A.advertiserId
           ORDER BY 1
        """.format(**project.task),
        'legacy': False
      }}
    )
  )
