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

DCM To BigQuery

Move existing DCM report into a BigQuery table.

Specify an account id.
Specify either report name or report id to move a report.
The most recent valid file will overwrite the table.
Schema is pulled from the official DCM specification.

'''

from starthinker_airflow.factory import DAG_Factory
 
# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'account': '',  # DCM network id.
  'report_id': '',  # DCM report id, empty if using name .
  'report_name': '',  # DCM report name, empty if using id instead.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'table': '',  # Table to be written to in BigQuery.
  'is_incremental_load': False,  # Clear data in destination table during this report's time period, then append report data to existing table.
}

TASKS = [
  {
    'dcm': {
      'auth': 'user',
      'report': {
        'account': {
          'field': {
            'name': 'account',
            'kind': 'integer',
            'order': 2,
            'default': '',
            'description': 'DCM network id.'
          }
        },
        'report_id': {
          'field': {
            'name': 'report_id',
            'kind': 'integer',
            'order': 3,
            'default': '',
            'description': 'DCM report id, empty if using name .'
          }
        },
        'name': {
          'field': {
            'name': 'report_name',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'DCM report name, empty if using id instead.'
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 5,
              'default': '',
              'description': 'Dataset to be written to in BigQuery.'
            }
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 6,
              'default': '',
              'description': 'Table to be written to in BigQuery.'
            }
          },
          'is_incremental_load': {
            'field': {
              'name': 'is_incremental_load',
              'kind': 'boolean',
              'order': 7,
              'default': False,
              'description': "Clear data in destination table during this report's time period, then append report data to existing table."
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
