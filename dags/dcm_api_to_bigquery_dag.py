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

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

CM API To BigQuery

Write the current state of accounts, subaccounts, profiles, advertisers, campaigns, sites, roles, and reports to BigQuery for a given list of CM accounts.

Specify the name of the dataset, several tables will be created here.
If dataset exists, it is inchanged.
Add CM account ids for the accounts to pull data from.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'endpoint': '',
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'dataset': '',  # Google BigQuery dataset to create tables in.
  'accounts': '',  # Comma separated CM account ids.
}

TASKS = [
  {
    'dcm_api': {
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 1,
          'default': 'user',
          'description': 'Credentials used for reading data.'
        }
      },
      'endpoints': {
        'field': {
          'name': 'endpoint',
          'kind': 'choice',
          'choices': [
            'accountPermissionGroups',
            'accountPermissions',
            'accountUserProfiles',
            'accounts',
            'ads',
            'advertiserGroups',
            'advertiserLandingPages',
            'advertisers',
            'browsers',
            'campaigns',
            'changeLogs',
            'cities',
            'connectionTypes',
            'contentCategories',
            'countries',
            'creativeFields',
            'creativeGroups',
            'creatives',
            'directorySites',
            'dynamicTargetingKeys',
            'eventTags',
            'files',
            'floodlightActivities',
            'floodlightActivityGroups',
            'floodlightConfigurations',
            'languages',
            'metros',
            'mobileApps',
            'mobileCarriers',
            'operatingSystemVersions',
            'operatingSystems',
            'placementGroups',
            'placementStrategies',
            'placements',
            'platformTypes',
            'postalCodes',
            'projects',
            'regions',
            'remarketingLists',
            'reports',
            'sites',
            'sizes',
            'subaccounts',
            'targetableRemarketingLists',
            'targetingTemplates',
            'userprofiles',
            'userRolePermissionGroups',
            'userRolePermissions',
            'userRoles',
            'videoFormats'
          ],
          'default': ''
        }
      },
      'accounts': {
        'single_cell': True,
        'values': {
          'field': {
            'name': 'accounts',
            'kind': 'integer_list',
            'order': 2,
            'default': '',
            'description': 'Comma separated CM account ids.'
          }
        }
      },
      'out': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Credentials used for writing data.'
          }
        },
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Google BigQuery dataset to create tables in.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_api_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
