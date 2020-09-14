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

SmartSheet Report To BigQuery

Move report data into a BigQuery table.

Specify <a href='https://smartsheet-platform.github.io/api-docs/'
target='_blank'>SmartSheet Report</a> token.
Locate the ID of a report by viewing its properties.
Provide a BigQuery dataset ( must exist ) and table to write the data into.
StarThinker will automatically map the correct schema.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'auth_write': 'service',  # Credentials used for writing data.
    'token': '',  # Retrieve from SmartSheet account settings.
    'report': '',  # Retrieve from report properties.
    'dataset': '',  # Existing BigQuery dataset.
    'table': '',  # Table to create from this report.
    'schema':
        '',  # Schema provided in JSON list format or leave empty to auto detect.
}

TASKS = [{
    'smartsheet': {
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
                'dataset': {
                    'field': {
                        'description': 'Existing BigQuery dataset.',
                        'name': 'dataset',
                        'default': '',
                        'kind': 'string',
                        'order': 4
                    }
                },
                'schema': {
                    'field': {
                        'description':
                            'Schema provided in JSON list format or leave '
                            'empty to auto detect.',
                        'name':
                            'schema',
                        'kind':
                            'json',
                        'order':
                            6
                    }
                },
                'table': {
                    'field': {
                        'description': 'Table to create from this report.',
                        'name': 'table',
                        'default': '',
                        'kind': 'string',
                        'order': 5
                    }
                }
            }
        },
        'report': {
            'field': {
                'description': 'Retrieve from report properties.',
                'name': 'report',
                'kind': 'string',
                'order': 3
            }
        },
        'token': {
            'field': {
                'description': 'Retrieve from SmartSheet account settings.',
                'name': 'token',
                'default': '',
                'kind': 'string',
                'order': 2
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('smartsheet_report_to_bigquery', {'tasks': TASKS},
                          INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
