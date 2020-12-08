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

Segmentology DV360

DV360 funnel analysis using Census data.

  - Wait for <b>BigQuery->UNDEFINED->UNDEFINED->Census_Join</b> to be created.
  - Join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/reporting/4a908845-fdba-4023-9bb7-68666202bafb/page/K15YB/' target='_blank'>DV360 Segmentology</a>. Leave the Data Source as is, you will change it in the next step.
  - Click Edit Connection, and change to <b>BigQuery->UNDEFINED->(field:recipe_slug}->Census_Join</b>.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'recipe_project': '',  # Project ID hosting dataset.
  'auth_write': 'service',  # Authorization used for writing data.
  'recipe_name': '',  # Name of report, not needed if ID used.
  'recipe_slug': '',  # Name of Google BigQuery dataset to create.
  'partners': [],  # DV360 partner id.
  'advertisers': [],  # Comma delimited list of DV360 advertiser ids.
}

RECIPE = {
  'tasks': [
    {
      'dataset': {
        'description': 'Create a dataset for bigquery tables.',
        'hour': [
          4
        ],
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
            'description': 'Place where tables will be created in BigQuery.'
          }
        }
      }
    },
    {
      'bigquery': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Credentials used for writing function.'
          }
        },
        'function': 'pearson_significance_test',
        'to': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Name of Google BigQuery dataset to create.'
            }
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
            'order': 0,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'report': {
          'filters': {
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'name': 'partners',
                  'kind': 'integer_list',
                  'order': 5,
                  'default': [
                  ],
                  'description': 'DV360 partner id.'
                }
              }
            },
            'FILTER_ADVERTISER': {
              'values': {
                'field': {
                  'name': 'advertisers',
                  'kind': 'integer_list',
                  'order': 6,
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.'
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
                  'order': 3,
                  'prefix': 'Segmentology ',
                  'default': '',
                  'description': 'Name of report, not needed if ID used.'
                }
              },
              'dataRange': 'LAST_30_DAYS',
              'format': 'CSV'
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
            },
            'schedule': {
              'frequency': 'WEEKLY'
            }
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
            'order': 0,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'report': {
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 3,
              'prefix': 'Segmentology ',
              'default': '',
              'description': 'Name of report, not needed if ID used.'
            }
          }
        },
        'out': {
          'bigquery': {
            'auth': {
              'field': {
                'name': 'auth_write',
                'kind': 'authentication',
                'order': 1,
                'default': 'service',
                'description': 'Authorization used for writing data.'
              }
            },
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 4,
                'default': '',
                'description': 'Name of Google BigQuery dataset to create.'
              }
            },
            'table': 'DV360_KPI',
            'header': True,
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
            ]
          }
        }
      }
    },
    {
      'bigquery': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Authorization used for writing data.'
          }
        },
        'from': {
          'query': 'SELECT            Partner_Id,            Partner,            Advertiser_Id,            Advertiser,            Campaign_Id,            Campaign,            Zip,            SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY Advertiser_Id)) AS Impression_Percent,            SAFE_DIVIDE(Clicks, Impressions) AS Click_Percent,            SAFE_DIVIDE(Conversions, Impressions) AS Conversion_Percent,            Impressions AS Impressions          FROM            `{project}.{dataset}.DV360_KPI`;        ',
          'parameters': {
            'project': {
              'field': {
                'name': 'recipe_project',
                'kind': 'string',
                'description': 'Project ID hosting dataset.'
              }
            },
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            }
          },
          'legacy': False
        },
        'to': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          'view': 'DV360_KPI_Normalized'
        }
      }
    },
    {
      'census': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Authorization used for writing data.'
          }
        },
        'normalize': {
          'census_geography': 'zip_codes',
          'census_year': '2018',
          'census_span': '5yr'
        },
        'to': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Name of Google BigQuery dataset to create.'
            }
          },
          'type': 'view'
        }
      }
    },
    {
      'census': {
        'auth': {
          'field': {
            'name': 'auth_write',
            'kind': 'authentication',
            'order': 1,
            'default': 'service',
            'description': 'Authorization used for writing data.'
          }
        },
        'correlate': {
          'join': 'Zip',
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
          'correlate': [
            'Impression_Percent',
            'Click_Percent',
            'Conversion_Percent'
          ],
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Name of Google BigQuery dataset to create.'
            }
          },
          'table': 'DV360_KPI_Normalized',
          'significance': 80
        },
        'to': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Name of Google BigQuery dataset to create.'
            }
          },
          'type': 'view'
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('segmentology_dv360', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
