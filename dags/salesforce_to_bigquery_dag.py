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

Salesforce To BigQuery

Move query results into a BigQuery table.

Specify <a href='https://developer.salesforce.com/'
target='_blank'>Salesforce</a> credentials.
Specify the query youd like to execute.
Specify a <a
href='https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file'
target='_blank'>SCHEMA</a> for that query ( optional ).

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'secret': '',  # Retrieve from a Salesforce App.
    'username': '',  # Your Salesforce user email.
    'client': '',  # Retrieve from a Salesforce App.
    'query': '',  # The query to run in Salesforce.
    'domain': 'login.salesforce.com',  # Retrieve from a Salesforce Domain.
    'password': '',  # Your Salesforce login password.
    'auth_read': 'user',  # Credentials used for reading data.
    'dataset': '',  # Existing BigQuery dataset.
    'table': '',  # Table to create from this report.
    'schema': '[]',  # Schema provided in JSON list format or empty list.
}

TASKS = [{
    'salesforce': {
        'secret': {
            'field': {
                'description': 'Retrieve from a Salesforce App.',
                'name': 'secret',
                'default': '',
                'kind': 'string'
            }
        },
        'query': {
            'field': {
                'description': 'The query to run in Salesforce.',
                'name': 'query',
                'default': '',
                'kind': 'string'
            }
        },
        'username': {
            'field': {
                'description': 'Your Salesforce user email.',
                'name': 'username',
                'default': '',
                'kind': 'email'
            }
        },
        'client': {
            'field': {
                'description': 'Retrieve from a Salesforce App.',
                'name': 'client',
                'default': '',
                'kind': 'string'
            }
        },
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'domain': {
            'field': {
                'description': 'Retrieve from a Salesforce Domain.',
                'name': 'domain',
                'default': 'login.salesforce.com',
                'kind': 'string'
            }
        },
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'description': 'Existing BigQuery dataset.',
                        'name': 'dataset',
                        'default': '',
                        'kind': 'string',
                        'order': 3
                    }
                },
                'schema': {
                    'field': {
                        'description':
                            'Schema provided in JSON list format or empty list.',
                        'name':
                            'schema',
                        'default':
                            '[]',
                        'kind':
                            'json',
                        'order':
                            5
                    }
                },
                'table': {
                    'field': {
                        'description': 'Table to create from this report.',
                        'name': 'table',
                        'default': '',
                        'kind': 'string',
                        'order': 4
                    }
                }
            }
        },
        'password': {
            'field': {
                'description': 'Your Salesforce login password.',
                'name': 'password',
                'default': '',
                'kind': 'password'
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('salesforce_to_bigquery', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
