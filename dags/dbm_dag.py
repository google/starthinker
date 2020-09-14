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
"""--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

DV360 Report

Create a DV360 report.

Reference field values from the <a
href='https://developers.google.com/bid-manager/v1/reports'>DV360 API</a> to
build a report.
Copy and paste the JSON definition of a report, <a
href='https://github.com/google/starthinker/blob/master/tests/scripts/dbm_to_bigquery.json#L9-L40'
target='_blank'>sample for reference</a>.
The report is only created, a seperate script is required to move the data.
To reset a report, delete it from DV360 reporting.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'report': '{}',  # Report body and filters.
    'delete': False,  # If report exists, delete it before creating a new one.
}

TASKS = [{
    'dbm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'delete': {
            'field': {
                'description':
                    'If report exists, delete it before creating a new one.',
                'name':
                    'delete',
                'default':
                    False,
                'kind':
                    'boolean',
                'order':
                    2
            }
        },
        'report': {
            'field': {
                'description': 'Report body and filters.',
                'name': 'report',
                'default': '{}',
                'kind': 'json',
                'order': 1
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dbm', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
