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

CM360 Geo Trends

Analyze performance against radius around specific locations.  Includes correlation to local landmarks and features derived from public data sets.



  - Add required parameters and run recipe.
  - After recipe completes make a copy of the 1-Geo Trends Dashboard.
  - Keep the data source as is on the copy screen. It will change later.
  - After the copy is made, click Edit->Resource->Manage Added Data Sources->CC_Report->Edit->Edit Connection.
  - Connect to the newly created BigQuery->->->GT_Dashboard table.
  - Or give these intructions to the client.

  1-Geo Trends Dashboard: https://datastudio.google.com/c/u/0/reporting/e34669ec-0894-4453-9ac4-ae9c3e739c48/page/p_pkxetkzemc'

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_bq':'user',  # Credentials used for reading data.
  'auth_cm':'user',  # Credentials used for reading data.
  'auth_sheet':'user',  # Credentials used for reading data.
  'recipe_slug':'',  # Existing BigQuery dataset.
  'account':12345,  # Campaign Manager Account ID
  'recipe_name':'',  # Name of sheet where Line Item settings will be read from.
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
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Geo_Trends','default':'','description':'Name of dataset.'}}
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
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Geo_Trends','default':'','description':'Name of dataset.'}},
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
          'fields':'advertisers.id,advertisers.name',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Geo_Trends','default':'','description':'Name of dataset.'}},
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
          'fields':'campaigns.id,campaigns.name',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Geo_Trends','default':'','description':'Name of dataset.'}},
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
          'fields':'ads.id,ads.name,ads.type',
          'accountId':{'field':{'name':'account','kind':'integer','order':1,'default':12345,'description':'Campaign Manager Account ID'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'service','description':'Authorization used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Geo_Trends','default':'','description':'Name of dataset.'}},
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
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'suffix':'_Geo_Trends','default':'','description':'Name of dataset.'}},
            'table':'CM_Placements'
          }
        }
      }
    },
    {
      'sheets':{
        'description':'Read locations from a sheet and place into BigQuery.',
        'auth':{'field':{'name':'auth_sheet','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'template':{
          'sheet':'https://docs.google.com/spreadsheets/d/12optvWdUCCzlQmEYjOFEnWodMNqY_5B29NqtAjNBss8/',
          'tab':'Locations'
        },
        'sheet':{'field':{'name':'recipe_name','kind':'string','prefix':'Geo Trends For ','order':2,'description':'Name of sheet where Line Item settings will be read from.','default':''}},
        'tab':'Locations',
        'range':'A2:M',
        'out':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}},
            'table':'SHEET_Locations',
            'schema':[
              {
                'name':'url',
                'type':'STRING'
              },
              {
                'name':'name',
                'type':'STRING'
              },
              {
                'name':'phone',
                'type':'STRING'
              },
              {
                'name':'latitude',
                'type':'FLOAT'
              },
              {
                'name':'longitude',
                'type':'FLOAT'
              },
              {
                'name':'addressstreet',
                'type':'STRING'
              },
              {
                'name':'addresslocality',
                'type':'STRING'
              },
              {
                'name':'addresspostal',
                'type':'STRING'
              },
              {
                'name':'addressregion',
                'type':'STRING'
              },
              {
                'name':'addressregionshort',
                'type':'STRING'
              },
              {
                'name':'addresscounrty',
                'type':'STRING'
              },
              {
                'name':'hours',
                'type':'STRING'
              },
              {
                'name':'services',
                'type':'STRING'
              }
            ]
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'from':{
          'query':"           WITH REPORT_REDUCED AS (             SELECT                CONCAT(CA.name, ' - ', CA.id) AS Advertiser,               CONCAT(CC.name, ' - ', CC.id) AS Campaign,               CONCAT(CD.name, ' - ', CD.id) AS Ad,               CONCAT(CP.name, ' - ', CP.id) AS Placement,               Zip_Postal_Code AS Zip_Code,               Designated_Market_Area_Dma AS DMA,               SUM(CR.Impressions) AS Impressions,               SUM(CR.Clicks) AS Clicks,               SUM(CAST(CR.Total_conversions AS INT64)) AS Conversions             FROM `{dataset}.CM_Report` AS CR             LEFT JOIN `{dataset}.CM_Advertisers` AS CA             ON CR.Advertiser_Id=CA.id             LEFT JOIN `{dataset}.CM_Campaigns` AS CC             ON CR.Campaign_Id=CC.id             LEFT JOIN `{dataset}.CM_Ads` AS CD             ON CR.Ad_Id=CD.id             LEFT JOIN `{dataset}.CM_Placements` AS CP             ON CR.Placement_Id=CP.id             GROUP BY 1,2,3,4,5           ),                      NEARBY_POSTAL AS (             SELECT               SLE.url AS Url,               POSTAL.zip_code AS Zip_Code,               ST_DISTANCE(POSTAL.zip_code_geom, SLE.geo_point) / 1609.34 AS distance_miles               FROM `{dataset}.SHEET_Locations` AS SLE             CROSS JOIN `bigquery-public-data.geo_us_boundaries.zip_codes` AS POSTAL             WHERE ST_DWithin(POSTAL.zip_code_geom , SLE.geo_point, 1609.34 * 50)           )                      SELECT             Advertiser,             Campaign,             Ad,             Placement,             Url,             STRUCT(               SUM(Impressions) AS all_mile,               SUM(IF(distance_miles <= 1, Impressions, 0)) AS walk_1_mile,               SUM(IF(distance_miles > 1 AND distance_miles <= 5, Impressions, 0)) AS commute_5_mile,               SUM(IF(distance_miles > 5 AND distance_miles <= 15, Impressions, 0)) AS drive_15_mile,               SUM(IF(distance_miles > 15 AND distance_miles <= 50, Impressions, 0)) AS travel_50_mile             ) AS Impressions,             STRUCT(               SUM(Clicks) AS all_mile,               SUM(IF(distance_miles <= 1, Clicks, 0)) AS walk_1_mile,               SUM(IF(distance_miles > 1 AND distance_miles <= 5, Clicks, 0)) AS commute_5_mile,               SUM(IF(distance_miles > 5 AND distance_miles <= 15, Clicks, 0)) AS drive_15_mile,               SUM(IF(distance_miles > 15 AND distance_miles <= 50, Clicks, 0)) AS travel_50_mile             ) AS Clicks,             STRUCT(               SUM(Conversions) AS all_mile,               SUM(IF(distance_miles <= 1, Conversions, 0)) AS walk_1_mile,               SUM(IF(distance_miles > 1 AND distance_miles <= 5, Conversions, 0)) AS commute_5_mile,               SUM(IF(distance_miles > 5 AND distance_miles <= 15, Conversions, 0)) AS drive_15_mile,               SUM(IF(distance_miles > 15 AND distance_miles <= 50, Conversions, 0)) AS travel_50_mile             ) AS Conversions           FROM REPORT_REDUCED           RIGHT JOIN NEARBY_POSTAL USING(Zip_Code)           GROUP BY Advertiser, Campaign, Ad, Placement, Url         ",
          'legacy':False,
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':3,'description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Existing BigQuery dataset.'}},
          'view':'GT_Report'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'run':{
          'query':"           CREATE OR REPLACE FUNCTION `{dataset}`.hours_to_struct(hours ARRAY<STRING>)           RETURNS ARRAY<STRUCT<day STRING, open STRING, close STRING, twenty_four BOOL>>           LANGUAGE js AS '''             var results = [];             var i;             if (hours != null) {               for(i = 0; i < hours.length; i++)               {                 var fields = hours[i].split('-');                 results.push({                   'day':fields[0],                   'open':fields[1],                   'close':fields[2],                   'twenty_four': fields[1] == fields[2]                 })               }             }             return results;           ''';         ",
          'legacy':False,
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':3,'description':'Place where tables will be written in BigQuery.'}}
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'from':{
          'query':"SELECT           * EXCEPT(services, hours, longitude, latitude),           ST_GEOGPOINT(longitude, latitude) AS geo_point,           `{dataset}`.hours_to_struct(SPLIT(hours, '|')) AS hours,           SPLIT(services, '|') AS services,         FROM `{dataset}.SHEET_Locations`",
          'legacy':False,
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':3,'description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Existing BigQuery dataset.'}},
          'view':'GT_Locations'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'from':{
          'query':"           NEARBY AS (             SELECT                url,               ARRAY_AGG(                 STRUCT(                   Category,                   Label,                   Quantity,                   Distance                 )               ) AS Nearby             FROM (               SELECT                 SLE.url AS url,                   A.key AS Category,                 A.value AS Label,                 COUNT(*) AS Quantity,                 MIN(ST_Distance(SLE.geo_point, PF.geometry)) / 1609.34 AS Distance               FROM `bigquery-public-data.geo_openstreetmap.planet_features` AS PF, UNNEST(all_tags) AS A               CROSS JOIN `{dataset}.Store_Locations_Expanded` AS SLE               WHERE ST_DWithin(SLE.geo_point, PF.geometry, 1609.34 * 50)               AND A.key IN ('amenity', 'brand', 'cuisine', 'highway', 'sport', 'shop', 'natural', 'sport', 'man_made', 'leisure')               AND A.value != 'yes'               GROUP BY Url, Category, Label               ORDER BY 2             )             GROUP BY 1           )                      SELECT             SLE.*,             NEARBY.* Except(url),           FROM `{dataset}.Store_Locations_Expanded` AS SLE           LEFT JOIN NEARBY USING(url)         ",
          'legacy':False,
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':3,'description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Existing BigQuery dataset.'}},
          'view':'GT_Nearby'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'from':{
          'query':'           SELECT             S.*,             R.* EXCEPT(Url)           FROM `{dataset}.GT_Nearby` AS S           LEFT JOIN `{dataset}.GT_Report` AS R USING (Url)         ',
          'legacy':False,
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':3,'description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'','description':'Existing BigQuery dataset.'}},
          'view':'GT_Dashboard'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('cm360_geo_trends', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
