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
from starthinker.task.bigquery.run import bigquery
from starthinker.task.google_api.run import google_api
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
      'timeout':120,
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
        },
        'schedule':{
          'frequency':'ONE_TIME'
        }
      },
      'schedule':{
        'frequency':'ONE_TIME'
      }
    },
    'delete':True
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
          'dataRange':'LAST_90_DAYS',
          'format':'CSV'
        },
        'params':{
          'type':'TYPE_GENERAL',
          'groupBys':[
            'FILTER_DATE',
            'FILTER_ADVERTISER_CURRENCY',
            'FILTER_LINE_ITEM_NAME',
            'FILTER_LINE_ITEM',
            'FILTER_USER_LIST',
            'FILTER_USER_LIST_TYPE'
          ],
          'metrics':[
            'METRIC_IMPRESSIONS',
            'METRIC_BILLABLE_IMPRESSIONS',
            'METRIC_CLICKS',
            'METRIC_CTR',
            'METRIC_TOTAL_CONVERSIONS',
            'METRIC_LAST_CLICKS',
            'METRIC_LAST_IMPRESSIONS',
            'METRIC_REVENUE_ADVERTISER',
            'METRIC_CM360_POST_VIEW_REVENUE',
            'METRIC_CM360_POST_CLICK_REVENUE'
          ],
          'options':{
            'includeOnlyTargetedUserLists':False
          }
        },
        'schedule':{
          'frequency':'DAILY'
        }
      }
    },
    'delete':False
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
          'active':False,
          'repeats':'WEEKLY',
          'repeatsOnWeekDays':[
            'MONDAY'
          ],
          'every':1
        },
        'delivery':{
          'emailOwner':False
        }
      },
      'delete':True
    }
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

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'firstAndThirdPartyAudiences.list',
    'kwargs':{
      'partnerId':dv360_partner_id
    },
    'results':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'z_dv_audiences'
      }
    }
  })

  dbm(config, {
    'auth':auth_dv,
    'report':{
      'name':recipe_name
    },
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
    'report':{
      'account':cm_account_id,
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'z_CM_Browser_Report_Dirty',
        'header':True,
        'is_incremental_load':False
      }
    }
  })

  dbm(config, {
    'auth':auth_dv,
    'report':{
      'name':recipe_name
    },
    'out':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':recipe_slug,
        'table':'z_Dv_Audience_Report',
        'header':True,
        'schema':[
          {
            'name':'Advertiser_Currency',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Line_Item',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Line_Item_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Audience_List_Id',
            'type':'INTEGER',
            'mode':'NULLABLE'
          },
          {
            'name':'Audience_List_Type',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'ReportDate',
            'type':'STRING',
            'mode':'NULLABLE'
          },
          {
            'name':'Impressions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Billable_Impressions',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Clicks',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'CTR',
            'type':'FLOAT',
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
            'name':'Revenue_Adv_Currency',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Cm_Post_View_Revenue',
            'type':'FLOAT',
            'mode':'NULLABLE'
          },
          {
            'name':'Cm_Post_Click_Revenue',
            'type':'FLOAT',
            'mode':'NULLABLE'
          }
        ]
      }
    }
  })

  bigquery(config, {
    'auth':auth_bq,
    'run':{
      'legacy':False,
      'query':'CREATE OR REPLACE TABLE `{dataset}.DV_Audiences` AS with dv_entities as ( SELECT distinct b.Advertiser, b.Advertiser_Id, b.Campaign, b.Campaign_Id, b.Insertion_Order, b.Insertion_Order_Id, b.Line_Item_Id FROM `{dataset}.z_Dv360_Browser_Report_Dirty` AS b ) SELECT case when a.firstAndThirdPartyAudienceType = 'FIRST_AND_THIRD_PARTY_AUDIENCE_TYPE_UNSPECIFIED' then 'N/A' when a.firstAndThirdPartyAudienceType is null then 'N/A' when a.firstAndThirdPartyAudienceType = 'FIRST_AND_THIRD_PARTY_AUDIENCE_TYPE_FIRST_PARTY' then 'First Party' when a.firstAndThirdPartyAudienceType = 'FIRST_AND_THIRD_PARTY_AUDIENCE_TYPE_THIRD_PARTY' then 'Third Party' end as firstAndThirdPartyAudienceType, CASE WHEN a.audienceType = 'AUDIENCE_TYPE_UNSPECIFIED' THEN 'N/A' WHEN a.audienceType is null THEN 'N/A' WHEN a.audienceType = 'CUSTOMER_MATCH_CONTACT_INFO' THEN 'CustomerMatch ContactInfo' WHEN a.audienceType = 'CUSTOMER_MATCH_DEVICE_ID' THEN 'CustomerMatch DeviceId' WHEN a.audienceType = 'CUSTOMER_MATCH_USER_ID' THEN 'CustomerMatch UserId' WHEN a.audienceType = 'ACTIVITY_BASED' THEN 'Activity Based' WHEN a.audienceType = 'FREQUENCY_CAP' THEN 'Frequency Cap' WHEN a.audienceType = 'TAG_BASED' THEN 'Tag Based' WHEN a.audienceType = 'YOUTUBE_USERS' THEN 'YouTube Users' WHEN a.audienceType = 'LICENSED' THEN 'Licensed' ELSE a.audienceType END AS audienceType, b.Advertiser, b.Advertiser_Id, b.Campaign, b.Campaign_Id, b.Insertion_Order, b.Insertion_Order_Id, r.Line_Item, r.Line_Item_Id, r.Audience_List_Id, r.Date, r.Impressions, r.Clicks, r.CTR, r.Total_Conversions, r.Post_Click_Conversions, r.Post_View_Conversions, r.Revenue_Adv_Currency, r.Cm_Post_View_Revenue, r.Cm_Post_Click_Revenue FROM `{dataset}.z_Dv_Audience_Report` AS r LEFT JOIN `{dataset}.z_dv_audiences` AS a ON r.Audience_List_Id = a.firstAndThirdPartyAudienceId LEFT JOIN dv_entities AS b ON b.Line_Item_Id = r.Line_Item_Id;',
      'parameters':{
        'dataset':recipe_slug
      }
    }
  })

  itp_audit(config, {
    'auth_dv':auth_dv,
    'auth_cm':auth_cm,
    'auth_sheets':auth_sheets,
    'auth_bq':auth_bq,
    'account':cm_account_id,
    'dataset':recipe_slug,
    'sheet':recipe_name,
    'timeout':120,
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
