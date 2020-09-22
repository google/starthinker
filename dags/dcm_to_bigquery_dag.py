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

CM To BigQuery

Move existing CM report into a BigQuery table.

Specify an account id.
Specify either report name or report id to move a report.
The most recent valid file will overwrite the table.
Schema is pulled from the official CM specification.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'account': '',  # CM network id.
  'report_id': '',  # CM report id, empty if using name .
  'report_name': '',  # CM report name, empty if using id instead.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'table': '',  # Table to be written to in BigQuery.
  'is_incremental_load': False,  # Clear data in destination table during this report's time period, then append report data to existing table.
}

TASKS = [
  {
    'dcm': {
      'report': {
        'name': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'report_name',
            'description': 'CM report name, empty if using id instead.',
            'default': ''
          }
        },
        'report_id': {
          'field': {
            'order': 3,
            'kind': 'integer',
            'name': 'report_id',
            'description': 'CM report id, empty if using name .',
            'default': ''
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'account',
            'description': 'CM network id.',
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'table': {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'table',
              'description': 'Table to be written to in BigQuery.',
              'default': ''
            }
          },
          'is_incremental_load': {
            'field': {
              'order': 7,
              'kind': 'boolean',
              'name': 'is_incremental_load',
              'description': "Clear data in destination table during this report's time period, then append report data to existing table.",
              'default': False
            }
          },
          'dataset': {
            'field': {
              'order': 5,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Dataset to be written to in BigQuery.',
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

DAG_FACTORY = DAG_Factory('dcm_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
