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

Salesforce To BigQuery

Move query results into a BigQuery table.

  - Specify <a href='https://developer.salesforce.com/' target='_blank'>Salesforce</a> credentials.
  - Specify the query youd like to execute.
  - Specify a <a href='https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file' target='_blank'>SCHEMA</a> for that query ( optional ).

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'domain':'login.salesforce.com',  # Retrieve from a Salesforce Domain.
  'client':'',  # Retrieve from a Salesforce App.
  'secret':'',  # Retrieve from a Salesforce App.
  'username':'',  # Your Salesforce user email.
  'password':'',  # Your Salesforce login password.
  'query':'',  # The query to run in Salesforce.
  'auth_read':'user',  # Credentials used for reading data.
  'dataset':'',  # Existing BigQuery dataset.
  'table':'',  # Table to create from this report.
  'schema':'[]',  # Schema provided in JSON list format or empty list.
}

RECIPE = {
  'tasks':[
    {
      'salesforce':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'domain':{'field':{'name':'domain','kind':'string','default':'login.salesforce.com','description':'Retrieve from a Salesforce Domain.'}},
        'client':{'field':{'name':'client','kind':'string','default':'','description':'Retrieve from a Salesforce App.'}},
        'secret':{'field':{'name':'secret','kind':'string','default':'','description':'Retrieve from a Salesforce App.'}},
        'username':{'field':{'name':'username','kind':'email','default':'','description':'Your Salesforce user email.'}},
        'password':{'field':{'name':'password','kind':'password','default':'','description':'Your Salesforce login password.'}},
        'query':{'field':{'name':'query','kind':'string','default':'','description':'The query to run in Salesforce.'}},
        'out':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'Existing BigQuery dataset.'}},
            'table':{'field':{'name':'table','kind':'string','order':4,'default':'','description':'Table to create from this report.'}},
            'schema':{'field':{'name':'schema','kind':'json','order':5,'default':'[]','description':'Schema provided in JSON list format or empty list.'}}
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('salesforce_to_bigquery', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
