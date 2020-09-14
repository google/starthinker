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

CM To Sheets

Move existing CM report into a Sheet tab.

Specify an account id.
Specify either report name or report id to move a report.
The most recent valid file will be moved to the sheet.
Schema is pulled from the official CM specification.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'account': '',
    'report_id': '',
    'report_name': '',
    'sheet': '',
    'tab': '',
}

TASKS = [{
    'dcm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'out': {
            'sheets': {
                'tab': {
                    'field': {
                        'name': 'tab',
                        'default': '',
                        'kind': 'string',
                        'order': 6
                    }
                },
                'sheet': {
                    'field': {
                        'name': 'sheet',
                        'default': '',
                        'kind': 'string',
                        'order': 5
                    }
                },
                'range': 'A1'
            }
        },
        'report': {
            'report_id': {
                'field': {
                    'name': 'report_id',
                    'default': '',
                    'kind': 'integer',
                    'order': 3
                }
            },
            'name': {
                'field': {
                    'name': 'report_name',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            },
            'account': {
                'field': {
                    'name': 'account',
                    'default': '',
                    'kind': 'integer',
                    'order': 2
                }
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dcm_to_sheets', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
