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

DBM To BigQuery

Move existing DBM reports into a BigQuery table.

Specify either report name or report id to move a report.
A schema is recommended, if not provided it will be guessed.
The most recent valid file will be moved to the table.

'''

from starthinker_airflow.factory import DAG_Factory
 
# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'dbm_report_id': '',  # DBM report ID given in UI, not needed if name used.
  'dbm_report_name': '',  # Name of report, not needed if ID used.
  'dbm_dataset': '',  # Existing BigQuery dataset.
  'dbm_table': '',  # Table to create from this report.
  'dbm_schema': '[]',  # Schema provided in JSON list format or empty list.
  'is_incremental_load': False,  # Clear data in destination table during this report's time period, then append report data to destination table.
}

TASKS = [
  {
    'dbm': {
      'auth': 'user',
      'report': {
        'report_id': {
          'field': {
            'name': 'dbm_report_id',
            'kind': 'integer',
            'order': 1,
            'default': '',
            'description': 'DBM report ID given in UI, not needed if name used.'
          }
        },
        'name': {
          'field': {
            'name': 'dbm_report_name',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name of report, not needed if ID used.'
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dbm_dataset',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Existing BigQuery dataset.'
            }
          },
          'table': {
            'field': {
              'name': 'dbm_table',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Table to create from this report.'
            }
          },
          'schema': {
            'field': {
              'name': 'dbm_schema',
              'kind': 'json',
              'order': 5,
              'default': '[]',
              'description': 'Schema provided in JSON list format or empty list.'
            }
          },
          'is_incremental_load': {
            'field': {
              'name': 'is_incremental_load',
              'kind': 'boolean',
              'order': 6,
              'default': False,
              'description': "Clear data in destination table during this report's time period, then append report data to destination table."
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dbm_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
