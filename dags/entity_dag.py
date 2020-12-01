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

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

Entity Read Files

Import public and private <a href='https://developers.google.com/bid-manager/guides/entity-read/format-v2' target='_blank'>Entity Read Files</a> into a BigQuery dataset.<br/>CAUTION: PARTNER ONLY, ADVERTISER FILTER IS NOT APPLIED.

  - Entity Read Files ONLY work at the partner level.
  - Advertiser filter is NOT APPLIED.
  - Specify one or more partners to be moved into the dataset.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_write': 'service',  # Credentials used for writing data.
  'auth_read': 'user',  # Credentials used for reading data.
  'partners': '[]',  # Comma sparated list of DV360 partners.
  'dataset': '',  # BigQuery dataset to write tables for each entity.
}

RECIPE = {
  'setup': {
    'day': [
      'Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'
    ],
    'hour': [
      5
    ]
  },
  'tasks': [
    {
      'dataset': {
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
            'order': 3,
            'default': '',
            'description': 'BigQuery dataset to write tables for each entity.'
          }
        }
      }
    },
    {
      'entity': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'prefix': 'Entity',
        'entities': [
          'Campaign',
          'LineItem',
          'Creative',
          'UserList',
          'Partner',
          'Advertiser',
          'InsertionOrder',
          'Pixel',
          'InventorySource',
          'CustomAffinity',
          'UniversalChannel',
          'UniversalSite',
          'SupportedExchange',
          'DataPartner',
          'GeoLocation',
          'Language',
          'DeviceCriteria',
          'Browser',
          'Isp'
        ],
        'partners': {
          'single_cell': True,
          'values': {
            'field': {
              'name': 'partners',
              'kind': 'integer_list',
              'order': 1,
              'default': '[]',
              'description': 'Comma sparated list of DV360 partners.'
            }
          }
        },
        'out': {
          'bigquery': {
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
                'order': 3,
                'default': '',
                'description': 'BigQuery dataset to write tables for each entity.'
              }
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('entity', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
