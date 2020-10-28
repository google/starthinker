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

Anonymize Dataset

Copies tables and view from one dataset to another and anynonamizes all rows.  Used to create sample datasets for dashboards.

Ensure you have user access to both datasets.
Provide the source project and dataset.
Provide the destination project and dataset.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'service',  # Credentials used for reading data.
  'from_project': '',  # Original project to copy from.
  'from_dataset': '',  # Original dataset to copy from.
  'to_project': None,  # Anonymous data will be writen to.
  'to_dataset': '',  # Anonymous data will be writen to.
}

TASKS = [
  {
    'anonymize': {
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 1,
          'default': 'service',
          'description': 'Credentials used for reading data.'
        }
      },
      'bigquery': {
        'from': {
          'project': {
            'field': {
              'name': 'from_project',
              'kind': 'string',
              'order': 1,
              'description': 'Original project to copy from.'
            }
          },
          'dataset': {
            'field': {
              'name': 'from_dataset',
              'kind': 'string',
              'order': 2,
              'description': 'Original dataset to copy from.'
            }
          }
        },
        'to': {
          'project': {
            'field': {
              'name': 'to_project',
              'kind': 'string',
              'order': 3,
              'default': None,
              'description': 'Anonymous data will be writen to.'
            }
          },
          'dataset': {
            'field': {
              'name': 'to_dataset',
              'kind': 'string',
              'order': 4,
              'description': 'Anonymous data will be writen to.'
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('anonymize', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
