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

Floodlight Monitor

Monitor floodlight impressions specified in sheet and send email alerts.

Specify an account_id or account_id:subaccount_id.
Will copy <a
href='https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing'>Floodlight
Monitor Sheet</a> to the sheet you specify.
Follow instructions on sheet.
Emails are sent once a day.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'dcm_account': '',  # Specify an account_id as a number.
    'sheet':
        '',  # Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.
}

TASKS = [{
    'floodlight_monitor': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'template': {
            'template': {
                'tab':
                    'Floodlight Monitor',
                'sheet':
                    'https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing',
                'range':
                    'A1'
            }
        },
        'sheet': {
            'tab': 'Floodlight Monitor',
            'sheet': {
                'field': {
                    'description':
                        'Full Name or URL to Google Sheet, Floodlight Monitor '
                        'tab will be added.',
                    'name':
                        'sheet',
                    'default':
                        '',
                    'kind':
                        'string',
                    'order':
                        2
                }
            },
            'range': 'A2:B'
        },
        'account': {
            'field': {
                'description': 'Specify an account_id as a number.',
                'name': 'dcm_account',
                'default': '',
                'kind': 'string',
                'order': 1
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('floodlight_monitor', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
