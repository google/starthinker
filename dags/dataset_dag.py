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

BigQuery Dataset

Create and permission a dataset in BigQuery.

Specify the name of the dataset.
If dataset exists, it is inchanged.
Add emails and / or groups to add read permission.
CAUTION: Removing permissions in StarThinker has no effect.
CAUTION: To remove permissions you have to edit the dataset.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'dataset_dataset': '',  # Name of Google BigQuery dataset to create.
    'auth_write': 'service',  # Credentials used for writing data.
    'dataset_emails': [],  # Comma separated emails.
    'dataset_groups': [],  # Comma separated groups.
}

TASKS = [{
    'dataset': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'emails': {
            'field': {
                'description': 'Comma separated emails.',
                'name': 'dataset_emails',
                'default': [],
                'kind': 'string_list',
                'order': 2
            }
        },
        'dataset': {
            'field': {
                'description': 'Name of Google BigQuery dataset to create.',
                'name': 'dataset_dataset',
                'default': '',
                'kind': 'string',
                'order': 1
            }
        },
        'groups': {
            'field': {
                'description': 'Comma separated groups.',
                'name': 'dataset_groups',
                'default': [],
                'kind': 'string_list',
                'order': 3
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dataset', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
