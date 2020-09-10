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

Census Data Correlation

Correlate another table with US Census data.  Expands a data set dimensions by finding population segments that correlate with the master table.

Pre-requisite is Census Normalize, run that at least once.
Specify JOIN, PASS, SUM, and CORRELATE columns to build the correlation query.
Define the DATASET and TABLE for the joinable source. Can be a view.
Choose the significance level.  More significance usually means more NULL results, balance quantity and quality using this value.
Specify where to write the results.
<br>IMPORTANT:</b> If you use VIEWS, you will have to delete them manually if the recipe changes.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth': 'service',  # Credentials used for writing data.
  'join': '',  # Name of column to join on, must match Census Geo_Id column.
  'pass': [],  # Comma seperated list of columns to pass through.
  'sum': [],  # Comma seperated list of columns to sum, optional.
  'correlate': [],  # Comma seperated list of percentage columns to correlate.
  'from_dataset': '',  # Existing BigQuery dataset.
  'from_table': '',  # Table to use as join data.
  'significance': '80',  # Select level of significance to test.
  'to_dataset': '',  # Existing BigQuery dataset.
  'type': 'table',  # Write Census_Percent as table or view.
}

TASKS = [
  {
    'census': {
      'to': {
        'type': {
          'field': {
            'choices': [
              'table',
              'view'
            ],
            'description': 'Write Census_Percent as table or view.',
            'name': 'type',
            'kind': 'choice',
            'order': 10,
            'default': 'table'
          }
        },
        'dataset': {
          'field': {
            'description': 'Existing BigQuery dataset.',
            'kind': 'string',
            'name': 'to_dataset',
            'order': 9,
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for writing data.',
          'kind': 'authentication',
          'name': 'auth',
          'order': 0,
          'default': 'service'
        }
      },
      'correlate': {
        'sum': {
          'field': {
            'description': 'Comma seperated list of columns to sum, optional.',
            'kind': 'string_list',
            'name': 'sum',
            'order': 3,
            'default': [
            ]
          }
        },
        'join': {
          'field': {
            'description': 'Name of column to join on, must match Census Geo_Id column.',
            'kind': 'string',
            'name': 'join',
            'order': 1,
            'default': ''
          }
        },
        'correlate': {
          'field': {
            'description': 'Comma seperated list of percentage columns to correlate.',
            'kind': 'string_list',
            'name': 'correlate',
            'order': 4,
            'default': [
            ]
          }
        },
        'pass': {
          'field': {
            'description': 'Comma seperated list of columns to pass through.',
            'kind': 'string_list',
            'name': 'pass',
            'order': 2,
            'default': [
            ]
          }
        },
        'dataset': {
          'field': {
            'description': 'Existing BigQuery dataset.',
            'kind': 'string',
            'name': 'from_dataset',
            'order': 5,
            'default': ''
          }
        },
        'table': {
          'field': {
            'description': 'Table to use as join data.',
            'kind': 'string',
            'name': 'from_table',
            'order': 6,
            'default': ''
          }
        },
        'significance': {
          'field': {
            'choices': [
              '80',
              '90',
              '98',
              '99',
              '99.5',
              '99.95'
            ],
            'description': 'Select level of significance to test.',
            'name': 'significance',
            'kind': 'choice',
            'order': 7,
            'default': '80'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_census_correlate', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
