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

DV360 Bulk Targeting Editor

Allows bulk targeting DV360 through Sheets and BigQuery.

  - Select <b>Load</b>, click <b>Save + Run</b>, a sheet called <b> DV Targeter</b> will be created.
  - In the <b>Partners</b> sheet tab, fill in <i>Filter</i> column then select <b>Load</b>, click <b>Save + Run</b>.
  - In the <b>Advertisers</b> sheet tab, fill in <i>Filter</i> column. then select <b>Load</b>, click <b>Save + Run</b>.
  - Check the First And Third Party option to load audiences, which may be slow.  If not loaded, user will enter audience ids into the sheet manually.
  - On the <b>Line Items</b> sheet tab, the <i>Filter</i> is used only to limit drop down choices in the rest of the tool.
  - Optionally edit or filter the <i>Targeting Options</i> or <i>Inventory Sources</i> sheets to limit choices.
  - Make targeting updates, fill in changes on all tabs with colored fields (RED FIELDS ARE NOT IMPLEMENTED, IGNORE).
  - Select <i>Preview</i>, click <b>Save + Run</b> then check the <b>Preview</b> tabs.
  - Select <b>Update</b>, click <b>Save + Run</b> then check the <b>Success</b> and <b>Error</b> tabs.
  - Load and Update can be run multiple times.
  - If an update fails, all parts of the update failed, break it up into multiple updates.
  - To refresh the Partner, Advertiser, or Line Item list, remove the filters and run load.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_dv':'user',  # Credentials used for dv.
  'auth_sheet':'user',  # Credentials used for sheet.
  'auth_bigquery':'service',  # Credentials used for bigquery.
  'recipe_name':'',  # Name of Google Sheet to create.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
  'command':'Load',  # Action to take.
  'first_and_third':False,  # Load first and third party data (may be slow). If not selected, enter audience identifiers into sheet manually.
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
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':2,'default':'','description':'Name of Google BigQuery dataset to create.'}}
      }
    },
    {
      'drive':{
        '__comment__':'Copy the default template to sheet with the recipe name',
        'auth':{'field':{'name':'auth_sheet','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'copy':{
          'source':'https://docs.google.com/spreadsheets/d/1ARkIvh0D-gltZeiwniUonMNrm0Mi1s2meZ9FUjutXOE/',
          'destination':{'field':{'name':'recipe_name','suffix':' DV Targeter','kind':'string','order':3,'default':'','description':'Name of Google Sheet to create.'}}
        }
      }
    },
    {
      'dv_targeter':{
        '__comment':'Depending on users choice, execute a different part of the solution.',
        'auth_dv':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials used for dv.'}},
        'auth_sheets':{'field':{'name':'auth_sheet','kind':'authentication','order':2,'default':'user','description':'Credentials used for sheet.'}},
        'auth_bigquery':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials used for bigquery.'}},
        'sheet':{'field':{'name':'recipe_name','suffix':' DV Targeter','kind':'string','order':4,'default':'','description':'Name of Google Sheet to create.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'Name of Google BigQuery dataset to create.'}},
        'command':{'field':{'name':'command','kind':'choice','choices':['Clear','Load','Preview','Update'],'order':6,'default':'Load','description':'Action to take.'}},
        'first_and_third':{'field':{'name':'first_and_third','kind':'boolean','order':6,'default':False,'description':'Load first and third party data (may be slow). If not selected, enter audience identifiers into sheet manually.'}}
      }
    }
  ]
}

dag_maker = DAG_Factory('dv360_targeter', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
