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


def cm_placement_group_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'CM_PlacementGroups',
    Discovery_To_BigQuery(
      'dfareporting',
      'v3.4'
    ).method_schema(
      'placementGroups.list',
      iterate=True
    )
  )

def cm_placement_group_load(config, task):

  # load multiple partners from user defined sheet
  def load_multiple():

    campaigns = [str(lookup_id(r)) for r in set(get_rows(
      config,
      task['auth_cm'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'CM Campaigns',
        'header':False,
        'range': 'A2:A'
      }},
      unnest=True
    ))]

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
        kwargs = { 'profileId': profile_id, 'campaignIds':campaigns, 'archived':False }
        if is_superuser:
          kwargs['accountId'] = account_id

        yield from API_DCM(
          config,
          task['auth_cm'],
          iterate=True,
          internal=is_superuser
        ).placementGroups().list( **kwargs).execute()

  cm_placement_group_clear(config, task)

  # write placement_groups to database
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'CM_PlacementGroups',
      'schema': Discovery_To_BigQuery(
        'dfareporting',
        'v3.4'
      ).method_schema(
        'placementGroups.list',
        iterate=True
      ),
      'format':'JSON'
    }},
    load_multiple()
  )
