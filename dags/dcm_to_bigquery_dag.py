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

CM To BigQuery

Move existing CM report into a BigQuery table.

Specify an account id.
Specify either report name or report id to move a report.
The most recent valid file will overwrite the table.
Schema is pulled from the official CM specification.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'auth_write': 'service',  # Credentials used for writing data.
    'account': '',  # CM network id.
    'report_id': '',  # CM report id, empty if using name .
    'report_name': '',  # CM report name, empty if using id instead.
    'dataset': '',  # Dataset to be written to in BigQuery.
    'table': '',  # Table to be written to in BigQuery.
    'is_incremental_load':
        False,  # Clear data in destination table during this report's time period, then append report data to existing table.
}

TASKS = [{
    'dcm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 0
            }
        },
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
                'is_incremental_load': {
                    'field': {
                        'description':
                            "Clear data in destination table during this "
                            "report's time period, then append report data to "
                            "existing table.",
                        'name':
                            'is_incremental_load',
                        'default':
                            False,
                        'kind':
                            'boolean',
                        'order':
                            7
                    }
                },
                'dataset': {
                    'field': {
                        'description': 'Dataset to be written to in BigQuery.',
                        'name': 'dataset',
                        'default': '',
                        'kind': 'string',
                        'order': 5
                    }
                },
                'table': {
                    'field': {
                        'description': 'Table to be written to in BigQuery.',
                        'name': 'table',
                        'default': '',
                        'kind': 'string',
                        'order': 6
                    }
                }
            }
        },
        'report': {
            'report_id': {
                'field': {
                    'description': 'CM report id, empty if using name .',
                    'name': 'report_id',
                    'default': '',
                    'kind': 'integer',
                    'order': 3
                }
            },
            'name': {
                'field': {
                    'description': 'CM report name, empty if using id instead.',
                    'name': 'report_name',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            },
            'account': {
                'field': {
                    'description': 'CM network id.',
                    'name': 'account',
                    'default': '',
                    'kind': 'integer',
                    'order': 2
                }
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dcm_to_bigquery', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
