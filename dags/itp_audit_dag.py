###########################################################################
#
#  Copyright 2020 Google LLC
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
#  This code generated (see starthinker/scripts for possible source):
#    - Command: "python starthinker_ui/manage.py airflow"
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

DV360 / CM360 Privacy Audit

Dashboard that shows performance metrics across browser to see the impact of privacy changes.

  - Follow the instructions from <a href="https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/edit?usp=sharing" target="_blank">this document</a>

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_timezone':'America/Los_Angeles',  # Timezone for report dates.
  'auth_sheets':'user',  # Credentials used for Sheets.
  'auth_bq':'service',  # Credentials used for BigQuery.
  'auth_dv':'user',  # Credentials used for DV360.
  'auth_cm':'user',  # Credentials used for CM.
  'cm_account_id':'',  # Campaign Manager Account Id.
  'floodlight_configuration_ids':[],  # Comma delimited list of floodlight configuration ids for the Campaign Manager floodlight report.
  'date_range':'LAST_365_DAYS',  # Timeframe to run the ITP report for.
  'cm_advertiser_ids':[],  # Optional: Comma delimited list of CM advertiser ids.
  'dv360_partner_id':'',  # DV360 Partner id
  'dv360_advertiser_ids':[],  # Optional: Comma delimited list of DV360 Advertiser ids.
  'recipe_name':'',  # Name of report in DBM, should be unique.
  'recipe_slug':'ITP_Audit_Dashboard',  # BigQuery dataset for store dashboard tables.
}

