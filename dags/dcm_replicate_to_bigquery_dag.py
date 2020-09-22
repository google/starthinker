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

CM Report Replicate

Replicate a report across multiple networks and advertisers.

Provide the name or ID of an existing report.
Run the recipe once to generate the input sheet called CM Replicate For UNDEFINED.
Enter network and advertiser ids to replicate the report.
Data will be written to BigQuery &gt; UNDEFINED &gt; UNDEFINED &gt; [REPORT NAME]_All

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_name': '',  # Sheet to read ids from.
  'account': '',  # CM network id.
  'recipe_slug': '',
  'report_id': '',  # CM template report id, for template
  'report_name': '',  # CM template report name, empty if using id instead.
  'delete': False,  # Use only to reset the reports if setup changes.
  'Aggregate': False,  # Append report data to existing table, requires Date column.
}

TASKS = [
  {
    'drive': {
      'copy': {
        'destination': {
          'field': {
            'description': 'Name of document to deploy to.',
            'prefix': 'CM Replicate For ',
            'order': 1,
            'kind': 'string',
            'name': 'recipe_name',
            'default': ''
          }
        },
        'source': 'https://docs.google.com/spreadsheets/d/1Su3t2YUWV_GG9RD63Wa3GNANmQZswTHstFY6aDPm6qE/'
      },
      'auth': 'user'
    }
  },
  {
    'dataset': {
      'dataset': {
        'field': {
          'order': 2,
          'kind': 'string',
          'name': 'recipe_slug',
          'description': 'Name of Google BigQuery dataset to create.',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Credentials used for writing data.',
          'default': 'service'
        }
      }
    }
  },
  {
    'dcm_replicate': {
      'report': {
        'id': {
          'field': {
            'order': 4,
            'kind': 'integer',
            'name': 'report_id',
            'description': 'CM template report id, for template',
            'default': ''
          }
        },
        'name': {
          'field': {
            'order': 5,
            'kind': 'string',
            'name': 'report_name',
            'description': 'CM template report name, empty if using id instead.',
            'default': ''
          }
        },
        'delete': {
          'field': {
            'order': 6,
            'kind': 'boolean',
            'name': 'delete',
            'description': 'Use only to reset the reports if setup changes.',
            'default': False
          }
        },
        'account': {
          'field': {
            'order': 3,
            'kind': 'integer',
            'name': 'account',
            'description': 'CM network id.',
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'in': {
        'sheet': {
          'field': {
            'description': 'Sheet to read ids from.',
            'default': '',
            'order': 1,
            'kind': 'string',
            'name': 'recipe_name',
            'prefix': 'CM Replicate For '
          }
        },
        'tab': 'Accounts'
      },
      'out': {
        'bigquery': {
          'is_incremental_load': {
            'field': {
              'order': 7,
              'kind': 'boolean',
              'name': 'Aggregate',
              'description': 'Append report data to existing table, requires Date column.',
              'default': False
            }
          },
          'dataset': {
            'field': {
              'order': 4,
              'kind': 'string',
              'name': 'recipe_slug',
              'default': ''
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_replicate_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
