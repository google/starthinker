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

Salesforce To BigQuery

Move query results into a BigQuery table.

Specify <a href='https://developer.salesforce.com/' target='_blank'>Salesforce</a> credentials.
Specify the query youd like to execute.
Specify a <a href='https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file' target='_blank'>SCHEMA</a> for that query ( optional ).

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'password': '',  # Your Salesforce login password.
  'username': '',  # Your Salesforce user email.
  'query': '',  # The query to run in Salesforce.
  'secret': '',  # Retrieve from a Salesforce App.
  'domain': 'login.salesforce.com',  # Retrieve from a Salesforce Domain.
  'client': '',  # Retrieve from a Salesforce App.
  'auth_read': 'user',  # Credentials used for reading data.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this report.
  'schema': '[]',  # Schema provided in JSON list format or empty list.
}

TASKS = [
  {
    'salesforce': {
      'query': {
        'field': {
          'kind': 'string',
          'name': 'query',
          'description': 'The query to run in Salesforce.',
          'default': ''
        }
      },
      'password': {
        'field': {
          'kind': 'password',
          'name': 'password',
          'description': 'Your Salesforce login password.',
          'default': ''
        }
      },
      'username': {
        'field': {
          'kind': 'email',
          'name': 'username',
          'description': 'Your Salesforce user email.',
          'default': ''
        }
      },
      'domain': {
        'field': {
          'kind': 'string',
          'name': 'domain',
          'description': 'Retrieve from a Salesforce Domain.',
          'default': 'login.salesforce.com'
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
      'secret': {
        'field': {
          'kind': 'string',
          'name': 'secret',
          'description': 'Retrieve from a Salesforce App.',
          'default': ''
        }
      },
      'out': {
        'bigquery': {
          'schema': {
            'field': {
              'order': 5,
              'kind': 'json',
              'name': 'schema',
              'description': 'Schema provided in JSON list format or empty list.',
              'default': '[]'
            }
          },
          'table': {
            'field': {
              'order': 4,
              'kind': 'string',
              'name': 'table',
              'description': 'Table to create from this report.',
              'default': ''
            }
          },
          'dataset': {
            'field': {
              'order': 3,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Existing BigQuery dataset.',
              'default': ''
            }
          }
        }
      },
      'client': {
        'field': {
          'kind': 'string',
          'name': 'client',
          'description': 'Retrieve from a Salesforce App.',
          'default': ''
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('salesforce_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
