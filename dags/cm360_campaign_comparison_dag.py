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

CM360 Campaign Comparison

Group KPIs into cohorts and compare performance across time and geography. Quickly discover where national and local campaigns need to be targeted, funded, or optimized.



  - Add required parameters and run recipe.
  - After recipe completes make a copy of the 1-Campaign Comparison Dashboard.
  - Keep the data source as is on the copy screen. It will change later.
  - After the copy is made, click Edit->Resource->Manage Added Data Sources->CC_Report->Edit->Edit Connection.
  - Connect to the newly created BigQuery->->_Campaign_Comparison->Comparison table.
  - Or give these intructions to the client.

  1-Campaign Comparison Dashboard: https://datastudio.google.com/c/u/0/reporting/e34669ec-0894-4453-9ac4-ae9c3e739c48/page/p_pkxetkzemc

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_bq':'user',  # Credentials used for reading data.
  'auth_cm':'user',  # Credentials used for reading data.
  'recipe_slug':'',  # Name of dataset.
  'account':12345,  # Campaign Manager Account ID
  'recipe_name':'',  # Name of report.
  'advertiser':[],  # Optional comma delimited list of ids.
  'relativeDateRange':'LAST_365_DAYS',  # Timeframe to run the report for.
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
      3
    ]
  },
  'tasks':[
    {
      'dataset':{
        'description':'Create a dataset for bigquery tables.',
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}}
      }
    },
    {
      'dcm':{
        'description':'Create KPI report.',
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'account':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}},
          'name':{'field':{'name':'recipe_name','kind':'string','order':3,'suffix':' Campaign Comparison','default':'','description':'Name of report.'}},
          'body':{
            'kind':'dfareporting#report',
            'format':'CSV',
            'type':'STANDARD',
            'criteria':{
              'dateRange':{
                'kind':'dfareporting#dateRange',
                'relativeDateRange':{'field':{'name':'relativeDateRange','kind':'choice','order':4,'default':'LAST_365_DAYS','choices':['LAST_7_DAYS','LAST_14_DAYS','LAST_30_DAYS','LAST_365_DAYS','LAST_60_DAYS','LAST_7_DAYS','LAST_90_DAYS','MONTH_TO_DATE','PREVIOUS_MONTH','PREVIOUS_QUARTER','PREVIOUS_WEEK','PREVIOUS_YEAR','QUARTER_TO_DATE','WEEK_TO_DATE','YEAR_TO_DATE'],'description':'Timeframe to run the report for.'}}
              },
              'dimensions':[
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'date'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'advertiserId'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'campaignId'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'adId'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'placementId'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'platformType'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'dmaRegion'
                },
                {
                  'kind':'dfareporting#sortedDimension',
                  'name':'zipCode'
                }
              ],
              'metricNames':[
                'impressions',
                'clicks',
                'totalConversions',
                'mediaCost'
              ]
            },
            'schedule':{
              'active':True,
              'repeats':'WEEKLY',
              'repeatsOnWeekDays':'MONDAY',
              'every':1
            },
            'delivery':{
              'emailOwner':False
            }
          },
          'filters':{
            'advertiser':{
              'values':{'field':{'name':'advertiser','kind':'integer_list','order':3,'default':[],'description':'Optional comma delimited list of ids.'}}
            }
          }
        }
      }
    },
    {
      'dcm':{
        'description':'Download KPI report.',
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'account':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}},
          'name':{'field':{'name':'recipe_name','kind':'string','order':3,'suffix':' Campaign Comparison','default':'','description':'Name of report.'}}
        },
        'out':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
            'table':'CM_Report',
            'header':True
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.5',
        'function':'advertisers.list',
        'iterate':True,
        'kwargs':{
          'fields':'advertisers.id,advertisers.name,nextPageToken',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
            'table':'CM_Advertisers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.5',
        'function':'campaigns.list',
        'iterate':True,
        'kwargs':{
          'fields':'campaigns.id,campaigns.name,nextPageToken',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
            'table':'CM_Campaigns'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.5',
        'function':'ads.list',
        'iterate':True,
        'kwargs':{
          'fields':'ads.id,ads.name,ads.type,nextPageToken',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
            'table':'CM_Ads'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.5',
        'function':'placements.list',
        'iterate':True,
        'kwargs':{
          'fields':'placements.id,placements.name',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Credentials used for reading data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
            'table':'CM_Placements'
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Credentials used for reading data.'}},
        'from':{
          'query':"WITH           CCReport AS (             SELECT               Report_Day,               CONCAT(CA.name, ' - ', CA.id) AS Advertiser,               CONCAT(CC.name, ' - ', CC.id) AS Campaign,               CONCAT(CD.name, ' - ', CD.id) AS Ad,               CONCAT(CP.name, ' - ', CP.id) AS Placement,               CR.Platform_Type AS Platform_Type,               CD.type AS Ad_Type,               Zip_Postal_Code AS Zip_Code,               Designated_Market_Area_Dma AS DMA,               CR.Impressions AS Impressions,               CR.Clicks AS Clicks,               CAST(CR.Total_conversions AS INT64) AS Conversions,               CR.Media_Cost AS Costs             FROM `{dataset}.CM_Report` AS CR             LEFT JOIN `{dataset}.CM_Advertisers` AS CA             ON CR.Advertiser_Id=CA.id             LEFT JOIN `{dataset}.CM_Campaigns` AS CC             ON CR.Campaign_Id=CC.id             LEFT JOIN `{dataset}.CM_Ads` AS CD             ON CR.Ad_Id=CD.id             LEFT JOIN `{dataset}.CM_Placements` AS CP             ON CR.Placement_Id=CP.id           ),            CCReportZip AS (             SELECT               R.* EXCEPT(Zip_Code, DMA),               STRUCT (                 R.Zip_Code,                 Z.city AS City,                 Z.county AS County,                 R.DMA,                 Z.state_code AS State_Code,                 Z.area_land_meters AS Area_Land_Meters               ) AS Location             FROM CCReport AS R             LEFT JOIN `bigquery-public-data.geo_us_boundaries.zip_codes` AS Z             ON Z.zip_code=R.Zip_Code           ),            CCReportPopulation AS (             SELECT               R.*,               C.pop_16_over AS Population             FROM CCReportZip AS R             LEFT JOIN `bigquery-public-data.census_bureau_acs.zip_codes_2018_5yr` AS C             ON R.Location.Zip_Code=C.geo_id           ),            CCReportMax AS (             SELECT               MAX(Population) AS Population,               MAX(SAFE_DIVIDE(Population, Location.Area_Land_Meters)) AS Density,               MAX(Impressions) AS Impression,               MAX(SAFE_DIVIDE(Impressions, Population)) AS Impression_Rate,               MAX(SAFE_DIVIDE(Impressions, Costs)) AS Impression_Cost,               MAX(Clicks) AS Click,               MAX(SAFE_DIVIDE(Clicks, Impressions)) AS Click_Rate,               MAX(SAFE_DIVIDE(Clicks, Costs)) AS Click_Cost,               MAX(Conversions) AS Conversion,               MAX(SAFE_DIVIDE(Conversions, Clicks)) AS Conversion_Rate,               MAX(SAFE_DIVIDE(Conversions, Costs)) AS Conversion_Cost,               MAX(Costs) AS Costs             FROM CCReportPopulation           ),            CCReportRanks AS (             SELECT               R.*,               STRUCT (                 ROUND(SAFE_DIVIDE(R.Population, M.Population),3) AS Population,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Population, Location.Area_Land_Meters), M.Density),3) AS Density,                 ROUND(SAFE_DIVIDE(R.Impressions, M.Impression),3) AS Impression,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Impressions,R.Population), M.Impression_Rate),3) AS Impression_Rate,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Impressions,R.Costs), M.Impression_Cost),3) AS Impression_Cost,                 ROUND(SAFE_DIVIDE(R.Clicks, M.Click),3) AS Click,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Clicks,R.Impressions),M.Click_Rate),3) AS Click_Rate,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Clicks, R.Costs), M.Click_Cost),3) AS Click_Cost,                 ROUND(SAFE_DIVIDE(R.Conversions, M.Conversion),3) AS Conversion,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Conversions, R.Clicks), M.Conversion_Rate),3) AS Conversion_Rate,                 ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Conversions, R.Costs), M.Conversion_Cost),3) AS Conversion_Cost,                 ROUND(SAFE_DIVIDE(R.Costs, M.Costs),3) AS Costs               ) AS Location_Ranking             FROM CCReportPopulation AS R             CROSS JOIN CCReportMax AS M           )            SELECT             'COHORT-A' AS Cohort,             Report_Day,             Advertiser,             Campaign,             Ad,             Placement,             Ad_Type,             Platform_Type,             Location,             Location_Ranking,             STRUCT(               Advertiser,               Campaign,               Ad,               Placement,               Population,               Impressions,               Clicks,               Conversions,               Costs             ) AS Cohort_A,             STRUCT(               '!COHORT-B' AS Advertiser,               '!COHORT-B' AS Campaign,               '!COHORT-B' AS Ad,               '!COHORT-B' AS Placement,               0 AS Population,               0 AS Impressions,               0 AS Clicks,               0 AS Conversions,               0 AS Costs             ) AS Cohort_B           FROM CCReportRanks           UNION ALL           SELECT             'COHORT-B' AS Cohort,             Report_Day,             Advertiser,             Campaign,             Ad,             Placement,             Ad_Type,             Platform_Type,             Location,             Location_Ranking,             STRUCT(               '!COHORT-A' AS Advertiser,               '!COHORT-A' AS Campaign,               '!COHORT-A' AS Ad,               '!COHORT-A' AS Placement,               0 AS Population,               0 AS Impressions,               0 AS Clicks,               0 AS Conversions,               0 AS Costs             ) AS Cohort_A,             STRUCT(               Advertiser,               Campaign,               Ad,               Placement,               Population,               Impressions,               Clicks,               Conversions,               Costs             ) AS Cohort_B,           FROM CCReportRanks",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
          'view':'Comparison_View'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'from':{
          'query':'SELECT * FROM `{dataset}.Comparison_View`',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Campaign_Comparison','default':'','description':'Name of dataset.'}},
          'table':'Comparison'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('cm360_campaign_comparison', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
