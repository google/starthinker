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

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_name': '',  # Name of document to deploy to.
  'recipe_slug': 'ITP_Audit_Dashboard',  # BigQuery dataset for store dashboard tables.
  'auth_write': 'service',  # Credentials used for writing data.
  'cm_account_id': '',  # Campaign Manager Account Id.
  'cm_advertiser_ids': '',  # Optional: Comma delimited list of CM advertiser ids.
  'floodlight_configuration_id': '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
  'dv360_partner_ids': '',  # Comma delimited list of DV360 Partner ids.
  'dv360_advertiser_ids': '',  # Optional: Comma delimited list of DV360 Advertiser ids.
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
            'description': 'Name of document to deploy to.',
            'name': 'recipe_name',
            'kind': 'string',
            'order': 1,
            'prefix': 'ITP Audit ',
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
          'description': 'Credentials used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'dataset': {
        'field': {
          'description': 'BigQuery dataset for store dashboard tables.',
          'kind': 'string',
          'name': 'recipe_slug',
          'order': 1,
          'default': 'ITP_Audit_Dashboard'
        }
      }
    }
  },
  {
    'dbm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'delete': False,
      'report': {
        'filters': {
          'FILTER_ADVERTISER': {
            'values': {
              'field': {
                'description': 'Optional: Comma delimited list of DV360 Advertiser ids.',
                'kind': 'integer_list',
                'name': 'dv360_advertiser_ids',
                'order': 6,
                'default': ''
              }
            }
          },
          'FILTER_PARTNER': {
            'values': {
              'field': {
                'description': 'Comma delimited list of DV360 Partner ids.',
                'kind': 'integer_list',
                'name': 'dv360_partner_ids',
                'order': 5,
                'default': ''
              }
            }
          }
        },
        'body': {
          'timezoneCode': {
            'field': {
              'description': 'Timezone for report dates.',
              'name': 'recipe_timezone',
              'default': 'America/Los_Angeles',
              'kind': 'timezone'
            }
          },
          'metadata': {
            'title': {
              'field': {
                'name': 'recipe_name',
                'order': 1,
                'prefix': 'ITP_Audit_Browser_',
                'description': 'Name of report in DV360, should be unique.',
                'kind': 'string'
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
        },
        'timeout': 90
      }
    }
  },
  {
    'dcm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_Floodlight_CM_Report',
          'is_incremental_load': False
        }
      },
      'delete': False,
      'report': {
        'account': {
          'field': {
            'description': 'Campaign Manager Account Id.',
            'kind': 'string',
            'name': 'cm_account_id',
            'order': 2,
            'default': ''
          }
        },
        'body': {
          'type': 'FLOODLIGHT',
          'delivery': {
            'emailOwner': False
          },
          'name': {
            'field': {
              'name': 'recipe_name',
              'order': 1,
              'prefix': 'ITP_Audit_Floodlight_',
              'description': 'Name of report in DV360, should be unique.',
              'kind': 'string'
            }
          },
          'format': 'CSV',
          'floodlightCriteria': {
            'dimensions': [
              {
                'name': 'dfa:site',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:floodlightAttributionType',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:interactionType',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:pathType',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:browserPlatform',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:platformType',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:week',
                'kind': 'dfareporting#sortedDimension'
              }
            ],
            'floodlightConfigId': {
              'matchType': 'EXACT',
              'dimensionName': 'dfa:floodlightConfigId',
              'value': {
                'field': {
                  'description': 'Floodlight Configuration Id for the Campaign Manager floodlight report.',
                  'kind': 'integer',
                  'name': 'floodlight_configuration_id',
                  'order': 4,
                  'default': ''
                }
              },
              'kind': 'dfareporting#dimensionValue'
            },
            'reportProperties': {
              'includeUnattributedIPConversions': False,
              'includeUnattributedCookieConversions': True
            },
            'metricNames': [
              'dfa:activityClickThroughConversions',
              'dfa:activityViewThroughConversions',
              'dfa:totalConversions',
              'dfa:totalConversionsRevenue'
            ],
            'dateRange': {
              'relativeDateRange': 'LAST_30_DAYS',
              'kind': 'dfareporting#dateRange'
            }
          },
          'kind': 'dfareporting#report',
          'schedule': {
            'repeatsOnWeekDays': [
              'Sunday'
            ],
            'repeats': 'WEEKLY',
            'active': True,
            'every': 1
          }
        },
        'timeout': 90
      }
    }
  },
  {
    'dcm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_CM_Browser_Report_Dirty',
          'is_incremental_load': False
        }
      },
      'delete': False,
      'report': {
        'account': {
          'field': {
            'description': 'Campaign Manager Account Id.',
            'kind': 'string',
            'name': 'cm_account_id',
            'order': 2,
            'default': ''
          }
        },
        'timeout': 90,
        'body': {
          'fileName': {
            'field': {
              'description': 'Name of the Campaign Manager browser report.',
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'prefix': 'ITP_Audit_Browser_',
              'default': 'ITP_Audit_Dashboard_Browser'
            }
          },
          'type': 'STANDARD',
          'delivery': {
            'emailOwner': False
          },
          'name': {
            'field': {
              'description': 'Name of the Campaign Manager browser report.',
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'prefix': 'ITP_Audit_Browser_',
              'default': 'ITP_Audit_Dashboard_Browser'
            }
          },
          'criteria': {
            'dimensions': [
              {
                'name': 'dfa:campaign',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:campaignId',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:site',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:advertiser',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:advertiserId',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:browserPlatform',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:platformType',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:month',
                'kind': 'dfareporting#sortedDimension'
              },
              {
                'name': 'dfa:week',
                'kind': 'dfareporting#sortedDimension'
              }
            ],
            'dimensionFilters': [
            ],
            'metricNames': [
              'dfa:impressions',
              'dfa:clicks',
              'dfa:totalConversions',
              'dfa:activityViewThroughConversions',
              'dfa:activityClickThroughConversions'
            ],
            'dateRange': {
              'relativeDateRange': 'LAST_365_DAYS',
              'kind': 'dfareporting#dateRange'
            }
          },
          'format': 'CSV',
          'kind': 'dfareporting#report',
          'schedule': {
            'repeatsOnWeekDays': [
              'Sunday'
            ],
            'repeats': 'WEEKLY',
            'active': True,
            'every': 1
          }
        },
        'filters': {
          'dfa:advertiser': {
            'values': {
              'field': {
                'description': 'Optional: Comma delimited list of CM advertiser ids.',
                'kind': 'integer_list',
                'name': 'cm_advertiser_ids',
                'order': 3,
                'default': ''
              }
            }
          }
        }
      }
    }
  },
  {
    'sheets': {
      'tab': 'Enviroment',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_Environment'
        },
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        }
      },
      'header': True,
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'ITP Audit ',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'range': 'A:B'
    }
  },
  {
    'sheets': {
      'tab': 'Browser',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_Browser'
        },
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        }
      },
      'header': True,
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'ITP Audit ',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'range': 'A:C'
    }
  },
  {
    'sheets': {
      'tab': 'CM_Browser_lookup',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_CM_Browser_lookup'
        },
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        }
      },
      'header': True,
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'ITP Audit ',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'range': 'A:C'
    }
  },
  {
    'sheets': {
      'tab': 'Device_Type',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_Device_Type'
        },
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        }
      },
      'header': True,
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'ITP Audit ',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'range': 'A:B'
    }
  },
  {
    'sheets': {
      'tab': 'Floodlight_Attribution',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_Floodlight_Attribution'
        },
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        }
      },
      'header': True,
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'ITP Audit ',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'range': 'A:B'
    }
  },
  {
    'dbm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery dataset for store dashboard tables.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 1,
              'default': 'ITP_Audit_Dashboard'
            }
          },
          'table': 'z_Dv360_Browser_Report_Dirty'
        }
      },
      'report': {
        'name': {
          'field': {
            'name': 'recipe_name',
            'order': 1,
            'prefix': 'ITP_Audit_Browser_',
            'description': 'Name of report in DV360, should be unique.',
            'kind': 'string'
          }
        }
      }
    }
  },
  {
    'itp_audit': {
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'ITP Audit ',
          'default': ''
        }
      },
      'account': {
        'field': {
          'description': 'Campaign Manager Account Id.',
          'kind': 'string',
          'name': 'cm_account_id',
          'order': 2,
          'default': ''
        }
      },
      'auth': 'service',
      'dataset': {
        'field': {
          'description': 'BigQuery dataset for store dashboard tables.',
          'kind': 'string',
          'name': 'recipe_slug',
          'order': 1,
          'default': 'ITP_Audit_Dashboard'
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
