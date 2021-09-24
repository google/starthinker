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

GoogleAds Segmentology

GoogleAds funnel analysis using Census data.

  - Wait for <b>BigQuery->->->Census_Join</b> to be created.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/' target='_blank'>GoogleAds Segmentology Sample</a>. Leave the Data Source as is, you will change it in the next step.
  - Click Edit Connection, and change to <b>BigQuery->->->Census_Join</b>.
  - Or give these instructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for reading data.
  'customer_id':'',  # Google Ads customer.
  'developer_token':'',  # Google Ads developer token.
  'login_id':'',  # Google Ads login.
  'auth_write':'service',  # Authorization used for writing data.
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
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'api':'googleads',
        'version':'v8',
        'function':'customers.googleAds.search',
        'kwargs':{
          'customerId':{'field':{'name':'customer_id','kind':'string','description':'Google Ads customer.','default':''}},
          'body':{
            'query':'SELECT           campaign.name,           ad_group.name,           segments.geo_target_postal_code,           metrics.impressions,           metrics.clicks,           metrics.conversions,           metrics.interactions           FROM user_location_view         '
          }
        },
        'headers':{
          'developer-token':{'field':{'name':'developer_token','kind':'string','description':'Google Ads developer token.','default':''}},
          'login-customer-id':{'field':{'name':'login_id','kind':'string','description':'Google Ads login.','default':''}}
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'GoogleAds_KPI',
            'schema':[
              {
                'name':'userLocationView',
                'type':'RECORD',
                'mode':'NULLABLE',
                'fields':[
                  {
                    'name':'resourceName',
                    'type':'STRING',
                    'mode':'NULLABLE'
                  }
                ]
              },
              {
                'name':'segments',
                'type':'RECORD',
                'mode':'NULLABLE',
                'fields':[
                  {
                    'name':'geoTargetPostalCode',
                    'type':'STRING',
                    'mode':'NULLABLE'
                  }
                ]
              },
              {
                'name':'metrics',
                'type':'RECORD',
                'mode':'NULLABLE',
                'fields':[
                  {
                    'name':'interactions',
                    'type':'INTEGER',
                    'mode':'NULLABLE'
                  },
                  {
                    'name':'impressions',
                    'type':'INTEGER',
                    'mode':'NULLABLE'
                  },
                  {
                    'name':'conversions',
                    'type':'INTEGER',
                    'mode':'NULLABLE'
                  },
                  {
                    'name':'clicks',
                    'type':'INTEGER',
                    'mode':'NULLABLE'
                  }
                ]
              },
              {
                'name':'adGroup',
                'type':'RECORD',
                'mode':'NULLABLE',
                'fields':[
                  {
                    'name':'name',
                    'type':'STRING',
                    'mode':'NULLABLE'
                  },
                  {
                    'name':'resourceName',
                    'type':'STRING',
                    'mode':'NULLABLE'
                  }
                ]
              },
              {
                'name':'campaign',
                'type':'RECORD',
                'mode':'NULLABLE',
                'fields':[
                  {
                    'name':'name',
                    'type':'STRING',
                    'mode':'NULLABLE'
                  },
                  {
                    'name':'resourceName',
                    'type':'STRING',
                    'mode':'NULLABLE'
                  }
                ]
              }
            ]
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Authorization used for writing data.'}},
        'from':{
          'query':'SELECT            campaign.name AS Campaign,            adGRoup.name AS Ad_Group,            segments.geoTargetPostalCode AS Postal_Code,            SAFE_DIVIDE(metrics.impressions, SUM(metrics.impressions) OVER()) AS Impression,            SAFE_DIVIDE(metrics.clicks, metrics.impressions) AS Click,            SAFE_DIVIDE(metrics.conversions, metrics.impressions) AS Conversion,            SAFE_DIVIDE(metrics.interactions, metrics.impressions) AS Interaction,            metrics.impressions AS Impressions          FROM            `{dataset}.GoogleAds_KPI`;        ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','description':'Place where tables will be created in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','description':'Place where tables will be written in BigQuery.'}},
          'view':'GoogleAds_KPI_Normalized'
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
          'join':'Postal_Code',
          'pass':[
            'Campaign',
            'Ad_Group'
          ],
          'sum':[
            'Impressions'
          ],
          'correlate':[
            'Impression',
            'Click',
            'Conversion',
            'Interaction'
          ],
          'dataset':{'field':{'name':'recipe_slug','kind':'string','suffix':'_Segmentology','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'table':'GoogleAds_KPI_Normalized',
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

dag_maker = DAG_Factory('google_ads_segmentology', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
