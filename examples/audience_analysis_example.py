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


def recipe_audience_analysis(config, recipe_slug, recipe_timezone, recipe_name, partners, advertisers):
  """The Audience Wizard Dashboard helps you to track the audience performance across
     all audiences on Display.

     Args:
       recipe_slug (string) - Place where tables will be created in BigQuery.
       recipe_timezone (timezone) - Timezone for report dates.
       recipe_name (string) - Name of report in DV360, should be unique.
       partners (integer_list) - DV360 partner id.
       advertisers (integer_list) - Comma delimited list of DV360 advertiser ids.
  """

  dataset(config, {
    'hour':[
      1
    ],
    'auth':'service',
    'description':'Create a dataset for bigquery tables.',
    'dataset':recipe_slug
  })

  dbm(config, {
    'hour':[
      2
    ],
    'auth':'user',
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
          'dataRange':'LAST_7_DAYS',
          'format':'CSV',
          'title':recipe_name
        },
        'params':{
          'type':'TYPE_GENERAL',
          'groupBys':[
            'FILTER_ADVERTISER_NAME',
            'FILTER_ADVERTISER',
            'FILTER_AUDIENCE_LIST',
            'FILTER_USER_LIST',
            'FILTER_AUDIENCE_LIST_TYPE',
            'FILTER_AUDIENCE_LIST_COST',
            'FILTER_PARTNER_CURRENCY'
          ],
          'metrics':[
            'METRIC_IMPRESSIONS',
            'METRIC_CLICKS',
            'METRIC_TOTAL_CONVERSIONS',
            'METRIC_LAST_CLICKS',
            'METRIC_LAST_IMPRESSIONS',
            'METRIC_TOTAL_MEDIA_COST_PARTNER'
          ]
        }
      }
    }
  })

  dbm(config, {
    'hour':[
      2
    ],
    'auth':'user',
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
          'dataRange':'LAST_7_DAYS',
          'format':'CSV',
          'title':recipe_name
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'groupBys':[
            'FILTER_ADVERTISER_NAME',
            'FILTER_ADVERTISER',
            'FILTER_USER_LIST_FIRST_PARTY_NAME',
            'FILTER_USER_LIST_FIRST_PARTY',
            'FILTER_FIRST_PARTY_AUDIENCE_LIST_TYPE',
            'FILTER_FIRST_PARTY_AUDIENCE_LIST_COST'
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ]
        }
      }
    }
  })

  dbm(config, {
    'hour':[
      2
    ],
    'auth':'user',
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
          'dataRange':'LAST_7_DAYS',
          'format':'CSV',
          'title':recipe_name
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'groupBys':[
            'FILTER_ADVERTISER_NAME',
            'FILTER_ADVERTISER',
            'FILTER_AUDIENCE_LIST',
            'FILTER_USER_LIST',
            'FILTER_AUDIENCE_LIST_TYPE',
            'FILTER_AUDIENCE_LIST_COST'
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ]
        }
      }
    }
  })

  dbm(config, {
    'hour':[
      2
    ],
    'auth':'user',
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
          'dataRange':'LAST_7_DAYS',
          'format':'CSV',
          'title':recipe_name
        },
        'params':{
          'type':'TYPE_INVENTORY_AVAILABILITY',
          'groupBys':[
            'FILTER_ADVERTISER_NAME',
            'FILTER_ADVERTISER',
            'FILTER_USER_LIST_THIRD_PARTY_NAME',
            'FILTER_USER_LIST_THIRD_PARTY',
            'FILTER_THIRD_PARTY_AUDIENCE_LIST_TYPE',
            'FILTER_THIRD_PARTY_AUDIENCE_LIST_COST'
          ],
          'metrics':[
            'METRIC_BID_REQUESTS',
            'METRIC_UNIQUE_VISITORS_COOKIES'
          ]
        }
      }
    }
  })

  dbm(config, {
    'hour':[
      6
    ],
    'auth':'user',
    'report':{
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'DV360_Audience_Performance',
        'header':True,
        'schema':[
          {
            'mode':'REQUIRED',
            'name':'advertiser',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'advertiser_id',
            'type':'INT64'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list_id',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_type',
            'type':'STRING'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_cost_usd',
            'type':'STRING'
          },
          {
            'mode':'NULLABLE',
            'name':'partner_currency',
            'type':'STRING'
          },
          {
            'mode':'NULLABLE',
            'name':'impressions',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'clicks',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'total_conversions',
            'type':'FLOAT'
          },
          {
            'mode':'NULLABLE',
            'name':'post_click_conversions',
            'type':'FLOAT'
          },
          {
            'mode':'NULLABLE',
            'name':'post_view_conversions',
            'type':'FLOAT'
          },
          {
            'mode':'NULLABLE',
            'name':'total_media_cost_partner_currency',
            'type':'FLOAT'
          }
        ]
      }
    }
  })

  dbm(config, {
    'hour':[
      6
    ],
    'auth':'user',
    'report':{
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'DV360_First_Party_Audience',
        'header':True,
        'schema':[
          {
            'mode':'REQUIRED',
            'name':'advertiser',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'advertiser_id',
            'type':'INT64'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list_id',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_type',
            'type':'STRING'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_cost_usd',
            'type':'FLOAT'
          },
          {
            'mode':'NULLABLE',
            'name':'potential_impressions',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'unique_cookies_with_impressions',
            'type':'INT64'
          }
        ]
      }
    }
  })

  dbm(config, {
    'hour':[
      6
    ],
    'auth':'user',
    'report':{
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'DV360_Google_Audience',
        'header':True,
        'schema':[
          {
            'mode':'REQUIRED',
            'name':'advertiser',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'advertiser_id',
            'type':'INT64'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list_id',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_type',
            'type':'STRING'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_cost_usd',
            'type':'FLOAT'
          },
          {
            'mode':'NULLABLE',
            'name':'potential_impressions',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'unique_cookies_with_impressions',
            'type':'INT64'
          }
        ]
      }
    }
  })

  dbm(config, {
    'hour':[
      6
    ],
    'auth':'user',
    'report':{
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'DV360_Third_Party_Audience',
        'header':True,
        'schema':[
          {
            'mode':'REQUIRED',
            'name':'advertiser',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'advertiser_id',
            'type':'INT64'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list',
            'type':'STRING'
          },
          {
            'mode':'REQUIRED',
            'name':'audience_list_id',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_type',
            'type':'STRING'
          },
          {
            'mode':'NULLABLE',
            'name':'audience_list_cost_usd',
            'type':'FLOAT'
          },
          {
            'mode':'NULLABLE',
            'name':'potential_impressions',
            'type':'INT64'
          },
          {
            'mode':'NULLABLE',
            'name':'unique_cookies_with_impressions',
            'type':'INT64'
          }
        ]
      }
    }
  })

  bigquery(config, {
    'hour':[
      6
    ],
    'auth':'service',
    'from':{
      'query':'''
         SELECT
           p.advertiser_id,
           p.advertiser,
           p.audience_list_id,
           IF (p.audience_list_type = 'Bid Manager Audiences', 'Google', p.audience_list_type) AS audience_list_type,
           CASE
             WHEN REGEXP_CONTAINS(p.audience_list, 'Affinity') THEN 'Affinity'
             WHEN REGEXP_CONTAINS(p.audience_list, 'Demographics') THEN 'Demographics'
             WHEN REGEXP_CONTAINS(p.audience_list, 'In-Market') THEN 'In-Market'
             WHEN REGEXP_CONTAINS(p.audience_list, 'Similar') THEN 'Similar'
             ELSE 'Custom'
           END AS audience_list_category,
           p.audience_list,
           IF(p.audience_list_cost_usd = 'Unknown', 0.0, CAST(p.audience_list_cost_usd AS FLOAT64)) AS audience_list_cost,
           p.total_media_cost_partner_currency AS total_media_cost,
           p.impressions,
           p.clicks,
           p.total_conversions,
           COALESCE(ggl.potential_impressions, fst.potential_impressions, trd.potential_impressions) AS potential_impressions,
           COALESCE(ggl.unique_cookies_with_impressions, fst.unique_cookies_with_impressions, trd.unique_cookies_with_impressions) AS potential_reach
         FROM
           `{dataset}.DV360_Audience_Performance` p
         LEFT JOIN
           `{dataset}.DV360_Google_Audience` ggl
           USING (advertiser_id, audience_list_id)
         LEFT JOIN
           `{dataset}.DV360_First_Party_Audience` fst
           USING (advertiser_id, audience_list_id)
         LEFT JOIN
           `{dataset}.DV360_Third_Party_Audience` trd
           USING (advertiser_id, audience_list_id)
         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'DV360_Audience_Analysis'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      The Audience Wizard Dashboard helps you to track the audience performance across all audiences on Display.

      1. Wait for BigQuery->->->DV360_Audience_Analysis to be created.
      2. Join the 1-StarThinker Assets Group to access the following assets
         2.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      3. Copy <a 1-Sample DV360 Audience Analysis Dataset.
         3.1 - Sample DV360 Audience Analysis Dataset: https://datastudio.google.com/open/1d2vlf4C1roN95NsdsvWNZqKFcYN8N9Jg
      4. Click Edit Connection, and change to BigQuery->->->DV360_Audience_Analysis.
      5. Copy 1-Sample DV360 Audience Analysis Report.
         5.1 - Sample DV360 Audience Analysis Report: https://datastudio.google.com/open/1Ij_RluqolElm7Nny9fBrIAPRB9ObUl0M
      6. When prompted choose the new data source you just created.
      7. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_slug", help="Place where tables will be created in BigQuery.", default=None)
  parser.add_argument("-recipe_timezone", help="Timezone for report dates.", default='America/Los_Angeles')
  parser.add_argument("-recipe_name", help="Name of report in DV360, should be unique.", default=None)
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

  recipe_audience_analysis(config, args.recipe_slug, args.recipe_timezone, args.recipe_name, args.partners, args.advertisers)
