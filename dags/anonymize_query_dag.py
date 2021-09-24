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
#
#  This code generated (see starthinker/scripts for possible source):
#    - Command: "python starthinker_ui/manage.py airflow"
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

BigQuery Anonymize Query

Runs a query and anynonamizes all rows.  Used to create sample table for dashboards.

  - Ensure you have user access to both datasets.
  - Provide the source project, dataset and query.
  - Provide the destination project, dataset, and table.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'service',  # Credentials used.
  'from_project':'',  # Original project to read from.
  'from_dataset':'',  # Original dataset to read from.
  'from_query':'',  # Query to read data.
  'to_project':None,  # Anonymous data will be writen to.
  'to_dataset':'',  # Anonymous data will be writen to.
  'to_table':'',  # Anonymous data will be writen to.
}

RECIPE = {
  'setup':{
    'day':[
    ],
    'hour':[
    ]
  },
  'tasks':[
    {
      'anonymize':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'service','description':'Credentials used.'}},
        'bigquery':{
          'from':{
            'project':{'field':{'name':'from_project','kind':'string','order':1,'description':'Original project to read from.'}},
            'dataset':{'field':{'name':'from_dataset','kind':'string','order':2,'description':'Original dataset to read from.'}},
            'query':{'field':{'name':'from_query','kind':'string','order':3,'description':'Query to read data.'}}
          },
          'to':{
            'project':{'field':{'name':'to_project','kind':'string','order':4,'default':None,'description':'Anonymous data will be writen to.'}},
            'dataset':{'field':{'name':'to_dataset','kind':'string','order':5,'description':'Anonymous data will be writen to.'}},
            'table':{'field':{'name':'to_table','kind':'string','order':6,'description':'Anonymous data will be writen to.'}}
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('anonymize_query', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
