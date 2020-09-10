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

Trends Places To BigQuery Via Query

Move using a WOEID query.

Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
Provide BigQuery WOEID source query.
Specify BigQuery dataset and table to write API call results to.
Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'secret': '',
  'auth_write': 'service',  # Credentials used for writing data.
  'key': '',
  'places_dataset': '',
  'places_query': '',
  'places_legacy': False,
  'destination_dataset': '',
  'destination_table': '',
}

TASKS = [
  {
    'twitter': {
      'key': {
        'field': {
          'order': 2,
          'name': 'key',
          'default': '',
          'kind': 'string'
        }
      },
      'secret': {
        'field': {
          'order': 1,
          'name': 'secret',
          'default': '',
          'kind': 'string'
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'order': 6,
              'name': 'destination_dataset',
              'default': '',
              'kind': 'string'
            }
          },
          'table': {
            'field': {
              'order': 7,
              'name': 'destination_table',
              'default': '',
              'kind': 'string'
            }
          }
        }
      },
      'trends': {
        'places': {
          'bigquery': {
            'legacy': {
              'field': {
                'order': 5,
                'name': 'places_legacy',
                'default': False,
                'kind': 'boolean'
              }
            },
            'query': {
              'field': {
                'order': 4,
                'name': 'places_query',
                'default': '',
                'kind': 'string'
              }
            },
            'dataset': {
              'field': {
                'order': 3,
                'name': 'places_dataset',
                'default': '',
                'kind': 'string'
              }
            }
          },
          'single_cell': True
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('trends_places_to_bigquery_via_query', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
