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

Trends Places To Sheets Via Query

Move using a WOEID query.

Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
Provide BigQuery WOEID source query.
Specify Sheet url and tab to write API call results to.
Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_write': 'service',  # Credentials used for writing data.
  'secret': '',
  'key': '',
  'places_dataset': '',
  'places_query': '',
  'places_legacy': False,
  'destination_sheet': '',
  'destination_tab': '',
}

TASKS = [
  {
    'twitter': {
      'auth': {
        'field': {
          'name': 'auth_write',
          'kind': 'authentication',
          'order': 1,
          'default': 'service',
          'description': 'Credentials used for writing data.'
        }
      },
      'secret': {
        'field': {
          'name': 'secret',
          'kind': 'string',
          'order': 1,
          'default': ''
        }
      },
      'key': {
        'field': {
          'name': 'key',
          'kind': 'string',
          'order': 2,
          'default': ''
        }
      },
      'trends': {
        'places': {
          'single_cell': True,
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'places_dataset',
                'kind': 'string',
                'order': 3,
                'default': ''
              }
            },
            'query': {
              'field': {
                'name': 'places_query',
                'kind': 'string',
                'order': 4,
                'default': ''
              }
            },
            'legacy': {
              'field': {
                'name': 'places_legacy',
                'kind': 'boolean',
                'order': 5,
                'default': False
              }
            }
          }
        }
      },
      'out': {
        'sheets': {
          'sheet': {
            'field': {
              'name': 'destination_sheet',
              'kind': 'string',
              'order': 6,
              'default': ''
            }
          },
          'tab': {
            'field': {
              'name': 'destination_tab',
              'kind': 'string',
              'order': 7,
              'default': ''
            }
          },
          'range': 'A1'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('trends_places_to_sheets_via_query', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
