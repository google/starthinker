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

DBM To Storage

Move existing DBM report into a Storage bucket.

Specify either report name or report id to move a report.
The most recent valid file will be moved to the bucket.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dbm_report_id': '',  # DBM report ID given in UI, not needed if name used.
  'dbm_report_name': '',  # Name of report, not needed if ID used.
  'dbm_bucket': '',  # Google cloud bucket.
  'dbm_path': '',  # Path and filename to write to.
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
        'storage': {
          'bucket': {
            'field': {
              'name': 'dbm_bucket',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Google cloud bucket.'
            }
          },
          'path': {
            'field': {
              'name': 'dbm_path',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Path and filename to write to.'
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dbm_to_storage', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
