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
  'auth_write': 'service',  # Credentials used for writing data.
  'partner_id': '',  # The sdf file types.
  'auth_read': 'user',  # Credentials used for reading data.
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
      'dataset': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'dataset',
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
    'dbm': {
      'report': {
        'timeout': 90,
        'filters': {
          'FILTER_ADVERTISER': {
            'values': {
              'field': {
                'order': 7,
                'kind': 'integer_list',
                'name': 'filter_ids',
                'description': 'The comma separated list of Advertiser Ids.',
                'default': ''
              }
            }
          }
        },
        'body': {
          'metadata': {
            'dataRange': 'PREVIOUS_MONTH',
            'title': {
              'field': {
                'order': 1,
                'kind': 'string',
                'name': 'recipe_name',
                'description': 'Name of report in DV360, should be unique.',
                'prefix': 'Monthly_Budget_Mover_'
              }
            },
            'format': 'CSV'
          },
          'params': {
            'groupBys': [
              'FILTER_ADVERTISER_CURRENCY',
              'FILTER_INSERTION_ORDER'
            ],
            'type': 'TYPE_GENERAL',
            'metrics': [
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
    'monthly_budget_mover': {
      'report_name': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'recipe_name',
          'description': 'Name of report in DV360, should be unique.',
          'prefix': 'Monthly_Budget_Mover_'
        }
      },
      'sdf': {
        'partner_id': {
          'field': {
            'order': 1,
            'kind': 'integer',
            'name': 'partner_id',
            'description': 'The sdf file types.'
          }
        },
        'create_single_day_table': False,
        'file_types': 'INSERTION_ORDER',
        'dataset': {
          'field': {
            'order': 6,
            'kind': 'string',
            'name': 'dataset',
            'description': 'Dataset to be written to in BigQuery.',
            'default': ''
          }
        },
        'version': {
          'field': {
            'description': 'The sdf version to be returned.',
            'choices': [
              'SDF_VERSION_5',
              'SDF_VERSION_5_1'
            ],
            'order': 6,
            'kind': 'choice',
            'name': 'version',
            'default': '5'
          }
        },
        'time_partitioned_table': False,
        'auth': 'user',
        'table_suffix': '',
        'read': {
          'filter_ids': {
            'values': {
              'field': {
                'order': 4,
                'kind': 'integer_list',
                'name': 'filter_ids',
                'description': 'Comma separated list of filter ids for the request.',
                'default': [
                ]
              }
            },
            'single_cell': True
          }
        },
        'filter_type': 'FILTER_TYPE_ADVERTISER_ID'
      },
      'is_colab': {
        'field': {
          'order': 7,
          'kind': 'boolean',
          'name': 'is_colab',
          'description': 'Are you running this in Colab? (This will store the files in Colab instead of Bigquery)',
          'default': True
        }
      },
      'out_old_sdf': {
        'file': '/content/old_sdf.csv',
        'bigquery': {
          'schema': [
          ],
          'table': {
            'field': {
              'kind': 'string',
              'name': 'recipe_name',
              'description': '',
              'prefix': 'SDF_OLD_'
            }
          },
          'disposition': 'WRITE_TRUNCATE',
          'dataset': {
            'field': {
              'order': 8,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Dataset that you would like your output tables to be produced in.',
              'default': ''
            }
          },
          'skip_rows': 0
        }
      },
      'out_changes': {
        'file': '/content/log.csv',
        'bigquery': {
          'schema': [
          ],
          'table': {
            'field': {
              'kind': 'string',
              'name': 'recipe_name',
              'description': '',
              'prefix': 'SDF_BUDGET_MOVER_LOG_'
            }
          },
          'disposition': 'WRITE_TRUNCATE',
          'dataset': {
            'field': {
              'order': 8,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Dataset that you would like your output tables to be produced in.',
              'default': ''
            }
          },
          'skip_rows': 0
        }
      },
      'auth': 'user',
      'budget_categories': {
        'field': {
          'order': 3,
          'kind': 'json',
          'name': 'budget_categories',
          'description': 'A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',
          'default': '{}'
        }
      },
      'out_new_sdf': {
        'file': '/content/new_sdf.csv',
        'bigquery': {
          'schema': [
          ],
          'table': {
            'field': {
              'kind': 'string',
              'name': 'recipe_name',
              'description': '',
              'prefix': 'SDF_NEW_'
            }
          },
          'disposition': 'WRITE_TRUNCATE',
          'dataset': {
            'field': {
              'order': 8,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Dataset that you would like your output tables to be produced in.',
              'default': ''
            }
          },
          'skip_rows': 0
        }
      },
      'excluded_ios': {
        'field': {
          'order': 4,
          'kind': 'integer_list',
          'name': 'excluded_ios',
          'description': 'A comma separated list of Inserion Order Ids that should be exluded from the budget calculations'
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
