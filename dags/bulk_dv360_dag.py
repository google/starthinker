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

Bulk Editor For DV360

Allows bulk editing DV360 through Sheets and BigQuery.

  - Select <b>Create Sheet</b> and run the recipe.
  - Fill in <i>Partners</i> tab filter.
  - Run <b>Load Advertisers</b>.
  - Fill in <i>Advertisers</i> tab filter.
  - Run <b>Load Insertion Orders</b> or <b>Load Line Items</b> or <b>Load Creatives</b>.
  - Fill in changes on all tabs with colored fields.
  - Select <i>Audit</i> and run the recipe.
  - Check the <b>Audit</b> and <b>Preview</b> tabs.
  - Select <i>Patch</i> and run the recipe.
  - Check the <b>Success</b> and <b>Error</b> tabs.
  - Patch can be run multiple times.
  - Patch ONLY changes edited fields.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_dv': 'user',  # Credentials used for dv.
  'auth_sheet': 'user',  # Credentials used for sheet.
  'auth_bigquery': 'service',  # Credentials used for bigquery.
  'recipe_slug': '',  # Name of Google BigQuery dataset to create.
  'command': '',  # Action to take.
}

RECIPE = {
  'setup': {
    'day': [
    ],
    'hour': [
    ]
  },
  'tasks': [
    {
      'dataset': {
        '__comment__': 'Ensure dataset exists.',
        'auth': {
          'field': {
            'name': 'auth_bigquery',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Credentials used for writing data.'
          }
        },
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'prefix': 'DV_Sheet_',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name of Google BigQuery dataset to create.'
          }
        }
      }
    },
    {
      'drive': {
        '__comment__': 'Copy the default template to sheet with the recipe name',
        'auth': {
          'field': {
            'name': 'auth_sheet',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'copy': {
          'source': 'https://docs.google.com/spreadsheets/d/10ByZKMIPZQQOEwJlskzggRhhQqe44on_ebUxkjmZI_w/',
          'destination': {
            'field': {
              'name': 'recipe_slug',
              'prefix': 'DV Sheet ',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Name of Google Sheet to create.'
            }
          }
        }
      }
    },
    {
      'dv_sheets': {
        '__comment': 'Depending on users choice, execute a different part of the solution.',
        'auth_dv': {
          'field': {
            'name': 'auth_dv',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for dv.'
          }
        },
        'auth_sheets': {
          'field': {
            'name': 'auth_sheet',
            'kind': 'authentication',
            'order': 2,
            'default': 'user',
            'description': 'Credentials used for sheet.'
          }
        },
        'auth_bigquery': {
          'field': {
            'name': 'auth_bigquery',
            'kind': 'authentication',
            'order': 3,
            'default': 'service',
            'description': 'Credentials used for bigquery.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_slug',
            'prefix': 'DV Sheet ',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Name of Google Sheet to create.'
          }
        },
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'prefix': 'DV_Sheet_',
            'kind': 'string',
            'order': 5,
            'default': '',
            'description': 'Name of Google BigQuery dataset to create.'
          }
        },
        'command': {
          'field': {
            'name': 'command',
            'kind': 'choice',
            'choices': [
              'Clear Partners',
              'Clear Advertisers',
              'Clear Campaigns',
              'Clear Creatives',
              'Clear Insertion Orders',
              'Clear Line Items',
              'Clear Preview',
              'Clear Patch',
              'Load Partners',
              'Load Advertisers',
              'Load Campaigns',
              'Load Creatives',
              'Load Insertion Orders',
              'Load Line Items',
              'Preview',
              'Patch'
            ],
            'order': 6,
            'default': '',
            'description': 'Action to take.'
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('bulk_dv360', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
