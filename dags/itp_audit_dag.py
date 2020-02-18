###########################################################################
# 
#  Copyright 2019 Google Inc.
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

  Install StarThinker in cloud composer from open source: 

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu	   
    l) Install All

--------------------------------------------------------------

ITP Audit Dashboard ( 2020 )

Dashboard that shows performance metrics across browser to see the impact of ITP.

Follow the instructions from <a href="https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/edit?usp=sharing" target="_blank">this document</a>

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'cm_account_id': '',  # Campaign Manager Account Id.
  'floodlight_configuration_id': '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
  'cm_advertiser_ids': '',  # Optional: Comma delimited list of DCM advertiser ids.
  'dv360_partner_ids': '',  # Comma delimited list of DV360 Partner ids.
  'dv360_advertiser_ids': '',  # Optional: Comma delimited list of DV360 Advertiser ids.
  'recipe_name': '',  # Name of document to deploy to.
}

TASKS = [
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
            'order': 7,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        }
      }
    }
  },
  {
    'dataset': {
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'recipe_name',
          'kind': 'string',
          'order': 7,
          'default': 'ITP_Audit_Dashboard',
          'description': 'BigQuery dataset for store dashboard tables.'
        }
      }
    }
  },
  {
    'dbm': {
      'auth': 'user',
      'report': {
        'timeout': 90,
        'filters': {
          'FILTER_ADVERTISER': {
            'values': {
              'field': {
                'name': 'dv360_advertiser_ids',
                'kind': 'integer_list',
                'order': 5,
                'default': '',
                'description': 'Optional: Comma delimited list of DV360 Advertiser ids.'
              }
            }
          },
          'FILTER_PARTNER': {
            'values': {
              'field': {
                'name': 'dv360_partner_ids',
                'kind': 'integer_list',
                'order': 4,
                'default': '',
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
                'order': 7,
                'description': 'Name of report in DBM, should be unique.'
              }
            },
            'dataRange': 'LAST_365_DAYS',
            'format': 'CSV'
          },
          'params': {
            'type': 'TYPE_GENERAL',
            'groupBys': [
              'FILTER_ADVERTISER',
              'FILTER_ADVERTISER_CURRENCY',
              'FILTER_MEDIA_PLAN',
              'FILTER_INSERTION_ORDER',
              'FILTER_LINE_ITEM',
              'FILTER_PAGE_LAYOUT',
              'FILTER_WEEK',
              'FILTER_MONTH',
              'FILTER_YEAR',
              'FILTER_PARTNER',
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
      'auth': 'user',
      'report': {
        'timeout': 90,
        'account': {
          'field': {
            'name': 'cm_account_id',
            'kind': 'string',
            'order': 1,
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
              'order': 7,
              'description': 'Name of report in DBM, should be unique.'
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
                  'order': 2,
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
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'report': {
        'timeout': 90,
        'account': {
          'field': {
            'name': 'cm_account_id',
            'kind': 'string',
            'order': 1,
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
                'description': 'Optional: Comma delimited list of DCM advertiser ids.'
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
              'order': 9,
              'prefix': 'ITP_Audit_Browser_',
              'default': 'ITP_Audit_Dashboard_Browser',
              'description': 'Name of the Campaign Manager browser report.'
            }
          },
          'fileName': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 9,
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
              'relativeDateRange': 'LAST_365_DAYS'
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
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit ',
          'kind': 'string',
          'order': 7,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Enviroment',
      'range': 'A:B',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit ',
          'kind': 'string',
          'order': 7,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Browser',
      'range': 'A:C',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit ',
          'kind': 'string',
          'order': 7,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'CM_Browser_lookup',
      'range': 'A:C',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit ',
          'kind': 'string',
          'order': 7,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Device_Type',
      'range': 'A:B',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit ',
          'kind': 'string',
          'order': 7,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Floodlight_Attribution',
      'range': 'A:B',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
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
      'auth': 'user',
      'report': {
        'name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'ITP_Audit_Browser_',
            'order': 7,
            'description': 'Name of report in DBM, should be unique.'
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 7,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'z_Dv360_Browser_Report_Dirty'
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
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'Campaign Manager Account Id.'
        }
      },
      'dataset': {
        'field': {
          'name': 'recipe_name',
          'kind': 'string',
          'order': 7,
          'default': 'ITP_Audit_Dashboard',
          'description': 'BigQuery dataset for store dashboard tables.'
        }
      },
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit ',
          'kind': 'string',
          'order': 7,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'timeout': 60
    }
  }
]

DAG_FACTORY = DAG_Factory('itp_audit', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
