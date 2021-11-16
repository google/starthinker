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
from starthinker.task.ga.run import ga
from starthinker.task.census.run import census


def recipe_ga360_segmentology(config, auth_write, auth_read, view, recipe_slug):
  """GA360 funnel analysis using Census data.

     Args:
       auth_write (authentication) - Authorization used for writing data.
       auth_read (authentication) - Authorization for reading GA360.
       view (string) - View Id
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

  ga(config, {
    'auth':auth_read,
    'kwargs':{
      'reportRequests':[
        {
          'viewId':view,
          'dateRanges':[
            {
              'startDate':'90daysAgo',
              'endDate':'today'
            }
          ],
          'dimensions':[
            {
              'name':'ga:userType'
            },
            {
              'name':'ga:userDefinedValue'
            },
            {
              'name':'ga:latitude'
            },
            {
              'name':'ga:longitude'
            }
          ],
          'metrics':[
            {
              'expression':'ga:users'
            },
            {
              'expression':'ga:sessionsPerUser'
            },
            {
              'expression':'ga:bounces'
            },
            {
              'expression':'ga:timeOnPage'
            },
            {
              'expression':'ga:pageviews'
            }
          ]
        }
      ],
      'useResourceQuotas':False
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'GA360_KPI'
      }
    }
  })

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':'''WITH GA360_SUM AS (
         SELECT
            A.Dimensions.userType AS User_Type,
           A.Dimensions.userDefinedValue AS User_Value,
           B.zip_code AS Zip,
           SUM(Metrics.users) AS Users,
           SUM(Metrics.sessionsPerUser) AS Sessions,
           SUM(Metrics.timeOnPage) AS Time_On_Site,
           SUM(Metrics.bounces) AS Bounces,
           SUM(Metrics.pageviews) AS Page_Views
         FROM `{dataset}.GA360_KPI` AS A
          JOIN `bigquery-public-data.geo_us_boundaries.zip_codes` AS B
         ON ST_WITHIN(ST_GEOGPOINT(A.Dimensions.longitude, A.Dimensions.latitude), B.zip_code_geom)
         GROUP BY 1,2,3
         )
         SELECT
           User_Type,
           User_Value,
           Zip,
           Users,
           SAFE_DIVIDE(Users, SUM(Users) OVER()) AS User_Percent,
           SAFE_DIVIDE(Sessions, SUM(Sessions) OVER()) AS Impression_Percent,
           SAFE_DIVIDE(Time_On_Site, SUM(Time_On_Site) OVER()) AS Time_On_Site_Percent,
           SAFE_DIVIDE(Bounces, SUM(Bounces) OVER()) AS Bounce_Percent,
           SAFE_DIVIDE(Page_Views, SUM(Page_Views) OVER()) AS Page_View_Percent
         FROM GA360_SUM        ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'GA360_KPI_Normalized'
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
        'User_Type',
        'User_Value'
      ],
      'sum':[
        'Users'
      ],
      'correlate':[
        'User_Percent',
        'Impression_Percent',
        'Time_On_Site_Percent',
        'Bounce_Percent',
        'Page_View_Percent'
      ],
      'dataset':recipe_slug,
      'table':'GA360_KPI_Normalized',
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
      GA360 funnel analysis using Census data.

      1. Wait for BigQuery->->->Census_Join to be created.
      2. Join the 1- to access the following assets
         2.1 - : https://groups.google.com/d/forum/starthinker-assets
      3. Copy 1-. Leave the Data Source as is, you will change it in the next step.
         3.1 - : https://datastudio.google.com/c/u/0/reporting/3673497b-f36f-4448-8fb9-3e05ea51842f/
      4. Click Edit Connection, and change to BigQuery->->->Census_Join.
      5. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Authorization used for writing data.", default='service')
  parser.add_argument("-auth_read", help="Authorization for reading GA360.", default='service')
  parser.add_argument("-view", help="View Id", default='service')
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

  recipe_ga360_segmentology(config, args.auth_write, args.auth_read, args.view, args.recipe_slug)
