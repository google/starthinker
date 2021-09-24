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

DV360 Deal Finder

Compares open vs. deal CPM, CPC, and CPA so that clients can decide which sites, inventory, and deals work best.

  - Wait for <b>BigQuery->->->Deal_Finder_Dashboard</b> to be created.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/open/1QrWNTurvQT6nx20vnzdDveSzSmRjqHxQ' target='_blank'>Deal Finder Sample Data</a>.
  - Click Edit Connection, and change to <b>BigQuery->StarThinker Data->->Deal_Finder_Dashboard</b>.
  - Copy <a href='https://datastudio.google.com/open/1fjRI5AIKTYTA4fWs-pYkJbIMgCumlMyO' target='_blank'>Deal Finder Sample Report</a>.
  - When prompted choose the new data source you just created.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug':'',  # Place where tables will be written in BigQuery.
  'recipe_timezone':'America/Los_Angeles',  # Timezone for report dates.
  'recipe_name':'',  # Name of report in DV360, should be unique.
  'auth_write':'service',  # Credentials used for writing data.
  'auth_read':'user',  # Credentials used for reading data.
  'partners':[],  # DV360 partner id.
  'advertisers':[],  # Comma delimited list of DV360 advertiser ids.
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
      3,
      4
    ]
  },
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
      'dbm':{
        'description':'Create a DV360 report.',
        'hour':[
          3
        ],
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'filters':{
            'FILTER_PARTNER':{
              'values':{'field':{'name':'partners','kind':'integer_list','order':5,'default':[],'description':'DV360 partner id.'}}
            },
            'FILTER_ADVERTISER':{
              'values':{'field':{'name':'advertisers','kind':'integer_list','order':6,'default':[],'description':'Comma delimited list of DV360 advertiser ids.'}}
            }
          },
          'body':{
            'timezoneCode':{'field':{'name':'recipe_timezone','kind':'timezone','description':'Timezone for report dates.','default':'America/Los_Angeles'}},
            'metadata':{
              'title':{'field':{'name':'recipe_name','kind':'string','prefix':'Deal Finder For ','description':'Name of report in DV360, should be unique.'}},
              'dataRange':'LAST_30_DAYS',
              'format':'CSV'
            },
            'params':{
              'type':'TYPE_CROSS_PARTNER',
              'groupBys':[
                'FILTER_PARTNER_NAME',
                'FILTER_PARTNER',
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_APP_URL',
                'FILTER_SITE_ID',
                'FILTER_INVENTORY_SOURCE_NAME',
                'FILTER_INVENTORY_SOURCE',
                'FILTER_INVENTORY_SOURCE_TYPE',
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_CREATIVE_WIDTH',
                'FILTER_CREATIVE_HEIGHT',
                'FILTER_CREATIVE_TYPE'
              ],
              'metrics':[
                'METRIC_IMPRESSIONS',
                'METRIC_CLICKS',
                'METRIC_TOTAL_CONVERSIONS',
                'METRIC_TOTAL_MEDIA_COST_ADVERTISER',
                'METRIC_REVENUE_ADVERTISER',
                'METRIC_ACTIVE_VIEW_MEASURABLE_IMPRESSIONS',
                'METRIC_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS'
              ]
            }
          }
        }
      }
    },
    {
      'dbm':{
        'description':'Copy a DV360 report to BigQuery.',
        'hour':[
          4
        ],
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'name':{'field':{'name':'recipe_name','kind':'string','prefix':'Deal Finder For ','description':'Name of report in DV360, should be unique.'}},
          'timeout':10
        },
        'out':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
            'table':'Deal_Finder_DV360_Report',
            'header':True,
            'schema':[
              {
                'name':'Partner',
                'type':'STRING'
              },
              {
                'name':'Partner_ID',
                'type':'INTEGER'
              },
              {
                'name':'Advertiser',
                'type':'STRING'
              },
              {
                'name':'Advertiser_ID',
                'type':'INTEGER'
              },
              {
                'name':'Site',
                'type':'STRING'
              },
              {
                'name':'Site_ID',
                'type':'INTEGER'
              },
              {
                'name':'Inventory',
                'type':'STRING',
                'mode':'NULLABLE'
              },
              {
                'name':'Inventory_ID',
                'type':'INTEGER',
                'mode':'NULLABLE'
              },
              {
                'name':'Inventory_Type',
                'type':'STRING'
              },
              {
                'name':'Advertiser_Currency',
                'type':'STRING'
              },
              {
                'name':'Creative_Width',
                'type':'STRING',
                'mode':'NULLABLE'
              },
              {
                'name':'Creative_Height',
                'type':'STRING',
                'mode':'NULLABLE'
              },
              {
                'name':'Creative_Type',
                'type':'STRING'
              },
              {
                'name':'Impressions',
                'type':'INTEGER'
              },
              {
                'name':'Clicks',
                'type':'INTEGER'
              },
              {
                'name':'Conversions',
                'type':'FLOAT'
              },
              {
                'name':'Cost',
                'type':'FLOAT'
              },
              {
                'name':'Revenue',
                'type':'FLOAT'
              },
              {
                'name':'AV_Impressions_Measurable',
                'type':'INTEGER'
              },
              {
                'name':'AV_Impressions_Viewable',
                'type':'INTEGER'
              }
            ]
          }
        }
      }
    },
    {
      'bigquery':{
        'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
        'hour':[
          4
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'query':"SELECT Partner, Partner_ID, Advertiser, Advertiser_ID, Site, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Size, Always_On, Deal_Impressions, Open_Impressions, Rank_Impressions, Deal_Clicks, Open_Clicks, Rank_Clicks, Deal_Conversions, Open_Conversions, Rank_Conversions, Deal_Impressions_Viewable, Open_Impressions_Viewable, Rank_Impressions_Viewable, Deal_Impressions_Measurable, Open_Impressions_Measurable, Rank_Impressions_Measurable, Deal_Cost, Open_Cost, Rank_Cost, FROM ( SELECT FIRST(Partner) AS Partner, FIRST(Partner_ID) AS Partner_ID, FIRST(Advertiser) AS Advertiser, Advertiser_ID, First(Site) AS Site, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Width + ' x ' + Creative_Height AS Creative_Size, IF (LEFT(Inventory, 5) == 'AO - ', True, False) AS Always_On, SUM(Deal_Impressions) AS Deal_Impressions, SUM(Open_Impressions) AS Open_Impressions, SUM(Open_Impressions) + SUM(Deal_Impressions) AS Total_Impressions, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Impressions DESC) AS Rank_Impressions, SUM(Deal_Clicks) AS Deal_Clicks, SUM(Open_Clicks) AS Open_Clicks, SUM(Open_Clicks) + SUM(Deal_Clicks) AS Total_Clicks, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Clicks DESC) AS Rank_Clicks, SUM(Deal_Conversions) AS Deal_Conversions, SUM(Open_Conversions) AS Open_Conversions, SUM(Open_Conversions) + SUM(Deal_Conversions) AS Total_Conversions, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Conversions DESC) AS Rank_Conversions, SUM(Deal_Cost) AS Deal_Cost, SUM(Open_Cost) AS Open_Cost, SUM(Open_Cost) + SUM(Deal_Cost) AS Total_Cost, RANK() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Cost DESC) AS Rank_Cost, SUM(Deal_Impressions_Viewable) AS Deal_Impressions_Viewable, SUM(Open_Impressions_Viewable) AS Open_Impressions_Viewable, SUM(Open_Impressions_Viewable) + SUM(Deal_Impressions_Viewable) AS Total_Impressions_Viewable, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Impressions_Viewable DESC) AS Rank_Impressions_Viewable, SUM(Deal_Impressions_Measurable) AS Deal_Impressions_Measurable, SUM(Open_Impressions_Measurable) AS Open_Impressions_Measurable, SUM(Open_Impressions_Measurable) + SUM(Deal_Impressions_Measurable) AS Total_Impressions_Measurable, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Impressions_Measurable DESC) AS Rank_Impressions_Measurable, FROM ( SELECT Partner, Partner_ID, Advertiser, Advertiser_ID, Site, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Width, Creative_Height, IF(Inventory_ID IS NULL, Impressions, 0) AS Open_Impressions, IF(Inventory_ID IS NULL, 0, Impressions) AS Deal_Impressions, IF(Inventory_ID IS NULL, Clicks, 0) AS Open_Clicks, IF(Inventory_ID IS NULL, 0, Clicks) AS Deal_Clicks, IF(Inventory_ID IS NULL, Conversions, 0) AS Open_Conversions, IF(Inventory_ID IS NULL, 0, Conversions) AS Deal_Conversions, IF(Inventory_ID IS NULL, Cost, 0) AS Open_Cost, IF(Inventory_ID IS NULL, 0, Cost) AS Deal_Cost, IF(Inventory_ID IS NULL, AV_Impressions_Viewable, 0) AS Open_Impressions_Viewable, IF(Inventory_ID IS NULL, 0, AV_Impressions_Viewable) AS Deal_Impressions_Viewable, IF(Inventory_ID IS NULL, AV_Impressions_Measurable, 0) AS Open_Impressions_Measurable, IF(Inventory_ID IS NULL, 0, AV_Impressions_Measurable) AS Deal_Impressions_Measurable, FROM [[PARAMETER].Deal_Finder_DV360_Report] OMIT RECORD IF Site == 'Low volume inventory') GROUP By Advertiser_ID, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Size, Always_On) WHERE Rank_Impressions < 100 OR Rank_Clicks < 100 OR Rank_Conversions < 100 OR Rank_Cost < 100;",
          'parameters':[
            {'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          ]
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Deal_Finder_Dashboard'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('deal_finder', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
