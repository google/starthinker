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


def partner_clear():
  table_create(
    project.task['auth_bigquery'],
    project.id,
    project.task['dataset'],
    'DV_Partners',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).method_schema(
      'partners.list'
    )
  )

  sheets_clear(
    project.task['auth_sheets'],
    project.task['sheet'],
    'Partners',
    'B2:Z'
  )


def partner_load():
  # write partners to BQ
  rows = API_DV360(
    project.task['auth_dv'],
    iterate=True
  ).partners().list().execute()

  put_rows(
    project.task['auth_bigquery'],
    { 'bigquery': {
      'dataset': project.task['dataset'],
      'table': 'DV_Partners',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema('partners.list'),
      'format':
      'JSON'
    }},
    rows
  )

  # write partners to sheet
  put_rows(project.task['auth_sheets'],
    { 'sheets': {
      'sheet': project.task['sheet'],
      'tab': 'Partners',
      'range': 'B2'
    }},
    get_rows(
      project.task['auth_bigquery'],
      { 'bigquery': {
        'dataset': project.task['dataset'],
        'query': "SELECT CONCAT(displayName, ' - ', partnerId), entityStatus  FROM `%s.DV_Partners`" % project.task['dataset'],
        'legacy': False
      }}
    )
  )


def partner_load_targeting():

  def load_bulk():
    partners = [lookup_id(p[0]) for p in get_rows(
      project.task['auth_sheets'],
      { 'sheets': {
        'sheet': project.task['sheet'],
        'tab': 'Partners',
        'range': 'A2:A'
      }}
    )]

    for partner in partners:
      yield from API_DV360(
        project.task["auth_dv"],
        iterate=True
      ).partners().targetingTypes().assignedTargetingOptions().list(
        partnerId=str(partner),
        targetingType='TARGETING_TYPE_CHANNEL'
      ).execute()

  put_rows(
    project.task['auth_bigquery'],
    { 'bigquery': {
      'dataset': project.task['dataset'],
      'table': 'DV_Targeting',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).resource_schema(
        'AssignedTargetingOption'
      ),
      'disposition':'WRITE_APPEND',
      'format': 'JSON'
    }},
    load_bulk()
  )


