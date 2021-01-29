###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the 'License');
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an 'AS IS' BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

from collections import OrderedDict

from starthinker.util.data import put_rows
from starthinker.util.google_api import API_Analytics
from starthinker.util.project import project
from starthinker.task.ga_settings_download.ga_schemas import CUSTOM_DIMENSION_SCHEMA
from starthinker.task.ga_settings_download.ga_schemas import CUSTOM_METRIC_SCHEMA
from starthinker.task.ga_settings_download.ga_schemas import VIEW_SCHEMA
from starthinker.task.ga_settings_download.ga_schemas import GOAL_SCHEMA
from starthinker.task.ga_settings_download.ga_schemas import GOOGLE_ADS_LINK_SCHEMA
from starthinker.task.ga_settings_download.ga_schemas import REMARKETING_AUDIENCE_SCHEMA
from starthinker.task.ga_settings_download.ga_schemas import ACCOUNT_SUMMARIES_SCHEMA


def custom_dimensions_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA Custom Dimensions')

  for account in accounts:
    for web_property in account.get('webProperties', []):
      for custom_dimension in API_Analytics(
          project.task['auth'],
          iterate=True).management().customDimensions().list(
              accountId=account.get('id'),
              webPropertyId=web_property.get('id')).execute():
        yield (account.get('name'), account.get('id'), web_property.get('name'),
               web_property.get('id'), custom_dimension.get('id'),
               custom_dimension.get('name'), custom_dimension.get('index'),
               custom_dimension.get('scope'), custom_dimension.get('active'),
               custom_dimension.get('created'), custom_dimension.get('updated'),
               current_date, custom_dimension.get('selfLink'))


def custom_metrics_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA Custom Metrics')

  for account in accounts:
    for web_property in account.get('webProperties', []):
      for custom_metric in API_Analytics(
          project.task['auth'], iterate=True).management().customMetrics().list(
              accountId=account.get('id'),
              webPropertyId=web_property.get('id')).execute():
        yield (account.get('name'), account.get('id'), web_property.get('name'),
               web_property.get('id'), custom_metric.get('id'),
               custom_metric.get('name'), custom_metric.get('index'),
               custom_metric.get('scope'), custom_metric.get('active'),
               custom_metric.get('created'), custom_metric.get('updated'),
               current_date, custom_metric.get('selfLink'),
               custom_metric.get('type'), custom_metric.get('min_value'),
               custom_metric.get('max_value'))


