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

CM360 Log Audit

Downloads Campaign manager logs and allows audits.



  - Wait for BigQuery->->->CM_... to be created.
  - Wait for BigQuery->->->Barnacle_... to be created, then copy and connect the following data sources.
  - Join the 1-StarThinker Assets Group to access the following assets
  - Copy 2-Barnacle Profile Advertiser Map and connect.
  - Copy 3-Barnacle Profile Campaign Map and connect.
  - Copy 4-Barnacle Profile Site Map and connect.
  - Copy 5-Barnacle Profiles Connections and connect.
  - Copy 6-Barnacle Report Delivery Profiles and connect.
  - Copy 7-Barnacle Roles Duplicates and connect.
  - Copy 8-Barnacle Roles Not Used and connect.
  - Copy 9-Barnacle Site Contacts Profiles and connect.
  - If reports checked, copy 10-Barnacle Profile Report Map and connect.
  - Copy 11-Barnacle Report.
  - When prompted choose the new data sources you just created.
  - Or give these intructions to the client.

  1-StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
  2-Barnacle Profile Advertiser Map: https://datastudio.google.com/open/1a6K-XdPUzCYRXZp1ZcmeOUOURc9wn2Jj
  3-Barnacle Profile Campaign Map: https://datastudio.google.com/open/1NEzrQWWnPjkD90iUwN-ASKbVBzoeBdoT
  4-Barnacle Profile Site Map: https://datastudio.google.com/open/1v_GRaitwPaHHKUzfJZYNBhzotvZ-bR7Y
  5-Barnacle Profiles Connections: https://datastudio.google.com/open/14tWlh7yiqzxKJIppMFVOw2MoMtQV_ucE
  6-Barnacle Report Delivery Profiles: https://datastudio.google.com/open/1mavjxvHSEPfJq5aW4FYgCXsBCE5rthZG
  7-Barnacle Roles Duplicates: https://datastudio.google.com/open/1Azk_Nul-auinf4NnDq8T9fDyiKkUWD7A
  8-Barnacle Roles Not Used: https://datastudio.google.com/open/1ogoofpKtqkLwcW9qC_Ju_JvJdIajsjNI
  9-Barnacle Site Contacts Profiles: https://datastudio.google.com/open/1xLgZPjOPDtmPyEqYMiMbWwMI8-WTslfj
  10-Barnacle Profile Report Map: https://datastudio.google.com/open/1-YGDiQPDnk0gD78_QOY5XdTXRlTrLeEq
  11-Barnacle Report: https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for reading data.
  'auth_write':'service',  # Credentials used for writing data.
  'accounts':[],  # Comma separated CM account ids.
  'days':7,  # Number of days to backfill the log, works on first run only.
  'recipe_slug':'',  # Google BigQuery dataset to create tables in.
}

RECIPE = {
  'setup':{
    'day':[
      'Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'
    ],
    'hour':[
      1,
      2
    ]
  },
  'tasks':[
    {
      'dataset':{
        'description':'The dataset will hold log table, Create it exists.',
        'hour':[
          1
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
      }
    },
    {
      'dcm_log':{
        'description':'Will create tables with format CM_* to hold each endpoint via a call to the API list function. Exclude reports for its own task.',
        'hour':[
          2
        ],
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'accounts':{
          'single_cell':True,
          'values':{'field':{'name':'accounts','kind':'integer_list','order':2,'default':[],'description':'Comma separated CM account ids.'}}
        },
        'days':{'field':{'name':'days','kind':'integer','order':3,'default':7,'description':'Number of days to backfill the log, works on first run only.'}},
        'out':{
          'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'Google BigQuery dataset to create tables in.'}}
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dcm_log', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
