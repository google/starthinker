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

URL

Pull URL list from a table, fetch them, and write the results to another table.

  - Specify a table with only two columns URL, URI (can be null).
  - Check bigquery destination for results of fetching each URL.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth':'service',  # Credentials used for rading and writing data.
  'status':True,  # Pull status of HTTP request.
  'read':False,  # Pull data from HTTP request.
  'dataset':'',  # Name of Google BigQuery dataset to write.
  'table':'',  # Name of Google BigQuery table to write.
}

RECIPE = {
  'tasks':[
    {
      'url':{
        'auth':{'field':{'name':'auth','kind':'authentication','order':1,'default':'service','description':'Credentials used for rading and writing data.'}},
        'status':{'field':{'name':'status','kind':'boolean','order':2,'default':True,'description':'Pull status of HTTP request.'}},
        'read':{'field':{'name':'read','kind':'boolean','order':3,'default':False,'description':'Pull data from HTTP request.'}},
        'urls':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to write.'}},
            'query':{'field':{'name':'table','kind':'text','order':5,'default':'','description':'Query to run to pull URLs.'}},
            'legacy':False
          }
        },
        'to':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':6,'default':'','description':'Name of Google BigQuery dataset to write.'}},
            'table':{'field':{'name':'table','kind':'string','order':7,'default':'','description':'Name of Google BigQuery table to write.'}}
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('url', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
