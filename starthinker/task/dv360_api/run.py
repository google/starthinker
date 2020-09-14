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

from starthinker.util.project import project
from starthinker.util.data import put_rows, get_rows
from starthinker.util.google_api import API_DV360_Beta
from starthinker.util.google_api.discovery import discovery_schema

DV360_API_TO_RESOURCE = {
    'advertisers':
        'Advertiser',
    'advertisers.campaigns':
        'Campaign',
    'advertisers.channels':
        'Channel',
    'advertisers.channels.sites':
        'Site',
    'advertisers.creatives':
        'Creative',
    'advertisers.insertionOrders':
        'InsertionOrder',
    'advertisers.lineItems':
        'LineItem',
    'advertisers.lineItems.targetingTypes':
        'TargetingType',
    'advertisers.locationLists':
        'LocationList',
    'advertisers.locationLists.assignedLocations':
        'AssignedLocation',
    'advertisers.negativeKeywordLists':
        'NegativeKeywordList',
    'advertisers.negativeKeywordLists.negativeKeywords':
        'NegativeKeyword',
    'advertisers.targetingTypes.assignedTargetingOptions':
        'AssignedTargetingOption',
    'combinedAudiences':
        'CombinedAudience',
    'customBiddingAlgorithms':
        'CustomBiddingAlgorithm',
    'customLists':
        'CustomList',
    'firstAndThirdPartyAudiences':
        'FirstAndThirdPartyAudience',
    'floodlightGroups':
        'FloodlightGroup',
    'googleAudiences':
        'GoogleAudience',
    'inventorySourceGroups':
        'InventorySourceGroup',
    'inventorySourceGroups.assignedInventorySources':
        'AssignedInventorySource',
    'inventorySources':
        'InventorySource',
    'partners':
        'Partner',
    'partners.channels':
        'Channel',
    'partners.channels.sites':
        'Site',
    'floodlightActivityGroups':
        'FloodlightActivityGroup',
    'partners.targetingTypes.assignedTargetingOptions':
        'AssignedTargetingOption',
    'targetingTypes.targetingOptions':
        'TargetingOption',
    'users':
        'User'
}


def put_data(endpoint):

  schema = discovery_schema('displayvideo', 'v1',
                            DV360_API_TO_RESOURCE.get(endpoint))

  out = {}

  if 'dataset' in project.task['out']:
    out['bigquery'] = {
        'dataset': project.task['out']['dataset'],
        'table': 'DV360_%s' % endpoint.replace('.', '_'),
        'schema': schema,
        'skip_rows': 0,
        'format': 'JSON',
    }

  if 'sheet' in project.task:
    out['sheets'] = {
        'url': project.task['out']['sheet'],
        'tab': endpoint,
        'range': 'A1:A1',
        'delete': True
    }

  return out


def dv360_api_list(endpoint):

  if 'partners' in project.task:
    partners = set(get_rows('user', project.task['partners']))

    for partner in partners:
      kwargs = {'partnerId': partner}
      yield from API_DV360_Beta(
          project.task['auth'],
          iterate=True).call(endpoint).list(**kwargs).execute()

  if 'advertisers' in project.task:
    advertisers = set(get_rows('user', project.task['advertisers']))

    for advertiser in advertisers:
      kwargs = {'advertiserId': str(advertiser)}
      yield from API_DV360_Beta(
          project.task['auth'],
          iterate=True).call(endpoint).list(**kwargs).execute()


def dv360_api_patch(endpoint, row):
  kwargs = {
      'advertiserId': str(row['advertiserId']),
      'updateMask': 'displayName',
      'body': row
  }
  print(
      API_DV360_Beta(
          project.task['auth']).call(endpoint).patch(**kwargs).execute())


def dv360_api_insert(endpoint, row):
  print(row)
  kwargs = {'advertiserId': str(row['advertiserId']), 'body': row}
  print(
      API_DV360_Beta(
          project.task['auth']).call(endpoint).create(**kwargs).execute())


@project.from_parameters
def dv360_api():
  if project.verbose:
    print('DV360 API')

  if 'out' in project.task:
    if isinstance(project.task['endpoints'], str):
      project.task['endpoints'] = [project.task['endpoints']]

    for endpoint in project.task['endpoints']:
      rows = dv360_api_list(endpoint)
      put_rows(project.task['out']['auth'], put_data(endpoint), rows)

  elif 'patch' in project.task:
    rows = get_rows(project.task['auth'], project.task)

    for row in rows:
      dv360_api_patch(project.task['patch'], row)
      print(row)

  elif 'insert' in project.task:
    rows = get_rows(project.task['auth'], project.task)

    for row in rows:
      dv360_api_insert(project.task['insert'], row)
      print(row)


if __name__ == '__main__':
  dv360_api()
