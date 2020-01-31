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

Move sheet data into a BigQuery table.

Specify <a href='https://smartsheet-platform.github.io/api-docs/' target='_blank'>SmartSheet</a> token.
Locate the ID of a sheet by viewing its properties.
Provide a BigQuery dataset ( must exist ) and table to write the data into.
StarThinker will automatically map the correct schema.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'token': '',  # Retrieve from SmartSheet account settings.
  'sheet': '',  # Retrieve from sheet properties.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this report.
}

TASKS = [
  {
    'smartsheet': {
      'auth': 'service',
      'token': {
        'field': {
          'name': 'token',
          'kind': 'string',
          'default': '',
          'description': 'Retrieve from SmartSheet account settings.'
        }
      },
      'sheet': {
        'field': {
          'name': 'sheet',
          'kind': 'string',
          'default': '',
          'description': 'Retrieve from sheet properties.'
        }
      },
      'out': {
        'bigquery': {
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
              'description': 'Table to create from this report.'
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