def goals_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA Goals')

  for goal in API_Analytics(
      project.task['auth'], iterate=True).management().goals().list(
          accountId='~all', webPropertyId='~all', profileId='~all').execute():
    for account in accounts:
      if goal.get('accountId') == account.get('id'):
        for prop in account.get('webProperties', []):
          if goal.get('webPropertyId') == prop.get('id'):
            for view in prop.get('profiles', []):
              if goal.get('profileId') == view.get('id'):
                ordered_goal = OrderedDict()
                ordered_goal['date'] = str(current_date)
                ordered_goal['id'] = goal.get('id')
                ordered_goal['accountId'] = goal.get('accountId')
                ordered_goal['webPropertyId'] = goal.get('webPropertyId')
                ordered_goal['profileId'] = goal.get('profileId')
                ordered_goal['internalWebPropertyId'] = goal.get(
                    'internalWebPropertyId')
                ordered_goal['name'] = goal.get('name')
                ordered_goal['accountName'] = account.get('name')
                ordered_goal['webPropertyName'] = prop.get('name')
                ordered_goal['profileName'] = view.get('name')
                ordered_goal['value'] = goal.get('value')
                ordered_goal['active'] = goal.get('active')
                ordered_goal['type'] = goal.get('type')
                ordered_goal['created'] = goal.get('created')
                ordered_goal['updated'] = goal.get('updated')
                if goal.get('urlDestinationDetails'):
                  ordered_goal['urlDestinationDetails'] = {
                      'url':
                          goal.get('urlDestinationDetails').get('url'),
                      'caseSensitive':
                          goal.get('urlDestinationDetails').get('caseSensitive'
                                                               ),
                      'matchType':
                          goal.get('urlDestinationDetails').get('matchType'),
                      'firstStepRequired':
                          goal.get('urlDestinationDetails').get(
                              'firstStepRequired')
                  }
                  if goal.get('urlDestinationDetails').get('steps', []):
                    ordered_goal['urlDestinationDetails']['steps'] = []
                    for step in goal.get('urlDestinationDetails').get(
                        'steps', []):
                      ordered_goal['urlDestinationDetails']['steps'].append({
                          'number': step.get('number'),
                          'name': step.get('name'),
                          'url': step.get('url')
                      })
                if goal.get('visitTimeOnSiteDetails'):
                  ordered_goal['visitTimeOnSiteDetails'] = {
                      'comparisonType':
                          goal.get('visitTimeOnSiteDetails').get(
                              'comparisonType'),
                      'comparisonValue':
                          goal.get('visitTimeOnSiteDetails').get(
                              'comparisonValue')
                  }
                if goal.get('visitNumPagesDetails'):
                  ordered_goal['visitNumPagesDetails'] = {
                      'comparisonType':
                          goal.get('visitNumPagesDetails').get('comparisonType'
                                                              ),
                      'comparisonValue':
                          goal.get('visitNumPagesDetails').get('comparisonValue'
                                                              )
                  }
                if goal.get('eventDetails'):
                  ordered_goal['eventDetails'] = {
                      'useEventValue':
                          goal.get('eventDetails').get('useEventValue'),
                      'eventConditions': []
                  }
                  for conditions in goal.get('eventDetails').get(
                      'eventConditions'):
                    ordered_goal['eventDetails']['eventConditions'].append({
                        'type': conditions.get('type'),
                        'matchType': conditions.get('matchType'),
                        'expression': conditions.get('expression'),
                        'comprisonType': conditions.get('comprisonType'),
                        'comparisonValue': conditions.get('comparisonValue')
                    })
                yield ordered_goal


def views_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA views')

  for view in API_Analytics(
      project.task['auth'], iterate=True).management().profiles().list(
          accountId='~all', webPropertyId='~all').execute():
    for account in accounts:
      if view.get('accountId') == account.get('id'):
        for prop in account.get('webProperties', []):
          if view.get('webPropertyId') == prop.get('id'):
            yield (current_date, view.get('id'), view.get('selfLink'),
                   view.get('accountId'), view.get('webPropertyId'),
                   account.get('name'), prop.get('name'), view.get('name'),
                   view.get('currency'), view.get('timezone'),
                   view.get('websiteUrl'), view.get('defaultPage'),
                   view.get('excludeQueryParameters'),
                   view.get('siteSearchQueryParameters'),
                   view.get('stripSiteSearchQueryParameters'),
                   view.get('siteSearchCategoryParameters'),
                   view.get('stripSiteSearchCategoryParameters'),
                   view.get('type'), view.get('created'), view.get('updated'),
                   view.get('eCommerceTracking'),
                   view.get('enhancedECommerceTracking'),
                   view.get('botFilteringEnabled'), view.get('starred'))


def google_ads_links_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA Google Ads Links')

  for account in accounts:
    for prop in account.get('webProperties', []):
      for link in API_Analytics(
          project.task['auth'],
          iterate=True).management().webPropertyAdWordsLinks().list(
              accountId=account.get('id'),
              webPropertyId=prop.get('id')).execute():
        ordered_link = OrderedDict()
        ordered_link['date'] = str(current_date)
        ordered_link['id'] = link.get('id')
        ordered_link['kind'] = link.get('kind')
        ordered_link['selfLink'] = link.get('selfLink')
        ordered_link['entity'] = {
            'webPropertyRef': {
                'id':
                    link.get('entity').get('webPropertyRef').get('id'),
                'kind':
                    link.get('entity').get('webPropertyRef').get('kind'),
                'href':
                    link.get('entity').get('webPropertyRef').get('href'),
                'accountId':
                    link.get('entity').get('webPropertyRef').get('accountId'),
                'internalWebPropertyId':
                    link.get('entity').get('webPropertyRef').get(
                        'internalWebPropertyId'),
                'name':
                    link.get('entity').get('webPropertyRef').get('name')
            }
        }
        ordered_link['adWordsAccounts'] = []
        for ad_account in link.get('adWordsAccounts'):
          ordered_link['adWordsAccounts'].append({
              'kind': ad_account.get('kind'),
              'customerId': ad_account.get('customerId'),
              'autoTaggingEnabled': ad_account.get('autoTaggingEnabled')
          })
        ordered_link['name'] = link.get('name')
        ordered_link['profileIds'] = []
        for profile_id in link.get('profileIds', []):
          ordered_link['profileIds'].append({'id': profile_id})
        yield ordered_link


