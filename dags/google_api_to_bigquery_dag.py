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

API To BigQuery

Execute a Google API function and store results to BigQuery.

Enter an api name and version.
Specify the function using dot notation and arguments using json.
If nextPageToken can be in response check iterate.
Give BigQuery dataset and table where response will be written.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'api': 'doubleclickbidmanager',  # See developer guide.
  'version': 'v1',  # Must be supported version.
  'function': 'reports.files.list',  # Full function dot notation path.
  'kwargs': {'accountId': 7480, 'profileId': 2782211, 'reportId': 132847265},  # Dictionray object of name value pairs.
  'iterate': False,  # Is the result a list?
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Table to write API call results to.
  'schema': [],  # Schema provided in JSON list format or empty list.
}

TASKS = [
  {
    'google_api': {
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 1,
          'default': 'user',
          'description': 'Credentials used for reading data.'
        }
      },
      'api': {
        'field': {
          'name': 'api',
          'kind': 'string',
          'order': 1,
          'default': 'doubleclickbidmanager',
          'description': 'See developer guide.'
        }
      },
      'version': {
        'field': {
          'name': 'version',
          'kind': 'string',
          'order': 2,
          'default': 'v1',
          'description': 'Must be supported version.'
        }
      },
      'function': {
        'field': {
          'name': 'function',
          'kind': 'string',
          'order': 3,
          'default': 'reports.files.list',
          'description': 'Full function dot notation path.'
        }
      },
      'kwargs': {
        'field': {
          'name': 'kwargs',
          'kind': 'json',
          'order': 4,
          'default': {
            'accountId': 7480,
            'profileId': 2782211,
            'reportId': 132847265
          },
          'description': 'Dictionray object of name value pairs.'
        }
      },
      'iterate': {
        'field': {
          'name': 'iterate',
          'kind': 'boolean',
          'order': 5,
          'default': False,
          'description': 'Is the result a list?'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 6,
              'default': '',
              'description': 'Existing dataset in BigQuery.'
            }
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 7,
              'default': '',
              'description': 'Table to write API call results to.'
            }
          },
          'schema': {
            'field': {
              'name': 'schema',
              'kind': 'json',
              'order': 9,
              'default': [
              ],
              'description': 'Schema provided in JSON list format or empty list.'
            }
          },
          'format': 'JSON'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('google_api_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
