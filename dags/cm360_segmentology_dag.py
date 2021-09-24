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

CM360 Segmentology

CM360 funnel analysis using Census data.

  - Wait for <b>BigQuery->->->Census_Join</b> to be created.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/' target='_blank'>CM360 Segmentology Sample</a>. Leave the Data Source as is, you will change it in the next step.
  - Click Edit Connection, and change to <b>BigQuery->->->Census_Join</b>.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'account':'',
  'auth_read':'user',  # Credentials used for reading data.
  'auth_write':'service',  # Authorization used for writing data.
  'recipe_name':'',  # Name of report, not needed if ID used.
  'date_range':'LAST_365_DAYS',  # Timeframe to run report for.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
  'advertisers':[],  # Comma delimited list of CM360 advertiser ids.
}

RECIPE = {
  'tasks':[
    {
      'dataset':{
        'description':'Create a dataset for bigquery tables.',
        'hour':[
          4
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','description':'Place where tables will be created in BigQuery.'}}
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing function.'}},
        'function':'Pearson Significance Test',
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
        }
      }
    },
    {
      'google_api':{
        'auth':'user',
        'api':'dfareporting',
        'version':'v3.4',
        'function':'accounts.get',
        'kwargs':{
          'id':{'field':{'name':'account','kind':'integer','order':5,'default':'','description':'Campaign Manager Account ID'}},
          'fields':'id,name'
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing function.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_Account'
          }
        }
      }
    },
    {
      'dcm':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'filters':{
            'advertiser':{
              'values':{'field':{'name':'advertisers','kind':'integer_list','order':6,'default':[],'description':'Comma delimited list of CM360 advertiser ids.'}}
            }
          },
          'account':{'field':{'name':'account','kind':'string','order':5,'default':'','description':'Campaign Manager Account ID'}},
          'body':{
            'name':{'field':{'name':'recipe_name','kind':'string','suffix':' Segmentology','description':'The report name.','default':''}},
            'criteria':{
              'dateRange':{
                'kind':'dfareporting#dateRange',
                'relativeDateRange':{'field':{'name':'date_range','kind':'choice','order':3,'default':'LAST_365_DAYS','choices':['LAST_7_DAYS','LAST_14_DAYS','LAST_30_DAYS','LAST_365_DAYS','LAST_60_DAYS','LAST_7_DAYS','LAST_90_DAYS','LAST_24_MONTHS','MONTH_TO_DATE','PREVIOUS_MONTH','PREVIOUS_QUARTER','PREVIOUS_WEEK','PREVIOUS_YEAR','QUARTER_TO_DATE','WEEK_TO_DATE','YEAR_TO_DATE'],'description':'Timeframe to run report for.'}}
              },
              'dimensions':[
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'advertiserId'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'advertiser'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'zipCode'
                }
              ],
              'metricNames':[
                'impressions',
                'clicks',
                'totalConversions'
              ]
            },
            'type':'STANDARD',
            'delivery':{
              'emailOwner':False
            },
            'format':'CSV'
          }
        }
      }
    },
    {
      'dcm':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'account':{'field':{'name':'account','kind':'string','default':''}},
          'name':{'field':{'name':'recipe_name','kind':'string','order':3,'suffix':' Segmentology','default':'','description':'Name of report, not needed if ID used.'}}
        },
        'out':{
          'bigquery':{
            'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_KPI',
            'header':True
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
        'from':{
          'query':'SELECT            Id AS Partner_Id,            Name AS Partner,            Advertiser_Id,            Advertiser,            Zip_Postal_Code AS Zip,            SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY Advertiser_Id)) AS Impression,            SAFE_DIVIDE(Clicks, Impressions) AS Click,            SAFE_DIVIDE(Total_Conversions, Impressions) AS Conversion,            Impressions AS Impressions          FROM `{dataset}.CM360_KPI`          CROSS JOIN `{dataset}.CM360_Account`        ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','description':'Place where tables will be created in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','description':'Place where tables will be written in BigQuery.'}},
          'view':'CM360_KPI_Normalized'
        }
      }
    },
    {
      'census':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
        'normalize':{
          'census_geography':'zip_codes',
          'census_year':'2018',
          'census_span':'5yr'
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'type':'view'
        }
      }
    },
    {
      'census':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
        'correlate':{
          'join':'Zip',
          'pass':[
            'Partner_Id',
            'Partner',
            'Advertiser_Id',
            'Advertiser'
          ],
          'sum':[
            'Impressions'
          ],
          'correlate':[
            'Impression',
            'Click',
            'Conversion'
          ],
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'table':'CM360_KPI_Normalized',
          'significance':80
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'type':'view'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('cm360_segmentology', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
