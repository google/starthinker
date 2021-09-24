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

SA360 Report

Move SA360 report to BigQuery.

  - Fill in the report definition and destination table.
  - Wait for <b>BigQuery->->-></b> to be created.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_sa':'service',  # Credentials used for writing data.
  'auth_bq':'service',  # Authorization used for writing data.
  'dataset':'',  # Existing BigQuery dataset.
  'table':'',  # Table to create from this report.
  'report':{},  # Body part of report request API call.
  'is_incremental_load':False,  # Clear data in destination table during this report's time period, then append report data to destination table.
}

RECIPE = {
  'tasks':[
    {
      'sa':{
        'description':'Create a dataset for bigquery tables.',
        'auth':{'field':{'name':'auth_sa','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'body':{'field':{'name':'report','kind':'json','order':4,'default':{},'description':'Body part of report request API call.'}},
        'out':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'dataset','kind':'string','order':2,'default':'','description':'Existing BigQuery dataset.'}},
            'table':{'field':{'name':'table','kind':'string','order':3,'default':'','description':'Table to create from this report.'}},
            'is_incremental_load':{'field':{'name':'is_incremental_load','kind':'boolean','order':4,'default':False,'description':"Clear data in destination table during this report's time period, then append report data to destination table."}},
            'header':True
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('sa_report', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
