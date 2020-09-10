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

CM To Storage

Move existing CM report into a Storage bucket.

Specify an account id.
Specify either report name or report id to move a report.
The most recent file will be moved to the bucket.
Schema is pulled from the official CM specification.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'account': '',
  'report_id': '',
  'report_name': '',
  'bucket': '',
  'path': 'CM_Report',
}

TASKS = [
  {
    'dcm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'storage': {
          'bucket': {
            'field': {
              'order': 5,
              'name': 'bucket',
              'default': '',
              'kind': 'string'
            }
          },
          'auth': {
            'field': {
              'description': 'Credentials used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1,
              'default': 'service'
            }
          },
          'path': {
            'field': {
              'order': 6,
              'name': 'path',
              'default': 'CM_Report',
              'kind': 'string'
            }
          }
        }
      },
      'report': {
        'account': {
          'field': {
            'order': 2,
            'name': 'account',
            'default': '',
            'kind': 'integer'
          }
        },
        'name': {
          'field': {
            'order': 4,
            'name': 'report_name',
            'default': '',
            'kind': 'string'
          }
        },
        'report_id': {
          'field': {
            'order': 3,
            'name': 'report_id',
            'default': '',
            'kind': 'integer'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_to_storage', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
