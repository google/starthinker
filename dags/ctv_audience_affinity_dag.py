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

cTV Inventory Availability Dashboard

The cTV Audience Affinity dashboard is designed to give clients insights into which cTV apps their audiences have a high affinity for using.  The goal of this dashboard is to provide some assistance with the lack of audience targeting for cTV within DV360.

  - Find instructions and recommendations for this dashboard <a href="https://docs.google.com/document/d/120kcR9OrS4hGdTxRK0Ig2koNmm6Gl7sH0L6U56N0SAM/view?usp=sharing" target="_blank">here</a>

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'dataset':'',  # BigQuery Dataset where all data will live.
  'recipe_project':'',  # Project where BigQuery dataset will be created.
  'recipe_name':'',  # Name of document to deploy to.
  'auth_write':'service',  # Credentials used for writing data.
  'partner_id':'',  # DV360 Partner id.
  'auth_read':'user',  # Credentials used for reading data.
  'audience_ids':'',  # Comma separated list of Audience Ids
}

RECIPE = {
  'tasks':[
    {
      'drive':{
        'auth':'user',
        'copy':{
          'source':'https://docs.google.com/spreadsheets/d/1PPPk2b4gGJHNgQ4hXLiTKzH8pRIdlF5fNy9VCw1v7tM/',
          'destination':{'field':{'name':'recipe_name','prefix':'cTV App Match Table ','kind':'string','order':1,'description':'Name of document to deploy to.','default':''}}
        }
      }
    },
    {
      'dataset':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'BigQuery Dataset where all data will live.'}}
      }
    },
    {
      'dbm':{
        'auth':'user',
        'report':{
          'body':{
            'timezoneCode':'America/Los_Angeles',
            'kind':'doubleclickbidmanager#query',
            'metadata':{
              'title':{'field':{'name':'recipe_name','kind':'string','prefix':'us_country_app_'}},
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
                  'value':{'field':{'name':'partner_id','kind':'integer','order':1,'description':'DV360 Partner id.'}}
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
            'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'BigQuery Dataset where all data will live.'}},
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
      }
    },
    {
      'dbm':{
        'auth':'user',
        'report':{
          'body':{
            'timezoneCode':'America/Los_Angeles',
            'kind':'doubleclickbidmanager#query',
            'metadata':{
              'title':{'field':{'name':'recipe_name','kind':'string','prefix':'us_country_baseline_'}},
              'dataRange':'LAST_30_DAYS',
              'format':'CSV',
              'sendNotification':False
            },
            'params':{
              'type':'TYPE_INVENTORY_AVAILABILITY',
              'filters':[
                {
                  'type':'FILTER_PARTNER',
                  'value':{'field':{'name':'partner_id','kind':'integer','order':1,'description':'DV360 Partner id.'}}
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
            'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'BigQuery Dataset where all data will live.'}},
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
      }
    },
    {
      'dbm':{
        'auth':'user',
        'report':{
          'filters':{
            'FILTER_USER_LIST':{
              'single_cell':True,
              'values':{'field':{'name':'audience_ids','kind':'integer_list','order':2,'description':'Comma separated list of Audience Ids'}}
            }
          },
          'body':{
            'timezoneCode':'America/Los_Angeles',
            'kind':'doubleclickbidmanager#query',
            'metadata':{
              'title':{'field':{'name':'recipe_name','kind':'string','prefix':'us_audience_baseline_'}},
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
                  'value':{'field':{'name':'partner_id','kind':'integer','order':1,'description':'DV360 Partner id.'}}
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
            'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'BigQuery Dataset where all data will live.'}},
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
      }
    },
    {
      'dbm':{
        'auth':'user',
        'report':{
          'filters':{
            'FILTER_USER_LIST':{
              'single_cell':True,
              'values':{'field':{'name':'audience_ids','kind':'integer_list','order':2,'description':'Comma separated list of Audience Ids'}}
            }
          },
          'body':{
            'timezoneCode':'America/Los_Angeles',
            'kind':'doubleclickbidmanager#query',
            'metadata':{
              'title':{'field':{'name':'recipe_name','kind':'string','prefix':'us_audience_app_'}},
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
                  'value':{'field':{'name':'partner_id','kind':'integer','order':1,'description':'DV360 Partner id.'}}
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
            'dataset':{'field':{'name':'dataset','kind':'string','order':3,'default':'','description':'BigQuery Dataset where all data will live.'}},
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
      }
    },
    {
      'sheets':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'sheet':{'field':{'name':'recipe_name','prefix':'cTV App Match Table ','kind':'string','order':1,'description':'Name of document to deploy to.','default':''}},
        'tab':'data',
        'range':'A:Z',
        'header':True,
        'out':{
          'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','description':'BigQuery Dataset where all data will live.'}},
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
      }
    },
    {
      'bigquery':{
        'description':'The query to join all the IAR reports into an Affinity Index.',
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'query':"WITH audience_app_clean AS ( SELECT ctv_app.CTV_App_name AS ctv_app_name, user_list, app_url, IF (app_url LIKE '%Android%' OR app_url LIKE '%iOS', 'App', 'Domain') AS app_or_domain, CAST( IF (cast(impressions as string) LIKE '%< 1000%', cast(0 as int64), CAST(impressions AS int64)) AS int64) AS potential_impressions, CAST( IF (uniques LIKE '%< 1000%', cast(0 as int64), CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions FROM `[PARAMETER].[PARAMETER].us_audience_app` AS a LEFT JOIN `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app ON a.app_url = ctv_app.Publisher_Name ), us_country_app_clean AS ( SELECT a.app_url, ctv_app.CTV_App_name AS ctv_app_name, CAST( IF (CAST(a.impressions AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(a.impressions AS int64)) AS int64) AS POtential_ImpressionS, CAST( IF (CAST(a.uniques AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(a.uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions FROM `[PARAMETER].[PARAMETER].us_country_app` AS a LEFT JOIN `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app ON a.app_url = ctv_app.Publisher_Name ) SELECT audience_app.ctv_app_name, audience_app.app_or_domain, audience_app.user_list AS audience_list, audience_app.Potential_Impressions AS audience_app_impressions, audience_app.Unique_Cookies_With_Impressions AS audience_app_uniques, audience_baseline.Potential_Impressions AS audience_baseline_impressions, audience_baseline.Unique_Cookies_With_Impressions AS audience_baseline_uniques, country_app.Potential_Impressions AS country_app_impressions, country_app.Unique_Cookies_With_Impressions AS country_app_uniques, country_baseline.Potential_Impressions AS country_baseline_impressions, country_baseline.Unique_Cookies_With_Impressions AS country_baseline_uniques, ((audience_app.Unique_Cookies_With_Impressions/NULLIF(audience_baseline.Unique_Cookies_With_Impressions, 0))/NULLIF((country_app.Unique_Cookies_With_Impressions/NULLIF(CAST(country_baseline.Unique_Cookies_With_Impressions AS int64), 0)), 0))*100 AS affinity_index FROM ( SELECT user_list, CAST( IF (cast(impressions as string) LIKE '%< 1000%', cast(0 as int64), CAST(impressions AS int64)) AS int64) AS POTential_impressions, CAST( IF (uniques LIKE '%< 100%', cast(0 as int64), CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions FROM `[PARAMETER].[PARAMETER].us_audience_baseline` ) AS audience_baseline JOIN ( SELECT ctv_app_name, user_list, app_or_domain, SUM(potential_impressions) as poTEntial_impressions, SUM(unique_cookies_with_impressions) as unique_cookies_with_impressions, FROM audience_app_clean GROUP BY ctv_app_name, user_list, app_or_domain) AS audience_app ON audience_baseline.user_list = audience_app.user_list LEFT JOIN ( SELECT ctv_app_name, SUM(potential_impressions) as potENtial_impressions, SUM(unique_cookies_with_impressions) as unique_cookies_with_impressions, FROM us_country_app_clean GROUP BY ctv_app_name) AS country_app ON country_app.ctv_app_name = audience_app.ctv_app_name CROSS JOIN ( SELECT CAST( IF (CAST(impressions AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(impressions AS int64)) AS int64) AS PotenTial_Impressions, CAST( IF (CAST(uniques AS STRING) LIKE '%< 1000%', cast(0 as int64), CAST(uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions FROM `[PARAMETER].[PARAMETER].us_country_baseline` ) AS country_baseline",
          'legacy':False,
          'parameters':[
            {'field':{'name':'recipe_project','kind':'string','description':'Project where BigQuery dataset will be created.'}},
            {'field':{'name':'dataset','kind':'string','description':'Place where tables will be written in BigQuery.'}},
            {'field':{'name':'recipe_project','kind':'string','description':'Project where BigQuery dataset will be created.'}},
            {'field':{'name':'dataset','kind':'string','description':'Place where tables will be written in BigQuery.'}},
            {'field':{'name':'recipe_project','kind':'string','description':'Project where BigQuery dataset will be created.'}},
            {'field':{'name':'dataset','kind':'string','description':'Place where tables will be written in BigQuery.'}},
            {'field':{'name':'recipe_project','kind':'string','description':'Project where BigQuery dataset will be created.'}},
            {'field':{'name':'dataset','kind':'string','description':'Place where tables will be written in BigQuery.'}},
            {'field':{'name':'recipe_project','kind':'string','description':'Project where BigQuery dataset will be created.'}},
            {'field':{'name':'dataset','kind':'string','description':'Place where tables will be written in BigQuery.'}},
            {'field':{'name':'recipe_project','kind':'string','description':'Project where BigQuery dataset will be created.'}},
            {'field':{'name':'dataset','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          ]
        },
        'to':{
          'dataset':{'field':{'name':'dataset','kind':'string','description':'BigQuery Dataset where all data will live.'}},
          'table':'final_table'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('ctv_audience_affinity', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
