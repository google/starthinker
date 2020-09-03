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

Storage To Table

Move using bucket and path prefix.

Specify a bucket and path prefix, * suffix is NOT required.
Every time the job runs it will overwrite the table.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'bucket': '',  # Google cloud bucket.
  'auth_write': 'service',  # Credentials used for writing data.
  'path': '',  # Path prefix to read from, no * required.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this query.
  'schema': '[]',  # Schema provided in JSON list format or empty list.
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
        'bucket': {
          'field': {
            'name': 'bucket',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Google cloud bucket.'
          }
        },
        'path': {
          'field': {
            'name': 'path',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Path prefix to read from, no * required.'
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
            'order': 3,
            'default': '',
            'description': 'Existing BigQuery dataset.'
          }
        },
        'table': {
          'field': {
            'name': 'table',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Table to create from this query.'
          }
        }
      },
      'schema': {
        'field': {
          'name': 'schema',
          'kind': 'json',
          'order': 5,
          'default': '[]',
          'description': 'Schema provided in JSON list format or empty list.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_storage', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
