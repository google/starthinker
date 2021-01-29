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

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

Line Item To BigQuery Via Query

Move using an Id query.

  - Specify the query that will pull the lineitem ids to download.
  - Specify the dataset and table where the lineitems will be written.
  - The schema will match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'id_dataset': '',
  'id_query': 'SELECT * FROM `Dataset.Table`;',
  'id_legacy': False,
  'destination_dataset': '',
  'destination_table': '',
}

RECIPE = {
  'tasks': [
    {
      'lineitem': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'read': {
          'line_items': {
            'single_cell': True,
            'bigquery': {
              'dataset': {
                'field': {
                  'name': 'id_dataset',
                  'kind': 'string',
                  'order': 1,
                  'default': ''
                }
              },
              'query': {
                'field': {
                  'name': 'id_query',
                  'kind': 'string',
                  'order': 2,
                  'default': 'SELECT * FROM `Dataset.Table`;'
                }
              },
              'legacy': {
                'field': {
                  'name': 'id_legacy',
                  'kind': 'boolean',
                  'order': 3,
                  'default': False
                }
              }
            }
          },
          'out': {
            'bigquery': {
              'dataset': {
                'field': {
                  'name': 'destination_dataset',
                  'kind': 'string',
                  'order': 4,
                  'default': ''
                }
              },
              'table': {
                'field': {
                  'name': 'destination_table',
                  'kind': 'string',
                  'order': 5,
                  'default': ''
                }
              }
            }
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('lineitem_read_to_bigquery_via_query', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
