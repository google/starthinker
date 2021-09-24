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

DV360 Report Emailed To BigQuery

Pulls a DV360 Report from a gMail email into BigQuery.

  - The person executing this recipe must be the recipient of the email.
  - Schedule a DV360 report to be sent to an email like <b></b>.
  - Or set up a redirect rule to forward a report you already receive.
  - The report can be sent as an attachment or a link.
  - Ensure this recipe runs after the report is email daily.
  - Give a regular expression to match the email subject.
  - Configure the destination in BigQuery to write the data.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for reading data.
  'email':'',  # Email address report was sent to.
  'subject':'.*',  # Regular expression to match subject. Double escape backslashes.
  'dataset':'',  # Existing dataset in BigQuery.
  'table':'',  # Name of table to be written to.
  'dbm_schema':'[]',  # Schema provided in JSON list format or empty list.
  'is_incremental_load':False,  # Append report data to table based on date column, de-duplicates.
}

RECIPE = {
  'tasks':[
    {
      'email':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'read':{
          'from':'noreply-dv360@google.com',
          'to':{'field':{'name':'email','kind':'string','order':1,'default':'','description':'Email address report was sent to.'}},
          'subject':{'field':{'name':'subject','kind':'string','order':2,'default':'.*','description':'Regular expression to match subject. Double escape backslashes.'}},
          'link':'https://storage.googleapis.com/.*',
          'attachment':'.*'
        },
        'write':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'Existing dataset in BigQuery.'}},
            'table':{'field':{'name':'table','kind':'string','order':4,'default':'','description':'Name of table to be written to.'}},
            'schema':{'field':{'name':'dbm_schema','kind':'json','order':5,'default':'[]','description':'Schema provided in JSON list format or empty list.'}},
            'header':True,
            'is_incremental_load':{'field':{'name':'is_incremental_load','kind':'boolean','order':6,'default':False,'description':'Append report data to table based on date column, de-duplicates.'}}
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('email_dv360_to_bigquery', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
