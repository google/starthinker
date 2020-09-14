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

DV360 To Sheets

Move existing DV360 report into a Sheets tab.

Specify either report name or report id to move a report.
The most recent valid file will be moved to the sheet.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'report_id': '',  # DV360 report ID given in UI, not needed if name used.
    'report_name': '',  # Name of report, not needed if ID used.
    'sheet': '',  # Full URL to sheet being written to.
    'tab': '',  # Existing tab in sheet to write to.
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
        'out': {
            'sheets': {
                'tab': {
                    'field': {
                        'description': 'Existing tab in sheet to write to.',
                        'name': 'tab',
                        'default': '',
                        'kind': 'string',
                        'order': 4
                    }
                },
                'sheet': {
                    'field': {
                        'description': 'Full URL to sheet being written to.',
                        'name': 'sheet',
                        'default': '',
                        'kind': 'string',
                        'order': 3
                    }
                },
                'range': 'A1'
            }
        },
        'report': {
            'report_id': {
                'field': {
                    'description':
                        'DV360 report ID given in UI, not needed if name used.',
                    'name':
                        'report_id',
                    'default':
                        '',
                    'kind':
                        'integer',
                    'order':
                        1
                }
            },
            'name': {
                'field': {
                    'description': 'Name of report, not needed if ID used.',
                    'name': 'report_name',
                    'default': '',
                    'kind': 'string',
                    'order': 2
                }
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dbm_to_sheets', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
