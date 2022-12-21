###########################################################################
#
#  Copyright 2021 Google LLC
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
#  This code generated (see scripts folder for possible source):
#    - Command: "python starthinker_ui/manage.py example"
#
###########################################################################

import argparse
import textwrap

from starthinker.util.configuration import Configuration
from starthinker.task.dataset.run import dataset
from starthinker.task.dcm.run import dcm
from starthinker.task.google_api.run import google_api
from starthinker.task.sheets.run import sheets
from starthinker.task.bigquery.run import bigquery


def recipe_cm360_geo_trends(config, auth_bq, auth_cm, auth_sheet, recipe_slug, account, recipe_name, advertiser, relativeDateRange):
  """Analyze performance against radius around specific locations.  Includes
     correlation to local landmarks and features derived from public data sets.

     Args:
       auth_bq (authentication) - Credentials used for reading data.
       auth_cm (authentication) - Credentials used for reading data.
       auth_sheet (authentication) - Credentials used for reading data.
       recipe_slug (string) - Existing BigQuery dataset.
       account (integer) - Campaign Manager Account ID
       recipe_name (string) - Name of sheet where Line Item settings will be read from.
       advertiser (integer_list) - Optional comma delimited list of ids.
       relativeDateRange (choice) - Timeframe to run the report for.
  """

  dataset(config, {
    'description':'Create a dataset for bigquery tables.',
    'auth':auth_bq,
    'dataset':recipe_slug
  })

  dcm(config, {
    'description':'Create KPI report.',
    'auth':auth_cm,
    'report':{
      'account':account,
      'name':recipe_name,
      'body':{
        'kind':'dfareporting#report',
        'format':'CSV',
        'type':'STANDARD',
        'criteria':{
          'dateRange':{
            'kind':'dfareporting#dateRange',
            'relativeDateRange':relativeDateRange
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
          'values':advertiser
        }
      }
    }
  })

  dcm(config, {
    'description':'Download KPI report.',
    'auth':auth_cm,
    'report':{
      'account':account,
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'CM_Report',
        'header':True
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.5',
    'function':'advertisers.list',
    'iterate':True,
    'kwargs':{
      'fields':'advertisers.id,advertisers.name',
      'accountId':account
    },
    'results':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'CM_Advertisers'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.5',
    'function':'campaigns.list',
    'iterate':True,
    'kwargs':{
      'fields':'campaigns.id,campaigns.name',
      'accountId':account
    },
    'results':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'CM_Campaigns'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.5',
    'function':'ads.list',
    'iterate':True,
    'kwargs':{
      'fields':'ads.id,ads.name,ads.type',
      'accountId':account
    },
    'results':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'CM_Ads'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.5',
    'function':'placements.list',
    'iterate':True,
    'kwargs':{
      'fields':'placements.id,placements.name',
      'accountId':account
    },
    'results':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'CM_Placements'
      }
    }
  })

  sheets(config, {
    'description':'Read locations from a sheet and place into BigQuery.',
    'auth':auth_sheet,
    'template':{
      'sheet':'https://docs.google.com/spreadsheets/d/12optvWdUCCzlQmEYjOFEnWodMNqY_5B29NqtAjNBss8/',
      'tab':'Locations'
    },
    'sheet':recipe_name,
    'tab':'Locations',
    'range':'A2:M',
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
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
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'query':'''
         WITH REPORT_REDUCED AS (
           SELECT
             CONCAT(CA.name, ' - ', CA.id) AS Advertiser,
             CONCAT(CC.name, ' - ', CC.id) AS Campaign,
             CONCAT(CD.name, ' - ', CD.id) AS Ad,
             CONCAT(CP.name, ' - ', CP.id) AS Placement,
             Zip_Postal_Code AS Zip_Code,
             Designated_Market_Area_Dma AS DMA,
             SUM(CR.Impressions) AS Impressions,
             SUM(CR.Clicks) AS Clicks,
             SUM(CAST(CR.Total_conversions AS INT64)) AS Conversions
           FROM `{dataset}.CM_Report` AS CR
           LEFT JOIN `{dataset}.CM_Advertisers` AS CA
           ON CR.Advertiser_Id=CA.id
           LEFT JOIN `{dataset}.CM_Campaigns` AS CC
           ON CR.Campaign_Id=CC.id
           LEFT JOIN `{dataset}.CM_Ads` AS CD
           ON CR.Ad_Id=CD.id
           LEFT JOIN `{dataset}.CM_Placements` AS CP
           ON CR.Placement_Id=CP.id
           GROUP BY 1,2,3,4,5
         ),
          NEARBY_POSTAL AS (
           SELECT
             SLE.url AS Url,
             POSTAL.zip_code AS Zip_Code,
             ST_DISTANCE(POSTAL.zip_code_geom, SLE.geo_point) / 1609.34 AS distance_miles
             FROM `{dataset}.SHEET_Locations` AS SLE
           CROSS JOIN `bigquery-public-data.geo_us_boundaries.zip_codes` AS POSTAL
           WHERE ST_DWithin(POSTAL.zip_code_geom , SLE.geo_point, 1609.34 * 50)
         )
          SELECT
           Advertiser,
           Campaign,
           Ad,
           Placement,
           Url,
           STRUCT(
             SUM(Impressions) AS all_mile,
             SUM(IF(distance_miles <= 1, Impressions, 0)) AS walk_1_mile,
             SUM(IF(distance_miles > 1 AND distance_miles <= 5, Impressions, 0)) AS commute_5_mile,
             SUM(IF(distance_miles > 5 AND distance_miles <= 15, Impressions, 0)) AS drive_15_mile,
             SUM(IF(distance_miles > 15 AND distance_miles <= 50, Impressions, 0)) AS travel_50_mile
           ) AS Impressions,
           STRUCT(
             SUM(Clicks) AS all_mile,
             SUM(IF(distance_miles <= 1, Clicks, 0)) AS walk_1_mile,
             SUM(IF(distance_miles > 1 AND distance_miles <= 5, Clicks, 0)) AS commute_5_mile,
             SUM(IF(distance_miles > 5 AND distance_miles <= 15, Clicks, 0)) AS drive_15_mile,
             SUM(IF(distance_miles > 15 AND distance_miles <= 50, Clicks, 0)) AS travel_50_mile
           ) AS Clicks,
           STRUCT(
             SUM(Conversions) AS all_mile,
             SUM(IF(distance_miles <= 1, Conversions, 0)) AS walk_1_mile,
             SUM(IF(distance_miles > 1 AND distance_miles <= 5, Conversions, 0)) AS commute_5_mile,
             SUM(IF(distance_miles > 5 AND distance_miles <= 15, Conversions, 0)) AS drive_15_mile,
             SUM(IF(distance_miles > 15 AND distance_miles <= 50, Conversions, 0)) AS travel_50_mile
           ) AS Conversions
         FROM REPORT_REDUCED
         RIGHT JOIN NEARBY_POSTAL USING(Zip_Code)
         GROUP BY Advertiser, Campaign, Ad, Placement, Url         ''',
      'legacy':False,
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'GT_Report'
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'run':{
      'query':'''
         CREATE OR REPLACE FUNCTION `{dataset}`.hours_to_struct(hours ARRAY<STRING>)
         RETURNS ARRAY<STRUCT<day STRING, open STRING, close STRING, twenty_four BOOL>>
         LANGUAGE js AS '''
           var results = [];
           var i;
           if (hours != null) {
             for(i = 0; i < hours.length; i++)
             {
               var fields = hours[i].split('-');
               results.push({
                 'day':fields[0],
                 'open':fields[1],
                 'close':fields[2],
                 'twenty_four': fields[1] == fields[2]
               })
             }
           }
           return results;
         ''';         ''',
      'legacy':False,
      'parameters':{
        'dataset':recipe_slug
      }
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'query':'''SELECT
         * EXCEPT(services, hours, longitude, latitude),
         ST_GEOGPOINT(longitude, latitude) AS geo_point,
         `{dataset}`.hours_to_struct(SPLIT(hours, '|')) AS hours,
         SPLIT(services, '|') AS services,         FROM `{dataset}.SHEET_Locations`''',
      'legacy':False,
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'GT_Locations'
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'query':'''
         NEARBY AS (
           SELECT
             url,
             ARRAY_AGG(
               STRUCT(
                 Category,
                 Label,
                 Quantity,
                 Distance
               )
             ) AS Nearby
           FROM (
             SELECT
               SLE.url AS url,
               A.key AS Category,
               A.value AS Label,
               COUNT(*) AS Quantity,
               MIN(ST_Distance(SLE.geo_point, PF.geometry)) / 1609.34 AS Distance
             FROM `bigquery-public-data.geo_openstreetmap.planet_features` AS PF, UNNEST(all_tags) AS A
             CROSS JOIN `{dataset}.Store_Locations_Expanded` AS SLE
             WHERE ST_DWithin(SLE.geo_point, PF.geometry, 1609.34 * 50)
             AND A.key IN ('amenity', 'brand', 'cuisine', 'highway', 'sport', 'shop', 'natural', 'sport', 'man_made', 'leisure')
             AND A.value != 'yes'
             GROUP BY Url, Category, Label
             ORDER BY 2
           )
           GROUP BY 1
         )
          SELECT
           SLE.*,
           NEARBY.* Except(url),
         FROM `{dataset}.Store_Locations_Expanded` AS SLE
         LEFT JOIN NEARBY USING(url)         ''',
      'legacy':False,
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'GT_Nearby'
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'query':'''
         SELECT
           S.*,
           R.* EXCEPT(Url)
         FROM `{dataset}.GT_Nearby` AS S
         LEFT JOIN `{dataset}.GT_Report` AS R USING (Url)         ''',
      'legacy':False,
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'GT_Dashboard'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Analyze performance against radius around specific locations.  Includes correlation to local landmarks and features derived from public data sets.

      1. Add required parameters and run recipe.
      2. After recipe completes make a copy of the 1-Geo Trends Dashboard.
         2.1 - Geo Trends Dashboard: https://datastudio.google.com/c/u/0/reporting/e34669ec-0894-4453-9ac4-ae9c3e739c48/page/p_pkxetkzemc'
      3. Keep the data source as is on the copy screen. It will change later.
      4. After the copy is made, click Edit->Resource->Manage Added Data Sources->CC_Report->Edit->Edit Connection.
      5. Connect to the newly created BigQuery->->->GT_Dashboard table.
      6. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_bq", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_cm", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_sheet", help="Credentials used for reading data.", default='user')
  parser.add_argument("-recipe_slug", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-account", help="Campaign Manager Account ID", default=12345)
  parser.add_argument("-recipe_name", help="Name of sheet where Line Item settings will be read from.", default='')
  parser.add_argument("-advertiser", help="Optional comma delimited list of ids.", default=[])
  parser.add_argument("-relativeDateRange", help="Timeframe to run the report for.", default='LAST_365_DAYS')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm360_geo_trends(config, args.auth_bq, args.auth_cm, args.auth_sheet, args.recipe_slug, args.account, args.recipe_name, args.advertiser, args.relativeDateRange)
