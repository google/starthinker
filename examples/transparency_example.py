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
from starthinker.task.bigquery.run import bigquery


def recipe_transparency(config, recipe_slug, recipe_name, dcm_account, dcm_advertisers):
  """Reports the percentage of CM impressions that can be attributed to a specific
     domain or application.  Allows diagnostic of which domains and apps are
     misconfigured by publisher resulting in underreporting.

     Args:
       recipe_slug (string) - Place where tables will be written in BigQuery.
       recipe_name (string) - Name of report in CM, should be unique.
       dcm_account (integer) - CM account id of client.
       dcm_advertisers (integer_list) - Comma delimited list of CM advertiser ids.
  """

  dataset(config, {
    'hour':[
      1
    ],
    'auth':'service',
    'dataset':recipe_slug
  })

  dcm(config, {
    'hour':[
      2
    ],
    'auth':'user',
    'report':{
      'account':dcm_account,
      'filters':{
        'advertiser':{
          'values':dcm_advertisers
        }
      },
      'body':{
        'type':'STANDARD',
        'format':'CSV',
        'name':recipe_name,
        'criteria':{
          'dateRange':{
            'relativeDateRange':'PREVIOUS_MONTH'
          },
          'dimensions':[
            {
              'name':'advertiser'
            },
            {
              'name':'advertiserId'
            },
            {
              'name':'campaign'
            },
            {
              'name':'campaignId'
            },
            {
              'name':'siteId'
            },
            {
              'name':'site'
            },
            {
              'name':'adType'
            },
            {
              'name':'environment'
            },
            {
              'name':'appId'
            },
            {
              'name':'app'
            }
          ],
          'metricNames':[
            'impressions'
          ]
        },
        'schedule':{
          'active':True,
          'every':1,
          'repeats':'MONTHLY',
          'runsOnDayOfMonth':'DAY_OF_MONTH'
        }
      }
    }
  })

  dcm(config, {
    'hour':[
      2
    ],
    'auth':'user',
    'report':{
      'account':dcm_account,
      'filters':{
        'advertiser':{
          'values':dcm_advertisers
        }
      },
      'body':{
        'type':'STANDARD',
        'format':'CSV',
        'name':recipe_name,
        'criteria':{
          'dateRange':{
            'relativeDateRange':'PREVIOUS_MONTH'
          },
          'dimensions':[
            {
              'name':'advertiser'
            },
            {
              'name':'advertiserId'
            },
            {
              'name':'campaign'
            },
            {
              'name':'campaignId'
            },
            {
              'name':'site'
            },
            {
              'name':'siteId'
            },
            {
              'name':'adType'
            },
            {
              'name':'domain'
            }
          ],
          'metricNames':[
            'verificationVerifiableImpressions'
          ]
        },
        'schedule':{
          'active':True,
          'every':1,
          'repeats':'MONTHLY',
          'runsOnDayOfMonth':'DAY_OF_MONTH'
        }
      }
    }
  })

  dcm(config, {
    'hour':[
      4
    ],
    'auth':'user',
    'report':{
      'account':dcm_account,
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':'service',
        'dataset':recipe_slug,
        'table':'Transparency_Domain_KPI'
      }
    }
  })

  dcm(config, {
    'hour':[
      4
    ],
    'auth':'user',
    'report':{
      'account':dcm_account,
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':'service',
        'dataset':recipe_slug,
        'table':'Transparency_App_KPI'
      }
    }
  })

  bigquery(config, {
    'hour':[
      5
    ],
    'auth':'user',
    'to':{
      'dataset':recipe_slug,
      'view':'Transparency_Combined_KPI'
    },
    'from':{
      'query':'''WITH
         Transparent_Domains AS (
           SELECT
             CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,
             CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,
             CONCAT(Site_Cm360, ' - ', CAST(Site_Id_Cm360 AS STRING)) AS Site,
             Domain,
             Ad_Type,
             Verifiable_Impressions AS Impressions,
             IF(Domain IS NOT NULL, Verifiable_Impressions, 0) AS Visible_Impressions,
             IF(Domain IS NULL, Verifiable_Impressions, 0) AS Null_Impressions
           FROM `{dataset}.Transparency_Domain_KPI`
         ),
         Transparent_Apps AS (
           SELECT
             CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,
             CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,
             CONCAT(Site_Cm360, ' - ', CAST(Site_Id_Cm360 AS STRING)) AS Site,
             /*If(App IS NOT NULL, CONCAT(App, ' - ', CAST(App_Id AS STRING)), App_Id) AS App, */
             CASE
               WHEN App IS NOT NULL THEN CONCAT(App, ' - ', CAST(App_Id AS STRING))
               WHEN App_Id IS NOT NULL THEN App_Id
               ELSE NULL
             END AS App,
             Ad_Type,
             Impressions,
             IF(App IS NOT NULL OR App_ID IS NOT NULL, Impressions, 0) AS Visible_Impressions,
             IF(App IS NULL AND App_Id IS NULL, Impressions, 0) AS Null_Impressions
           FROM `{dataset}.Transparency_App_KPI`  WHERE Environment = 'App'
         ),
         Domains_And_Apps AS (
           SELECT
             TD.Advertiser,
             TD.Campaign,
             TD.Site,
             TD.Ad_Type,
             TD.Domain,
             TD.Impressions AS Domain_Impressions,
             TD.Visible_Impressions AS Domain_Visible_Impressions,
             TD.Null_Impressions AS Domain_Null_Impressions,
             NULL AS App,
             0 AS App_Impressions,
             0 AS App_Visible_Impressions,
             0 AS App_Null_Impressions  FROM Transparent_Domains AS TD  UNION ALL  SELECT
             TA.Advertiser,
             TA.Campaign,
             TA.Site,
             TA.Ad_Type,
             NULL AS Domain,
             0 AS Domain_Impressions,
             0 AS Domain_Visible_Impressions,
             0 AS Domain_Null_Impressions,
             TA.App,
             TA.Impressions AS App_Impressions,
             TA.Visible_Impressions AS App_Visible_Impressions,
             TA.Null_Impressions AS App_Null_Impressions
           FROM Transparent_Apps AS TA
         )
         SELECT
           Advertiser,
           Campaign,
           Site,
           COALESCE(Domain, App, '') AS Domain_Or_App,
           Ad_Type,
           CASE
             WHEN App IS NOT NULL AND Domain IS NOT NULL THEN 'Both' /* SHOULD NOT HAPPEN */
             WHEN App IS NOT NULL THEN 'App'
             WHEN Domain IS NOT NULL Then 'Domain'
             ELSE 'Neither'
           END AS Category,
           SUM(Domain_Impressions) AS Domain_Impressions,
           SUM(Domain_Visible_Impressions) AS Domain_Visible_Impressions,
           SUM(Domain_Null_Impressions) AS Domain_Null_Impressions,
           SUM(App_Impressions) AS App_Impressions,
           SUM(App_Visible_Impressions) AS App_Visible_Impressions,
           SUM(App_Null_Impressions) AS App_Null_Impressions,
           SUM(App_Impressions + Domain_Impressions) AS Impressions
           /* Could also be MAX as its always one or the other*/
         FROM Domains_And_Apps  GROUP By 1,2,3,4,5,6''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Reports the percentage of CM impressions that can be attributed to a specific domain or application.  Allows diagnostic of which domains and apps are misconfigured by publisher resulting in underreporting.

      1. Wait for 1-BigQuery :  :  :  to be created.
         1.1 - BigQuery :  :  : : https://console.cloud.google.com/bigquery?project=&d=
      2. Copy DataStudio 1-Transparency Combined KPI and connect.
         2.1 - Transparency Combined KPI: https://datastudio.google.com/c/u/0/datasources/1Az6d9loAHo69GSIyKUfusrtyf_IDqTVs
      3. Copy DataStudio 1-Transparency Breakdown.
         3.1 - Transparency Breakdown: https://datastudio.google.com/c/u/0/reporting/1foircGRxgYCL_PR8gfdmYOleBacnPKwB/page/QCXj
      4. When prompted choose the new data source you just created.
      5. Or give these intructions to the client, they will have to join the 1-StarThinker Assets Group.
         5.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_slug", help="Place where tables will be written in BigQuery.", default=None)
  parser.add_argument("-recipe_name", help="Name of report in CM, should be unique.", default=None)
  parser.add_argument("-dcm_account", help="CM account id of client.", default='')
  parser.add_argument("-dcm_advertisers", help="Comma delimited list of CM advertiser ids.", default=None)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_transparency(config, args.recipe_slug, args.recipe_name, args.dcm_account, args.dcm_advertisers)
