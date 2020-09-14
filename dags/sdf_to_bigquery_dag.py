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
"""--------------------------------------------------------------

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
Enter the <a href='https://developers.google.com/bid-manager/v1.1/sdf/download'
target='_blank'>file types</a> using commas.
SDF_ will be prefixed to all tables and date appended to daily tables.
File types take the following format: FILE_TYPE_CAMPAIGN, FILE_TYPE_AD_GROUP,...

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'partner_id': '',  # The sdf file types.
    'auth_write': 'service',  # Credentials used for writing data.
    'file_types': [],  # The sdf file types.
    'filter_type': '',  # The filter type for the filter ids.
    'filter_ids': [],  # Comma separated list of filter ids for the request.
    'dataset': '',  # Dataset to be written to in BigQuery.
    'table_suffix':
        '',  # Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)
    'version': '5',  # The sdf version to be returned.
    'time_partitioned_table': False,  # Is the end table a time partitioned
    'create_single_day_table':
        False,  # Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.
}

TASKS = [{
    'dataset': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'dataset': {
            'field': {
                'description': 'Dataset to be written to in BigQuery.',
                'name': 'dataset',
                'default': '',
                'kind': 'string',
                'order': 6
            }
        }
    }
}, {
    'sdf': {
        'time_partitioned_table': {
            'field': {
                'description': 'Is the end table a time partitioned',
                'name': 'time_partitioned_table',
                'default': False,
                'kind': 'boolean',
                'order': 7
            }
        },
        'create_single_day_table': {
            'field': {
                'description':
                    'Would you like a separate table for each day? This will '
                    'result in an extra table each day and the end table with '
                    'the most up to date SDF.',
                'name':
                    'create_single_day_table',
                'default':
                    False,
                'kind':
                    'boolean',
                'order':
                    8
            }
        },
        'version': {
            'field': {
                'order': 6,
                'name': 'version',
                'default': '5',
                'description': 'The sdf version to be returned.',
                'choices': ['SDF_VERSION_5', 'SDF_VERSION_5_1'],
                'kind': 'choice'
            }
        },
        'read': {
            'filter_ids': {
                'single_cell': True,
                'values': {
                    'field': {
                        'description':
                            'Comma separated list of filter ids for the request.',
                        'name':
                            'filter_ids',
                        'default': [],
                        'kind':
                            'integer_list',
                        'order':
                            4
                    }
                }
            }
        },
        'auth': 'user',
        'file_types': {
            'field': {
                'description': 'The sdf file types.',
                'name': 'file_types',
                'default': [],
                'kind': 'string_list',
                'order': 2
            }
        },
        'table_suffix': {
            'field': {
                'description':
                    'Optional: Suffix string to put at the end of the table '
                    'name (Must contain alphanumeric or underscores)',
                'name':
                    'table_suffix',
                'default':
                    '',
                'kind':
                    'string',
                'order':
                    6
            }
        },
        'filter_type': {
            'field': {
                'order': 3,
                'name': 'filter_type',
                'default': '',
                'description': 'The filter type for the filter ids.',
                'choices': [
                    'FILTER_TYPE_ADVERTISER_ID', 'FILTER_TYPE_CAMPAIGN_ID',
                    'FILTER_TYPE_INSERTION_ORDER_ID',
                    'FILTER_TYPE_MEDIA_PRODUCT_ID', 'FILTER_TYPE_LINE_ITEM_ID'
                ],
                'kind': 'choice'
            }
        },
        'dataset': {
            'field': {
                'description': 'Dataset to be written to in BigQuery.',
                'name': 'dataset',
                'default': '',
                'kind': 'string',
                'order': 6
            }
        },
        'partner_id': {
            'field': {
                'description': 'The sdf file types.',
                'name': 'partner_id',
                'kind': 'integer',
                'order': 1
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('sdf_to_bigquery', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
