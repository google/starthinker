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

CM Report Emailed To BigQuery

Pulls a CM Report from a gMail powered email account into BigQuery.

The person executing this recipe must be the recipient of the email.
Schedule a CM report to be sent to <b>UNDEFINED</b>.
Or set up a redirect rule to forward a report you already receive.
The report must be sent as an attachment.
Ensure this recipe runs after the report is email daily.
Give a regular expression to match the email subject.
Configure the destination in BigQuery to write the data.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'email': '',  # Email address report was sent to.
  'auth_read': 'user',  # Credentials used for reading data.
  'subject': '.*',  # Regular expression to match subject. Double escape backslashes.
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Name of table to be written to.
  'is_incremental_load': False,  # Append report data to table based on date column, de-duplicates.
}

TASKS = [
  {
    'email': {
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'read': {
        'out': {
          'bigquery': {
            'table': {
              'field': {
                'order': 4,
                'kind': 'string',
                'name': 'table',
                'description': 'Name of table to be written to.',
                'default': ''
              }
            },
            'is_incremental_load': {
              'field': {
                'order': 6,
                'kind': 'boolean',
                'name': 'is_incremental_load',
                'description': 'Append report data to table based on date column, de-duplicates.',
                'default': False
              }
            },
            'dataset': {
              'field': {
                'order': 3,
                'kind': 'string',
                'name': 'dataset',
                'description': 'Existing dataset in BigQuery.',
                'default': ''
              }
            }
          }
        },
        'subject': {
          'field': {
            'order': 2,
            'kind': 'string',
            'name': 'subject',
            'description': 'Regular expression to match subject. Double escape backslashes.',
            'default': '.*'
          }
        },
        'to': {
          'field': {
            'order': 1,
            'kind': 'string',
            'name': 'email',
            'description': 'Email address report was sent to.',
            'default': ''
          }
        },
        'attachment': '.*',
        'from': 'noreply-cm@google.com'
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('email_cm_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
