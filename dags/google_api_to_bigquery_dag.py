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

Google API To BigQuery

Execute any Google API function and store results to BigQuery.

  - Enter an api name and version.
  - Specify the function using dot notation.
  - Specify the arguments using json.
  - Iterate is optional, use if API returns a list of items that are not unpacking correctly.
  - The <a href='https://cloud.google.com/docs/authentication/api-keys' target='_blank'>API Key</a> may be required for some calls.
  - The <a href='https://developers.google.com/google-ads/api/docs/first-call/dev-token' target='_blank'>Developer Token</a> may be required for some calls.
  - Give BigQuery dataset and table where response will be written.
  - All API calls are based on <a href='https://developers.google.com/discovery/v1/reference'  target='_blank'>discovery document</a>, for example the <a href='https://developers.google.com/display-video/api/reference/rest/v1/advertisers/list' target='_blank'>Campaign Manager API</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for reading data.
  'api':'displayvideo',  # See developer guide.
  'version':'v1',  # Must be supported version.
  'function':'advertisers.list',  # Full function dot notation path.
  'kwargs':{'partnerId': 234340},  # Dictionray object of name value pairs.
  'kwargs_remote':{},  # Fetch arguments from remote source.
  'api_key':'',  # Associated with a Google Cloud Project.
  'developer_token':'',  # Associated with your organization.
  'login_customer_id':'',  # Associated with your Adwords account.
  'dataset':'',  # Existing dataset in BigQuery.
  'table':'',  # Table to write API call results to.
}

RECIPE = {
  'tasks':[
    {
      'google_api':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'api':{'field':{'name':'api','kind':'string','order':1,'default':'displayvideo','description':'See developer guide.'}},
        'version':{'field':{'name':'version','kind':'string','order':2,'default':'v1','description':'Must be supported version.'}},
        'function':{'field':{'name':'function','kind':'string','order':3,'default':'advertisers.list','description':'Full function dot notation path.'}},
        'kwargs':{'field':{'name':'kwargs','kind':'json','order':4,'default':{'partnerId':234340},'description':'Dictionray object of name value pairs.'}},
        'kwargs_remote':{'field':{'name':'kwargs_remote','kind':'json','order':5,'default':{},'description':'Fetch arguments from remote source.'}},
        'key':{'field':{'name':'api_key','kind':'string','order':6,'default':'','description':'Associated with a Google Cloud Project.'}},
        'headers':{
          'developer-token':{'field':{'name':'developer_token','kind':'string','order':7,'default':'','description':'Associated with your organization.'}},
          'login-customer-id':{'field':{'name':'login_customer_id','kind':'string','order':8,'default':'','description':'Associated with your Adwords account.'}}
        },
        'results':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':9,'default':'','description':'Existing dataset in BigQuery.'}},
            'table':{'field':{'name':'table','kind':'string','order':10,'default':'','description':'Table to write API call results to.'}}
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('google_api_to_bigquery', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