RECIPE = {
  'setup':{
    'hour':[
      3
    ],
    'day':[
      'Mon'
    ]
  },
  'tasks':[
    {
      'drive':{
        'auth':{'field':{'name':'auth_sheets','kind':'authentication','order':1,'default':'user','description':'Credentials used for Sheets.'}},
        'hour':[
        ],
        'copy':{
          'source':'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/',
          'destination':{'field':{'name':'recipe_name','prefix':'Privacy Audit ','kind':'string','order':1,'description':'Name of document to deploy to.','default':''}}
        }
      }
    },
    {
      'dataset':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}}
      }
    },
    {
      'dbm':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials used for DV360.'}},
        'report':{
          'name':{'field':{'name':'recipe_name','kind':'string','prefix':'ITP_Audit_Browser_','default':'ITP_Audit_Browser_','order':1,'description':'Name of report in DV360, should be unique.'}},
          'timeout':90,
          'filters':{
            'FILTER_ADVERTISER':{
              'values':{'field':{'name':'dv360_advertiser_ids','kind':'integer_list','order':6,'default':[],'description':'Optional: Comma delimited list of DV360 Advertiser ids.'}}
            },
            'FILTER_PARTNER':{
              'values':{'field':{'name':'dv360_partner_id','kind':'integer','order':5,'default':'','description':'DV360 Partner id'}}
            }
          },
          'body':{
            'timezoneCode':{'field':{'name':'recipe_timezone','kind':'timezone','description':'Timezone for report dates.','default':'America/Los_Angeles'}},
            'metadata':{
              'title':{'field':{'name':'recipe_name','default':'ITP_Audit_Browser_','kind':'string','prefix':'ITP_Audit_Browser_','order':1,'description':'Name of report in DV360, should be unique.'}},
              'dataRange':{'field':{'name':'date_range','kind':'choice','order':3,'default':'LAST_365_DAYS','choices':['LAST_7_DAYS','LAST_14_DAYS','LAST_30_DAYS','LAST_365_DAYS','LAST_60_DAYS','LAST_7_DAYS','LAST_90_DAYS','MONTH_TO_DATE','PREVIOUS_MONTH','PREVIOUS_QUARTER','PREVIOUS_WEEK','PREVIOUS_YEAR','QUARTER_TO_DATE','WEEK_TO_DATE','YEAR_TO_DATE'],'description':'Timeframe to run the ITP report for.'}},
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
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'dcm':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'user','description':'Credentials used for CM.'}},
        'timeout':90,
        'report':{
          'timeout':90,
          'account':{'field':{'name':'cm_account_id','kind':'string','order':2,'default':'','description':'Campaign Manager Account Id.'}},
          'filters':{
            'advertiser':{
              'values':{'field':{'name':'cm_advertiser_ids','kind':'integer_list','order':3,'default':[],'description':'Optional: Comma delimited list of CM advertiser ids.'}}
            }
          },
          'body':{
            'kind':'dfareporting#report',
            'name':{'field':{'name':'recipe_name','kind':'string','order':1,'prefix':'ITP_Audit_Browser_','default':'ITP_Audit_Dashboard_Browser','description':'Name of the Campaign Manager browser report.'}},
            'format':'CSV',
            'type':'STANDARD',
            'criteria':{
              'dateRange':{
                'kind':'dfareporting#dateRange',
                'relativeDateRange':{'field':{'name':'date_range','kind':'choice','order':3,'default':'LAST_365_DAYS','choices':['LAST_7_DAYS','LAST_14_DAYS','LAST_30_DAYS','LAST_365_DAYS','LAST_60_DAYS','LAST_7_DAYS','LAST_90_DAYS','MONTH_TO_DATE','PREVIOUS_MONTH','PREVIOUS_QUARTER','PREVIOUS_WEEK','PREVIOUS_YEAR','QUARTER_TO_DATE','WEEK_TO_DATE','YEAR_TO_DATE'],'description':'Timeframe to run the ITP report for.'}}
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
            'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':1,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
            'table':'z_CM_Browser_Report_Dirty',
            'header':True,
            'is_incremental_load':False
          }
        },
        'delete':False
      }
    },
    {
      'sdf':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials used for DV360.'}},
        'version':'SDF_VERSION_5_3',
        'partner_id':{'field':{'name':'dv360_partner_id','kind':'integer','order':5,'default':'','description':'DV360 Partner id'}},
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
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
              'query':'select distinct Advertiser_Id from `{dataset}.z_Dv360_Browser_Report_Dirty`',
              'parameters':{
                'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'description':'BigQuery dataset for store dashboard tables.'}}
              },
              'legacy':False
            }
          }
        },
        'time_partitioned_table':False,
        'create_single_day_table':False,
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}}
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'sheets':{
        'auth':{'field':{'name':'auth_sheets','kind':'authentication','order':1,'default':'user','description':'Credentials used for Sheets.'}},
        'sheet':{'field':{'name':'recipe_name','prefix':'Privacy Audit ','kind':'string','order':1,'description':'Name of document to deploy to.','default':''}},
        'tab':'SdfScoring',
        'range':'A2:M',
        'header':False,
        'out':{
          'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
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
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
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
      }
    },
    {
      'itp_audit':{
        'auth_dv':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials used for DV360.'}},
        'auth_cm':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'user','description':'Credentials used for CM.'}},
        'auth_sheets':{'field':{'name':'auth_sheets','kind':'authentication','order':1,'default':'user','description':'Credentials used for Sheets.'}},
        'auth_bq':{'field':{'name':'auth_bq','kind':'authentication','order':1,'default':'service','description':'Credentials used for BigQuery.'}},
        'account':{'field':{'name':'cm_account_id','kind':'string','order':2,'default':'','description':'Campaign Manager Account Id.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
        'sheet':{'field':{'name':'recipe_name','prefix':'Privacy Audit ','kind':'string','order':7,'description':'Name of document to deploy to.','default':''}},
        'timeout':60,
        'read':{
          'advertiser_ids':{
            'single_cell':True,
            'bigquery':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}},
              'query':'select distinct Advertiser_Id from `{dataset}.z_CM_Browser_Report_Dirty`',
              'parameters':{
                'dataset':{'field':{'name':'recipe_slug','kind':'string','order':7,'default':'ITP_Audit_Dashboard','description':'BigQuery dataset for store dashboard tables.'}}
              },
              'legacy':False
            }
          }
        },
        'floodlightConfigIds':{'field':{'name':'floodlight_configuration_ids','kind':'integer_list','order':2,'default':[],'description':'Comma delimited list of floodlight configuration ids for the Campaign Manager floodlight report.'}},
        'reportPrefix':{'field':{'name':'recipe_name','kind':'string','prefix':'ITP_Audit_Floodlight_','order':7,'description':'Name of report in DBM, should be unique.'}}
      }
    }
  ]
}

dag_maker = DAG_Factory('itp_audit', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
