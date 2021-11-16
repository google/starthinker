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
from starthinker.task.bigquery.run import bigquery


def recipe_cm360_campaign_comparison(config, auth_bq, auth_cm, recipe_slug, account, recipe_name, advertiser, relativeDateRange):
  """Group KPIs into cohorts and compare performance across time and geography.
     Quickly discover where national and local campaigns need to be targeted,
     funded, or optimized.

     Args:
       auth_bq (authentication) - Credentials used for reading data.
       auth_cm (authentication) - Credentials used for reading data.
       recipe_slug (string) - Name of dataset.
       account (integer) - Campaign Manager Account ID
       recipe_name (string) - Name of report.
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
      'fields':'advertisers.id,advertisers.name,nextPageToken',
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
      'fields':'campaigns.id,campaigns.name,nextPageToken',
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
      'fields':'ads.id,ads.name,ads.type,nextPageToken',
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

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'query':'''WITH
         CCReport AS (
           SELECT
             Report_Day,
             CONCAT(CA.name, ' - ', CA.id) AS Advertiser,
             CONCAT(CC.name, ' - ', CC.id) AS Campaign,
             CONCAT(CD.name, ' - ', CD.id) AS Ad,
             CONCAT(CP.name, ' - ', CP.id) AS Placement,
             CR.Platform_Type AS Platform_Type,
             CD.type AS Ad_Type,
             Zip_Postal_Code AS Zip_Code,
             Designated_Market_Area_Dma AS DMA,
             CR.Impressions AS Impressions,
             CR.Clicks AS Clicks,
             CAST(CR.Total_conversions AS INT64) AS Conversions,
             CR.Media_Cost AS Costs
           FROM `{dataset}.CM_Report` AS CR
           LEFT JOIN `{dataset}.CM_Advertisers` AS CA
           ON CR.Advertiser_Id=CA.id
           LEFT JOIN `{dataset}.CM_Campaigns` AS CC
           ON CR.Campaign_Id=CC.id
           LEFT JOIN `{dataset}.CM_Ads` AS CD
           ON CR.Ad_Id=CD.id
           LEFT JOIN `{dataset}.CM_Placements` AS CP
           ON CR.Placement_Id=CP.id
         ),
          CCReportZip AS (
           SELECT
             R.* EXCEPT(Zip_Code, DMA),
             STRUCT (
               R.Zip_Code,
               Z.city AS City,
               Z.county AS County,
               R.DMA,
               Z.state_code AS State_Code,
               Z.area_land_meters AS Area_Land_Meters
             ) AS Location
           FROM CCReport AS R
           LEFT JOIN `bigquery-public-data.geo_us_boundaries.zip_codes` AS Z
           ON Z.zip_code=R.Zip_Code
         ),
          CCReportPopulation AS (
           SELECT
             R.*,
             C.pop_16_over AS Population
           FROM CCReportZip AS R
           LEFT JOIN `bigquery-public-data.census_bureau_acs.zip_codes_2018_5yr` AS C
           ON R.Location.Zip_Code=C.geo_id
         ),
          CCReportMax AS (
           SELECT
             MAX(Population) AS Population,
             MAX(SAFE_DIVIDE(Population, Location.Area_Land_Meters)) AS Density,
             MAX(Impressions) AS Impression,
             MAX(SAFE_DIVIDE(Impressions, Population)) AS Impression_Rate,
             MAX(SAFE_DIVIDE(Impressions, Costs)) AS Impression_Cost,
             MAX(Clicks) AS Click,
             MAX(SAFE_DIVIDE(Clicks, Impressions)) AS Click_Rate,
             MAX(SAFE_DIVIDE(Clicks, Costs)) AS Click_Cost,
             MAX(Conversions) AS Conversion,
             MAX(SAFE_DIVIDE(Conversions, Clicks)) AS Conversion_Rate,
             MAX(SAFE_DIVIDE(Conversions, Costs)) AS Conversion_Cost,
             MAX(Costs) AS Costs
           FROM CCReportPopulation
         ),
          CCReportRanks AS (
           SELECT
             R.*,
             STRUCT (
               ROUND(SAFE_DIVIDE(R.Population, M.Population),3) AS Population,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Population, Location.Area_Land_Meters), M.Density),3) AS Density,
               ROUND(SAFE_DIVIDE(R.Impressions, M.Impression),3) AS Impression,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Impressions,R.Population), M.Impression_Rate),3) AS Impression_Rate,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Impressions,R.Costs), M.Impression_Cost),3) AS Impression_Cost,
               ROUND(SAFE_DIVIDE(R.Clicks, M.Click),3) AS Click,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Clicks,R.Impressions),M.Click_Rate),3) AS Click_Rate,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Clicks, R.Costs), M.Click_Cost),3) AS Click_Cost,
               ROUND(SAFE_DIVIDE(R.Conversions, M.Conversion),3) AS Conversion,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Conversions, R.Clicks), M.Conversion_Rate),3) AS Conversion_Rate,
               ROUND(SAFE_DIVIDE(SAFE_DIVIDE(R.Conversions, R.Costs), M.Conversion_Cost),3) AS Conversion_Cost,
               ROUND(SAFE_DIVIDE(R.Costs, M.Costs),3) AS Costs
             ) AS Location_Ranking
           FROM CCReportPopulation AS R
           CROSS JOIN CCReportMax AS M
         )
          SELECT
           'COHORT-A' AS Cohort,
           Report_Day,
           Advertiser,
           Campaign,
           Ad,
           Placement,
           Ad_Type,
           Platform_Type,
           Location,
           Location_Ranking,
           STRUCT(
             Advertiser,
             Campaign,
             Ad,
             Placement,
             Population,
             Impressions,
             Clicks,
             Conversions,
             Costs
           ) AS Cohort_A,
           STRUCT(
             '!COHORT-B' AS Advertiser,
             '!COHORT-B' AS Campaign,
             '!COHORT-B' AS Ad,
             '!COHORT-B' AS Placement,
             0 AS Population,
             0 AS Impressions,
             0 AS Clicks,
             0 AS Conversions,
             0 AS Costs
           ) AS Cohort_B
         FROM CCReportRanks
         UNION ALL
         SELECT
           'COHORT-B' AS Cohort,
           Report_Day,
           Advertiser,
           Campaign,
           Ad,
           Placement,
           Ad_Type,
           Platform_Type,
           Location,
           Location_Ranking,
           STRUCT(
             '!COHORT-A' AS Advertiser,
             '!COHORT-A' AS Campaign,
             '!COHORT-A' AS Ad,
             '!COHORT-A' AS Placement,
             0 AS Population,
             0 AS Impressions,
             0 AS Clicks,
             0 AS Conversions,
             0 AS Costs
           ) AS Cohort_A,
           STRUCT(
             Advertiser,
             Campaign,
             Ad,
             Placement,
             Population,
             Impressions,
             Clicks,
             Conversions,
             Costs
           ) AS Cohort_B,
         FROM CCReportRanks''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Comparison_View'
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'query':'SELECT * FROM `{dataset}.Comparison_View`',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'table':'Comparison'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Group KPIs into cohorts and compare performance across time and geography. Quickly discover where national and local campaigns need to be targeted, funded, or optimized.

      1. Add required parameters and run recipe.
      2. After recipe completes make a copy of the 1-Campaign Comparison Dashboard.
         2.1 - Campaign Comparison Dashboard: https://datastudio.google.com/c/u/0/reporting/e34669ec-0894-4453-9ac4-ae9c3e739c48/page/p_pkxetkzemc
      3. Keep the data source as is on the copy screen. It will change later.
      4. After the copy is made, click Edit->Resource->Manage Added Data Sources->CC_Report->Edit->Edit Connection.
      5. Connect to the newly created BigQuery->->_Campaign_Comparison->Comparison table.
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
  parser.add_argument("-recipe_slug", help="Name of dataset.", default='')
  parser.add_argument("-account", help="Campaign Manager Account ID", default=12345)
  parser.add_argument("-recipe_name", help="Name of report.", default='')
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

  recipe_cm360_campaign_comparison(config, args.auth_bq, args.auth_cm, args.recipe_slug, args.account, args.recipe_name, args.advertiser, args.relativeDateRange)
