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
from starthinker.task.dbm.run import dbm
from starthinker.task.bigquery.run import bigquery


def recipe_deal_finder(config, recipe_slug, recipe_timezone, recipe_name, auth_write, auth_read, partners, advertisers):
  """Compares open vs. deal CPM, CPC, and CPA so that clients can decide which sites,
     inventory, and deals work best.

     Args:
       recipe_slug (string) - Place where tables will be written in BigQuery.
       recipe_timezone (timezone) - Timezone for report dates.
       recipe_name (string) - Name of report in DV360, should be unique.
       auth_write (authentication) - Credentials used for writing data.
       auth_read (authentication) - Credentials used for reading data.
       partners (integer_list) - DV360 partner id.
       advertisers (integer_list) - Comma delimited list of DV360 advertiser ids.
  """

  dataset(config, {
    'description':'Create a dataset for bigquery tables.',
    'hour':[
      4
    ],
    'auth':auth_write,
    'dataset':recipe_slug
  })

  dbm(config, {
    'description':'Create a DV360 report.',
    'hour':[
      3
    ],
    'auth':auth_read,
    'report':{
      'filters':{
        'FILTER_PARTNER':{
          'values':partners
        },
        'FILTER_ADVERTISER':{
          'values':advertisers
        }
      },
      'body':{
        'timezoneCode':recipe_timezone,
        'metadata':{
          'title':recipe_name,
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
  })

  dbm(config, {
    'description':'Copy a DV360 report to BigQuery.',
    'hour':[
      4
    ],
    'auth':auth_read,
    'report':{
      'name':recipe_name,
      'timeout':10
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
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
  })

  bigquery(config, {
    'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
    'hour':[
      4
    ],
    'auth':auth_write,
    'from':{
      'query':'SELECT Partner, Partner_ID, Advertiser, Advertiser_ID, Site, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Size, Always_On, Deal_Impressions, Open_Impressions, Rank_Impressions, Deal_Clicks, Open_Clicks, Rank_Clicks, Deal_Conversions, Open_Conversions, Rank_Conversions, Deal_Impressions_Viewable, Open_Impressions_Viewable, Rank_Impressions_Viewable, Deal_Impressions_Measurable, Open_Impressions_Measurable, Rank_Impressions_Measurable, Deal_Cost, Open_Cost, Rank_Cost, FROM ( SELECT FIRST(Partner) AS Partner, FIRST(Partner_ID) AS Partner_ID, FIRST(Advertiser) AS Advertiser, Advertiser_ID, First(Site) AS Site, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Width + ' x ' + Creative_Height AS Creative_Size, IF (LEFT(Inventory, 5) == 'AO - ', True, False) AS Always_On, SUM(Deal_Impressions) AS Deal_Impressions, SUM(Open_Impressions) AS Open_Impressions, SUM(Open_Impressions) + SUM(Deal_Impressions) AS Total_Impressions, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Impressions DESC) AS Rank_Impressions, SUM(Deal_Clicks) AS Deal_Clicks, SUM(Open_Clicks) AS Open_Clicks, SUM(Open_Clicks) + SUM(Deal_Clicks) AS Total_Clicks, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Clicks DESC) AS Rank_Clicks, SUM(Deal_Conversions) AS Deal_Conversions, SUM(Open_Conversions) AS Open_Conversions, SUM(Open_Conversions) + SUM(Deal_Conversions) AS Total_Conversions, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Conversions DESC) AS Rank_Conversions, SUM(Deal_Cost) AS Deal_Cost, SUM(Open_Cost) AS Open_Cost, SUM(Open_Cost) + SUM(Deal_Cost) AS Total_Cost, RANK() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Cost DESC) AS Rank_Cost, SUM(Deal_Impressions_Viewable) AS Deal_Impressions_Viewable, SUM(Open_Impressions_Viewable) AS Open_Impressions_Viewable, SUM(Open_Impressions_Viewable) + SUM(Deal_Impressions_Viewable) AS Total_Impressions_Viewable, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Impressions_Viewable DESC) AS Rank_Impressions_Viewable, SUM(Deal_Impressions_Measurable) AS Deal_Impressions_Measurable, SUM(Open_Impressions_Measurable) AS Open_Impressions_Measurable, SUM(Open_Impressions_Measurable) + SUM(Deal_Impressions_Measurable) AS Total_Impressions_Measurable, ROW_NUMBER() OVER (PARTITION BY Advertiser_ID ORDER BY Total_Impressions_Measurable DESC) AS Rank_Impressions_Measurable, FROM ( SELECT Partner, Partner_ID, Advertiser, Advertiser_ID, Site, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Width, Creative_Height, IF(Inventory_ID IS NULL, Impressions, 0) AS Open_Impressions, IF(Inventory_ID IS NULL, 0, Impressions) AS Deal_Impressions, IF(Inventory_ID IS NULL, Clicks, 0) AS Open_Clicks, IF(Inventory_ID IS NULL, 0, Clicks) AS Deal_Clicks, IF(Inventory_ID IS NULL, Conversions, 0) AS Open_Conversions, IF(Inventory_ID IS NULL, 0, Conversions) AS Deal_Conversions, IF(Inventory_ID IS NULL, Cost, 0) AS Open_Cost, IF(Inventory_ID IS NULL, 0, Cost) AS Deal_Cost, IF(Inventory_ID IS NULL, AV_Impressions_Viewable, 0) AS Open_Impressions_Viewable, IF(Inventory_ID IS NULL, 0, AV_Impressions_Viewable) AS Deal_Impressions_Viewable, IF(Inventory_ID IS NULL, AV_Impressions_Measurable, 0) AS Open_Impressions_Measurable, IF(Inventory_ID IS NULL, 0, AV_Impressions_Measurable) AS Deal_Impressions_Measurable, FROM [[PARAMETER].Deal_Finder_DV360_Report] OMIT RECORD IF Site == 'Low volume inventory') GROUP By Advertiser_ID, Site_ID, Inventory, Inventory_Type, Creative_Type, Creative_Size, Always_On) WHERE Rank_Impressions < 100 OR Rank_Clicks < 100 OR Rank_Conversions < 100 OR Rank_Cost < 100;',
      'parameters':[
        recipe_slug
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Deal_Finder_Dashboard'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Compares open vs. deal CPM, CPC, and CPA so that clients can decide which sites, inventory, and deals work best.

      1. Wait for BigQuery->->->Deal_Finder_Dashboard to be created.
      2. Join the 1-StarThinker Assets Group to access the following assets
         2.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      3. Copy 1-Deal Finder Sample Data.
         3.1 - Deal Finder Sample Data: https://datastudio.google.com/open/1QrWNTurvQT6nx20vnzdDveSzSmRjqHxQ
      4. Click Edit Connection, and change to BigQuery->StarThinker Data->->Deal_Finder_Dashboard.
      5. Copy 1-Deal Finder Sample Report.
         5.1 - Deal Finder Sample Report: https://datastudio.google.com/open/1fjRI5AIKTYTA4fWs-pYkJbIMgCumlMyO
      6. When prompted choose the new data source you just created.
      7. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_slug", help="Place where tables will be written in BigQuery.", default=None)
  parser.add_argument("-recipe_timezone", help="Timezone for report dates.", default='America/Los_Angeles')
  parser.add_argument("-recipe_name", help="Name of report in DV360, should be unique.", default=None)
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-partners", help="DV360 partner id.", default=[])
  parser.add_argument("-advertisers", help="Comma delimited list of DV360 advertiser ids.", default=[])


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_deal_finder(config, args.recipe_slug, args.recipe_timezone, args.recipe_name, args.auth_write, args.auth_read, args.partners, args.advertisers)
