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

DV360 Audience Analysis

The Audience Wizard Dashboard helps you to track the audience performance across all audiences on Display.

Wait for <b>BigQuery->UNDEFINED->UNDEFINED->DV360_Audience_Analysis</b> to be created.
Join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
Copy <a href='https://datastudio.google.com/open/1d2vlf4C1roN95NsdsvWNZqKFcYN8N9Jg' target='_blank'>Sample DV360 Audience Analysis Dataset</a>.
Click Edit Connection, and change to <b>BigQuery->UNDEFINED->UNDEFINED->DV360_Audience_Analysis</b>.
Copy <a href='https://datastudio.google.com/open/1Ij_RluqolElm7Nny9fBrIAPRB9ObUl0M' target='_blank'>Sample DV360 Audience Analysis Report</a>.
When prompted choose the new data source you just created.
Or give these intructions to the client.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_slug': '',  # Place where tables will be created in BigQuery.
  'recipe_name': '',  # Name of report in DV360, should be unique.
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'partners': [],  # DV360 partner id.
  'recipe_project': '',  # Google Cloud Project Id.
  'advertisers': [],  # Comma delimited list of DV360 advertiser ids.
}

TASKS = [
  {
    'dataset': {
      'hour': [
        1
      ],
      'description': 'Create a dataset for bigquery tables.',
      'dataset': {
        'field': {
          'kind': 'string',
          'name': 'recipe_slug',
          'description': 'Place where tables will be created in BigQuery.'
        }
      },
      'auth': 'service'
    }
  },
  {
    'dbm': {
      'hour': [
        2
      ],
      'auth': 'user',
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
            'dataRange': 'LAST_7_DAYS',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'description': 'Name of report in DV360, should be unique.',
                'prefix': 'Audience Analysis Performance '
              }
            },
            'format': 'CSV'
          },
          'params': {
            'groupBys': [
              'FILTER_ADVERTISER_NAME',
              'FILTER_ADVERTISER',
              'FILTER_AUDIENCE_LIST',
              'FILTER_USER_LIST',
              'FILTER_AUDIENCE_LIST_TYPE',
              'FILTER_AUDIENCE_LIST_COST',
              'FILTER_PARTNER_CURRENCY'
            ],
            'type': 'TYPE_GENERAL',
            'metrics': [
              'METRIC_IMPRESSIONS',
              'METRIC_CLICKS',
              'METRIC_TOTAL_CONVERSIONS',
              'METRIC_LAST_CLICKS',
              'METRIC_LAST_IMPRESSIONS',
              'METRIC_TOTAL_MEDIA_COST_PARTNER'
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
      }
    }
  },
  {
    'dbm': {
      'hour': [
        6
      ],
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'advertiser',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'advertiser_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list_type',
              'mode': 'NULLABLE',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_cost_usd',
              'mode': 'NULLABLE',
              'type': 'STRING'
            },
            {
              'name': 'partner_currency',
              'mode': 'NULLABLE',
              'type': 'STRING'
            },
            {
              'name': 'impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            },
            {
              'name': 'clicks',
              'mode': 'NULLABLE',
              'type': 'INT64'
            },
            {
              'name': 'total_conversions',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            },
            {
              'name': 'post_click_conversions',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            },
            {
              'name': 'post_view_conversions',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            },
            {
              'name': 'total_media_cost_partner_currency',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            }
          ],
          'table': 'DV360_Audience_Performance',
          'dataset': {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          }
        }
      },
      'report': {
        'name': {
          'field': {
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in DV360, should be unique.',
            'prefix': 'Audience Analysis Performance '
          }
        }
      }
    }
  },
  {
    'dbm': {
      'hour': [
        2
      ],
      'auth': 'user',
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
            'dataRange': 'LAST_7_DAYS',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'description': 'Name of report in DV360, should be unique.',
                'prefix': 'Audience Analysis First Party'
              }
            },
            'format': 'CSV'
          },
          'params': {
            'groupBys': [
              'FILTER_ADVERTISER_NAME',
              'FILTER_ADVERTISER',
              'FILTER_USER_LIST_FIRST_PARTY_NAME',
              'FILTER_USER_LIST_FIRST_PARTY',
              'FILTER_FIRST_PARTY_AUDIENCE_LIST_TYPE',
              'FILTER_FIRST_PARTY_AUDIENCE_LIST_COST'
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
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
      }
    }
  },
  {
    'dbm': {
      'hour': [
        6
      ],
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'advertiser',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'advertiser_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list_type',
              'mode': 'NULLABLE',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_cost_usd',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            },
            {
              'name': 'potential_impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            },
            {
              'name': 'unique_cookies_with_impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            }
          ],
          'table': 'DV360_First_Party_Audience',
          'dataset': {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          }
        }
      },
      'report': {
        'name': {
          'field': {
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in DV360, should be unique.',
            'prefix': 'Audience Analysis First Party'
          }
        }
      }
    }
  },
  {
    'dbm': {
      'hour': [
        2
      ],
      'auth': 'user',
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
            'dataRange': 'LAST_7_DAYS',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'description': 'Name of report in DV360, should be unique.',
                'prefix': 'Audience Analysis Google'
              }
            },
            'format': 'CSV'
          },
          'params': {
            'groupBys': [
              'FILTER_ADVERTISER_NAME',
              'FILTER_ADVERTISER',
              'FILTER_AUDIENCE_LIST',
              'FILTER_USER_LIST',
              'FILTER_AUDIENCE_LIST_TYPE',
              'FILTER_AUDIENCE_LIST_COST'
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
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
      }
    }
  },
  {
    'dbm': {
      'hour': [
        6
      ],
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'advertiser',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'advertiser_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list_type',
              'mode': 'NULLABLE',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_cost_usd',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            },
            {
              'name': 'potential_impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            },
            {
              'name': 'unique_cookies_with_impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            }
          ],
          'table': 'DV360_Google_Audience',
          'dataset': {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          }
        }
      },
      'report': {
        'name': {
          'field': {
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in DV360, should be unique.',
            'prefix': 'Audience Analysis Google'
          }
        }
      }
    }
  },
  {
    'dbm': {
      'hour': [
        2
      ],
      'auth': 'user',
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
            'dataRange': 'LAST_7_DAYS',
            'title': {
              'field': {
                'kind': 'string',
                'name': 'recipe_name',
                'description': 'Name of report in DV360, should be unique.',
                'prefix': 'Audience Analysis Third Party'
              }
            },
            'format': 'CSV'
          },
          'params': {
            'groupBys': [
              'FILTER_ADVERTISER_NAME',
              'FILTER_ADVERTISER',
              'FILTER_USER_LIST_THIRD_PARTY_NAME',
              'FILTER_USER_LIST_THIRD_PARTY',
              'FILTER_THIRD_PARTY_AUDIENCE_LIST_TYPE',
              'FILTER_THIRD_PARTY_AUDIENCE_LIST_COST'
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
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
      }
    }
  },
  {
    'dbm': {
      'hour': [
        6
      ],
      'auth': 'user',
      'out': {
        'bigquery': {
          'schema': [
            {
              'name': 'advertiser',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'advertiser_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list',
              'mode': 'REQUIRED',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_id',
              'mode': 'REQUIRED',
              'type': 'INT64'
            },
            {
              'name': 'audience_list_type',
              'mode': 'NULLABLE',
              'type': 'STRING'
            },
            {
              'name': 'audience_list_cost_usd',
              'mode': 'NULLABLE',
              'type': 'FLOAT'
            },
            {
              'name': 'potential_impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            },
            {
              'name': 'unique_cookies_with_impressions',
              'mode': 'NULLABLE',
              'type': 'INT64'
            }
          ],
          'table': 'DV360_Third_Party_Audience',
          'dataset': {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          }
        }
      },
      'report': {
        'name': {
          'field': {
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in DV360, should be unique.',
            'prefix': 'Audience Analysis Third Party'
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'hour': [
        6
      ],
      'auth': 'service',
      'from': {
        'query': " SELECT   p.advertiser_id,   p.advertiser,   p.audience_list_id,   IF (p.audience_list_type = 'Bid Manager Audiences', 'Google', p.audience_list_type) AS audience_list_type,   CASE     WHEN REGEXP_CONTAINS(p.audience_list, 'Affinity') THEN 'Affinity'     WHEN REGEXP_CONTAINS(p.audience_list, 'Demographics') THEN 'Demographics'     WHEN REGEXP_CONTAINS(p.audience_list, 'In-Market') THEN 'In-Market'     WHEN REGEXP_CONTAINS(p.audience_list, 'Similar') THEN 'Similar'     ELSE 'Custom'   END AS audience_list_category,   p.audience_list,   IF(p.audience_list_cost_usd = 'Unknown', 0.0, CAST(p.audience_list_cost_usd AS FLOAT64)) AS audience_list_cost,   p.total_media_cost_partner_currency AS total_media_cost,   p.impressions,   p.clicks,   p.total_conversions,   COALESCE(ggl.potential_impressions, fst.potential_impressions, trd.potential_impressions) AS potential_impressions,   COALESCE(ggl.unique_cookies_with_impressions, fst.unique_cookies_with_impressions, trd.unique_cookies_with_impressions) AS potential_reach FROM   `[PARAMETER].[PARAMETER].DV360_Audience_Performance` p LEFT JOIN   `[PARAMETER].[PARAMETER].DV360_Google_Audience` ggl   USING (advertiser_id, audience_list_id) LEFT JOIN   `[PARAMETER].[PARAMETER].DV360_First_Party_Audience` fst   USING (advertiser_id, audience_list_id) LEFT JOIN   `[PARAMETER].[PARAMETER].DV360_Third_Party_Audience` trd   USING (advertiser_id, audience_list_id) ",
        'parameters': [
          {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Google Cloud Project Id.',
              'default': ''
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Google Cloud Project Id.',
              'default': ''
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Google Cloud Project Id.',
              'default': ''
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Google Cloud Project Id.',
              'default': ''
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be created in BigQuery.'
            }
          }
        ],
        'legacy': False
      },
      'to': {
        'view': 'DV360_Audience_Analysis',
        'dataset': {
          'field': {
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Place where tables will be created in BigQuery.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('audience_analysis', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
