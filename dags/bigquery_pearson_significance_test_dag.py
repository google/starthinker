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

Pearson Significance Test Function

Add function to dataset for checking if correlation is significant.

Specify the dataset, and the function will be added and available.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth': 'service',  # Credentials used for writing function.
    'dataset': '',  # Existing BigQuery dataset.
}

TASKS = [{
    'bigquery': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing function.',
                'name': 'auth',
                'default': 'service',
                'kind': 'authentication',
                'order': 0
            }
        },
        'to': {
            'dataset': {
                'field': {
                    'description': 'Existing BigQuery dataset.',
                    'name': 'dataset',
                    'default': '',
                    'kind': 'string',
                    'order': 1
                }
            }
        },
        'function': 'pearson_significance_test'
    }
}]

DAG_FACTORY = DAG_Factory('bigquery_pearson_significance_test',
                          {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
