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

Line Item To BigQuery Via Values

Move using hard coded Id values.

Provide a comma delimited list of line item ids.
Specify the dataset and table where the lineitems will be written.
The schema will match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'ids': [],
  'destination_dataset': '',
  'destination_table': '',
}

TASKS = [
  {
    'lineitem': {
      'auth': 'user',
      'read': {
        'line_items': {
          'single_cell': True,
          'values': {
            'field': {
              'name': 'ids',
              'kind': 'integer_list',
              'order': 1,
              'default': [
              ]
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'destination_dataset',
                'kind': 'string',
                'order': 2,
                'default': ''
              }
            },
            'table': {
              'field': {
                'name': 'destination_table',
                'kind': 'string',
                'order': 3,
                'default': ''
              }
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('lineitem_read_to_bigquery_via_value', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
