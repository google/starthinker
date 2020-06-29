###########################################################################
# 
#  Copyright 2019 Google Inc.
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
  'auth_write': 'service',  # Credentials used for writing data.
  'partner_id': '',  # The sdf file types.
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
          'name': 'auth_write',
          'kind': 'authentication',
          'order': 1,
          'default': 'service',
          'description': 'Credentials used for writing data.'
        }
      },
      'dataset': {
        'field': {
          'name': 'dataset',
          'kind': 'string',
          'order': 6,
          'default': '',
          'description': 'Dataset to be written to in BigQuery.'
        }
      }
    }
  },
  {
    'sdf': {
      'auth': 'user',
      'version': {
        'field': {
          'name': 'version',
          'kind': 'choice',
          'order': 6,
          'default': '5',
          'description': 'The sdf version to be returned.',
          'choices': [
            'SDF_VERSION_5',
            'SDF_VERSION_5_1'
          ]
        }
      },
      'partner_id': {
        'field': {
          'name': 'partner_id',
          'kind': 'integer',
          'order': 1,
          'description': 'The sdf file types.'
        }
      },
      'file_types': {
        'field': {
          'name': 'file_types',
          'kind': 'string_list',
          'order': 2,
          'default': [
          ],
          'description': 'The sdf file types.'
        }
      },
      'filter_type': {
        'field': {
          'name': 'filter_type',
          'kind': 'choice',
          'order': 3,
          'default': '',
          'description': 'The filter type for the filter ids.',
          'choices': [
            'FILTER_TYPE_ADVERTISER_ID',
            'FILTER_TYPE_CAMPAIGN_ID',
            'FILTER_TYPE_INSERTION_ORDER_ID',
            'FILTER_TYPE_MEDIA_PRODUCT_ID',
            'FILTER_TYPE_LINE_ITEM_ID'
          ]
        }
      },
      'read': {
        'filter_ids': {
          'single_cell': True,
          'values': {
            'field': {
              'name': 'filter_ids',
              'kind': 'integer_list',
              'order': 4,
              'default': [
              ],
              'description': 'Comma separated list of filter ids for the request.'
            }
          }
        }
      },
      'time_partitioned_table': {
        'field': {
          'name': 'time_partitioned_table',
          'kind': 'boolean',
          'order': 7,
          'default': False,
          'description': 'Is the end table a time partitioned'
        }
      },
      'create_single_day_table': {
        'field': {
          'name': 'create_single_day_table',
          'kind': 'boolean',
          'order': 8,
          'default': False,
          'description': 'Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.'
        }
      },
      'dataset': {
        'field': {
          'name': 'dataset',
          'kind': 'string',
          'order': 6,
          'default': '',
          'description': 'Dataset to be written to in BigQuery.'
        }
      },
      'table_suffix': {
        'field': {
          'name': 'table_suffix',
          'kind': 'string',
          'order': 6,
          'default': '',
          'description': 'Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)'
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
