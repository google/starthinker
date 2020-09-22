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

Sheet To BigQuery

Import data from a sheet and move it to a BigQuery table.

For the sheet, provide the full edit URL.
If the tab does not exist it will be created.
Empty cells in the range will be NULL.
Check Sheets header if first row is a header

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'sheets_url': '',
  'sheets_tab': '',
  'sheets_range': '',
  'dataset': '',
  'table': '',
  'sheets_header': True,
}

TASKS = [
  {
    'sheets': {
      'tab': {
        'field': {
          'order': 3,
          'kind': 'string',
          'name': 'sheets_tab',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': {
        'field': {
          'order': 4,
          'kind': 'string',
          'name': 'sheets_range',
          'default': ''
        }
      },
      'out': {
        'bigquery': {
          'table': {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'table',
              'default': ''
            }
          },
          'dataset': {
            'field': {
              'order': 5,
              'kind': 'string',
              'name': 'dataset',
              'default': ''
            }
          }
        },
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_write',
            'description': 'Credentials used for writing data.',
            'default': 'service'
          }
        }
      },
      'sheet': {
        'field': {
          'order': 2,
          'kind': 'string',
          'name': 'sheets_url',
          'default': ''
        }
      },
      'header': {
        'field': {
          'order': 9,
          'kind': 'boolean',
          'name': 'sheets_header',
          'default': True
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('sheets_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
