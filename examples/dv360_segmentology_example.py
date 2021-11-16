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
from starthinker.task.bigquery.run import bigquery
from starthinker.task.dbm.run import dbm
from starthinker.task.census.run import census


def recipe_dv360_segmentology(config, auth_read, recipe_timezone, auth_write, recipe_name, date_range, recipe_slug, partners, advertisers):
  """DV360 funnel analysis using Census data.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       recipe_timezone (timezone) - Timezone for report dates.
       auth_write (authentication) - Authorization used for writing data.
       recipe_name (string) - Name of report, not needed if ID used.
       date_range (choice) - Timeframe to run the report for.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
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

  bigquery(config, {
    'auth':auth_write,
    'function':'Pearson Significance Test',
    'to':{
      'dataset':recipe_slug
    }
  })

  dbm(config, {
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
          'dataRange':date_range,
          'format':'CSV'
        },
        'params':{
          'type':'TYPE_CROSS_PARTNER',
          'groupBys':[
            'FILTER_PARTNER',
            'FILTER_PARTNER_NAME',
            'FILTER_ADVERTISER',
            'FILTER_ADVERTISER_NAME',
            'FILTER_MEDIA_PLAN',
            'FILTER_MEDIA_PLAN_NAME',
            'FILTER_ZIP_POSTAL_CODE'
          ],
          'metrics':[
            'METRIC_BILLABLE_IMPRESSIONS',
            'METRIC_CLICKS',
            'METRIC_TOTAL_CONVERSIONS'
          ]
        },
        'schedule':{
          'frequency':'WEEKLY'
        }
      }
    }
  })

  dbm(config, {
    'auth':auth_read,
    'report':{
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'DV360_KPI',
        'header':True,
        'schema':[
          {
            'name':'Partner_Id',
            'type':'INTEGER',
            'mode':'REQUIRED'
          },
          {
            'name':'Partner',
            'type':'STRING',
            'mode':'REQUIRED'
          },
          {
            'name':'Advertiser_Id',
            'type':'INTEGER',
            'mode':'REQUIRED'
          },
          {
            'name':'Advertiser',
            'type':'STRING',
            'mode':'REQUIRED'
          },
          {
            'name':'Campaign_Id',
            'type':'INTEGER',
            'mode':'REQUIRED'
          },
          {
            'name':'Campaign',
            'type':'STRING',
            'mode':'REQUIRED'
          },
          {
            'name':'Zip',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Impressions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Clicks',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Conversions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          }
        ]
      }
    }
  })

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':'''SELECT
          Partner_Id,
          Partner,
          Advertiser_Id,
          Advertiser,
          Campaign_Id,
          Campaign,
          Zip,
          SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY Advertiser_Id)) AS Impression,
          SAFE_DIVIDE(Clicks, Impressions) AS Click,
          SAFE_DIVIDE(Conversions, Impressions) AS Conversion,
          Impressions AS Impressions          FROM
          `{dataset}.DV360_KPI`;        ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'DV360_KPI_Normalized'
    }
  })

  census(config, {
    'auth':auth_write,
    'normalize':{
      'census_geography':'zip_codes',
      'census_year':'2018',
      'census_span':'5yr'
    },
    'to':{
      'dataset':recipe_slug,
      'type':'view'
    }
  })

  census(config, {
    'auth':auth_write,
    'correlate':{
      'join':'Zip',
      'pass':[
        'Partner_Id',
        'Partner',
        'Advertiser_Id',
        'Advertiser',
        'Campaign_Id',
        'Campaign'
      ],
      'sum':[
        'Impressions'
      ],
      'correlate':[
        'Impression',
        'Click',
        'Conversion'
      ],
      'dataset':recipe_slug,
      'table':'DV360_KPI_Normalized',
      'significance':80
    },
    'to':{
      'dataset':recipe_slug,
      'type':'view'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      DV360 funnel analysis using Census data.

      1. Wait for BigQuery->->->Census_Join to be created.
      2. Join the 1-StarThinker Assets Group to access the following assets
         2.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      3. Copy 1-DV360 Segmentology Sample. Leave the Data Source as is, you will change it in the next step.
         3.1 - DV360 Segmentology Sample: https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/
      4. Click Edit Connection, and change to BigQuery->->->Census_Join.
      5. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-recipe_timezone", help="Timezone for report dates.", default='America/Los_Angeles')
  parser.add_argument("-auth_write", help="Authorization used for writing data.", default='service')
  parser.add_argument("-recipe_name", help="Name of report, not needed if ID used.", default='')
  parser.add_argument("-date_range", help="Timeframe to run the report for.", default='LAST_365_DAYS')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')
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

  recipe_dv360_segmentology(config, args.auth_read, args.recipe_timezone, args.auth_write, args.recipe_name, args.date_range, args.recipe_slug, args.partners, args.advertisers)