def remarketing_audiences_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA Google Remarketing Audiences')

  for account in accounts:
    for prop in account.get('webProperties', []):
      for audience in API_Analytics(
          project.task['auth'],
          iterate=True).management().remarketingAudience().list(
              accountId=account.get('id'),
              webPropertyId=prop.get('id')).execute():
        ordered_audience = OrderedDict()
        ordered_audience['date'] = str(current_date)
        ordered_audience['kind'] = audience.get('kind')
        ordered_audience['id'] = audience.get('id')
        ordered_audience['accountId'] = audience.get('accountId')
        ordered_audience['webPropertyId'] = audience.get('webPropertyId')
        ordered_audience['webPropertyName'] = audience.get('name')
        ordered_audience['accountName'] = audience.get('name')
        ordered_audience['internalWebPropertyId'] = audience.get(
            'internalWebPropertyId')
        ordered_audience['created'] = audience.get('created')
        ordered_audience['updated'] = audience.get('updated')
        ordered_audience['name'] = audience.get('name')
        ordered_audience['description'] = audience.get('description')
        ordered_audience['linkedAdAccounts'] = []
        for linked_ad_account in audience.get('linkedAdAccounts', []):
          ordered_audience['linkedAdAccounts'].append({
              'kind':
                  linked_ad_account.get('kind'),
              'id':
                  linked_ad_account.get('id'),
              'accountId':
                  linked_ad_account.get('accountId'),
              'webPropertyId':
                  linked_ad_account.get('webPropertyId'),
              'internalWebPropertyId':
                  linked_ad_account.get('internalWebPropertyId'),
              'remarketingAudienceId':
                  linked_ad_account.get('remarketingAudienceId'),
              'linkedAccountId':
                  linked_ad_account.get('linkedAccountId'),
              'type':
                  linked_ad_account.get('type'),
              'status':
                  linked_ad_account.get('status'),
              'eligibleForSearch':
                  linked_ad_account.get('eligibleForSearch')
          })
        ordered_audience['linkedViews'] = []
        for linked_view in audience.get('linkedViews', []):
          ordered_audience['linkedViews'].append({'id': linked_view})
        ordered_audience['audienceType'] = audience.get('audienceType')
        if audience.get('audienceType') == 'SIMPLE':
          ordered_audience['audienceDefinition'] = {
              'includeConditions': {
                  'kind':
                      audience.get('audienceDefinition').get('includeConditions'
                                                            ).get('kind'),
                  'isSmartList':
                      audience.get('audienceDefinition').get(
                          'includeConditions').get('isSmartList'),
                  'segment':
                      audience.get('audienceDefinition').get('includeConditions'
                                                            ).get('segment'),
                  'membershipDurationDays':
                      audience.get('audienceDefinition').get(
                          'includeConditions').get('membershipDurationDays'),
                  'daysToLookBack':
                      audience.get('audienceDefinition').get(
                          'includeConditions').get('daysToLookBack')
              }
          }
        elif audience.get('audienceType') == 'STATE_BASED':
          if audience.get('stateBasedAudienceDefinition').get(
              'includeConditions'):
            ordered_audience['stateBasedAudienceDefinition'] = {
                'includeConditions': {
                    'kind':
                        audience.get('stateBasedAudienceDefinition').get(
                            'includeConditions').get('kind'),
                    'isSmartList':
                        audience.get('stateBasedAudienceDefinition').get(
                            'includeConditions').get('isSmartList'),
                    'segment':
                        audience.get('stateBasedAudienceDefinition').get(
                            'includeConditions').get('segment'),
                    'membershipDurationDays':
                        audience.get('stateBasedAudienceDefinition').get(
                            'includeConditions').get('membershipDurationDays'),
                    'daysToLookBack':
                        audience.get('stateBasedAudienceDefinition').get(
                            'includeConditions').get('daysToLookBack')
                }
            }
          if audience.get('stateBasedAudienceDefinition').get(
              'excludeConditions'):
            ordered_audience['stateBasedAudienceDefinition'] = {
                'excludeConditions': {
                    'segment':
                        audience.get('stateBasedAudienceDefinition').get(
                            'excludeConditions').get('segment'),
                    'exclusionDuration':
                        audience.get('stateBasedAudienceDefinition').get(
                            'excludeConditions').get('exclusionDuration')
                }
            }
        yield ordered_audience


