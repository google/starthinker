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
from starthinker.task.dcm.run import dcm
from starthinker.task.census.run import census


def recipe_cm360_segmentology(config, account, auth_read, auth_write, recipe_name, date_range, recipe_slug, advertisers):
  """CM360 funnel analysis using Census data.

     Args:
       account (string) - NA
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Authorization used for writing data.
       recipe_name (string) - Name of report, not needed if ID used.
       date_range (choice) - Timeframe to run report for.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
       advertisers (integer_list) - Comma delimited list of CM360 advertiser ids.
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
    'auth':'user',
    'api':'dfareporting',
    'version':'v3.4',
    'function':'accounts.get',
    'kwargs':{
      'id':account,
      'fields':'id,name'
    },
    'results':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'CM360_Account'
      }
    }
  })

  dcm(config, {
    'auth':auth_read,
    'report':{
      'filters':{
        'advertiser':{
          'values':advertisers
        }
      },
      'account':account,
      'body':{
        'name':recipe_name,
        'criteria':{
          'dateRange':{
            'kind':'dfareporting#dateRange',
            'relativeDateRange':date_range
          },
          'dimensions':[
            {
              'kind':'dfareporting#sortedDimension',
              'name':'advertiserId'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'advertiser'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'zipCode'
            }
          ],
          'metricNames':[
            'impressions',
            'clicks',
            'totalConversions'
          ]
        },
        'type':'STANDARD',
        'delivery':{
          'emailOwner':False
        },
        'format':'CSV'
      }
    }
  })

  dcm(config, {
    'auth':auth_read,
    'report':{
      'account':account,
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'CM360_KPI',
        'header':True
      }
    }
  })

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':'''SELECT
          Id AS Partner_Id,
          Name AS Partner,
          Advertiser_Id,
          Advertiser,
          Zip_Postal_Code AS Zip,
          SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY Advertiser_Id)) AS Impression,
          SAFE_DIVIDE(Clicks, Impressions) AS Click,
          SAFE_DIVIDE(Total_Conversions, Impressions) AS Conversion,
          Impressions AS Impressions          FROM `{dataset}.CM360_KPI`          CROSS JOIN `{dataset}.CM360_Account`        ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'CM360_KPI_Normalized'
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
        'Advertiser'
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
      'table':'CM360_KPI_Normalized',
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
      CM360 funnel analysis using Census data.

      1. Wait for BigQuery->->->Census_Join to be created.
      2. Join the 1-StarThinker Assets Group to access the following assets
         2.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      3. Copy 1-CM360 Segmentology Sample. Leave the Data Source as is, you will change it in the next step.
         3.1 - CM360 Segmentology Sample: https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/
      4. Click Edit Connection, and change to BigQuery->->->Census_Join.
      5. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-account", help="", default='')
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Authorization used for writing data.", default='service')
  parser.add_argument("-recipe_name", help="Name of report, not needed if ID used.", default='')
  parser.add_argument("-date_range", help="Timeframe to run report for.", default='LAST_365_DAYS')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')
  parser.add_argument("-advertisers", help="Comma delimited list of CM360 advertiser ids.", default=[])


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm360_segmentology(config, args.account, args.auth_read, args.auth_write, args.recipe_name, args.date_range, args.recipe_slug, args.advertisers)
