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

DV360 To BigQuery

Move existing DV360 reports into a BigQuery table.

Specify either report name or report id to move a report.
A schema is recommended, if not provided it will be guessed.
The most recent valid file will be moved to the table.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Authorization used for writing data.
  'dbm_report_id': '',  # DV360 report ID given in UI, not needed if name used.
  'dbm_report_name': '',  # Name of report, not needed if ID used.
  'dbm_dataset': '',  # Existing BigQuery dataset.
  'dbm_table': '',  # Table to create from this report.
  'dbm_schema': '',  # Schema provided in JSON list format or empty value to auto detect.
  'is_incremental_load': False,  # Clear data in destination table during this report's time period, then append report data to destination table.
}

TASKS = [
  {
    'dbm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 0,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'schema': {
            'field': {
              'order': 6,
              'name': 'dbm_schema',
              'description': 'Schema provided in JSON list format or empty value to auto detect.',
              'kind': 'json'
            }
          },
          'auth': {
            'field': {
              'description': 'Authorization used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1,
              'default': 'service'
            }
          },
          'dataset': {
            'field': {
              'description': 'Existing BigQuery dataset.',
              'kind': 'string',
              'name': 'dbm_dataset',
              'order': 4,
              'default': ''
            }
          },
          'table': {
            'field': {
              'description': 'Table to create from this report.',
              'kind': 'string',
              'name': 'dbm_table',
              'order': 5,
              'default': ''
            }
          },
          'is_incremental_load': {
            'field': {
              'description': "Clear data in destination table during this report's time period, then append report data to destination table.",
              'kind': 'boolean',
              'name': 'is_incremental_load',
              'order': 7,
              'default': False
            }
          }
        }
      },
      'report': {
        'report_id': {
          'field': {
            'description': 'DV360 report ID given in UI, not needed if name used.',
            'kind': 'integer',
            'name': 'dbm_report_id',
            'order': 2,
            'default': ''
          }
        },
        'name': {
          'field': {
            'description': 'Name of report, not needed if ID used.',
            'kind': 'string',
            'name': 'dbm_report_name',
            'order': 3,
            'default': ''
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
