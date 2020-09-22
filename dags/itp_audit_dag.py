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
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_slug': 'ITP_Audit_Dashboard',  # BigQuery dataset for store dashboard tables.
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_name': '',  # Name of document to deploy to.
  'cm_account_id': '',  # Campaign Manager Account Id.
  'cm_advertiser_ids': '',  # Optional: Comma delimited list of CM advertiser ids.
  'floodlight_configuration_id': '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
  'dv360_partner_ids': '',  # Comma delimited list of DV360 Partner ids.
  'dv360_advertiser_ids': '',  # Optional: Comma delimited list of DV360 Advertiser ids.
}

TASKS = [
  {
    'drive': {
      'hour': [
      ],
      'copy': {
        'destination': {
          'field': {
            'description': 'Name of document to deploy to.',
            'prefix': 'ITP Audit ',
            'order': 1,
            'kind': 'string',
            'name': 'recipe_name',
            'default': ''
          }
        },
        'source': 'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/'
      },
      'auth': 'user'
    }
  },
  {
    'dataset': {
      'dataset': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'recipe_slug',
          'description': 'BigQuery dataset for store dashboard tables.',
          'default': 'ITP_Audit_Dashboard'
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Credentials used for writing data.',
          'default': 'service'
        }
      }
    }
  },
  {
    'dbm': {
      'report': {
        'timeout': 90,
        'filters': {
          'FILTER_ADVERTISER': {
            'values': {
              'field': {
                'order': 6,
                'kind': 'integer_list',
                'name': 'dv360_advertiser_ids',
                'description': 'Optional: Comma delimited list of DV360 Advertiser ids.',
                'default': ''
              }
            }
          },
          'FILTER_PARTNER': {
            'values': {
              'field': {
                'order': 5,
                'kind': 'integer_list',
                'name': 'dv360_partner_ids',
                'description': 'Comma delimited list of DV360 Partner ids.',
                'default': ''
              }
            }
          }
        },
        'body': {
          'metadata': {
            'dataRange': 'LAST_365_DAYS',
            'title': {
              'field': {
                'order': 1,
                'kind': 'string',
                'name': 'recipe_name',
                'description': 'Name of report in DV360, should be unique.',
                'prefix': 'ITP_Audit_Browser_'
              }
            },
            'format': 'CSV'
          },
          'params': {
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
            'type': 'TYPE_GENERAL',
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
          },
          'timezoneCode': {
            'field': {
              'kind': 'timezone',
              'name': 'recipe_timezone',
              'description': 'Timezone for report dates.',
              'default': 'America/Los_Angeles'
            }
          }
        }
      },
      'delete': False,
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      }
    }
  },
  {
    'dcm': {
      'report': {
        'timeout': 90,
        'body': {
          'delivery': {
            'emailOwner': False
          },
          'floodlightCriteria': {
            'floodlightConfigId': {
              'matchType': 'EXACT',
              'kind': 'dfareporting#dimensionValue',
              'value': {
                'field': {
                  'order': 4,
                  'kind': 'integer',
                  'name': 'floodlight_configuration_id',
                  'description': 'Floodlight Configuration Id for the Campaign Manager floodlight report.',
                  'default': ''
                }
              },
              'dimensionName': 'dfa:floodlightConfigId'
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
            'dateRange': {
              'kind': 'dfareporting#dateRange',
              'relativeDateRange': 'LAST_30_DAYS'
            },
            'reportProperties': {
              'includeUnattributedCookieConversions': True,
              'includeUnattributedIPConversions': False
            },
            'metricNames': [
              'dfa:activityClickThroughConversions',
              'dfa:activityViewThroughConversions',
              'dfa:totalConversions',
              'dfa:totalConversionsRevenue'
            ]
          },
          'format': 'CSV',
          'kind': 'dfareporting#report',
          'schedule': {
            'every': 1,
            'repeatsOnWeekDays': [
              'Sunday'
            ],
            'repeats': 'WEEKLY',
            'active': True
          },
          'name': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_name',
              'description': 'Name of report in DV360, should be unique.',
              'prefix': 'ITP_Audit_Floodlight_'
            }
          },
          'type': 'FLOODLIGHT'
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'string',
            'name': 'cm_account_id',
            'description': 'Campaign Manager Account Id.',
            'default': ''
          }
        }
      },
      'delete': False,
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'table': 'z_Floodlight_CM_Report',
          'is_incremental_load': False,
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        }
      }
    }
  },
  {
    'dcm': {
      'report': {
        'timeout': 90,
        'filters': {
          'dfa:advertiser': {
            'values': {
              'field': {
                'order': 3,
                'kind': 'integer_list',
                'name': 'cm_advertiser_ids',
                'description': 'Optional: Comma delimited list of CM advertiser ids.',
                'default': ''
              }
            }
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'string',
            'name': 'cm_account_id',
            'description': 'Campaign Manager Account Id.',
            'default': ''
          }
        },
        'body': {
          'delivery': {
            'emailOwner': False
          },
          'name': {
            'field': {
              'description': 'Name of the Campaign Manager browser report.',
              'default': 'ITP_Audit_Dashboard_Browser',
              'order': 1,
              'kind': 'string',
              'name': 'recipe_name',
              'prefix': 'ITP_Audit_Browser_'
            }
          },
          'fileName': {
            'field': {
              'description': 'Name of the Campaign Manager browser report.',
              'default': 'ITP_Audit_Dashboard_Browser',
              'order': 1,
              'kind': 'string',
              'name': 'recipe_name',
              'prefix': 'ITP_Audit_Browser_'
            }
          },
          'format': 'CSV',
          'kind': 'dfareporting#report',
          'schedule': {
            'every': 1,
            'repeatsOnWeekDays': [
              'Sunday'
            ],
            'repeats': 'WEEKLY',
            'active': True
          },
          'type': 'STANDARD',
          'criteria': {
            'metricNames': [
              'dfa:impressions',
              'dfa:clicks',
              'dfa:totalConversions',
              'dfa:activityViewThroughConversions',
              'dfa:activityClickThroughConversions'
            ],
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
            'dimensionFilters': [
            ],
            'dateRange': {
              'kind': 'dfareporting#dateRange',
              'relativeDateRange': 'LAST_365_DAYS'
            }
          }
        }
      },
      'delete': False,
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'table': 'z_CM_Browser_Report_Dirty',
          'is_incremental_load': False,
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        }
      }
    }
  },
  {
    'sheets': {
      'tab': 'Enviroment',
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': 'A:B',
      'out': {
        'bigquery': {
          'table': 'z_Environment',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        },
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_write',
            'description': 'Credentials used for writing data.',
            'default': 'service'
          }
        }
      },
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'prefix': 'ITP Audit ',
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'default': ''
        }
      },
      'header': True
    }
  },
  {
    'sheets': {
      'tab': 'Browser',
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': 'A:C',
      'out': {
        'bigquery': {
          'table': 'z_Browser',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        },
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_write',
            'description': 'Credentials used for writing data.',
            'default': 'service'
          }
        }
      },
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'prefix': 'ITP Audit ',
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'default': ''
        }
      },
      'header': True
    }
  },
  {
    'sheets': {
      'tab': 'CM_Browser_lookup',
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': 'A:C',
      'out': {
        'bigquery': {
          'table': 'z_CM_Browser_lookup',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        },
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_write',
            'description': 'Credentials used for writing data.',
            'default': 'service'
          }
        }
      },
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'prefix': 'ITP Audit ',
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'default': ''
        }
      },
      'header': True
    }
  },
  {
    'sheets': {
      'tab': 'Device_Type',
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': 'A:B',
      'out': {
        'bigquery': {
          'table': 'z_Device_Type',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        },
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_write',
            'description': 'Credentials used for writing data.',
            'default': 'service'
          }
        }
      },
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'prefix': 'ITP Audit ',
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'default': ''
        }
      },
      'header': True
    }
  },
  {
    'sheets': {
      'tab': 'Floodlight_Attribution',
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': 'A:B',
      'out': {
        'bigquery': {
          'table': 'z_Floodlight_Attribution',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
          }
        },
        'auth': {
          'field': {
            'order': 1,
            'kind': 'authentication',
            'name': 'auth_write',
            'description': 'Credentials used for writing data.',
            'default': 'service'
          }
        }
      },
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'prefix': 'ITP Audit ',
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'default': ''
        }
      },
      'header': True
    }
  },
  {
    'dbm': {
      'report': {
        'name': {
          'field': {
            'order': 1,
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in DV360, should be unique.',
            'prefix': 'ITP_Audit_Browser_'
          }
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'table': 'z_Dv360_Browser_Report_Dirty',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'BigQuery dataset for store dashboard tables.',
              'default': 'ITP_Audit_Dashboard'
            }
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
          'prefix': 'ITP Audit ',
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'default': ''
        }
      },
      'timeout': 60,
      'account': {
        'field': {
          'order': 2,
          'kind': 'string',
          'name': 'cm_account_id',
          'description': 'Campaign Manager Account Id.',
          'default': ''
        }
      },
      'dataset': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'recipe_slug',
          'description': 'BigQuery dataset for store dashboard tables.',
          'default': 'ITP_Audit_Dashboard'
        }
      },
      'auth': 'service'
    }
  }
]

DAG_FACTORY = DAG_Factory('itp_audit', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
