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

DCM Report

Create a DCM report from a JSON definition.

Add a an account as [account_id]@[profile_id]
Fetch the report JSON definition. Arguably could be better.
The account is automatically added to the report definition.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'account': '',
  'body': '{}',
  'delete': False,
}

TASKS = [
  {
    'dcm': {
      'auth': 'user',
      'report': {
        'account': {
          'field': {
            'name': 'account',
            'kind': 'string',
            'order': 1,
            'default': ''
          }
        },
        'body': {
          'field': {
            'name': 'body',
            'kind': 'json',
            'order': 2,
            'default': '{}'
          }
        }
      },
      'delete': {
        'field': {
          'name': 'delete',
          'kind': 'boolean',
          'order': 3,
          'default': False
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
