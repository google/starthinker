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

SmartSheet Sheet To BigQuery

Move sheet data into a BigQuery table.

Specify <a href='https://smartsheet-platform.github.io/api-docs/' target='_blank'>SmartSheet</a> token.
Locate the ID of a sheet by viewing its properties.
Provide a BigQuery dataset ( must exist ) and table to write the data into.
StarThinker will automatically map the correct schema.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'token': '',  # Retrieve from SmartSheet account settings.
  'sheet': '',  # Retrieve from sheet properties.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this report.
  'schema': '',  # Schema provided in JSON list format or leave empty to auto detect.
  'link': True,  # Add a link to each row as the first column.
}

TASKS = [
  {
    'smartsheet': {
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'token': {
        'field': {
          'order': 2,
          'kind': 'string',
          'name': 'token',
          'description': 'Retrieve from SmartSheet account settings.',
          'default': ''
        }
      },
      'sheet': {
        'field': {
          'order': 3,
          'kind': 'string',
          'name': 'sheet',
          'description': 'Retrieve from sheet properties.'
        }
      },
      'link': {
        'field': {
          'order': 7,
          'kind': 'boolean',
          'name': 'link',
          'description': 'Add a link to each row as the first column.',
          'default': True
        }
      },
      'out': {
        'bigquery': {
          'schema': {
            'field': {
              'order': 6,
              'kind': 'json',
              'name': 'schema',
              'description': 'Schema provided in JSON list format or leave empty to auto detect.'
            }
          },
          'table': {
            'field': {
              'order': 5,
              'kind': 'string',
              'name': 'table',
              'description': 'Table to create from this report.',
              'default': ''
            }
          },
          'dataset': {
            'field': {
              'order': 4,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Existing BigQuery dataset.',
              'default': ''
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
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('smartsheet_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
