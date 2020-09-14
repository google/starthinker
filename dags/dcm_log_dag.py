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

CM Log Audit

Downloads Campaign manager logs and allows audits.

Wait for <b>BigQuery->UNDEFINED->UNDEFINED->CM_*</b> to be created.
Wait for <b>BigQuery->UNDEFINED->UNDEFINED->Barnacle_*</b> to be created, then
copy and connect the following data sources.
Join the <a hre='https://groups.google.com/d/forum/starthinker-assets'
target='_blank'>StarThinker Assets Group</a> to access the following assets
Copy <a
href='https://datastudio.google.com/open/1a6K-XdPUzCYRXZp1ZcmeOUOURc9wn2Jj'
target='_blank'>Barnacle Profile Advertiser Map</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1NEzrQWWnPjkD90iUwN-ASKbVBzoeBdoT'
target='_blank'>Barnacle Profile Campaign Map</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1v_GRaitwPaHHKUzfJZYNBhzotvZ-bR7Y'
target='_blank'>Barnacle Profile Site Map</a> and connect.
Copy <a
href='https://datastudio.google.com/open/14tWlh7yiqzxKJIppMFVOw2MoMtQV_ucE'
target='_blank'>Barnacle Profiles Connections</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1mavjxvHSEPfJq5aW4FYgCXsBCE5rthZG'
target='_blank'>Barnacle Report Delivery Profiles</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1Azk_Nul-auinf4NnDq8T9fDyiKkUWD7A'
target='_blank'>Barnacle Roles Duplicates</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1ogoofpKtqkLwcW9qC_Ju_JvJdIajsjNI'
target='_blank'>Barnacle Roles Not Used</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1xLgZPjOPDtmPyEqYMiMbWwMI8-WTslfj'
target='_blank'>Barnacle Site Contacts Profiles</a> and connect.
If reports checked, copy <a
href='https://datastudio.google.com/open/1-YGDiQPDnk0gD78_QOY5XdTXRlTrLeEq'
target='_blank'>Barnacle Profile Report Map</a> and connect.
Copy <a
href='https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT'
target='_blank'>Barnacle Report</a>.
When prompted choose the new data sources you just created.
Or give these intructions to the client.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'auth_write': 'service',  # Credentials used for writing data.
    'accounts': [],  # Comma separated CM account ids.
    'days': 7,  # Number of days to backfill the log, works on first run only.
    'recipe_project': '',  # Google BigQuery project to create tables in.
    'recipe_slug': '',  # Google BigQuery dataset to create tables in.
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
        'description': 'The dataset will hold log table, Create it exists.',
        'dataset': {
            'field': {
                'description': 'Name of Google BigQuery dataset to create.',
                'name': 'recipe_slug',
                'default': '',
                'kind': 'string',
                'order': 4
            }
        },
        'hour': [1]
    }
}, {
    'dcm_log': {
        'days': {
            'field': {
                'description':
                    'Number of days to backfill the log, works on first run only.',
                'name':
                    'days',
                'default':
                    7,
                'kind':
                    'integer',
                'order':
                    3
            }
        },
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 0
            }
        },
        'accounts': {
            'single_cell': True,
            'values': {
                'field': {
                    'description': 'Comma separated CM account ids.',
                    'name': 'accounts',
                    'default': [],
                    'kind': 'integer_list',
                    'order': 2
                }
            }
        },
        'description':
            'Will create tables with format CM_* to hold each endpoint via a '
            'call to the API list function. Exclude reports for its own task.',
        'out': {
            'auth': {
                'field': {
                    'description': 'Credentials used for writing data.',
                    'name': 'auth_write',
                    'default': 'service',
                    'kind': 'authentication',
                    'order': 1
                }
            },
            'project': {
                'field': {
                    'description':
                        'Google BigQuery project to create tables in.',
                    'name':
                        'recipe_project',
                    'default':
                        '',
                    'kind':
                        'string',
                    'order':
                        4
                }
            },
            'dataset': {
                'field': {
                    'description':
                        'Google BigQuery dataset to create tables in.',
                    'name':
                        'recipe_slug',
                    'default':
                        '',
                    'kind':
                        'string',
                    'order':
                        5
                }
            }
        },
        'hour': [2]
    }
}]

DAG_FACTORY = DAG_Factory('dcm_log', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
