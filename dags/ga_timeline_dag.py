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

Google Analytics Timeline

Download Google Analytics settings to a BigQuery table.

Enter the dateset to which the Google Analytics settings will be downloaded.
Add the starthinker service account email to the Google Analytics account(s) in
which you are interested.
Schedule the recipe to run once a day.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'account_ids': [],
    'dataset': '',  # Dataset to be written to in BigQuery.
}

TASKS = [{
    'ga_settings_download': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'description':
            'Will create tables with format ga_* to hold each endpoint via a '
            'call to the API list function.',
        'accounts': {
            'field': {
                'name': 'account_ids',
                'default': [],
                'kind': 'integer_list',
                'order': 1
            }
        },
        'dataset': {
            'field': {
                'description': 'Dataset to be written to in BigQuery.',
                'name': 'dataset',
                'default': '',
                'kind': 'string',
                'order': 2
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('ga_timeline', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
