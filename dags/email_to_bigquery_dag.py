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

Email Fetch

Import emailed CM report, Dv360 report, csv, or excel into a BigQuery table.

The person executing this recipe must be the recipient of the email.
Give a regular expression to match the email subject, link or attachment.
The data downloaded will overwrite the table specified.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'email_from': '',  # Must match from field.
  'auth_read': 'user',  # Credentials used for reading data.
  'email_to': '',  # Must match to field.
  'subject': '',  # Regular expression to match subject.
  'link': '',  # Regular expression to match email.
  'attachment': '',  # Regular expression to match atttachment.
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Name of table to be written to.
  'dbm_schema': '[]',  # Schema provided in JSON list format or empty list.
  'is_incremental_load': False,  # Append report data to table based on date column, de-duplicates.
}

TASKS = [
  {
    'email': {
      'out': {
        'bigquery': {
          'schema': {
            'field': {
              'order': 8,
              'kind': 'json',
              'name': 'dbm_schema',
              'description': 'Schema provided in JSON list format or empty list.',
              'default': '[]'
            }
          },
          'table': {
            'field': {
              'order': 7,
              'kind': 'string',
              'name': 'table',
              'description': 'Name of table to be written to.',
              'default': ''
            }
          },
          'is_incremental_load': {
            'field': {
              'order': 9,
              'kind': 'boolean',
              'name': 'is_incremental_load',
              'description': 'Append report data to table based on date column, de-duplicates.',
              'default': False
            }
          },
          'dataset': {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Existing dataset in BigQuery.',
              'default': ''
            }
          }
        }
      },
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
        'to': {
          'field': {
            'order': 2,
            'kind': 'string',
            'name': 'email_to',
            'description': 'Must match to field.',
            'default': ''
          }
        },
        'subject': {
          'field': {
            'order': 3,
            'kind': 'string',
            'name': 'subject',
            'description': 'Regular expression to match subject.',
            'default': ''
          }
        },
        'link': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'link',
            'description': 'Regular expression to match email.',
            'default': ''
          }
        },
        'attachment': {
          'field': {
            'order': 5,
            'kind': 'string',
            'name': 'attachment',
            'description': 'Regular expression to match atttachment.',
            'default': ''
          }
        },
        'from': {
          'field': {
            'order': 1,
            'kind': 'string',
            'name': 'email_from',
            'description': 'Must match from field.',
            'default': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('email_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
