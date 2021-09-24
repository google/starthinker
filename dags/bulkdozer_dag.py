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

CM360 Bulkdozer Editor

Bulkdozer is a tool that can reduce trafficking time in Campaign Manager by up to 80%% by providing automated bulk editing capabilities.

  - Open the <a href='https://docs.google.com/spreadsheets/d/1EjprWTDLWOvkV7znA0P4uciz0_E5_TNn3N3f8J4jTwA/edit?usp=sharing&resourcekey=0-jVCGjrPdnUnJ0rk7nQCFBQ' target='_blank'>Bulkdozer 0.28</a> feed.
  - Make your own copy of the feed by clicking the File -> Make a copy... menu in the feed.
  - Give it a meaninful name including the version, your name, and team to help you identify it and ensure you are using the correct version.
  - Under the Account ID field below, enter the your Campaign Manager Network ID.
  - Under Sheet URL, enter the URL of your copy of the feed that you just created in the steps above.
  - Go to the Store tab of your new feed, and enter your profile ID in the profileId field (cell B2). Your profile ID is visible in Campaign Manager by clicking your avatar on the top right corner.
  - Click the 'Save' button below.
  - After clicking 'Save', copy this page's URL from your browser address bar, and paste it in the Store tab for the recipe_url field (cell B5) your sheet.
  - Bulkdozer is ready for use
  - Stay up to date on new releases and other general anouncements by joining <a href='https://groups.google.com/forum/#!forum/bulkdozer-announcements' target='_blank'>Bulkdozer announcements</a>.
  - Review the <a href='https://github.com/google/starthinker/blob/master/tutorials/Bulkdozer/Installation_and_User_guides.md' target='_blank'>Bulkdozer documentation</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_timezone':'America/Chicago',  # Timezone for report dates.
  'account_id':None,  # Campaign Manager Network ID (optional if profile id provided)
  'dcm_profile_id':None,  # Campaign Manager Profile ID (optional if account id provided)
  'sheet_url':'',  # Feed Sheet URL
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
      'traffic':{
        'hour':[
        ],
        'account_id':{'field':{'name':'account_id','kind':'string','order':1,'description':'Campaign Manager Network ID (optional if profile id provided)','default':None}},
        'dcm_profile_id':{'field':{'name':'dcm_profile_id','kind':'string','order':1,'description':'Campaign Manager Profile ID (optional if account id provided)','default':None}},
        'auth':'user',
        'sheet_url':{'field':{'name':'sheet_url','kind':'string','order':2,'description':'Feed Sheet URL','default':''}},
        'timezone':{'field':{'name':'recipe_timezone','kind':'timezone','description':'Timezone for report dates.','default':'America/Chicago'}}
      }
    }
  ]
}

dag_maker = DAG_Factory('bulkdozer', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
