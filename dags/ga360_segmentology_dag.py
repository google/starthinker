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

GA360 Segmentology

GA360 funnel analysis using Census data.

  - Wait for <b>BigQuery->->->Census_Join</b> to be created.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/' target='_blank'>GA360 Segmentology Sample</a>. Leave the Data Source as is, you will change it in the next step.
  - Click Edit Connection, and change to <b>BigQuery->->->Census_Join</b>.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_write':'service',  # Authorization used for writing data.
  'auth_read':'service',  # Authorization for reading GA360.
  'view':'service',  # View Id
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
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
        'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}}
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing function.'}},
        'function':'Pearson Significance Test',
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
        }
      }
    },
    {
      'ga':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'service','description':'Authorization for reading GA360.'}},
        'kwargs':{
          'reportRequests':[
            {
              'viewId':{'field':{'name':'view','kind':'string','order':2,'default':'service','description':'View Id'}},
              'dateRanges':[
                {
                  'startDate':'90daysAgo',
                  'endDate':'today'
                }
              ],
              'dimensions':[
                {
                  'name':'ga:userType'
                },
                {
                  'name':'ga:userDefinedValue'
                },
                {
                  'name':'ga:latitude'
                },
                {
                  'name':'ga:longitude'
                }
              ],
              'metrics':[
                {
                  'expression':'ga:users'
                },
                {
                  'expression':'ga:sessionsPerUser'
                },
                {
                  'expression':'ga:bounces'
                },
                {
                  'expression':'ga:timeOnPage'
                },
                {
                  'expression':'ga:pageviews'
                }
              ]
            }
          ],
          'useResourceQuotas':False
        },
        'out':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'GA360_KPI'
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
        'from':{
          'query':'WITH GA360_SUM AS (           SELECT              A.Dimensions.userType AS User_Type,             A.Dimensions.userDefinedValue AS User_Value,             B.zip_code AS Zip,             SUM(Metrics.users) AS Users,             SUM(Metrics.sessionsPerUser) AS Sessions,             SUM(Metrics.timeOnPage) AS Time_On_Site,             SUM(Metrics.bounces) AS Bounces,             SUM(Metrics.pageviews) AS Page_Views           FROM `{dataset}.GA360_KPI` AS A            JOIN `bigquery-public-data.geo_us_boundaries.zip_codes` AS B           ON ST_WITHIN(ST_GEOGPOINT(A.Dimensions.longitude, A.Dimensions.latitude), B.zip_code_geom)           GROUP BY 1,2,3           )           SELECT             User_Type,             User_Value,             Zip,             Users,             SAFE_DIVIDE(Users, SUM(Users) OVER()) AS User_Percent,             SAFE_DIVIDE(Sessions, SUM(Sessions) OVER()) AS Impression_Percent,             SAFE_DIVIDE(Time_On_Site, SUM(Time_On_Site) OVER()) AS Time_On_Site_Percent,             SAFE_DIVIDE(Bounces, SUM(Bounces) OVER()) AS Bounce_Percent,             SAFE_DIVIDE(Page_Views, SUM(Page_Views) OVER()) AS Page_View_Percent           FROM GA360_SUM        ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'GA360_KPI_Normalized'
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
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
            'User_Type',
            'User_Value'
          ],
          'sum':[
            'Users'
          ],
          'correlate':[
            'User_Percent',
            'Impression_Percent',
            'Time_On_Site_Percent',
            'Bounce_Percent',
            'Page_View_Percent'
          ],
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'table':'GA360_KPI_Normalized',
          'significance':80
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'type':'view'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('ga360_segmentology', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
