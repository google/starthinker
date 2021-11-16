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
from starthinker.task.google_api.run import google_api
from starthinker.task.census.run import census


def recipe_google_ads_segmentology(config, auth_read, customer_id, developer_token, login_id, auth_write, recipe_slug):
  """GoogleAds funnel analysis using Census data.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       customer_id (string) - Google Ads customer.
       developer_token (string) - Google Ads developer token.
       login_id (string) - Google Ads login.
       auth_write (authentication) - Authorization used for writing data.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
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

  google_api(config, {
    'auth':auth_read,
    'api':'googleads',
    'version':'v8',
    'function':'customers.googleAds.search',
    'kwargs':{
      'customerId':customer_id,
      'body':{
        'query':'''SELECT
         campaign.name,
         ad_group.name,
         segments.geo_target_postal_code,
         metrics.impressions,
         metrics.clicks,
         metrics.conversions,
         metrics.interactions
         FROM user_location_view         '''
      }
    },
    'headers':{
      'developer-token':developer_token,
      'login-customer-id':login_id
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'dataset':recipe_slug,
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
  })

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':'''SELECT
          campaign.name AS Campaign,
          adGRoup.name AS Ad_Group,
          segments.geoTargetPostalCode AS Postal_Code,
          SAFE_DIVIDE(metrics.impressions, SUM(metrics.impressions) OVER()) AS Impression,
          SAFE_DIVIDE(metrics.clicks, metrics.impressions) AS Click,
          SAFE_DIVIDE(metrics.conversions, metrics.impressions) AS Conversion,
          SAFE_DIVIDE(metrics.interactions, metrics.impressions) AS Interaction,
          metrics.impressions AS Impressions          FROM
          `{dataset}.GoogleAds_KPI`;        ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'GoogleAds_KPI_Normalized'
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
      'dataset':recipe_slug,
      'table':'GoogleAds_KPI_Normalized',
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
      GoogleAds funnel analysis using Census data.

      1. Wait for BigQuery->->->Census_Join to be created.
      2. Join the 1-StarThinker Assets Group to access the following assets
         2.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      3. Copy 1-GoogleAds Segmentology Sample. Leave the Data Source as is, you will change it in the next step.
         3.1 - GoogleAds Segmentology Sample: https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/
      4. Click Edit Connection, and change to BigQuery->->->Census_Join.
      5. Or give these instructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-customer_id", help="Google Ads customer.", default='')
  parser.add_argument("-developer_token", help="Google Ads developer token.", default='')
  parser.add_argument("-login_id", help="Google Ads login.", default='')
  parser.add_argument("-auth_write", help="Authorization used for writing data.", default='service')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_google_ads_segmentology(config, args.auth_read, args.customer_id, args.developer_token, args.login_id, args.auth_write, args.recipe_slug)
