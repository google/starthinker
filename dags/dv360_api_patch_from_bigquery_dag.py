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

DV360 API Patch From BigQuery

Patch DV360 API endpoints.

Specify the name of the dataset and table.
Rows will be read and applied as a patch to DV360.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'patch': '',
  'auth_write': 'user',  # Credentials used for writing data.
  'auth_read': 'service',  # Credentials used for reading data.
  'dataset': '',  # Google BigQuery dataset to create tables in.
  'table': '',  # Google BigQuery dataset to create tables in.
}

TASKS = [
  {
    'dv360_api': {
      'patch': {
        'field': {
          'kind': 'choice',
          'name': 'patch',
          'default': '',
          'choices': [
            'advertisers',
            'advertisers.campaigns',
            'advertisers.channels',
            'advertisers.channels.sites',
            'advertisers.creatives',
            'advertisers.insertionOrders',
            'advertisers.lineItems',
            'advertisers.locationLists',
            'advertisers.locationLists.assignedLocations',
            'advertisers.negativeKeywordLists',
            'advertisers.negativeKeywordLists.negativeKeywords',
            'floodlightGroups',
            'inventorySourceGroups',
            'partners.channels',
            'users'
          ]
        }
      },
      'bigquery': {
        'table': {
          'field': {
            'order': 3,
            'kind': 'string',
            'name': 'table',
            'description': 'Google BigQuery dataset to create tables in.',
            'default': ''
          }
        },
        'dataset': {
          'field': {
            'order': 2,
            'kind': 'string',
            'name': 'dataset',
            'description': 'Google BigQuery dataset to create tables in.',
            'default': ''
          }
        },
        'as_object': True,
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_read',
            'description': 'Credentials used for reading data.',
            'default': 'service'
          }
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Credentials used for writing data.',
          'default': 'user'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dv360_api_patch_from_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
