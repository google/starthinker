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

Census Data Correlation

Correlate another table with US Census data.  Expands a data set dimensions by finding population segments that correlate with the master table.

  - Pre-requisite is Census Normalize, run that at least once.
  - Specify JOIN, PASS, SUM, and CORRELATE columns to build the correlation query.
  - Define the DATASET and TABLE for the joinable source. Can be a view.
  - Choose the significance level.  More significance usually means more NULL results, balance quantity and quality using this value.
  - Specify where to write the results.
  - <br>IMPORTANT:</b> If you use VIEWS, you will have to delete them manually if the recipe changes.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth':'service',  # Credentials used for writing data.
  'join':'',  # Name of column to join on, must match Census Geo_Id column.
  'pass':[],  # Comma seperated list of columns to pass through.
  'sum':[],  # Comma seperated list of columns to sum, optional.
  'correlate':[],  # Comma seperated list of percentage columns to correlate.
  'from_dataset':'',  # Existing BigQuery dataset.
  'from_table':'',  # Table to use as join data.
  'significance':'80',  # Select level of significance to test.
  'to_dataset':'',  # Existing BigQuery dataset.
  'type':'table',  # Write Census_Percent as table or view.
}

RECIPE = {
  'tasks':[
    {
      'census':{
        'auth':{'field':{'name':'auth','kind':'authentication','order':0,'default':'service','description':'Credentials used for writing data.'}},
        'correlate':{
          'join':{'field':{'name':'join','kind':'string','order':1,'default':'','description':'Name of column to join on, must match Census Geo_Id column.'}},
          'pass':{'field':{'name':'pass','kind':'string_list','order':2,'default':[],'description':'Comma seperated list of columns to pass through.'}},
          'sum':{'field':{'name':'sum','kind':'string_list','order':3,'default':[],'description':'Comma seperated list of columns to sum, optional.'}},
          'correlate':{'field':{'name':'correlate','kind':'string_list','order':4,'default':[],'description':'Comma seperated list of percentage columns to correlate.'}},
          'dataset':{'field':{'name':'from_dataset','kind':'string','order':5,'default':'','description':'Existing BigQuery dataset.'}},
          'table':{'field':{'name':'from_table','kind':'string','order':6,'default':'','description':'Table to use as join data.'}},
          'significance':{'field':{'name':'significance','kind':'choice','order':7,'default':'80','description':'Select level of significance to test.','choices':['80','90','98','99','99.5','99.95']}}
        },
        'to':{
          'dataset':{'field':{'name':'to_dataset','kind':'string','order':9,'default':'','description':'Existing BigQuery dataset.'}},
          'type':{'field':{'name':'type','kind':'choice','order':10,'default':'table','description':'Write Census_Percent as table or view.','choices':['table','view']}}
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('bigquery_census_correlate', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
