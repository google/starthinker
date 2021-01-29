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

CM360 Data Transfer To Bigquery

Move data from a DT bucket into a BigQuery table.

  - Ensure your user has <a href='https://developers.google.com/doubleclick-advertisers/dtv2/getting-started' target='_blank'>access to the bucket</a>.
  - Provide the DT bucket name to read from.
  - Provide the path of the files to read.
  - Each file is synchronized to a unique table.  Use a view or aggregate select.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'bucket': '',  # Name of bucket where DT files are stored.
  'paths': [],  # List of prefixes to pull specific DT files.
  'days': 2,  # Number of days back to synchronize.
  'hours': 0,  # Number of hours back to synchronize.
  'dataset': '',  # Existing dataset in BigQuery.
}

RECIPE = {
  'setup': {
    'timeout_seconds': '30000'
  },
  'tasks': [
    {
      'dt': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 0,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'from': {
          'bucket': {
            'field': {
              'name': 'bucket',
              'kind': 'string',
              'order': 2,
              'default': '',
              'description': 'Name of bucket where DT files are stored.'
            }
          },
          'paths': {
            'field': {
              'name': 'paths',
              'kind': 'string_list',
              'order': 3,
              'default': [
              ],
              'description': 'List of prefixes to pull specific DT files.'
            }
          },
          'days': {
            'field': {
              'name': 'days',
              'kind': 'integer',
              'order': 4,
              'default': 2,
              'description': 'Number of days back to synchronize.'
            }
          },
          'hours': {
            'field': {
              'name': 'hours',
              'kind': 'integer',
              'order': 5,
              'default': 0,
              'description': 'Number of hours back to synchronize.'
            }
          }
        },
        'to': {
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
              'order': 6,
              'default': '',
              'description': 'Existing dataset in BigQuery.'
            }
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dt', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
