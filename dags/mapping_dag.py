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

Column Mapping

Use sheet to define keyword to column mappings.

  - For the sheet, provide the full URL.
  - A tab called <strong>Mapping</strong> will be created.
  - Follow the instructions in the tab to complete the mapping.
  - The in table should have the columns you want to map.
  - The out view will have the new columns created in the mapping.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'sheet': '',
  'tab': '',
  'in_dataset': '',
  'in_table': '',
  'out_dataset': '',
  'out_view': '',
}

RECIPE = {
  'tasks': [
    {
      'mapping': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'sheet': {
          'field': {
            'name': 'sheet',
            'kind': 'string',
            'order': 1,
            'default': ''
          }
        },
        'tab': {
          'field': {
            'name': 'tab',
            'kind': 'string',
            'order': 2,
            'default': ''
          }
        },
        'in': {
          'dataset': {
            'field': {
              'name': 'in_dataset',
              'kind': 'string',
              'order': 3,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'in_table',
              'kind': 'string',
              'order': 4,
              'default': ''
            }
          }
        },
        'out': {
          'dataset': {
            'field': {
              'name': 'out_dataset',
              'kind': 'string',
              'order': 7,
              'default': ''
            }
          },
          'view': {
            'field': {
              'name': 'out_view',
              'kind': 'string',
              'order': 8,
              'default': ''
            }
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('mapping', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
