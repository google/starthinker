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

Project IAM

Sets project permissions for an email.

Provide a role in the form of projects/[project name]/roles/[role name]
Enter an email to grant that role to.
This only grants roles, you must remove them from the project manually.

'''

from starthinker_airflow.factory import DAG_Factory
 
# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'role': '',  # projects/[project name]/roles/[role name]
  'email': '',  # Email address to grant role to.
}

TASKS = [
  {
    'iam': {
      'auth': 'service',
      'role': {
        'field': {
          'name': 'role',
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'projects/[project name]/roles/[role name]'
        }
      },
      'email': {
        'field': {
          'name': 'email',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'Email address to grant role to.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('iam', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
