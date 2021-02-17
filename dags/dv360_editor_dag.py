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

DV360 Bulk Editor

Allows bulk editing DV360 through Sheets and BigQuery.

  - Select <b>Load Partners</b>, <b>save</b> the recipe, then run. A Sheet called DV_Editor_ will be created.
  - In the 'Partners' sheet tab, fill in <i>Partners</i> tab filter.
  - Select <b>Load Advertisers</b>, <b>save</b> the recipe, then run.
  - In the 'Advertisers' sheet tab, fill in <i>Advertisers</i> tab filter.
  - Select <b>Load Campaigns</b>, <b>save</b> the recipe, then run. Filtering by campaigns is optional.
  - Now, select <b>Load Insertion Orders and Line Items</b>, <b>save</b> the recipe, then run.
  - To patch, fill in changes on all tabs with colored fields.
  - Select <i>Preview</i>, <b>save</b> the recipe, then run the recipe.
  - Check the <b>Audit</b> and <b>Preview</b> tabs.
  - To Patch, select <i>Patch</i>, <b>save</b> the recipe, then run.
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
  'recipe_name': '',  # Name of Google Sheet to create.
  'recipe_slug': '',  # Name of Google BigQuery dataset to create.
  'command': 'Load Partners',  # Action to take.
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
            'prefix': 'DV_Editor_',
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
          'source': 'https://docs.google.com/spreadsheets/d/18G6cGo4j5SsY08H8P53R22D_Pm6m-zkE6APd3EDLf2c/',
          'destination': {
            'field': {
              'name': 'recipe_name',
              'prefix': 'DV Editor ',
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
      'dv_editor': {
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
            'name': 'recipe_name',
            'prefix': 'DV Editor ',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Name of Google Sheet to create.'
          }
        },
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'prefix': 'DV_Editor_',
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
              'Clear Insertion Orders and Line Items',
              'Clear Preview',
              'Clear Patch',
              'Load Partners',
              'Load Advertisers',
              'Load Campaigns',
              'Load Insertion Orders and Line Items',
              'Preview',
              'Patch'
            ],
            'order': 6,
            'default': 'Load Partners',
            'description': 'Action to take.'
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dv360_editor', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
