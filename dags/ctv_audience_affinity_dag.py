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

cTV Inventory Availability Dashboard

The cTV Audience Affinity dashboard is designed to give clients insights into which cTV apps their audiences have a high affinity for using.  The goal of this dashboard is to provide some assistance with the lack of audience targeting for cTV within DV360.

Find instructions and recommendations for this dashboard <a href="https://docs.google.com/document/d/120kcR9OrS4hGdTxRK0Ig2koNmm6Gl7sH0L6U56N0SAM/view?usp=sharing" target="_blank">here</a>

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_project': '',  # Project where BigQuery dataset will be created.
  'dataset': '',  # BigQuery Dataset where all data will live.
  'partner_id': '',  # DV360 Partner id.
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_name': '',  # Name of document to deploy to.
  'audience_ids': '',  # Comma separated list of Audience Ids
}

TASKS = [
  {
    'drive': {
      'copy': {
        'destination': {
          'field': {
            'description': 'Name of document to deploy to.',
            'prefix': 'cTV App Match Table ',
            'order': 1,
            'kind': 'string',
            'name': 'recipe_name',
            'default': ''
          }
        },
        'source': 'https://docs.google.com/spreadsheets/d/1PPPk2b4gGJHNgQ4hXLiTKzH8pRIdlF5fNy9VCw1v7tM/'
      },
      'auth': 'user'
    }
  },
  {
    'dataset': {
      'dataset': {
        'field': {
          'order': 3,
          'kind': 'string',
          'name': 'dataset',
          'description': 'BigQuery Dataset where all data will live.',
          'default': ''
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
        'body': {
          'kind': 'doubleclickbidmanager#query',
          'metadata': {
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'us_country_app_'
              }
            },
            'sendNotification': False
          },
          'params': {
            'groupBys': [
              'FILTER_APP_URL'
            ],
            'includeInviteData': True,
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'kind': 'integer',
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.'
                  }
                }
              },
              {
                'type': 'FILTER_INVENTORY_FORMAT',
                'value': 'VIDEO'
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ]
          },
          'timezoneCode': 'America/Los_Angeles',
          'schedule': {
            'nextRunTimezoneCode': 'America/Los_Angeles',
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0
          }
        }
      },
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'app_url',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'impressions',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'uniques',
              'type': 'STRING',
              'mode': 'NULLABLE'
            }
          ],
          'table': 'us_country_app',
          'dataset': {
            'field': {
              'order': 3,
              'kind': 'string',
              'name': 'dataset',
              'description': 'BigQuery Dataset where all data will live.',
              'default': ''
            }
          }
        }
      }
    }
  },
  {
    'dbm': {
      'report': {
        'body': {
          'kind': 'doubleclickbidmanager#query',
          'metadata': {
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'us_country_baseline_'
              }
            },
            'sendNotification': False
          },
          'params': {
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ],
            'includeInviteData': True,
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'kind': 'integer',
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.'
                  }
                }
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY'
          },
          'timezoneCode': 'America/Los_Angeles',
          'schedule': {
            'nextRunTimezoneCode': 'America/Los_Angeles',
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0
          }
        }
      },
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'impressions',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'uniques',
              'type': 'STRING',
              'mode': 'NULLABLE'
            }
          ],
          'table': 'us_country_baseline',
          'dataset': {
            'field': {
              'order': 3,
              'kind': 'string',
              'name': 'dataset',
              'description': 'BigQuery Dataset where all data will live.',
              'default': ''
            }
          }
        }
      }
    }
  },
  {
    'dbm': {
      'report': {
        'filters': {
          'FILTER_USER_LIST': {
            'values': {
              'field': {
                'order': 2,
                'kind': 'integer_list',
                'name': 'audience_ids',
                'description': 'Comma separated list of Audience Ids'
              }
            },
            'single_cell': True
          }
        },
        'body': {
          'kind': 'doubleclickbidmanager#query',
          'metadata': {
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'us_audience_baseline_'
              }
            },
            'sendNotification': False
          },
          'params': {
            'groupBys': [
              'FILTER_AUDIENCE_LIST'
            ],
            'includeInviteData': True,
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'kind': 'integer',
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.'
                  }
                }
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ]
          },
          'timezoneCode': 'America/Los_Angeles',
          'schedule': {
            'nextRunTimezoneCode': 'America/Los_Angeles',
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0
          }
        }
      },
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'user_list',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'impressions',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'uniques',
              'type': 'STRING',
              'mode': 'NULLABLE'
            }
          ],
          'table': 'us_audience_baseline',
          'dataset': {
            'field': {
              'order': 3,
              'kind': 'string',
              'name': 'dataset',
              'description': 'BigQuery Dataset where all data will live.',
              'default': ''
            }
          }
        }
      }
    }
  },
  {
    'dbm': {
      'report': {
        'filters': {
          'FILTER_USER_LIST': {
            'values': {
              'field': {
                'order': 2,
                'kind': 'integer_list',
                'name': 'audience_ids',
                'description': 'Comma separated list of Audience Ids'
              }
            },
            'single_cell': True
          }
        },
        'body': {
          'kind': 'doubleclickbidmanager#query',
          'metadata': {
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'prefix': 'us_audience_app_'
              }
            },
            'sendNotification': False
          },
          'params': {
            'groupBys': [
              'FILTER_APP_URL',
              'FILTER_AUDIENCE_LIST'
            ],
            'includeInviteData': True,
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'kind': 'integer',
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.'
                  }
                }
              },
              {
                'type': 'FILTER_INVENTORY_FORMAT',
                'value': 'VIDEO'
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ]
          },
          'timezoneCode': 'America/Los_Angeles',
          'schedule': {
            'nextRunTimezoneCode': 'America/Los_Angeles',
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0
          }
        }
      },
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'app_url',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'user_list',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'impressions',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'uniques',
              'type': 'STRING',
              'mode': 'NULLABLE'
            }
          ],
          'table': 'us_audience_app',
          'dataset': {
            'field': {
              'order': 3,
              'kind': 'string',
              'name': 'dataset',
              'description': 'BigQuery Dataset where all data will live.',
              'default': ''
            }
          }
        }
      }
    }
  },
  {
    'sheets': {
      'tab': 'data',
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'range': 'A:Z',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'Publisher_Name',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'CTV_App_name',
              'type': 'STRING',
              'mode': 'NULLABLE'
            }
          ],
          'table': 'CTV_App_Lookup',
          'dataset': {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'BigQuery Dataset where all data will live.'
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
          'prefix': 'cTV App Match Table ',
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
    'bigquery': {
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Credentials used for writing data.',
          'default': 'service'
        }
      },
      'description': 'The query to join all the IAR reports into an Affinity Index.',
      'from': {
        'query': "SELECT    audience_app.app_url,    audience_app.ctv_app_name,  IF    (audience_app.app_url LIKE '%Android%'      OR audience_app.app_url LIKE '%iOS',      'App',      'Domain') AS app_or_domain,    audience_app.user_list AS audience_list,    audience_app.Potential_Impressions AS audience_app_impressions,    audience_app.Unique_Cookies_With_Impressions AS audience_app_uniques,    audience_baseline.Potential_Impressions AS audience_baseline_impressions,    audience_baseline.Unique_Cookies_With_Impressions AS audience_baseline_uniques,    country_app.Potential_Impressions AS country_app_impressions,    country_app.Unique_Cookies_With_Impressions AS country_app_uniques,    country_baseline.Potential_Impressions AS country_baseline_impressions,    country_baseline.Unique_Cookies_With_Impressions AS country_baseline_uniques,    ((audience_app.Unique_Cookies_With_Impressions/NULLIF(audience_baseline.Unique_Cookies_With_Impressions,          0))/NULLIF((country_app.Unique_Cookies_With_Impressions/NULLIF(CAST(country_baseline.Unique_Cookies_With_Impressions AS int64),            0)),        0))*100 AS affinity_index  FROM (    SELECT      user_list,      CAST(      IF        (impressions LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS potential_impressions,      CAST(      IF        (uniques LIKE '%< 100%',          0,          CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions    FROM      `[PARAMETER].[PARAMETER].us_audience_baseline` ) AS audience_baseline  JOIN (    SELECT      ctv_app.CTV_App_name AS ctv_app_name,      user_list,      app_url,      CAST(      IF        (impressions LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS potential_impressions,      CAST(      IF        (uniques LIKE '%< 1000%',          0,          CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions    FROM      `[PARAMETER].[PARAMETER].us_audience_app` AS a    LEFT JOIN      `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app    ON      a.app_url = ctv_app.Publisher_Name ) AS audience_app  ON    audience_baseline.user_list = audience_app.user_list  LEFT JOIN (    SELECT      app_url,      CAST(      IF        (CAST(impressions AS STRING) LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS Potential_Impressions,      CAST(      IF        (CAST(uniques AS STRING) LIKE '%< 1000%',          0,          CAST(uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions    FROM      `[PARAMETER].[PARAMETER].us_country_app` ) AS country_app  ON    country_app.app_url = audience_app.app_url  CROSS JOIN (    SELECT      CAST(      IF        (CAST(impressions AS STRING) LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS Potential_Impressions,      CAST(      IF        (CAST(uniques AS STRING) LIKE '%< 1000%',          0,          CAST(uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions    FROM      `[PARAMETER].[PARAMETER].us_country_baseline` ) AS country_baseline",
        'legacy': False,
        'parameters': [
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'dataset',
              'description': 'Place where tables will be written in BigQuery.'
            }
          }
        ]
      },
      'to': {
        'table': 'final_table',
        'dataset': {
          'field': {
            'kind': 'string',
            'name': 'dataset',
            'description': 'BigQuery Dataset where all data will live.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('ctv_audience_affinity', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
