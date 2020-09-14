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

Email Fetch

Import emailed CM report, Dv360 report, csv, or excel into a BigQuery table.

The person executing this recipe must be the recipient of the email.
Give a regular expression to match the email subject, link or attachment.
The data downloaded will overwrite the table specified.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'email_from': '',  # Must match from field.
    'email_to': '',  # Must match to field.
    'subject': '',  # Regular expression to match subject.
    'link': '',  # Regular expression to match email.
    'attachment': '',  # Regular expression to match atttachment.
    'dataset': '',  # Existing dataset in BigQuery.
    'table': '',  # Name of table to be written to.
    'dbm_schema': '[]',  # Schema provided in JSON list format or empty list.
    'is_incremental_load':
        False,  # Append report data to table based on date column, de-duplicates.
}

TASKS = [{
    'email': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'read': {
            'attachment': {
                'field': {
                    'description': 'Regular expression to match atttachment.',
                    'name': 'attachment',
                    'default': '',
                    'kind': 'string',
                    'order': 5
                }
            },
            'link': {
                'field': {
                    'description': 'Regular expression to match email.',
                    'name': 'link',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            },
            'subject': {
                'field': {
                    'description': 'Regular expression to match subject.',
                    'name': 'subject',
                    'default': '',
                    'kind': 'string',
                    'order': 3
                }
            },
            'to': {
                'field': {
                    'description': 'Must match to field.',
                    'name': 'email_to',
                    'default': '',
                    'kind': 'string',
                    'order': 2
                }
            },
            'from': {
                'field': {
                    'description': 'Must match from field.',
                    'name': 'email_from',
                    'default': '',
                    'kind': 'string',
                    'order': 1
                }
            }
        },
        'out': {
            'bigquery': {
                'is_incremental_load': {
                    'field': {
                        'description':
                            'Append report data to table based on date column,'
                            ' de-duplicates.',
                        'name':
                            'is_incremental_load',
                        'default':
                            False,
                        'kind':
                            'boolean',
                        'order':
                            9
                    }
                },
                'dataset': {
                    'field': {
                        'description': 'Existing dataset in BigQuery.',
                        'name': 'dataset',
                        'default': '',
                        'kind': 'string',
                        'order': 6
                    }
                },
                'schema': {
                    'field': {
                        'description':
                            'Schema provided in JSON list format or empty list.',
                        'name':
                            'dbm_schema',
                        'default':
                            '[]',
                        'kind':
                            'json',
                        'order':
                            8
                    }
                },
                'table': {
                    'field': {
                        'description': 'Name of table to be written to.',
                        'name': 'table',
                        'default': '',
                        'kind': 'string',
                        'order': 7
                    }
                }
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('email_to_bigquery', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
