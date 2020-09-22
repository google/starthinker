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

Segmentology DV360

DV360 funnel analysis using Census data.

Wait for <b>BigQuery->UNDEFINED->UNDEFINED->Census_Pivot</b> to be created.
Join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
Copy <a href='https://datastudio.google.com/c/u/0/reporting/4a908845-fdba-4023-9bb7-68666202bafb/page/K15YB/' target='_blank'>DV360 Segmentology</a>. Leave the Data Source as is, you will change it in the next step.
Click Edit Connection, and change to <b>BigQuery->UNDEFINED->(field:recipe_slug}->Census_Pivot</b>.
Or give these intructions to the client.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_project': '',  # Project ID hosting dataset.
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'auth_write': 'service',  # Authorization used for writing data.
  'recipe_name': '',  # Name of report, not needed if ID used.
  'recipe_slug': '',  # Name of Google BigQuery dataset to create.
  'partners': [],  # DV360 partner id.
  'advertisers': [],  # Comma delimited list of DV360 advertiser ids.
}

TASKS = [
  {
    'dataset': {
      'hour': [
        4
      ],
      'description': 'Create a dataset for bigquery tables.',
      'dataset': {
        'field': {
          'kind': 'string',
          'name': 'recipe_slug',
          'description': 'Place where tables will be created in BigQuery.'
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
    'bigquery': {
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Credentials used for writing function.',
          'default': 'service'
        }
      },
      'function': 'pearson_significance_test',
      'to': {
        'dataset': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Name of Google BigQuery dataset to create.',
            'default': ''
          }
        }
      }
    }
  },
  {
    'dbm': {
      'report': {
        'filters': {
          'FILTER_PARTNER': {
            'values': {
              'field': {
                'order': 5,
                'kind': 'integer_list',
                'name': 'partners',
                'description': 'DV360 partner id.',
                'default': [
                ]
              }
            }
          },
          'FILTER_ADVERTISER': {
            'values': {
              'field': {
                'order': 6,
                'kind': 'integer_list',
                'name': 'advertisers',
                'description': 'Comma delimited list of DV360 advertiser ids.',
                'default': [
                ]
              }
            }
          }
        },
        'body': {
          'metadata': {
            'dataRange': 'LAST_30_DAYS',
            'title': {
              'field': {
                'description': 'Name of report, not needed if ID used.',
                'default': '',
                'order': 3,
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'Segmentology '
              }
            },
            'format': 'CSV'
          },
          'params': {
            'groupBys': [
              'FILTER_PARTNER',
              'FILTER_PARTNER_NAME',
              'FILTER_ADVERTISER',
              'FILTER_ADVERTISER_NAME',
              'FILTER_MEDIA_PLAN',
              'FILTER_MEDIA_PLAN_NAME',
              'FILTER_ZIP_POSTAL_CODE'
            ],
            'type': 'TYPE_CROSS_PARTNER',
            'metrics': [
              'METRIC_BILLABLE_IMPRESSIONS',
              'METRIC_CLICKS',
              'METRIC_TOTAL_CONVERSIONS'
            ]
          },
          'timezoneCode': {
            'field': {
              'kind': 'timezone',
              'name': 'recipe_timezone',
              'description': 'Timezone for report dates.',
              'default': 'America/Los_Angeles'
            }
          },
          'schedule': {
            'frequency': 'WEEKLY'
          }
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      }
    }
  },
  {
    'dbm': {
      'report': {
        'name': {
          'field': {
            'description': 'Name of report, not needed if ID used.',
            'default': '',
            'order': 3,
            'kind': 'string',
            'name': 'recipe_name',
            'prefix': 'Segmentology '
          }
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'Partner_Id',
              'type': 'INTEGER',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Partner',
              'type': 'STRING',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Advertiser_Id',
              'type': 'INTEGER',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Advertiser',
              'type': 'STRING',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Campaign_Id',
              'type': 'INTEGER',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Campaign',
              'type': 'STRING',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Zip',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Impressions',
              'type': 'FLOAT',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Clicks',
              'type': 'INTEGER',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Conversions',
              'type': 'FLOAT',
              'mode': 'NULLABLE'
            }
          ],
          'table': 'DV360_KPI',
          'dataset': {
            'field': {
              'order': 4,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Name of Google BigQuery dataset to create.',
              'default': ''
            }
          },
          'auth': {
            'field': {
              'order': 1,
              'kind': 'authentication',
              'name': 'auth_write',
              'description': 'Authorization used for writing data.',
              'default': 'service'
            }
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Authorization used for writing data.',
          'default': 'service'
        }
      },
      'from': {
        'query': 'SELECT            Partner_Id,            Partner,            Advertiser_Id,            Advertiser,            Campaign_Id,            Campaign,            Zip,            SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY Advertiser_Id)) AS Impression_Percent,            SAFE_DIVIDE(Clicks, Impressions) AS Click_Percent,            SAFE_DIVIDE(Conversions, Impressions) AS Conversion_Percent,            Impressions AS Impressions          FROM            `{project}.{dataset}.DV360_KPI`;        ',
        'parameters': {
          'project': {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project ID hosting dataset.'
            }
          },
          'dataset': {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          }
        },
        'legacy': False
      },
      'to': {
        'view': 'DV360_KPI_Normalized',
        'dataset': {
          'field': {
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Place where tables will be written in BigQuery.'
          }
        }
      }
    }
  },
  {
    'census': {
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Authorization used for writing data.',
          'default': 'service'
        }
      },
      'normalize': {
        'census_geography': 'zip_codes',
        'census_span': '5yr',
        'census_year': '2018'
      },
      'to': {
        'dataset': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Name of Google BigQuery dataset to create.',
            'default': ''
          }
        },
        'type': 'view'
      }
    }
  },
  {
    'census': {
      'correlate': {
        'correlate': [
          'Impression_Percent',
          'Click_Percent',
          'Conversion_Percent'
        ],
        'join': 'Zip',
        'significance': 80,
        'dataset': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Name of Google BigQuery dataset to create.',
            'default': ''
          }
        },
        'pass': [
          'Partner_Id',
          'Partner',
          'Advertiser_Id',
          'Advertiser',
          'Campaign_Id',
          'Campaign'
        ],
        'sum': [
          'Impressions'
        ],
        'table': 'DV360_KPI_Normalized'
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Authorization used for writing data.',
          'default': 'service'
        }
      },
      'to': {
        'dataset': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Name of Google BigQuery dataset to create.',
            'default': ''
          }
        },
        'type': 'view'
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('segmentology_dv360', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