def account_summaries_download(accounts, current_date):
  if project.verbose:
    print('Downloading GA Google Remarketing Audiences')

  for account in accounts:
    ordered_summary = OrderedDict()
    ordered_summary['date'] = str(current_date)
    ordered_summary['id'] = account.get('id')
    ordered_summary['kind'] = account.get('kind')
    ordered_summary['name'] = account.get('name')
    ordered_summary['starred'] = account.get('starred')
    ordered_summary['webProperties'] = []
    for prop in account.get('webProperties', []):
      ordered_prop = OrderedDict()
      ordered_prop['kind'] = prop.get('kind')
      ordered_prop['id'] = prop.get('id')
      ordered_prop['name'] = prop.get('name')
      ordered_prop['internalWebPropertyId'] = prop.get('internalWebPropertyId')
      ordered_prop['level'] = prop.get('level')
      ordered_prop['websiteUrl'] = prop.get('websiteUrl')
      ordered_prop['starred'] = prop.get('starred')
      ordered_prop['profiles'] = []
      for profile in prop.get('profiles', []):
        ordered_prop['profiles'].append({
            'kind': profile.get('kind'),
            'id': profile.get('id'),
            'name': profile.get('name'),
            'type': profile.get('type'),
            'starred': profile.get('starred'),
        })
      ordered_summary['webProperties'].append(ordered_prop)
    yield ordered_summary


def write_to_bigquery(table_id, schema, data, data_format):
  out = {
      'bigquery': {
          'format': data_format,
          'dataset': project.task['dataset'],
          'table': table_id,
          'schema': schema,
          'skip_rows': 0,
          'disposition': 'WRITE_TRUNCATE'
      }
  }
  put_rows(project.task['auth'], out, data)


@project.from_parameters
def ga_settings_download():
  if project.verbose:
    print('Initiating GA Settings Download')

  filters = [str(f) for f in project.task.get('accounts', [])
            ]  # in case integer list is provided
  accounts = [
      a for a in API_Analytics(project.task['auth'], iterate=True).management()
      .accountSummaries().list().execute()
      if not filters or a['id'] in filters or a['name'] in filters
  ]

  if accounts:
    current_date = project.date

    write_to_bigquery('ga_custom_dimension_settings', CUSTOM_DIMENSION_SCHEMA,
                      custom_dimensions_download(accounts, current_date), 'CSV')

    write_to_bigquery('ga_custom_metric_settings', CUSTOM_METRIC_SCHEMA,
                      custom_metrics_download(accounts, current_date), 'CSV')

    write_to_bigquery('ga_view_settings', VIEW_SCHEMA,
                      views_download(accounts, current_date), 'CSV')

    write_to_bigquery('ga_goal_settings', GOAL_SCHEMA,
                      goals_download(accounts, current_date), 'JSON')

    write_to_bigquery('ga_google_ad_link_settings', GOOGLE_ADS_LINK_SCHEMA,
                      google_ads_links_download(accounts, current_date), 'JSON')

    write_to_bigquery('ga_remarketing_audience_settings',
                      REMARKETING_AUDIENCE_SCHEMA,
                      remarketing_audiences_download(accounts,
                                                     current_date), 'JSON')

    write_to_bigquery('ga_account_summaries_settings', ACCOUNT_SUMMARIES_SCHEMA,
                      account_summaries_download(accounts, current_date),
                      'JSON')


if __name__ == '__main__':
  ga_settings_download()
