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

Query To View

Create a BigQuery view.

Specify a single query and choose legacy or standard mode.
For PLX use: SELECT * FROM [plx.google:FULL_TABLE_NAME.all] WHERE...
If the view exists, it is unchanged, delete it manually to re-create.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'query': '',  # SQL with newlines and all.
  'dataset': '',  # Existing BigQuery dataset.
  'view': '',  # View to create from this query.
  'legacy': True,  # Query type must match source tables.
}

TASKS = [
  {
    'bigquery': {
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 1,
          'default': 'user',
          'description': 'Credentials used for reading data.'
        }
      },
      'from': {
        'query': {
          'field': {
            'name': 'query',
            'kind': 'text',
            'order': 1,
            'default': '',
            'description': 'SQL with newlines and all.'
          }
        },
        'legacy': {
          'field': {
            'name': 'legacy',
            'kind': 'boolean',
            'order': 4,
            'default': True,
            'description': 'Query type must match source tables.'
          }
        }
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Existing BigQuery dataset.'
          }
        },
        'view': {
          'field': {
            'name': 'view',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'View to create from this query.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_view', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
