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

Column Mapping

Use sheet to define keyword to column mappings.

For the sheet, provide the full URL.
A tab called <strong>Mapping</strong> will be created.
Follow the instructions in the tab to complete the mapping.
The in table should have the columns you want to map.
The out view will have the new columns created in the mapping.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'sheet': '',
    'tab': '',
    'in_dataset': '',
    'in_table': '',
    'out_dataset': '',
    'out_view': '',
}

TASKS = [{
    'mapping': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'tab': {
            'field': {
                'name': 'tab',
                'default': '',
                'kind': 'string',
                'order': 2
            }
        },
        'out': {
            'view': {
                'field': {
                    'name': 'out_view',
                    'default': '',
                    'kind': 'string',
                    'order': 8
                }
            },
            'dataset': {
                'field': {
                    'name': 'out_dataset',
                    'default': '',
                    'kind': 'string',
                    'order': 7
                }
            }
        },
        'in': {
            'dataset': {
                'field': {
                    'name': 'in_dataset',
                    'default': '',
                    'kind': 'string',
                    'order': 3
                }
            },
            'table': {
                'field': {
                    'name': 'in_table',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            }
        },
        'sheet': {
            'field': {
                'name': 'sheet',
                'default': '',
                'kind': 'string',
                'order': 1
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('mapping', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
