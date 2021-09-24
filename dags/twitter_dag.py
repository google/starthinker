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

Twitter Targeting

Adjusts line item settings based on Twitter hashtags and locations specified in a sheet.

  - Click <b>Run Now</b> and a sheet called <b>Twitter Targeting </b> will be generated with a tab called <b>Twitter Triggers</b>.
  - Follow instructions on the sheets tab to provide triggers and lineitems.
  - Click <b>Run Now</b> again, trends are downloaded and triggered.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for reading data.
  'auth_write':'service',  # Credentials used for writing data.
  'recipe_name':'',  # Name of sheet where Line Item settings will be read from.
  'twitter_secret':'',  # Twitter API secret token.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
  'twitter_key':'',  # Twitter API key token.
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
      2,
      4,
      6,
      8,
      10,
      12,
      14,
      16,
      18,
      20,
      22,
      24
    ]
  },
  'tasks':[
    {
      'dataset':{
        'description':'Create a dataset where data will be combined and transfored for upload.',
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'description':'Place where tables will be created in BigQuery.'}}
      }
    },
    {
      'sheets':{
        'description':'Read mapping of hash tags to line item toggles from sheets.',
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'template':{
          'sheet':'https://docs.google.com/spreadsheets/d/1iYCGa2NKOZiL2mdT4yiDfV_SWV9C7SUosXdIr4NAEXE/edit?usp=sharing',
          'tab':'Twitter Triggers'
        },
        'sheet':{'field':{'name':'recipe_name','kind':'string','prefix':'Twitter Targeting For ','order':2,'description':'Name of sheet where Line Item settings will be read from.','default':''}},
        'tab':'Twitter Triggers',
        'range':'A7:E',
        'out':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}},
            'table':'Twitter_Triggers',
            'schema':[
              {
                'name':'Location',
                'type':'STRING',
                'mode':'REQUIRED'
              },
              {
                'name':'WOEID',
                'type':'INTEGER',
                'mode':'REQUIRED'
              },
              {
                'name':'Hashtag',
                'type':'STRING',
                'mode':'REQUIRED'
              },
              {
                'name':'Advertiser_Id',
                'type':'INTEGER',
                'mode':'REQUIRED'
              },
              {
                'name':'Line_Item_Id',
                'type':'INTEGER',
                'mode':'REQUIRED'
              }
            ]
          }
        }
      }
    },
    {
      'twitter':{
        'description':'Read trends from Twitter and place into BigQuery.',
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'secret':{'field':{'name':'twitter_secret','kind':'string','order':3,'default':'','description':'Twitter API secret token.'}},
        'key':{'field':{'name':'twitter_key','kind':'string','order':4,'default':'','description':'Twitter API key token.'}},
        'trends':{
          'places':{
            'single_cell':True,
            'bigquery':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}},
              'query':'SELECT DISTINCT WOEID FROM {dataset}.Twitter_Triggers',
              'legacy':False,
              'parameters':{
                'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}}
              }
            }
          }
        },
        'out':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}},
            'table':'Twitter_Trends_Place'
          }
        }
      }
    },
    {
      'google_api':{
        'description':'Combine sheet and twitter data into API operations for each line item.  Match all possibilities and PAUSE if no trigger match.',
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.lineItems.patch',
        'kwargs_remote':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'query':"             SELECT               CAST(S.Advertiser_Id AS STRING) advertiserId,               CAST(S.Line_Item_Id AS STRING) AS lineItemId,               STRUCT(                 IF(LOGICAL_OR(T.Name is NULL), 'ENTITY_STATUS_ACTIVE', 'ENTITY_STATUS_PAUSED') AS entityStatus               ) AS body,               'entityStatus' AS updateMask,             FROM `{dataset}.Twitter_Triggers` AS S             LEFT JOIN `{dataset}.Twitter_Trends_Place` As T             ON S.WOEID=T.WOEID AND REPLACE(LOWER(S.Hashtag), '#', '')=REPLACE(LOWER(T.Name), '#', '')             GROUP BY 1,2           ",
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}}
            }
          }
        },
        'results':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'Trigger_Results'
          }
        },
        'errors':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'Trigger_Errors'
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('twitter', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
