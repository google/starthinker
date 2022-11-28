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
from starthinker.task.drive.run import drive
from starthinker.task.dataset.run import dataset
from starthinker.task.dbm.run import dbm
from starthinker.task.sheets.run import sheets
from starthinker.task.bigquery.run import bigquery


def recipe_ctv_audience_affinity(config, dataset, recipe_project, recipe_name, auth_write, partner_id, auth_read, audience_ids):
  """The cTV Audience Affinity dashboard is designed to give clients insights into
     which cTV apps their audiences have a high affinity for using.  The goal of
     this dashboard is to provide some assistance with the lack of audience
     targeting for cTV within DV360.

     Args:
       dataset (string) - BigQuery Dataset where all data will live.
       recipe_project (string) - Project where BigQuery dataset will be created.
       recipe_name (string) - Name of document to deploy to.
       auth_write (authentication) - Credentials used for writing data.
       partner_id (integer) - DV360 Partner id.
       auth_read (authentication) - Credentials used for reading data.
       audience_ids (integer_list) - Comma separated list of Audience Ids
  """

  drive(config, {
    'auth':'user',
    'copy':{
      'source':'https://docs.google.com/spreadsheets/d/1PPPk2b4gGJHNgQ4hXLiTKzH8pRIdlF5fNy9VCw1v7tM/',
      'destination':recipe_name
    }
  })

  dataset(config, {
    'auth':auth_write,
    'dataset':dataset
  })

  dbm(config, {
    'auth':'user',
    'report':{
      'body':{
        'timezoneCode':'America/Los_Angeles',
        'kind':'doubleclickbidmanager#query',
        'metadata':{
          'title':recipe_name,
          'dataRange':'LAST_30_DAYS',
          'format':'CSV',
          'sendNotification':False
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'groupBys':[
            'FILTER_APP_URL'
          ],
          'filters':[
            {
              'type':'FILTER_PARTNER',
              'value':partner_id
            },
            {
              'type':'FILTER_INVENTORY_FORMAT',
              'value':'VIDEO'
            },
            {
              'type':'FILTER_COUNTRY',
              'value':'US'
            }
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ],
          'includeInviteData':True
        },
        'schedule':{
          'frequency':'DAILY',
          'nextRunMinuteOfDay':0,
          'nextRunTimezoneCode':'America/Los_Angeles',
          'endTimeMs':7983727200000
        }
      }
    },
    'out':{
      'bigquery':{
        'dataset':dataset,
        'schema':[
          {
            'type':'STRING',
            'name':'app_url',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'impressions',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'uniques',
            'mode':'NULLABLE'
          }
        ],
        'table':'us_country_app',
        'header':True
      }
    }
  })

  dbm(config, {
    'auth':'user',
    'report':{
      'body':{
        'timezoneCode':'America/Los_Angeles',
        'kind':'doubleclickbidmanager#query',
        'metadata':{
          'title':recipe_name,
          'dataRange':'LAST_30_DAYS',
          'format':'CSV',
          'sendNotification':False
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'filters':[
            {
              'type':'FILTER_PARTNER',
              'value':partner_id
            },
            {
              'type':'FILTER_COUNTRY',
              'value':'US'
            }
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ],
          'includeInviteData':True
        },
        'schedule':{
          'frequency':'DAILY',
          'nextRunMinuteOfDay':0,
          'nextRunTimezoneCode':'America/Los_Angeles',
          'endTimeMs':7983727200000
        }
      }
    },
    'out':{
      'bigquery':{
        'dataset':dataset,
        'schema':[
          {
            'type':'STRING',
            'name':'impressions',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'uniques',
            'mode':'NULLABLE'
          }
        ],
        'table':'us_country_baseline',
        'header':True
      }
    }
  })

  dbm(config, {
    'auth':'user',
    'report':{
      'filters':{
        'FILTER_USER_LIST':{
          'single_cell':True,
          'values':audience_ids
        }
      },
      'body':{
        'timezoneCode':'America/Los_Angeles',
        'kind':'doubleclickbidmanager#query',
        'metadata':{
          'title':recipe_name,
          'dataRange':'LAST_30_DAYS',
          'format':'CSV',
          'sendNotification':False
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'groupBys':[
            'FILTER_AUDIENCE_LIST'
          ],
          'filters':[
            {
              'type':'FILTER_PARTNER',
              'value':partner_id
            },
            {
              'type':'FILTER_COUNTRY',
              'value':'US'
            }
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ],
          'includeInviteData':True
        },
        'schedule':{
          'frequency':'DAILY',
          'nextRunMinuteOfDay':0,
          'nextRunTimezoneCode':'America/Los_Angeles',
          'endTimeMs':7983727200000
        }
      }
    },
    'out':{
      'bigquery':{
        'dataset':dataset,
        'schema':[
          {
            'type':'STRING',
            'name':'user_list',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'impressions',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'uniques',
            'mode':'NULLABLE'
          }
        ],
        'table':'us_audience_baseline',
        'header':True
      }
    }
  })

  dbm(config, {
    'auth':'user',
    'report':{
      'filters':{
        'FILTER_USER_LIST':{
          'single_cell':True,
          'values':audience_ids
        }
      },
      'body':{
        'timezoneCode':'America/Los_Angeles',
        'kind':'doubleclickbidmanager#query',
        'metadata':{
          'title':recipe_name,
          'dataRange':'LAST_30_DAYS',
          'format':'CSV',
          'sendNotification':False
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'groupBys':[
            'FILTER_APP_URL',
            'FILTER_AUDIENCE_LIST'
          ],
          'filters':[
            {
              'type':'FILTER_PARTNER',
              'value':partner_id
            },
            {
              'type':'FILTER_INVENTORY_FORMAT',
              'value':'VIDEO'
            },
            {
              'type':'FILTER_COUNTRY',
              'value':'US'
            }
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ],
          'includeInviteData':True
        },
        'schedule':{
          'frequency':'DAILY',
          'nextRunMinuteOfDay':0,
          'nextRunTimezoneCode':'America/Los_Angeles',
          'endTimeMs':7983727200000
        }
      }
    },
    'out':{
      'bigquery':{
        'dataset':dataset,
        'schema':[
          {
            'type':'STRING',
            'name':'app_url',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'user_list',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'impressions',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'uniques',
            'mode':'NULLABLE'
          }
        ],
        'table':'us_audience_app',
        'header':True
      }
    }
  })

  sheets(config, {
    'auth':auth_read,
    'sheet':recipe_name,
    'tab':'data',
    'range':'A:Z',
    'header':True,
    'out':{
      'auth':auth_write,
      'bigquery':{
        'dataset':dataset,
        'table':'CTV_App_Lookup',
        'schema':[
          {
            'type':'STRING',
            'name':'Publisher_Name',
            'mode':'NULLABLE'
          },
          {
            'type':'STRING',
            'name':'CTV_App_name',
            'mode':'NULLABLE'
          }
        ]
      }
    }
  })

  bigquery(config, {
    'description':'The query to join all the IAR reports into an Affinity Index.',
    'auth':auth_write,
    'from':{
      'query':'WITH audience_app_clean AS ( SELECT ctv_app.CTV_App_name AS ctv_app_name, user_list, app_url, IF (app_url LIKE '%Android%' OR app_url LIKE '%iOS', 'App', 'Domain') AS app_or_domain, CAST( IF (cast(impressions as string) LIKE '%< 1000%', cast(0 as int64), CAST(impressions AS int64)) AS int64) AS potential_impressions, CAST( IF (uniques LIKE '%< 1000%', cast(0 as int64), CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions FROM `[PARAMETER].[PARAMETER].us_audience_app` AS a LEFT JOIN `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app ON a.app_url = ctv_app.Publisher_Name ), us_country_app_clean AS ( SELECT a.app_url, ctv_app.CTV_App_name AS ctv_app_name, CAST( IF (CAST(a.impressions AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(a.impressions AS int64)) AS int64) AS POtential_ImpressionS, CAST( IF (CAST(a.uniques AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(a.uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions FROM `[PARAMETER].[PARAMETER].us_country_app` AS a LEFT JOIN `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app ON a.app_url = ctv_app.Publisher_Name ) SELECT audience_app.ctv_app_name, audience_app.app_url, audience_app.app_or_domain, audience_app.user_list AS audience_list, audience_app.Potential_Impressions AS audience_app_impressions, audience_app.Unique_Cookies_With_Impressions AS audience_app_uniques, audience_baseline.Potential_Impressions AS audience_baseline_impressions, audience_baseline.Unique_Cookies_With_Impressions AS audience_baseline_uniques, country_app.Potential_Impressions AS country_app_impressions, country_app.Unique_Cookies_With_Impressions AS country_app_uniques, country_baseline.Potential_Impressions AS country_baseline_impressions, country_baseline.Unique_Cookies_With_Impressions AS country_baseline_uniques, ((audience_app.Unique_Cookies_With_Impressions/NULLIF(audience_baseline.Unique_Cookies_With_Impressions, 0))/NULLIF((country_app.Unique_Cookies_With_Impressions/NULLIF(CAST(country_baseline.Unique_Cookies_With_Impressions AS int64), 0)), 0))*100 AS affinity_index FROM ( SELECT user_list, CAST( IF (cast(impressions as string) LIKE '%< 1000%', cast(0 as int64), CAST(impressions AS int64)) AS int64) AS POTential_impressions, CAST( IF (uniques LIKE '%< 100%', cast(0 as int64), CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions FROM `[PARAMETER].[PARAMETER].us_audience_baseline` ) AS audience_baseline JOIN ( SELECT ctv_app_name, app_url, user_list, app_or_domain, SUM(potential_impressions) as poTEntial_impressions, SUM(unique_cookies_with_impressions) as unique_cookies_with_impressions, FROM audience_app_clean GROUP BY ctv_app_name, user_list, app_url, app_or_domain) AS audience_app ON audience_baseline.user_list = audience_app.user_list LEFT JOIN ( SELECT ctv_app_name, SUM(potential_impressions) as potENtial_impressions, SUM(unique_cookies_with_impressions) as unique_cookies_with_impressions, FROM us_country_app_clean GROUP BY ctv_app_name) AS country_app ON country_app.ctv_app_name = audience_app.ctv_app_name CROSS JOIN ( SELECT CAST( IF (CAST(impressions AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(impressions AS int64)) AS int64) AS PotenTial_Impressions, CAST( IF (CAST(uniques AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions FROM `[PARAMETER].[PARAMETER].us_country_baseline` ) AS country_baseline',
      'legacy':False,
      'parameters':[
        recipe_project,
        dataset,
        recipe_project,
        dataset,
        recipe_project,
        dataset,
        recipe_project,
        dataset,
        recipe_project,
        dataset,
        recipe_project,
        dataset
      ]
    },
    'to':{
      'dataset':dataset,
      'table':'final_table'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      The cTV Audience Affinity dashboard is designed to give clients insights into which cTV apps their audiences have a high affinity for using.  The goal of this dashboard is to provide some assistance with the lack of audience targeting for cTV within DV360.

      1. Find instructions and recommendations for 1-this dashboard
         1.1 - this dashboard: https://docs.google.com/document/d/120kcR9OrS4hGdTxRK0Ig2koNmm6Gl7sH0L6U56N0SAM/
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-dataset", help="BigQuery Dataset where all data will live.", default=None)
  parser.add_argument("-recipe_project", help="Project where BigQuery dataset will be created.", default=None)
  parser.add_argument("-recipe_name", help="Name of document to deploy to.", default='')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-partner_id", help="DV360 Partner id.", default=None)
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-audience_ids", help="Comma separated list of Audience Ids", default=None)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_ctv_audience_affinity(config, args.dataset, args.recipe_project, args.recipe_name, args.auth_write, args.partner_id, args.auth_read, args.audience_ids)
