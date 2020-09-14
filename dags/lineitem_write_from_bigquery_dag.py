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

Line Item From BigQuery

Upload Line Items From BigQuery To DV360.

Specify the table or view where the lineitem data is defined.
The schema should match <a
href='https://developers.google.com/bid-manager/guides/entity-write/format'
target='_blank'>Entity Write Format</a>.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'dataset': '',
    'query': 'SELECT * FROM `Dataset.Table`;',
    'legacy': False,
}

TASKS = [{
    'lineitem': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'write': {
            'bigquery': {
                'query': {
                    'field': {
                        'name': 'query',
                        'default': 'SELECT * FROM `Dataset.Table`;',
                        'kind': 'string',
                        'order': 2
                    }
                },
                'legacy': {
                    'field': {
                        'name': 'legacy',
                        'default': False,
                        'kind': 'boolean',
                        'order': 3
                    }
                },
                'dataset': {
                    'field': {
                        'name': 'dataset',
                        'default': '',
                        'kind': 'string',
                        'order': 1
                    }
                }
            },
            'dry_run': False
        }
    }
}]

DAG_FACTORY = DAG_Factory('lineitem_write_from_bigquery', {'tasks': TASKS},
                          INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
