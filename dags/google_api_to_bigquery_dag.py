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
  'kwargs': {'profileId': 2782211, 'accountId': 7480, 'reportId': 132847265},  # Dictionray object of name value pairs.
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
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'Existing dataset in BigQuery.',
              'kind': 'string',
              'name': 'dataset',
              'order': 6,
              'default': ''
            }
          },
          'table': {
            'field': {
              'description': 'Table to write API call results to.',
              'kind': 'string',
              'name': 'table',
              'order': 7,
              'default': ''
            }
          },
          'format': 'JSON',
          'schema': {
            'field': {
              'description': 'Schema provided in JSON list format or empty list.',
              'kind': 'json',
              'name': 'schema',
              'order': 9,
              'default': [
              ]
            }
          }
        }
      },
      'function': {
        'field': {
          'description': 'Full function dot notation path.',
          'kind': 'string',
          'name': 'function',
          'order': 3,
          'default': 'reports.files.list'
        }
      },
      'version': {
        'field': {
          'description': 'Must be supported version.',
          'kind': 'string',
          'name': 'version',
          'order': 2,
          'default': 'v1'
        }
      },
      'kwargs': {
        'field': {
          'description': 'Dictionray object of name value pairs.',
          'kind': 'json',
          'name': 'kwargs',
          'order': 4,
          'default': {
            'profileId': 2782211,
            'accountId': 7480,
            'reportId': 132847265
          }
        }
      },
      'iterate': {
        'field': {
          'description': 'Is the result a list?',
          'kind': 'boolean',
          'name': 'iterate',
          'order': 5,
          'default': False
        }
      },
      'api': {
        'field': {
          'description': 'See developer guide.',
          'kind': 'string',
          'name': 'api',
          'order': 1,
          'default': 'doubleclickbidmanager'
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
