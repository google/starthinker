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

CM360 To DV360 Bulk Creator

Allows bulk creating DV360 Insertion Orders and Line Items from CM360.

  - Select <b>Load Partners</b>, then click <b>Save + Run</b>, then a sheet called DV Editor  will be created.
  - In the <b>Partners</b> sheet tab, fill in <i>Filter</i> column then select <b>Load Advertisers</b>, click <b>Save + Run</b>.
  - In the <b>Advertisers</b> sheet tab, fill in <i>Filter</i> column then select <b>Load Campaigns</b>, click <b>Save + Run</b>.
  - In the <b>Campaigns</b> sheet tab, fill in <i>Filter</i> column, optional.
  - Then select <b>Load Insertion Orders And Line Items</b>, click <b>Save + Run</b>.
  - To update values, make changes on all <i>Edit</i> columns.
  - Select <i>Preview</i>, then <b>Save + Run</b>.
  - Check the <b>Audit</b> and <b>Preview</b> tabs to verify commit.
  - To commit changes, select <i>Update</i>, then <b>Save + Run</b>.
  - Check the <b>Success</b> and <b>Error</b> tabs.
  - Update can be run multiple times.
  - Update ONLY changes fields that do not match their original value.
  - Insert operates only on Edit columns, ignores orignal value columns.
  - Carefull when using drag to copy rows, values are incremented automatically.
  - Modify audit logic by visting BigQuery and changing the views.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_dv':'user',  # Credentials used for dv.
  'auth_cm':'user',  # Credentials used for dv.
  'auth_sheet':'user',  # Credentials used for sheet.
  'auth_bigquery':'service',  # Credentials used for bigquery.
  'recipe_name':'',  # Name of Google Sheet to create.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
  'command':'Load',  # Action to take.
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
      'dataset':{
        '__comment__':'Ensure dataset exists.',
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','prefix':'CM_To_DV_','kind':'string','order':2,'default':'','description':'Name of Google BigQuery dataset to create.'}}
      }
    },
    {
      'drive':{
        '__comment__':'Copy the default template to sheet with the recipe name',
        'auth':{'field':{'name':'auth_sheet','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'copy':{
          'source':'https://docs.google.com/spreadsheets/d/1XjEHq-nEFMW8RVmCNJ-TVGvVcVBEADzjbvhmAvF04iQ/edit#gid=594912061',
          'destination':{'field':{'name':'recipe_name','prefix':'CM To DV ','kind':'string','order':3,'default':'','description':'Name of Google Sheet to create.'}}
        }
      }
    },
    {
      'cm_to_dv':{
        '__comment':'Depending on users choice, execute a different part of the solution.',
        'auth_dv':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials used for dv.'}},
        'auth_cm':{'field':{'name':'auth_cm','kind':'authentication','order':2,'default':'user','description':'Credentials used for dv.'}},
        'auth_sheets':{'field':{'name':'auth_sheet','kind':'authentication','order':3,'default':'user','description':'Credentials used for sheet.'}},
        'auth_bigquery':{'field':{'name':'auth_bigquery','kind':'authentication','order':4,'default':'service','description':'Credentials used for bigquery.'}},
        'sheet':{'field':{'name':'recipe_name','prefix':'CM To DV ','kind':'string','order':5,'default':'','description':'Name of Google Sheet to create.'}},
        'dataset':{'field':{'name':'recipe_slug','prefix':'CM_To_DV_','kind':'string','order':6,'default':'','description':'Name of Google BigQuery dataset to create.'}},
        'command':{'field':{'name':'command','kind':'choice','choices':['Clear','Load','Preview','Insert'],'order':6,'default':'Load','description':'Action to take.'}}
      }
    }
  ]
}

dag_maker = DAG_Factory('cm360_to_dv360', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
