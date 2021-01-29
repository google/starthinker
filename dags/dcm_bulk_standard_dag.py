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

CM Standard Bulk

Aggregate multiple standard CM reports into one BigQuery or Sheet.

See API docs for <a
href='https://developers.google.com/doubleclick-advertisers/v3.2/dimensions'
target='_blank'>Metrics</a>.
CM report name format '[Report Name] [Account ID] ( StarThinker )'.
Specify either bucket and path or dataset and table.
Schema is pulled from the official CM specification.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'accounts': '',
    'name': '',
    'range': 'LAST_7_DAYS',
    'dcm_dimensions': [
        'date', 'platformType', 'creativeType', 'state', 'dmaRegion'
    ],
    'dcm_metrics': ['impressions'],
    'dataset': '',
    'table': '',
    'bucket': '',
    'path': 'CM_Report',
    'delete': False,
    'datastudio': True,
}

TASKS = [{
    'dcm_bulk': {
        'auth': 'user',
        'accounts': {
            'field': {
                'name': 'accounts',
                'kind': 'integer_list',
                'order': 1,
                'default': ''
            }
        },
        'name': {
            'field': {
                'name': 'name',
                'kind': 'string',
                'order': 2,
                'default': ''
            }
        },
        'report': {
            'type': 'STANDARD',
            'timeout': 0,
            'relativeDateRange': {
                'field': {
                    'name':
                        'range',
                    'kind':
                        'choice',
                    'order':
                        3,
                    'default':
                        'LAST_7_DAYS',
                    'choices': [
                        'LAST_24_MONTHS', 'LAST_30_DAYS', 'LAST_365_DAYS',
                        'LAST_7_DAYS', 'LAST_90_DAYS', 'MONTH_TO_DATE',
                        'PREVIOUS_MONTH', 'PREVIOUS_QUARTER', 'PREVIOUS_WEEK',
                        'PREVIOUS_YEAR', 'QUARTER_TO_DATE', 'TODAY',
                        'WEEK_TO_DATE', 'YEAR_TO_DATE', 'YESTERDAY'
                    ]
                }
            },
            'dimensions': {
                'field': {
                    'name':
                        'dcm_dimensions',
                    'kind':
                        'string_list',
                    'order':
                        4,
                    'default': [
                        'date', 'platformType', 'creativeType', 'state',
                        'dmaRegion'
                    ]
                }
            },
            'metrics': {
                'field': {
                    'name': 'dcm_metrics',
                    'kind': 'string_list',
                    'order': 5,
                    'default': ['impressions']
                }
            }
        },
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'name': 'dataset',
                        'kind': 'string',
                        'order': 5,
                        'default': ''
                    }
                },
                'table': {
                    'field': {
                        'name': 'table',
                        'kind': 'string',
                        'order': 6,
                        'default': ''
                    }
                }
            },
            'storage': {
                'bucket': {
                    'field': {
                        'name': 'bucket',
                        'kind': 'string',
                        'order': 7,
                        'default': ''
                    }
                },
                'path': {
                    'field': {
                        'name': 'path',
                        'kind': 'string',
                        'order': 8,
                        'default': 'CM_Report'
                    }
                }
            }
        },
        'delete': {
            'field': {
                'name': 'delete',
                'kind': 'boolean',
                'order': 10,
                'default': False
            }
        },
        'datastudio': {
            'field': {
                'name': 'datastudio',
                'kind': 'boolean',
                'order': 11,
                'default': True
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dcm_bulk_standard', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
