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

SDF Download

Download SDF reports into a BigQuery table.

Select your filter types and the filter ideas.
Enter the <a href='https://developers.google.com/bid-manager/v1.1/sdf/download' target='_blank'>file types</a> using commas.
SDF_ will be prefixed to all tables and date appended to daily tables.
File types take the following format: FILE_TYPE_CAMPAIGN, FILE_TYPE_AD_GROUP,...

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'partner_id': '',  # The sdf file types.
  'auth_write': 'service',  # Credentials used for writing data.
  'file_types': [],  # The sdf file types.
  'filter_type': '',  # The filter type for the filter ids.
  'filter_ids': [],  # Comma separated list of filter ids for the request.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'version': '5',  # The sdf version to be returned.
  'table_suffix': '',  # Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)
  'time_partitioned_table': False,  # Is the end table a time partitioned
  'create_single_day_table': False,  # Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.
}

TASKS = [
  {
    'dataset': {
      'auth': {
        'field': {
          'description': 'Credentials used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'dataset': {
        'field': {
          'description': 'Dataset to be written to in BigQuery.',
          'kind': 'string',
          'name': 'dataset',
          'order': 6,
          'default': ''
        }
      }
    }
  },
  {
    'sdf': {
      'file_types': {
        'field': {
          'description': 'The sdf file types.',
          'kind': 'string_list',
          'name': 'file_types',
          'order': 2,
          'default': [
          ]
        }
      },
      'table_suffix': {
        'field': {
          'description': 'Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)',
          'kind': 'string',
          'name': 'table_suffix',
          'order': 6,
          'default': ''
        }
      },
      'dataset': {
        'field': {
          'description': 'Dataset to be written to in BigQuery.',
          'kind': 'string',
          'name': 'dataset',
          'order': 6,
          'default': ''
        }
      },
      'filter_type': {
        'field': {
          'choices': [
            'FILTER_TYPE_ADVERTISER_ID',
            'FILTER_TYPE_CAMPAIGN_ID',
            'FILTER_TYPE_INSERTION_ORDER_ID',
            'FILTER_TYPE_MEDIA_PRODUCT_ID',
            'FILTER_TYPE_LINE_ITEM_ID'
          ],
          'description': 'The filter type for the filter ids.',
          'name': 'filter_type',
          'kind': 'choice',
          'order': 3,
          'default': ''
        }
      },
      'partner_id': {
        'field': {
          'order': 1,
          'name': 'partner_id',
          'description': 'The sdf file types.',
          'kind': 'integer'
        }
      },
      'version': {
        'field': {
          'choices': [
            'SDF_VERSION_5',
            'SDF_VERSION_5_1'
          ],
          'description': 'The sdf version to be returned.',
          'name': 'version',
          'kind': 'choice',
          'order': 6,
          'default': '5'
        }
      },
      'auth': 'user',
      'create_single_day_table': {
        'field': {
          'description': 'Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.',
          'kind': 'boolean',
          'name': 'create_single_day_table',
          'order': 8,
          'default': False
        }
      },
      'read': {
        'filter_ids': {
          'values': {
            'field': {
              'description': 'Comma separated list of filter ids for the request.',
              'kind': 'integer_list',
              'name': 'filter_ids',
              'order': 4,
              'default': [
              ]
            }
          },
          'single_cell': True
        }
      },
      'time_partitioned_table': {
        'field': {
          'description': 'Is the end table a time partitioned',
          'kind': 'boolean',
          'name': 'time_partitioned_table',
          'order': 7,
          'default': False
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('sdf_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
