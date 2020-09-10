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

Monthly Budget Mover

Apply the previous month's budget/spend delta to the current month.  Aggregate up the budget and spend from the previous month of each category declared then apply the delta of the spend and budget equally to each Line Item under that Category.

No changes made can be made in DV360 from the start to the end of this process
Make sure there is budget information for the current and previous month's IOs in DV360
Make sure the provided spend report has spend data for every IO in the previous month
Spend report must contain 'Revenue (Adv Currency)' and 'Insertion Order ID'
There are no duplicate IO Ids in the categories outlined below
This process must be ran during the month of the budget it is updating
If you receive a 502 error then you must separate your jobs into two, because there is too much information being pulled in the sdf
Manually run this job
Once the job has completed go to the table for the new sdf and export to a csv
Take the new sdf and upload it into DV360

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_name': '',  # 
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'partner_id': '',  # The sdf file types.
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'budget_categories': '{}',  # A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}
  'filter_ids': [],  # Comma separated list of filter ids for the request.
  'excluded_ios': '',  # A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
  'version': '5',  # The sdf version to be returned.
  'is_colab': True,  # Are you running this in Colab? (This will store the files in Colab instead of Bigquery)
  'dataset': '',  # Dataset that you would like your output tables to be produced in.
}

TASKS = [
  {
    'dataset': {
      'description': 'Create a dataset where data will be combined and transfored for upload.',
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
          'order': 1,
          'name': 'dataset',
          'description': 'Place where tables will be created in BigQuery.',
          'kind': 'string'
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
                'description': 'The comma separated list of Advertiser Ids.',
                'kind': 'integer_list',
                'name': 'filter_ids',
                'order': 7,
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
                'prefix': 'Monthly_Budget_Mover_',
                'description': 'Name of report in DV360, should be unique.',
                'kind': 'string'
              }
            },
            'dataRange': 'PREVIOUS_MONTH',
            'format': 'CSV'
          },
          'params': {
            'type': 'TYPE_GENERAL',
            'groupBys': [
              'FILTER_ADVERTISER_CURRENCY',
              'FILTER_INSERTION_ORDER'
            ],
            'metrics': [
              'METRIC_REVENUE_ADVERTISER'
            ]
          }
        },
        'timeout': 90
      }
    }
  },
  {
    'monthly_budget_mover': {
      'is_colab': {
        'field': {
          'description': 'Are you running this in Colab? (This will store the files in Colab instead of Bigquery)',
          'kind': 'boolean',
          'name': 'is_colab',
          'order': 7,
          'default': True
        }
      },
      'report_name': {
        'field': {
          'name': 'recipe_name',
          'order': 1,
          'prefix': 'Monthly_Budget_Mover_',
          'description': 'Name of report in DV360, should be unique.',
          'kind': 'string'
        }
      },
      'out_old_sdf': {
        'bigquery': {
          'skip_rows': 0,
          'dataset': {
            'field': {
              'description': 'Dataset that you would like your output tables to be produced in.',
              'kind': 'string',
              'name': 'dataset',
              'order': 8,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'recipe_name',
              'description': '',
              'prefix': 'SDF_OLD_',
              'kind': 'string'
            }
          },
          'disposition': 'WRITE_TRUNCATE',
          'schema': [
          ]
        },
        'file': '/content/old_sdf.csv'
      },
      'budget_categories': {
        'field': {
          'description': 'A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',
          'kind': 'json',
          'name': 'budget_categories',
          'order': 3,
          'default': '{}'
        }
      },
      'out_new_sdf': {
        'bigquery': {
          'skip_rows': 0,
          'dataset': {
            'field': {
              'description': 'Dataset that you would like your output tables to be produced in.',
              'kind': 'string',
              'name': 'dataset',
              'order': 8,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'recipe_name',
              'description': '',
              'prefix': 'SDF_NEW_',
              'kind': 'string'
            }
          },
          'disposition': 'WRITE_TRUNCATE',
          'schema': [
          ]
        },
        'file': '/content/new_sdf.csv'
      },
      'sdf': {
        'file_types': 'INSERTION_ORDER',
        'table_suffix': '',
        'dataset': {
          'field': {
            'description': 'Dataset to be written to in BigQuery.',
            'kind': 'string',
            'name': 'dataset',
            'order': 6,
            'default': ''
          }
        },
        'filter_type': 'FILTER_TYPE_ADVERTISER_ID',
        'partner_id': {
          'field': {
            'order': 1,
            'name': 'partner_id',
            'description': 'The sdf file types.',
            'kind': 'integer'
          }
        },
        'version': {
          'field': {
            'choices': [
              'SDF_VERSION_5',
              'SDF_VERSION_5_1'
            ],
            'description': 'The sdf version to be returned.',
            'name': 'version',
            'kind': 'choice',
            'order': 6,
            'default': '5'
          }
        },
        'auth': 'user',
        'create_single_day_table': False,
        'read': {
          'filter_ids': {
            'values': {
              'field': {
                'description': 'Comma separated list of filter ids for the request.',
                'kind': 'integer_list',
                'name': 'filter_ids',
                'order': 4,
                'default': [
                ]
              }
            },
            'single_cell': True
          }
        },
        'time_partitioned_table': False
      },
      'auth': 'user',
      'out_changes': {
        'bigquery': {
          'skip_rows': 0,
          'dataset': {
            'field': {
              'description': 'Dataset that you would like your output tables to be produced in.',
              'kind': 'string',
              'name': 'dataset',
              'order': 8,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'recipe_name',
              'description': '',
              'prefix': 'SDF_BUDGET_MOVER_LOG_',
              'kind': 'string'
            }
          },
          'disposition': 'WRITE_TRUNCATE',
          'schema': [
          ]
        },
        'file': '/content/log.csv'
      },
      'excluded_ios': {
        'field': {
          'order': 4,
          'name': 'excluded_ios',
          'description': 'A comma separated list of Inserion Order Ids that should be exluded from the budget calculations',
          'kind': 'integer_list'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('monthly_budget_mover', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
