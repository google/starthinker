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
from starthinker.task.dcm.run import dcm
from starthinker.task.sdf.run import sdf
from starthinker.task.bigquery.run import bigquery
from starthinker.task.sheets.run import sheets
from starthinker.task.itp_audit.run import itp_audit


def recipe_itp_audit(config, recipe_timezone, auth_sheets, auth_bq, auth_dv, auth_cm, cm_account_id, floodlight_configuration_ids, date_range, cm_advertiser_ids, dv360_partner_id, dv360_advertiser_ids, recipe_name, recipe_slug):
  """Dashboard that shows performance metrics across browser to see the impact of
     privacy changes.

     Args:
       recipe_timezone (timezone) - Timezone for report dates.
       auth_sheets (authentication) - Credentials used for Sheets.
       auth_bq (authentication) - Credentials used for BigQuery.
       auth_dv (authentication) - Credentials used for DV360.
       auth_cm (authentication) - Credentials used for CM.
       cm_account_id (string) - Campaign Manager Account Id.
       floodlight_configuration_ids (integer_list) - Comma delimited list of floodlight configuration ids for the Campaign Manager floodlight report.
       date_range (choice) - Timeframe to run the ITP report for.
       cm_advertiser_ids (integer_list) - Optional: Comma delimited list of CM advertiser ids.
       dv360_partner_id (integer) - DV360 Partner id
       dv360_advertiser_ids (integer_list) - Optional: Comma delimited list of DV360 Advertiser ids.
       recipe_name (string) - Name of report in DBM, should be unique.
       recipe_slug (string) - BigQuery dataset for store dashboard tables.
  """

  drive(config, {
    'auth':auth_sheets,
    'hour':[
    ],
    'copy':{
      'source':'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/',
      'destination':recipe_name
    }
  })

  dataset(config, {
    'auth':auth_bq,
    'dataset':recipe_slug
  })

  dbm(config, {
    'auth':auth_dv,
    'report':{
      'name':recipe_name,
      'timeout':90,
      'filters':{
        'FILTER_ADVERTISER':{
          'values':dv360_advertiser_ids
        },
        'FILTER_PARTNER':{
          'values':dv360_partner_id
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
          'type':'TYPE_GENERAL',
          'groupBys':[
            'FILTER_ADVERTISER',
            'FILTER_ADVERTISER_NAME',
            'FILTER_ADVERTISER_CURRENCY',
            'FILTER_MEDIA_PLAN',
            'FILTER_MEDIA_PLAN_NAME',
            'FILTER_CAMPAIGN_DAILY_FREQUENCY',
            'FILTER_INSERTION_ORDER',
            'FILTER_INSERTION_ORDER_NAME',
            'FILTER_LINE_ITEM',
            'FILTER_LINE_ITEM_NAME',
            'FILTER_PAGE_LAYOUT',
            'FILTER_WEEK',
            'FILTER_MONTH',
            'FILTER_YEAR',
            'FILTER_PARTNER',
            'FILTER_PARTNER_NAME',
            'FILTER_LINE_ITEM_TYPE',
            'FILTER_DEVICE_TYPE',
            'FILTER_BROWSER',
            'FILTER_ANONYMOUS_INVENTORY_MODELING',
            'FILTER_OS'
          ],
          'metrics':[
            'METRIC_MEDIA_COST_ADVERTISER',
            'METRIC_IMPRESSIONS',
            'METRIC_CLICKS',
            'METRIC_TOTAL_CONVERSIONS',
            'METRIC_LAST_CLICKS',
            'METRIC_LAST_IMPRESSIONS',
            'METRIC_CM_POST_CLICK_REVENUE',
            'METRIC_CM_POST_VIEW_REVENUE',
            'METRIC_REVENUE_ADVERTISER'
          ]
        }
      }
    },
    'delete':False,
    'out':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'z_Dv360_Browser_Report_Dirty',
        'header':True,
        'schema':[
          {
            'name':'Advertiser_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Advertiser',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Advertiser_Currency',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Campaign_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Campaign',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Insertion_Order_Daily_Frequency',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Insertion_Order_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Insertion_Order',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Line_Item_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Line_Item',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Environment',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Week',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Month',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Year',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Partner_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Partner',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Line_Item_Type',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Device_Type',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Browser',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Anonymous_Inventory_Modeling',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Operating_System',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Media_Cost_Advertiser_Currency',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Impressions',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Clicks',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Total_Conversions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Post_Click_Conversions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Post_View_Conversions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Cm_Post_Click_Revenue',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Cm_Post_View_Revenue',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Revenue_Adv_Currency',
            'type':'FLOAT',
            'mode':'NULLABLE'
          }
        ]
      }
    }
  })

  dcm(config, {
    'auth':auth_cm,
    'timeout':90,
    'report':{
      'timeout':90,
      'account':cm_account_id,
      'filters':{
        'advertiser':{
          'values':cm_advertiser_ids
        }
      },
      'body':{
        'kind':'dfareporting#report',
        'name':recipe_name,
        'format':'CSV',
        'type':'STANDARD',
        'criteria':{
          'dateRange':{
            'kind':'dfareporting#dateRange',
            'relativeDateRange':date_range
          },
          'dimensions':[
            {
              'kind':'dfareporting#sortedDimension',
              'name':'campaign'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'campaignId'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'site'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'advertiser'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'advertiserId'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'browserPlatform'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'platformType'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'month'
            },
            {
              'kind':'dfareporting#sortedDimension',
              'name':'week'
            }
          ],
          'metricNames':[
            'impressions',
            'clicks',
            'totalConversions',
            'activityViewThroughConversions',
            'activityClickThroughConversions'
          ],
          'dimensionFilters':[
          ]
        },
        'schedule':{
          'active':True,
          'repeats':'WEEKLY',
          'every':1,
          'repeatsOnWeekDays':[
            'Sunday'
          ]
        },
        'delivery':{
          'emailOwner':False
        }
      }
    },
    'out':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'z_CM_Browser_Report_Dirty',
        'header':True,
        'is_incremental_load':False
      }
    },
    'delete':False
  })

  sdf(config, {
    'auth':auth_dv,
    'version':'SDF_VERSION_5_3',
    'partner_id':dv360_partner_id,
    'file_types':[
      'FILE_TYPE_CAMPAIGN',
      'FILE_TYPE_LINE_ITEM',
      'FILE_TYPE_INSERTION_ORDER'
    ],
    'filter_type':'FILTER_TYPE_ADVERTISER_ID',
    'read':{
      'filter_ids':{
        'single_cell':True,
        'bigquery':{
          'dataset':recipe_slug,
          'query':'select distinct Advertiser_Id from `{dataset}.z_Dv360_Browser_Report_Dirty`',
          'parameters':{
            'dataset':recipe_slug
          },
          'legacy':False
        }
      }
    },
    'time_partitioned_table':False,
    'create_single_day_table':False,
    'dataset':recipe_slug
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'values':[
        [
          'App',
          'App'
        ],
        [
          'Web optimized for device',
          'Web'
        ],
        [
          'Web not optimized for device',
          'Web'
        ]
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'table':'z_Environment'
    },
    'schema':[
      {
        'name':'Environment',
        'type':'STRING'
      },
      {
        'name':'Environment_clean',
        'type':'STRING'
      }
    ]
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'values':[
        [
          'Other',
          'TrueView',
          ''
        ],
        [
          'Opera',
          'Other',
          ''
        ],
        [
          'Google Chrome',
          'Chrome/Android',
          ''
        ],
        [
          'Android Webkit',
          'Chrome/Android',
          ''
        ],
        [
          'Safari',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 10',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 11',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 6',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 8',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 9',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 12',
          'Safari/iOS',
          'Includes Safari mobile web and webkit, both re v12'
        ],
        [
          'Safari 13',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 12+13',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 14',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 7',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 5',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 4',
          'Safari/iOS',
          ''
        ],
        [
          'Safari 3',
          'Safari/iOS',
          ''
        ],
        [
          'Firefox',
          'Firefox',
          ''
        ],
        [
          'Microsoft Edge',
          'IE/Edge',
          ''
        ],
        [
          'Internet Explorer 11',
          'IE/Edge',
          ''
        ],
        [
          'Internet Explorer 10',
          'IE/Edge',
          ''
        ],
        [
          'Internet Explorer 9',
          'IE/Edge',
          '',
          ''
        ],
        [
          'Internet Explorer 8',
          'IE/Edge',
          ''
        ]
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'table':'z_Browser'
    },
    'schema':[
      {
        'name':'Browser_Platform',
        'type':'STRING'
      },
      {
        'name':'Browser_Platform_clean',
        'type':'STRING'
      },
      {
        'name':'Browser_Platform_detail',
        'type':'STRING'
      }
    ]
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'values':[
        [
          'Other',
          'Other',
          0
        ],
        [
          'Android Webkit',
          'Android',
          1
        ],
        [
          'Firefox',
          'Firefox',
          2
        ],
        [
          'Chrome',
          'Chrome/Android',
          3
        ],
        [
          'Internet Explorer 9',
          'IE/Edge',
          4
        ],
        [
          'Safari',
          'Safari/iOS',
          6
        ],
        [
          'Safari 5',
          'Safari/iOS',
          7
        ],
        [
          'Internet Explorer 10',
          'IE/Edge',
          9
        ],
        [
          'Safari 6',
          'Safari/iOS',
          10
        ],
        [
          'Opera',
          'Opera',
          1038
        ],
        [
          'Internet Explorer 11',
          'IE/Edge',
          12
        ],
        [
          'Internet Explorer 8',
          'IE/Edge',
          13
        ],
        [
          'Internet Explorer 7',
          'IE/Edge',
          14
        ],
        [
          'Internet Explorer 6',
          'IE/Edge',
          15
        ],
        [
          'Internet Explorer 5',
          'IE/Edge',
          16
        ],
        [
          'Safari 4',
          'Safari/iOS',
          17
        ],
        [
          'Safari 3',
          'Safari/iOS',
          18
        ],
        [
          'Safari 2',
          'Safari/iOS',
          19
        ],
        [
          'Safari 1',
          'Safari/iOS',
          20
        ],
        [
          'Microsoft Edge',
          'IE/Edge',
          21
        ],
        [
          'Safari 7',
          'Safari/iOS',
          22
        ],
        [
          'Safari 8',
          'Safari/iOS',
          23
        ],
        [
          'Safari 9',
          'Safari/iOS',
          24
        ],
        [
          'Safari 10',
          'Safari/iOS',
          25
        ],
        [
          'Safari 11',
          'Safari/iOS',
          26
        ],
        [
          'Safari 12',
          'Safari/iOS',
          27
        ],
        [
          'Safari 13',
          'Safari/iOS',
          28
        ],
        [
          'Safari 14',
          'Safari/iOS',
          29
        ]
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'table':'z_Browser_SDF_lookup'
    },
    'schema':[
      {
        'name':'Browser_Platform',
        'type':'STRING'
      },
      {
        'name':'Browser_Platform_clean',
        'type':'STRING'
      },
      {
        'name':'Browser_Platform_id',
        'type':'INTEGER'
      }
    ]
  })

  sheets(config, {
    'auth':auth_sheets,
    'sheet':recipe_name,
    'tab':'SdfScoring',
    'range':'A2:M',
    'header':False,
    'out':{
      'auth':auth_bq,
      'bigquery':{
        'dataset':recipe_slug,
        'table':'z_dv360_scoring_matrix',
        'schema':[
          {
            'name':'Whole_Attribution_Score',
            'type':'INTEGER'
          },
          {
            'name':'Safari_Attribution_Score',
            'type':'INTEGER'
          },
          {
            'name':'Safari_Reach_Score',
            'type':'INTEGER'
          },
          {
            'name':'Audience_Targeting_Include',
            'type':'BOOL'
          },
          {
            'name':'Google_Audience_Include',
            'type':'BOOL'
          },
          {
            'name':'Contextual_Targeting_Include',
            'type':'BOOL'
          },
          {
            'name':'Conversion_Bid_Optimization',
            'type':'BOOL'
          },
          {
            'name':'Browser_Targeting_Include',
            'type':'BOOL'
          },
          {
            'name':'Safari_Browser_Targeting_Include',
            'type':'BOOL'
          },
          {
            'name':'Chrome_Browser_Targeting_Include',
            'type':'BOOL'
          },
          {
            'name':'FF_Browser_Targeting_Include',
            'type':'BOOL'
          },
          {
            'name':'View_Through_Enabled',
            'type':'BOOL'
          },
          {
            'name':'Comment',
            'type':'STRING'
          }
        ]
      }
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'values':[
        [
          'Firefox',
          'Firefox',
          'Firefox'
        ],
        [
          'Mozilla',
          'Firefox',
          'Firefox'
        ],
        [
          'Microsoft Edge',
          'IE/Edge',
          'IE/Edge'
        ],
        [
          'Microsoft Internet Explorer',
          'IE/Edge',
          'IE/Edge'
        ],
        [
          'Netscape Navigator',
          'Other',
          'Other'
        ],
        [
          'Opera',
          'Other',
          'Other'
        ],
        [
          'Opera Next',
          'Other',
          'Other'
        ],
        [
          'Roku',
          'Other',
          'Other'
        ],
        [
          'Yandex',
          'Other',
          'Other'
        ],
        [
          'Android',
          'Chrome/Android',
          'Android'
        ],
        [
          'Chrome',
          'Chrome/Android',
          'Chrome'
        ],
        [
          'iPad',
          'Safari/iOS',
          'iDevice'
        ],
        [
          'iPhone / iPod touch',
          'Safari/iOS',
          'iDevice'
        ],
        [
          'Safari',
          'Safari/iOS',
          'Safari'
        ],
        [
          'Unknown',
          'Unknown',
          'Unknown'
        ]
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'table':'z_CM_Browser_lookup'
    },
    'schema':[
      {
        'name':'Browser_Platform',
        'type':'STRING'
      },
      {
        'name':'Browser_Platform_clean',
        'type':'STRING'
      },
      {
        'name':'Browser_Platform_detail',
        'type':'STRING'
      }
    ]
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'values':[
        [
          'Desktop',
          'Desktop'
        ],
        [
          'Smart Phone',
          'Mobile'
        ],
        [
          'Tablet',
          'Mobile'
        ],
        [
          'Connected TV',
          'Connected TV'
        ]
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'table':'z_Device_Type'
    },
    'schema':[
      {
        'name':'Device_Type',
        'type':'STRING'
      },
      {
        'name':'Device',
        'type':'STRING'
      }
    ]
  })

  bigquery(config, {
    'auth':auth_bq,
    'from':{
      'values':[
        [
          'View-through',
          'Attributed'
        ],
        [
          'Attributed',
          'Attributed'
        ],
        [
          'Unattributed',
          'Unattributed'
        ],
        [
          'Click-through',
          'Unattributed'
        ]
      ]
    },
    'to':{
      'dataset':recipe_slug,
      'table':'z_Floodlight_Attribution'
    },
    'schema':[
      {
        'name':'Floodlight_Attribution_Type',
        'type':'STRING'
      },
      {
        'name':'Attribution_Type',
        'type':'STRING'
      }
    ]
  })

  itp_audit(config, {
    'auth_dv':auth_dv,
    'auth_cm':auth_cm,
    'auth_sheets':auth_sheets,
    'auth_bq':auth_bq,
    'account':cm_account_id,
    'dataset':recipe_slug,
    'sheet':recipe_name,
    'timeout':60,
    'read':{
      'advertiser_ids':{
        'single_cell':True,
        'bigquery':{
          'dataset':recipe_slug,
          'query':'select distinct Advertiser_Id from `{dataset}.z_CM_Browser_Report_Dirty`',
          'parameters':{
            'dataset':recipe_slug
          },
          'legacy':False
        }
      }
    },
    'floodlightConfigIds':floodlight_configuration_ids,
    'reportPrefix':recipe_name
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Dashboard that shows performance metrics across browser to see the impact of privacy changes.

      1. Follow the instructions from 1-this document.
         1.1 - this document: https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_timezone", help="Timezone for report dates.", default='America/Los_Angeles')
  parser.add_argument("-auth_sheets", help="Credentials used for Sheets.", default='user')
  parser.add_argument("-auth_bq", help="Credentials used for BigQuery.", default='service')
  parser.add_argument("-auth_dv", help="Credentials used for DV360.", default='user')
  parser.add_argument("-auth_cm", help="Credentials used for CM.", default='user')
  parser.add_argument("-cm_account_id", help="Campaign Manager Account Id.", default='')
  parser.add_argument("-floodlight_configuration_ids", help="Comma delimited list of floodlight configuration ids for the Campaign Manager floodlight report.", default=[])
  parser.add_argument("-date_range", help="Timeframe to run the ITP report for.", default='LAST_365_DAYS')
  parser.add_argument("-cm_advertiser_ids", help="Optional: Comma delimited list of CM advertiser ids.", default=[])
  parser.add_argument("-dv360_partner_id", help="DV360 Partner id", default='')
  parser.add_argument("-dv360_advertiser_ids", help="Optional: Comma delimited list of DV360 Advertiser ids.", default=[])
  parser.add_argument("-recipe_name", help="Name of report in DBM, should be unique.", default=None)
  parser.add_argument("-recipe_slug", help="BigQuery dataset for store dashboard tables.", default='ITP_Audit_Dashboard')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_itp_audit(config, args.recipe_timezone, args.auth_sheets, args.auth_bq, args.auth_dv, args.auth_cm, args.cm_account_id, args.floodlight_configuration_ids, args.date_range, args.cm_advertiser_ids, args.dv360_partner_id, args.dv360_advertiser_ids, args.recipe_name, args.recipe_slug)
