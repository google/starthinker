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

Video Overlay

Add images, text, and audio to videos.

  - Provide either a sheet or a BigQuery table.
  - Each video edit will be read from the sheet or table.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for reading data.
  'sheet':'',  # Name or URL of sheet.
  'tab':'',  # Name of sheet tab.
  'project':'',  # Google Cloud Project Identifier.
  'dataset':'',  # Name of dataset.
  'table':'',  # Name of table.
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
      'sheets':{
        '__comment__':'Copy the tamplate sheet to the users sheet.  If it already exists, nothing happens.',
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'template':{
          'sheet':'https://docs.google.com/spreadsheets/d/1BXRHWz-1P3gNS92WZy-3sPZslU8aalXa8heOgygWEFs/edit#gid=0',
          'tab':'Video'
        },
        'sheet':{'field':{'name':'sheet','kind':'string','order':1,'default':'','description':'Name or URL of sheet.'}},
        'tab':{'field':{'name':'tab','kind':'string','order':2,'default':'','description':'Name of sheet tab.'}}
      }
    },
    {
      'video':{
        '__comment__':'Read video effects and values from sheet and/or bigquery.',
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'sheets':{
          'sheet':{'field':{'name':'sheet','kind':'string','order':1,'default':'','description':'Name or URL of sheet.'}},
          'tab':{'field':{'name':'tab','kind':'string','order':2,'default':'','description':'Name of sheet tab.'}}
        },
        'bigquery':{
          'project':{'field':{'name':'project','kind':'string','order':3,'default':'','description':'Google Cloud Project Identifier.'}},
          'dataset':{'field':{'name':'dataset','kind':'string','order':4,'default':'','description':'Name of dataset.'}},
          'table':{'field':{'name':'table','kind':'string','order':5,'default':'','description':'Name of table.'}}
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('video', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
