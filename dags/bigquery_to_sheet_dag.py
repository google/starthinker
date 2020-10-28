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

Query to Sheet

Copy the contents of a query into a Google Sheet.

Specify the sheet and the query.
Leave range blank or set to A2 to insert one line down.
The range is cleared before the sheet is written to.
To select a table use SELECT * FROM table.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'sheet': '',  # Either sheet url or sheet name.
  'tab': '',  # Name of the tab where to put the data.
  'range': '',  # Range in the sheet to place the data, leave blank for whole sheet.
  'dataset': '',  # Existing BigQuery dataset.
  'query': '',  # Query to pull data from the table.
  'legacy': True,  # Use Legacy SQL
}

TASKS = [
  {
    'bigquery': {
      'auth': {
        'field': {
          'name': 'auth_read',
          'kind': 'authentication',
          'order': 1,
          'default': 'user',
          'description': 'Credentials used for reading data.'
        }
      },
      'from': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Existing BigQuery dataset.'
          }
        },
        'query': {
          'field': {
            'name': 'query',
            'kind': 'text',
            'order': 5,
            'default': '',
            'description': 'Query to pull data from the table.'
          }
        },
        'legacy': {
          'field': {
            'name': 'legacy',
            'kind': 'boolean',
            'order': 6,
            'default': True,
            'description': 'Use Legacy SQL'
          }
        }
      },
      'to': {
        'sheet': {
          'field': {
            'name': 'sheet',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Either sheet url or sheet name.'
          }
        },
        'tab': {
          'field': {
            'name': 'tab',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name of the tab where to put the data.'
          }
        },
        'range': {
          'field': {
            'name': 'range',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Range in the sheet to place the data, leave blank for whole sheet.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_to_sheet', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
