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

Dynamic Costs Reporting

Calculate DV360 cost at the dynamic creative combination level.

Add a sheet URL. This is where you will enter advertiser and campaign level
details.
Specify the CM network ID.
Click run now once, and a tab called <strong>Dynamic Costs</strong> will be
added to the sheet with instructions.
Follow the instructions on the sheet; this will be your configuration.
StarThinker will create two or three (depending on the case) reports in CM named
<strong>Dynamic Costs - ...</strong>.
Wait for <b>BigQuery->UNDEFINED->UNDEFINED->Dynamic_Costs_Analysis</b> to be
created or click Run Now.
Copy <a
href='https://datastudio.google.com/open/1vBvBEiMbqCbBuJTsBGpeg8vCLtg6ztqA'
target='_blank'>Dynamic Costs Sample Data ( Copy From This )</a>.
Click Edit Connection, and Change to
<b>BigQuery->UNDEFINED->UNDEFINED->Dynamic_Costs_Analysis</b>.
Copy <a
href='https://datastudio.google.com/open/1xulBAdx95SnvjnUzFP6r14lhkvvVbsP8'
target='_blank'>Dynamic Costs Sample Report ( Copy From This )</a>.
When prompted, choose the new data source you just created.
Edit the table to include or exclude columns as desired.
Or, give the dashboard connection intructions to the client.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'dcm_account': '',
    'auth_read': 'user',  # Credentials used for reading data.
    'configuration_sheet_url': '',
    'auth_write': 'service',  # Credentials used for writing data.
    'bigquery_dataset': 'dynamic_costs',
}

TASKS = [{
    'dynamic_costs': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
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
            'dataset': {
                'field': {
                    'name': 'bigquery_dataset',
                    'default': 'dynamic_costs',
                    'kind': 'string',
                    'order': 2
                }
            }
        },
        'sheet': {
            'url': {
                'field': {
                    'name': 'configuration_sheet_url',
                    'default': '',
                    'kind': 'string',
                    'order': 1
                }
            },
            'template': {
                'url':
                    'https://docs.google.com/spreadsheets/d/19J-Hjln2wd1E0aeG3JDgKQN9TVGRLWxIEUQSmmQetJc/edit?usp=sharing',
                'tab':
                    'Dynamic Costs',
                'range':
                    'A1'
            },
            'tab': 'Dynamic Costs',
            'range': 'A2:B'
        },
        'account': {
            'field': {
                'name': 'dcm_account',
                'default': '',
                'kind': 'string',
                'order': 0
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('dynamic_costs', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
