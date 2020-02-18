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

DBM Report

Create a DBM report.

Reference field values from the <a href='https://developers.google.com/bid-manager/v1/reports'>DBM API</a> to build a report.
Copy and paste the JSON definition of a report.
The report is only created, use a move script to move it.
To reset a report, delete it from DBM reporting.

'''

from starthinker_airflow.factory import DAG_Factory
 
# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'body': '{}',
  'delete': False,
}

TASKS = [
  {
    'dbm': {
      'auth': 'user',
      'report': {
        'body': {
          'field': {
            'name': 'body',
            'kind': 'json',
            'order': 1,
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

DAG_FACTORY = DAG_Factory('dbm', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
