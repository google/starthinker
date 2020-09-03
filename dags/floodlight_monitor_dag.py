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

Floodlight Monitor

Monitor floodlight impressions specified in sheet and send email alerts.

Specify an account_id or account_id:subaccount_id.
Will copy <a href='https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing'>Floodlight Monitor Sheet</a> to the sheet you specify.
Follow instructions on sheet.
Emails are sent once a day.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'dcm_account': '',  # Specify an account_id as a number.
  'sheet': '',  # Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.
}

TASKS = [
  {
    'floodlight_monitor': {
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 1,
          'default': 'user',
          'description': 'Credentials used for reading data.'
        }
      },
      'account': {
        'field': {
          'name': 'dcm_account',
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'Specify an account_id as a number.'
        }
      },
      'template': {
        'template': {
          'sheet': 'https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing',
          'tab': 'Floodlight Monitor',
          'range': 'A1'
        }
      },
      'sheet': {
        'sheet': {
          'field': {
            'name': 'sheet',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.'
          }
        },
        'tab': 'Floodlight Monitor',
        'range': 'A2:B'
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('floodlight_monitor', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
