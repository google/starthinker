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

DV360 ITP Audit

Dashboard that shows performance metrics across browser to see the impact of ITP.

  - Follow the instructions from <a href="https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/edit?usp=sharing" target="_blank">this document</a>

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'recipe_name': '',  # Name of document to deploy to.
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_slug': 'ITP_Audit_Dashboard',  # BigQuery dataset for store dashboard tables.
  'auth_read': 'user',  # Credentials used for reading data.
  'cm_account_id': '',  # Campaign Manager Account Id.
  'date_range': 'LAST_365_DAYS',  # Timeframe to run the ITP report for.
  'cm_advertiser_ids': '',  # Optional: Comma delimited list of CM advertiser ids.
  'floodlight_configuration_id': '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
  'dv360_partner_ids': [],  # Comma delimited list of DV360 Partner ids.
  'dv360_advertiser_ids': [],  # Optional: Comma delimited list of DV360 Advertiser ids.
}

RECIPE = {
  'setup': {
    'hour': [
      3
    ],
    'day': [
      'Mon'
    ]
  },
  'tasks': [
    {
      'drive': {
        'auth': 'user',
        'hour': [
        ],
        'copy': {
          'source': 'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/',
          'destination': {
            'field': {
              'name': 'recipe_name',
              'prefix': 'ITP Audit ',
              'kind': 'string',
              'order': 1,
              'description': 'Name of document to deploy to.',
              'default': ''
            }
          }
        }
      }
    },
    {
      'dataset': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Credentials used for writing data.'
          }
        },
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'order': 1,
            'default': 'ITP_Audit_Dashboard',
            'description': 'BigQuery dataset for store dashboard tables.'
          }
        }
      }
    },
    {
      'dbm': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'report': {
          'timeout': 90,
          'filters': {
            'FILTER_ADVERTISER': {
              'values': {
                'field': {
                  'name': 'dv360_advertiser_ids',
                  'kind': 'integer_list',
                  'order': 6,
                  'default': [
                  ],
                  'description': 'Optional: Comma delimited list of DV360 Advertiser ids.'
                }
              }
            },
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'name': 'dv360_partner_ids',
                  'kind': 'integer_list',
                  'order': 5,
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 Partner ids.'
                }
              }
            }
          },
          'body': {
            'timezoneCode': {
              'field': {
                'name': 'recipe_timezone',
                'kind': 'timezone',
                'description': 'Timezone for report dates.',
                'default': 'America/Los_Angeles'
              }
            },
            'metadata': {
              'title': {
                'field': {
                  'name': 'recipe_name',
                  'kind': 'string',
                  'prefix': 'ITP_Audit_Browser_',
                  'order': 1,
                  'description': 'Name of report in DV360, should be unique.'
                }
              },
              'dataRange': {
                'field': {
                  'name': 'date_range',
                  'kind': 'choice',
                  'order': 3,
                  'default': 'LAST_365_DAYS',
                  'choices': [
                    'LAST_7_DAYS',
                    'LAST_14_DAYS',
                    'LAST_30_DAYS',
                    'LAST_365_DAYS',
                    'LAST_60_DAYS',
                    'LAST_7_DAYS',
                    'LAST_90_DAYS',
                    'MONTH_TO_DATE',
                    'PREVIOUS_MONTH',
                    'PREVIOUS_QUARTER',
                    'PREVIOUS_WEEK',
                    'PREVIOUS_YEAR',
                    'QUARTER_TO_DATE',
                    'WEEK_TO_DATE',
                    'YEAR_TO_DATE'
                  ],
                  'description': 'Timeframe to run the ITP report for.'
                }
              },
              'format': 'CSV'
            },
            'params': {
              'type': 'TYPE_GENERAL',
              'groupBys': [
                'FILTER_PARTNER',
                'FILTER_PARTNER_NAME',
                'FILTER_ADVERTISER',
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_MEDIA_PLAN',
                'FILTER_MEDIA_PLAN_NAME',
                'FILTER_INSERTION_ORDER',
                'FILTER_INSERTION_ORDER_NAME',
                'FILTER_LINE_ITEM',
                'FILTER_LINE_ITEM_NAME',
                'FILTER_PAGE_LAYOUT',
                'FILTER_WEEK',
                'FILTER_MONTH',
                'FILTER_YEAR',
                'FILTER_LINE_ITEM_TYPE',
                'FILTER_DEVICE_TYPE',
                'FILTER_BROWSER'
              ],
              'metrics': [
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
        'delete': False
      }
    },
    {
      'dcm': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'report': {
          'timeout': 90,
          'account': {
            'field': {
              'name': 'cm_account_id',
              'kind': 'integer',
              'order': 2,
              'default': '',
              'description': 'Campaign Manager Account Id.'
            }
          },
          'body': {
            'kind': 'dfareporting#report',
            'name': {
              'field': {
                'name': 'recipe_name',
                'kind': 'string',
                'prefix': 'ITP_Audit_Floodlight_',
                'order': 1,
                'description': 'Name of report in DV360, should be unique.'
              }
            },
            'format': 'CSV',
            'type': 'FLOODLIGHT',
            'floodlightCriteria': {
              'dateRange': {
                'kind': 'dfareporting#dateRange',
                'relativeDateRange': 'LAST_30_DAYS'
              },
              'floodlightConfigId': {
                'kind': 'dfareporting#dimensionValue',
                'dimensionName': 'dfa:floodlightConfigId',
                'value': {
                  'field': {
                    'name': 'floodlight_configuration_id',
                    'kind': 'integer',
                    'order': 4,
                    'default': '',
                    'description': 'Floodlight Configuration Id for the Campaign Manager floodlight report.'
                  }
                },
                'matchType': 'EXACT'
              },
              'reportProperties': {
                'includeUnattributedIPConversions': False,
                'includeUnattributedCookieConversions': True
              },
              'dimensions': [
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:site'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:floodlightAttributionType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:interactionType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:pathType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:browserPlatform'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:platformType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:week'
                }
              ],
              'metricNames': [
                'dfa:activityClickThroughConversions',
                'dfa:activityViewThroughConversions',
                'dfa:totalConversions',
                'dfa:totalConversionsRevenue'
              ]
            },
            'schedule': {
              'active': True,
              'repeats': 'WEEKLY',
              'every': 1,
              'repeatsOnWeekDays': [
                'Sunday'
              ]
            },
            'delivery': {
              'emailOwner': False
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_Floodlight_CM_Report',
            'is_incremental_load': False
          }
        },
        'delete': False
      }
    },
    {
      'dcm': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'report': {
          'timeout': 90,
          'account': {
            'field': {
              'name': 'cm_account_id',
              'kind': 'integer',
              'order': 2,
              'default': '',
              'description': 'Campaign Manager Account Id.'
            }
          },
          'filters': {
            'dfa:advertiser': {
              'values': {
                'field': {
                  'name': 'cm_advertiser_ids',
                  'kind': 'integer_list',
                  'order': 3,
                  'default': '',
                  'description': 'Optional: Comma delimited list of CM advertiser ids.'
                }
              }
            }
          },
          'body': {
            'kind': 'dfareporting#report',
            'name': {
              'field': {
                'name': 'recipe_name',
                'kind': 'string',
                'order': 1,
                'prefix': 'ITP_Audit_Browser_',
                'default': 'ITP_Audit_Dashboard_Browser',
                'description': 'Name of the Campaign Manager browser report.'
              }
            },
            'format': 'CSV',
            'type': 'STANDARD',
            'criteria': {
              'dateRange': {
                'kind': 'dfareporting#dateRange',
                'relativeDateRange': {
                  'field': {
                    'name': 'date_range',
                    'kind': 'choice',
                    'order': 3,
                    'default': 'LAST_365_DAYS',
                    'choices': [
                      'LAST_7_DAYS',
                      'LAST_14_DAYS',
                      'LAST_30_DAYS',
                      'LAST_365_DAYS',
                      'LAST_60_DAYS',
                      'LAST_7_DAYS',
                      'LAST_90_DAYS',
                      'MONTH_TO_DATE',
                      'PREVIOUS_MONTH',
                      'PREVIOUS_QUARTER',
                      'PREVIOUS_WEEK',
                      'PREVIOUS_YEAR',
                      'QUARTER_TO_DATE',
                      'WEEK_TO_DATE',
                      'YEAR_TO_DATE'
                    ],
                    'description': 'Timeframe to run the ITP report for.'
                  }
                }
              },
              'dimensions': [
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:campaign'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:campaignId'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:site'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:advertiser'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:advertiserId'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:browserPlatform'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:platformType'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:month'
                },
                {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:week'
                }
              ],
              'metricNames': [
                'dfa:impressions',
                'dfa:clicks',
                'dfa:totalConversions',
                'dfa:activityViewThroughConversions',
                'dfa:activityClickThroughConversions'
              ],
              'dimensionFilters': [
              ]
            },
            'schedule': {
              'active': True,
              'repeats': 'WEEKLY',
              'every': 1,
              'repeatsOnWeekDays': [
                'Sunday'
              ]
            },
            'delivery': {
              'emailOwner': False
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_CM_Browser_Report_Dirty',
            'is_incremental_load': False
          }
        },
        'delete': False
      }
    },
    {
      'sheets': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        },
        'tab': 'Enviroment',
        'range': 'A:B',
        'header': True,
        'out': {
          'auth': {
            'field': {
              'name': 'auth_write',
              'kind': 'authentication',
              'order': 1,
              'default': 'service',
              'description': 'Credentials used for writing data.'
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_Environment'
          }
        }
      }
    },
    {
      'sheets': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        },
        'tab': 'Browser',
        'range': 'A:C',
        'header': True,
        'out': {
          'auth': {
            'field': {
              'name': 'auth_write',
              'kind': 'authentication',
              'order': 1,
              'default': 'service',
              'description': 'Credentials used for writing data.'
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_Browser'
          }
        }
      }
    },
    {
      'sheets': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        },
        'tab': 'CM_Browser_lookup',
        'range': 'A:C',
        'header': True,
        'out': {
          'auth': {
            'field': {
              'name': 'auth_write',
              'kind': 'authentication',
              'order': 1,
              'default': 'service',
              'description': 'Credentials used for writing data.'
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_CM_Browser_lookup'
          }
        }
      }
    },
    {
      'sheets': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        },
        'tab': 'Device_Type',
        'range': 'A:B',
        'header': True,
        'out': {
          'auth': {
            'field': {
              'name': 'auth_write',
              'kind': 'authentication',
              'order': 1,
              'default': 'service',
              'description': 'Credentials used for writing data.'
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_Device_Type'
          }
        }
      }
    },
    {
      'sheets': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        },
        'tab': 'Floodlight_Attribution',
        'range': 'A:B',
        'header': True,
        'out': {
          'auth': {
            'field': {
              'name': 'auth_write',
              'kind': 'authentication',
              'order': 1,
              'default': 'service',
              'description': 'Credentials used for writing data.'
            }
          },
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_Floodlight_Attribution'
          }
        }
      }
    },
    {
      'dbm': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'report': {
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'prefix': 'ITP_Audit_Browser_',
              'order': 1,
              'description': 'Name of report in DV360, should be unique.'
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': 'ITP_Audit_Dashboard',
                'description': 'BigQuery dataset for store dashboard tables.'
              }
            },
            'table': 'z_Dv360_Browser_Report_Dirty',
            'header': True,
            'schema': [
              {
                'name': 'Partner_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Partner',
                'type': 'STRING'
              },
              {
                'name': 'Advertiser_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Advertiser',
                'type': 'STRING'
              },
              {
                'name': 'Advertiser_Currency',
                'type': 'STRING'
              },
              {
                'name': 'Campaign_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Campaign',
                'type': 'STRING'
              },
              {
                'name': 'Insertion_Order_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Insertion_Order',
                'type': 'STRING'
              },
              {
                'name': 'Line_Item_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Line_Item',
                'type': 'STRING'
              },
              {
                'name': 'Environment',
                'type': 'STRING',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Week',
                'type': 'STRING',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Month',
                'type': 'STRING',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Year',
                'type': 'INTEGER',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Line_Item_Type',
                'type': 'STRING',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Device_Type',
                'type': 'STRING',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Browser',
                'type': 'STRING',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Media_Cost_Advertiser_Currency',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Impressions',
                'type': 'INTEGER',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Clicks',
                'type': 'INTEGER',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Total_Conversions',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Post_Click_Conversions',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Post_View_Conversions',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Cm_Post_Click_Revenue',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Cm_Post_View_Revenue',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              },
              {
                'name': 'Revenue_Adv_Currency',
                'type': 'FLOAT',
                'mode': 'NULLABLE'
              }
            ]
          }
        }
      }
    },
    {
      'itp_audit': {
        'auth': 'service',
        'account': {
          'field': {
            'name': 'cm_account_id',
            'kind': 'integer',
            'order': 2,
            'default': '',
            'description': 'Campaign Manager Account Id.'
          }
        },
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'order': 1,
            'default': 'ITP_Audit_Dashboard',
            'description': 'BigQuery dataset for store dashboard tables.'
          }
        },
        'sheet': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        },
        'timeout': 60
      }
    }
  ]
}

dag_maker = DAG_Factory('itp_audit', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
