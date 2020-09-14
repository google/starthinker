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

Entity Read Files

Import public and private <a
href='https://developers.google.com/bid-manager/guides/entity-read/format-v2'
target='_blank'>Entity Read Files</a> into a BigQuery dataset.<br/>CAUTION:
PARTNER ONLY, ADVERTISER FILTER IS NOT APPLIED.

Entity Read Files ONLY work at the partner level.
Advertiser filter is NOT APPLIED.
Specify one or more partners to be moved into the dataset.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'auth_write': 'service',  # Credentials used for writing data.
    'partners': '[]',  # Comma sparated list of DV360 partners.
    'dataset': '',  # BigQuery dataset to write tables for each entity.
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
                'description':
                    'BigQuery dataset to write tables for each entity.',
                'name':
                    'dataset',
                'default':
                    '',
                'kind':
                    'string',
                'order':
                    3
            }
        }
    }
}, {
    'entity': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'prefix': 'Entity',
        'out': {
            'bigquery': {
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
                        'description':
                            'BigQuery dataset to write tables for each entity.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            3
                    }
                }
            }
        },
        'entities': [
            'Campaign', 'LineItem', 'Creative', 'UserList', 'Partner',
            'Advertiser', 'InsertionOrder', 'Pixel', 'InventorySource',
            'CustomAffinity', 'UniversalChannel', 'UniversalSite',
            'SupportedExchange', 'DataPartner', 'GeoLocation', 'Language',
            'DeviceCriteria', 'Browser', 'Isp'
        ],
        'partners': {
            'single_cell': True,
            'values': {
                'field': {
                    'description': 'Comma sparated list of DV360 partners.',
                    'name': 'partners',
                    'default': '[]',
                    'kind': 'integer_list',
                    'order': 1
                }
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('entity', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
