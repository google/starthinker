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
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'schema': {
            'field': {
              'description': 'Schema provided in JSON list format or empty list.',
              'kind': 'json',
              'name': 'dbm_schema',
              'order': 8,
              'default': '[]'
            }
          },
          'dataset': {
            'field': {
              'description': 'Existing dataset in BigQuery.',
              'kind': 'string',
              'name': 'dataset',
              'order': 6,
              'default': ''
            }
          },
          'table': {
            'field': {
              'description': 'Name of table to be written to.',
              'kind': 'string',
              'name': 'table',
              'order': 7,
              'default': ''
            }
          },
          'is_incremental_load': {
            'field': {
              'description': 'Append report data to table based on date column, de-duplicates.',
              'kind': 'boolean',
              'name': 'is_incremental_load',
              'order': 9,
              'default': False
            }
          }
        }
      },
      'read': {
        'from': {
          'field': {
            'description': 'Must match from field.',
            'kind': 'string',
            'name': 'email_from',
            'order': 1,
            'default': ''
          }
        },
        'to': {
          'field': {
            'description': 'Must match to field.',
            'kind': 'string',
            'name': 'email_to',
            'order': 2,
            'default': ''
          }
        },
        'subject': {
          'field': {
            'description': 'Regular expression to match subject.',
            'kind': 'string',
            'name': 'subject',
            'order': 3,
            'default': ''
          }
        },
        'link': {
          'field': {
            'description': 'Regular expression to match email.',
            'kind': 'string',
            'name': 'link',
            'order': 4,
            'default': ''
          }
        },
        'attachment': {
          'field': {
            'description': 'Regular expression to match atttachment.',
            'kind': 'string',
            'name': 'attachment',
            'order': 5,
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
