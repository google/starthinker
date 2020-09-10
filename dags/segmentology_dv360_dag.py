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
  'recipe_project': '',  # Project ID hosting dataset.
  'auth_read': 'user',  # Credentials used for reading data.
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
      'description': 'Create a dataset for bigquery tables.',
      'auth': {
        'field': {
          'description': 'Credentials used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'hour': [
        4
      ],
      'dataset': {
        'field': {
          'description': 'Place where tables will be created in BigQuery.',
          'name': 'recipe_slug',
          'kind': 'string'
        }
      }
    }
  },
  {
    'bigquery': {
      'to': {
        'dataset': {
          'field': {
            'description': 'Name of Google BigQuery dataset to create.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 4,
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for writing function.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'function': 'pearson_significance_test'
    }
  },
  {
    'dbm': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 0,
          'default': 'user'
        }
      },
      'report': {
        'filters': {
          'FILTER_ADVERTISER': {
            'values': {
              'field': {
                'description': 'Comma delimited list of DV360 advertiser ids.',
                'kind': 'integer_list',
                'name': 'advertisers',
                'order': 6,
                'default': [
                ]
              }
            }
          },
          'FILTER_PARTNER': {
            'values': {
              'field': {
                'description': 'DV360 partner id.',
                'kind': 'integer_list',
                'name': 'partners',
                'order': 5,
                'default': [
                ]
              }
            }
          }
        },
        'body': {
          'metadata': {
            'title': {
              'field': {
                'description': 'Name of report, not needed if ID used.',
                'name': 'recipe_name',
                'kind': 'string',
                'order': 3,
                'prefix': 'Segmentology ',
                'default': ''
              }
            },
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV'
          },
          'timezoneCode': {
            'field': {
              'description': 'Timezone for report dates.',
              'name': 'recipe_timezone',
              'default': 'America/Los_Angeles',
              'kind': 'timezone'
            }
          },
          'schedule': {
            'frequency': 'WEEKLY'
          },
          'params': {
            'type': 'TYPE_CROSS_PARTNER',
            'groupBys': [
              'FILTER_PARTNER',
              'FILTER_PARTNER_NAME',
              'FILTER_ADVERTISER',
              'FILTER_ADVERTISER_NAME',
              'FILTER_MEDIA_PLAN',
              'FILTER_MEDIA_PLAN_NAME',
              'FILTER_ZIP_POSTAL_CODE'
            ],
            'metrics': [
              'METRIC_BILLABLE_IMPRESSIONS',
              'METRIC_CLICKS',
              'METRIC_TOTAL_CONVERSIONS'
            ]
          }
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
          'order': 0,
          'default': 'user'
        }
      },
      'out': {
        'bigquery': {
          'auth': {
            'field': {
              'description': 'Authorization used for writing data.',
              'kind': 'authentication',
              'name': 'auth_write',
              'order': 1,
              'default': 'service'
            }
          },
          'dataset': {
            'field': {
              'description': 'Name of Google BigQuery dataset to create.',
              'kind': 'string',
              'name': 'recipe_slug',
              'order': 4,
              'default': ''
            }
          },
          'table': 'DV360_KPI',
          'schema': [
            {
              'type': 'INTEGER',
              'name': 'Partner_Id',
              'mode': 'REQUIRED'
            },
            {
              'type': 'STRING',
              'name': 'Partner',
              'mode': 'REQUIRED'
            },
            {
              'type': 'INTEGER',
              'name': 'Advertiser_Id',
              'mode': 'REQUIRED'
            },
            {
              'type': 'STRING',
              'name': 'Advertiser',
              'mode': 'REQUIRED'
            },
            {
              'type': 'INTEGER',
              'name': 'Campaign_Id',
              'mode': 'REQUIRED'
            },
            {
              'type': 'STRING',
              'name': 'Campaign',
              'mode': 'REQUIRED'
            },
            {
              'type': 'STRING',
              'name': 'Zip',
              'mode': 'NULLABLE'
            },
            {
              'type': 'FLOAT',
              'name': 'Impressions',
              'mode': 'NULLABLE'
            },
            {
              'type': 'INTEGER',
              'name': 'Clicks',
              'mode': 'NULLABLE'
            },
            {
              'type': 'FLOAT',
              'name': 'Conversions',
              'mode': 'NULLABLE'
            }
          ]
        }
      },
      'report': {
        'name': {
          'field': {
            'description': 'Name of report, not needed if ID used.',
            'name': 'recipe_name',
            'kind': 'string',
            'order': 3,
            'prefix': 'Segmentology ',
            'default': ''
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'from': {
        'legacy': False,
        'parameters': {
          'project': {
            'field': {
              'description': 'Project ID hosting dataset.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          'dataset': {
            'field': {
              'description': 'Place where tables will be created in BigQuery.',
              'name': 'recipe_slug',
              'kind': 'string'
            }
          }
        },
        'query': 'SELECT            Partner_Id,            Partner,            Advertiser_Id,            Advertiser,            Campaign_Id,            Campaign,            Zip,            SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY Advertiser_Id)) AS Impression_Percent,            SAFE_DIVIDE(Clicks, Impressions) AS Click_Percent,            SAFE_DIVIDE(Conversions, Impressions) AS Conversion_Percent,            Impressions AS Impressions          FROM            `{project}.{dataset}.DV360_KPI`;        '
      },
      'to': {
        'view': 'DV360_KPI_Normalized',
        'dataset': {
          'field': {
            'description': 'Place where tables will be written in BigQuery.',
            'name': 'recipe_slug',
            'kind': 'string'
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Authorization used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      }
    }
  },
  {
    'census': {
      'to': {
        'type': 'view',
        'dataset': {
          'field': {
            'description': 'Name of Google BigQuery dataset to create.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 4,
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Authorization used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'normalize': {
        'census_span': '5yr',
        'census_year': '2018',
        'census_geography': 'zip_codes'
      }
    }
  },
  {
    'census': {
      'to': {
        'type': 'view',
        'dataset': {
          'field': {
            'description': 'Name of Google BigQuery dataset to create.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 4,
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Authorization used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      },
      'correlate': {
        'sum': [
          'Impressions'
        ],
        'join': 'Zip',
        'correlate': [
          'Impression_Percent',
          'Click_Percent',
          'Conversion_Percent'
        ],
        'pass': [
          'Partner_Id',
          'Partner',
          'Advertiser_Id',
          'Advertiser',
          'Campaign_Id',
          'Campaign'
        ],
        'dataset': {
          'field': {
            'description': 'Name of Google BigQuery dataset to create.',
            'kind': 'string',
            'name': 'recipe_slug',
            'order': 4,
            'default': ''
          }
        },
        'table': 'DV360_KPI_Normalized',
        'significance': 80
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('segmentology_dv360', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
