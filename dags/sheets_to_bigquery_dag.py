###########################################################################
# 
#  Copyright 2019 Google Inc.
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
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 0,
          'default': 'user',
          'description': 'Credentials used for reading data.'
        }
      },
      'sheet': {
        'field': {
          'name': 'sheets_url',
          'kind': 'string',
          'order': 2,
          'default': ''
        }
      },
      'tab': {
        'field': {
          'name': 'sheets_tab',
          'kind': 'string',
          'order': 3,
          'default': ''
        }
      },
      'range': {
        'field': {
          'name': 'sheets_range',
          'kind': 'string',
          'order': 4,
          'default': ''
        }
      },
      'header': {
        'field': {
          'name': 'sheets_header',
          'kind': 'boolean',
          'order': 9,
          'default': True
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
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 5,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 6,
              'default': ''
            }
          }
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
