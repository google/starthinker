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

CM Report Run

Trigger a CM report run

Specify an account id.
Specify either report name or report id to run.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'account': '',  # CM network id.
  'report_id': '',  # CM report id, empty if using name.
  'report_name': '',  # CM report name, empty if using id instead.
}

TASKS = [
  {
    'dcm': {
      'report': {
        'name': {
          'field': {
            'order': 3,
            'kind': 'string',
            'name': 'report_name',
            'description': 'CM report name, empty if using id instead.',
            'default': ''
          }
        },
        'report_id': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'report_id',
            'description': 'CM report id, empty if using name.',
            'default': ''
          }
        },
        'account': {
          'field': {
            'order': 1,
            'kind': 'integer',
            'name': 'account',
            'description': 'CM network id.',
            'default': ''
          }
        }
      },
      'report_run_only': True,
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_run', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
