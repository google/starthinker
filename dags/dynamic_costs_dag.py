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

Dynamic Costs Reporting

Calculate DV360 cost at the dynamic creative combination level.

  - Add a sheet URL. This is where you will enter advertiser and campaign level details.
  - Specify the CM network ID.
  - Click run now once, and a tab called <strong>Dynamic Costs</strong> will be added to the sheet with instructions.
  - Follow the instructions on the sheet; this will be your configuration.
  - StarThinker will create two or three (depending on the case) reports in CM named <strong>Dynamic Costs - ...</strong>.
  - Wait for <b>BigQuery->->->Dynamic_Costs_Analysis</b> to be created or click Run Now.
  - Copy <a href='https://datastudio.google.com/open/1vBvBEiMbqCbBuJTsBGpeg8vCLtg6ztqA' target='_blank'>Dynamic Costs Sample Data ( Copy From This )</a>.
  - Click Edit Connection, and Change to <b>BigQuery->->->Dynamic_Costs_Analysis</b>.
  - Copy <a href='https://datastudio.google.com/open/1xulBAdx95SnvjnUzFP6r14lhkvvVbsP8' target='_blank'>Dynamic Costs Sample Report ( Copy From This )</a>.
  - When prompted, choose the new data source you just created.
  - Edit the table to include or exclude columns as desired.
  - Or, give the dashboard connection intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'dcm_account':'',
  'auth_read':'user',  # Credentials used for reading data.
  'configuration_sheet_url':'',
  'auth_write':'service',  # Credentials used for writing data.
  'bigquery_dataset':'dynamic_costs',
}

RECIPE = {
  'tasks':[
    {
      'dynamic_costs':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'account':{'field':{'name':'dcm_account','kind':'string','order':0,'default':''}},
        'sheet':{
          'template':{
            'url':'https://docs.google.com/spreadsheets/d/19J-Hjln2wd1E0aeG3JDgKQN9TVGRLWxIEUQSmmQetJc/edit?usp=sharing',
            'tab':'Dynamic Costs',
            'range':'A1'
          },
          'url':{'field':{'name':'configuration_sheet_url','kind':'string','order':1,'default':''}},
          'tab':'Dynamic Costs',
          'range':'A2:B'
        },
        'out':{
          'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
          'dataset':{'field':{'name':'bigquery_dataset','kind':'string','order':2,'default':'dynamic_costs'}}
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dynamic_costs', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
