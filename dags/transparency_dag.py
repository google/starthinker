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

CM360 Domain And App Transparency

Reports the percentage of CM impressions that can be attributed to a specific domain or application.  Allows diagnostic of which domains and apps are misconfigured by publisher resulting in underreporting.

  - Wait for <a href='https://console.cloud.google.com/bigquery?project=&d=' target='_blank'>BigQuery : </a> :  : </a> to be created.
  - Copy DataStudio <a href='https://datastudio.google.com/c/u/0/datasources/1Az6d9loAHo69GSIyKUfusrtyf_IDqTVs' target='_blank'>Transparency Combined KPI</a> and connect.
  - Copy DataStudio <a href='https://datastudio.google.com/c/u/0/reporting/1foircGRxgYCL_PR8gfdmYOleBacnPKwB/page/QCXj' target='_blank'>Transparency Breakdown</a>.
  - When prompted choose the new data source you just created.
  - Or give these intructions to the client, they will have to join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug':'',  # Place where tables will be written in BigQuery.
  'recipe_name':'',  # Name of report in CM, should be unique.
  'dcm_account':'',  # CM account id of client.
  'dcm_advertisers':'',  # Comma delimited list of CM advertiser ids.
}

RECIPE = {
  'tasks':[
    {
      'dataset':{
        'hour':[
          1
        ],
        'auth':'service',
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Name of Google BigQuery dataset to create.'}}
      }
    },
    {
      'dcm':{
        'hour':[
          2
        ],
        'auth':'user',
        'report':{
          'account':{'field':{'name':'dcm_account','kind':'integer','order':2,'default':'','description':'CM account id of client.'}},
          'filters':{
            'advertiser':{
              'values':{'field':{'name':'dcm_advertisers','kind':'integer_list','order':3,'description':'Comma delimited list of CM advertiser ids.'}}
            }
          },
          'body':{
            'type':'STANDARD',
            'format':'CSV',
            'name':{'field':{'name':'recipe_name','kind':'string','prefix':'Transparency App For ','description':'Name of report in CM, unique.'}},
            'criteria':{
              'dateRange':{
                'relativeDateRange':'PREVIOUS_MONTH'
              },
              'dimensions':[
                {
                  'name':'advertiser'
                },
                {
                  'name':'advertiserId'
                },
                {
                  'name':'campaign'
                },
                {
                  'name':'campaignId'
                },
                {
                  'name':'siteId'
                },
                {
                  'name':'site'
                },
                {
                  'name':'adType'
                },
                {
                  'name':'environment'
                },
                {
                  'name':'appId'
                },
                {
                  'name':'app'
                }
              ],
              'metricNames':[
                'impressions'
              ]
            },
            'schedule':{
              'active':True,
              'every':1,
              'repeats':'MONTHLY',
              'runsOnDayOfMonth':'DAY_OF_MONTH'
            }
          }
        }
      }
    },
    {
      'dcm':{
        'hour':[
          2
        ],
        'auth':'user',
        'report':{
          'account':{'field':{'name':'dcm_account','kind':'integer','order':2,'default':'','description':'CM account id of client.'}},
          'filters':{
            'advertiser':{
              'values':{'field':{'name':'dcm_advertisers','kind':'integer_list','order':3,'description':'Comma delimited list of CM advertiser ids.'}}
            }
          },
          'body':{
            'type':'STANDARD',
            'format':'CSV',
            'name':{'field':{'name':'recipe_name','kind':'string','prefix':'Transparency Domain For ','description':'Name of report in CM, unique.'}},
            'criteria':{
              'dateRange':{
                'relativeDateRange':'PREVIOUS_MONTH'
              },
              'dimensions':[
                {
                  'name':'advertiser'
                },
                {
                  'name':'advertiserId'
                },
                {
                  'name':'campaign'
                },
                {
                  'name':'campaignId'
                },
                {
                  'name':'site'
                },
                {
                  'name':'siteId'
                },
                {
                  'name':'adType'
                },
                {
                  'name':'domain'
                }
              ],
              'metricNames':[
                'verificationVerifiableImpressions'
              ]
            },
            'schedule':{
              'active':True,
              'every':1,
              'repeats':'MONTHLY',
              'runsOnDayOfMonth':'DAY_OF_MONTH'
            }
          }
        }
      }
    },
    {
      'dcm':{
        'hour':[
          4
        ],
        'auth':'user',
        'report':{
          'account':{'field':{'name':'dcm_account','kind':'integer','order':2,'default':'','description':'CM account id of client.'}},
          'name':{'field':{'name':'recipe_name','kind':'string','prefix':'Transparency Domain For ','description':'Name of report in CM, should be unique.'}}
        },
        'out':{
          'bigquery':{
            'auth':'service',
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'Transparency_Domain_KPI'
          }
        }
      }
    },
    {
      'dcm':{
        'hour':[
          4
        ],
        'auth':'user',
        'report':{
          'account':{'field':{'name':'dcm_account','kind':'integer','order':2,'default':'','description':'CM account id of client.'}},
          'name':{'field':{'name':'recipe_name','kind':'string','prefix':'Transparency App For ','description':'Name of report in CM, should be unique.'}}
        },
        'out':{
          'bigquery':{
            'auth':'service',
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'Transparency_App_KPI'
          }
        }
      }
    },
    {
      'bigquery':{
        'hour':[
          5
        ],
        'auth':'user',
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'view':'Transparency_Combined_KPI'
        },
        'from':{
          'query':"WITH           Transparent_Domains AS (             SELECT               CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,               CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,               CONCAT(Site_Cm360, ' - ', CAST(Site_Id_Cm360 AS STRING)) AS Site,               Domain,               Ad_Type,               Verifiable_Impressions AS Impressions,               IF(Domain IS NOT NULL, Verifiable_Impressions, 0) AS Visible_Impressions,               IF(Domain IS NULL, Verifiable_Impressions, 0) AS Null_Impressions             FROM `{dataset}.Transparency_Domain_KPI`           ),           Transparent_Apps AS (             SELECT               CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,               CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,               CONCAT(Site_Cm360, ' - ', CAST(Site_Id_Cm360 AS STRING)) AS Site,               /*If(App IS NOT NULL, CONCAT(App, ' - ', CAST(App_Id AS STRING)), App_Id) AS App, */               CASE                 WHEN App IS NOT NULL THEN CONCAT(App, ' - ', CAST(App_Id AS STRING))                 WHEN App_Id IS NOT NULL THEN App_Id                 ELSE NULL               END AS App,               Ad_Type,               Impressions,               IF(App IS NOT NULL OR App_ID IS NOT NULL, Impressions, 0) AS Visible_Impressions,               IF(App IS NULL AND App_Id IS NULL, Impressions, 0) AS Null_Impressions             FROM `{dataset}.Transparency_App_KPI`  WHERE Environment = 'App'           ),           Domains_And_Apps AS (             SELECT               TD.Advertiser,               TD.Campaign,               TD.Site,               TD.Ad_Type,               TD.Domain,               TD.Impressions AS Domain_Impressions,               TD.Visible_Impressions AS Domain_Visible_Impressions,               TD.Null_Impressions AS Domain_Null_Impressions,               NULL AS App,               0 AS App_Impressions,               0 AS App_Visible_Impressions,               0 AS App_Null_Impressions  FROM Transparent_Domains AS TD  UNION ALL  SELECT               TA.Advertiser,               TA.Campaign,               TA.Site,               TA.Ad_Type,               NULL AS Domain,               0 AS Domain_Impressions,               0 AS Domain_Visible_Impressions,               0 AS Domain_Null_Impressions,               TA.App,               TA.Impressions AS App_Impressions,               TA.Visible_Impressions AS App_Visible_Impressions,               TA.Null_Impressions AS App_Null_Impressions             FROM Transparent_Apps AS TA           )           SELECT             Advertiser,             Campaign,             Site,             COALESCE(Domain, App, '') AS Domain_Or_App,             Ad_Type,             CASE               WHEN App IS NOT NULL AND Domain IS NOT NULL THEN 'Both' /* SHOULD NOT HAPPEN */               WHEN App IS NOT NULL THEN 'App'               WHEN Domain IS NOT NULL Then 'Domain'               ELSE 'Neither'             END AS Category,             SUM(Domain_Impressions) AS Domain_Impressions,             SUM(Domain_Visible_Impressions) AS Domain_Visible_Impressions,             SUM(Domain_Null_Impressions) AS Domain_Null_Impressions,             SUM(App_Impressions) AS App_Impressions,             SUM(App_Visible_Impressions) AS App_Visible_Impressions,             SUM(App_Null_Impressions) AS App_Null_Impressions,             SUM(App_Impressions + Domain_Impressions) AS Impressions             /* Could also be MAX as its always one or the other*/           FROM Domains_And_Apps  GROUP By 1,2,3,4,5,6",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          },
          'legacy':False
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('transparency', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
