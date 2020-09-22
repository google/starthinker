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
  'kwargs': {'accountId': 7480, 'reportId': 132847265, 'profileId': 2782211},  # Dictionray object of name value pairs.
  'iterate': False,  # Is the result a list?
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Table to write API call results to.
  'schema': [],  # Schema provided in JSON list format or empty list.
}

TASKS = [
  {
    'google_api': {
      'kwargs': {
        'field': {
          'order': 4,
          'kind': 'json',
          'name': 'kwargs',
          'description': 'Dictionray object of name value pairs.',
          'default': {
            'accountId': 7480,
            'reportId': 132847265,
            'profileId': 2782211
          }
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'function': {
        'field': {
          'order': 3,
          'kind': 'string',
          'name': 'function',
          'description': 'Full function dot notation path.',
          'default': 'reports.files.list'
        }
      },
      'version': {
        'field': {
          'order': 2,
          'kind': 'string',
          'name': 'version',
          'description': 'Must be supported version.',
          'default': 'v1'
        }
      },
      'out': {
        'bigquery': {
          'schema': {
            'field': {
              'order': 9,
              'kind': 'json',
              'name': 'schema',
              'description': 'Schema provided in JSON list format or empty list.',
              'default': [
              ]
            }
          },
          'table': {
            'field': {
              'order': 7,
              'kind': 'string',
              'name': 'table',
              'description': 'Table to write API call results to.',
              'default': ''
            }
          },
          'dataset': {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Existing dataset in BigQuery.',
              'default': ''
            }
          },
          'format': 'JSON'
        }
      },
      'iterate': {
        'field': {
          'order': 5,
          'kind': 'boolean',
          'name': 'iterate',
          'description': 'Is the result a list?',
          'default': False
        }
      },
      'api': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'api',
          'description': 'See developer guide.',
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
