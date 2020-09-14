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
"""--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

Monthly Budget Mover

Apply the previous month's budget/spend delta to the current month.  Aggregate
up the budget and spend from the previous month of each category declared then
apply the delta of the spend and budget equally to each Line Item under that
Category.

No changes made can be made in DV360 from the start to the end of this process
Make sure there is budget information for the current and previous month's IOs
in DV360
Make sure the provided spend report has spend data for every IO in the previous
month
Spend report must contain 'Revenue (Adv Currency)' and 'Insertion Order ID'
There are no duplicate IO Ids in the categories outlined below
This process must be ran during the month of the budget it is updating
If you receive a 502 error then you must separate your jobs into two, because
there is too much information being pulled in the sdf
Manually run this job
Once the job has completed go to the table for the new sdf and export to a csv
Take the new sdf and upload it into DV360

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
    'auth_read': 'user',  # Credentials used for reading data.
    'recipe_name': '',  # Name of report in DV360, should be unique.
    'auth_write': 'service',  # Credentials used for writing data.
    'partner_id': '',  # The sdf file types.
    'budget_categories':
        '{}',  # A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}
    'filter_ids': [],  # Comma separated list of filter ids for the request.
    'excluded_ios':
        '',  # A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
    'dataset': '',  # Dataset to be written to in BigQuery.
    'version': '5',  # The sdf version to be returned.
    'is_colab':
        True,  # Are you running this in Colab? (This will store the files in Colab instead of Bigquery)
}

TASKS = [{
    'dataset': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'description':
            'Create a dataset where data will be combined and transfored for '
            'upload.',
        'dataset': {
            'field': {
                'description':
                    'Place where tables will be created in BigQuery.',
                'name':
                    'dataset',
                'kind':
                    'string',
                'order':
                    1
            }
        }
    }
}, {
    'dbm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'delete': False,
        'report': {
            'filters': {
                'FILTER_ADVERTISER': {
                    'values': {
                        'field': {
                            'description':
                                'The comma separated list of Advertiser Ids.',
                            'name':
                                'filter_ids',
                            'default':
                                '',
                            'kind':
                                'integer_list',
                            'order':
                                7
                        }
                    }
                }
            },
            'timeout': 90,
            'body': {
                'params': {
                    'type':
                        'TYPE_GENERAL',
                    'metrics': ['METRIC_REVENUE_ADVERTISER'],
                    'groupBys': [
                        'FILTER_ADVERTISER_CURRENCY', 'FILTER_INSERTION_ORDER'
                    ]
                },
                'metadata': {
                    'dataRange': 'PREVIOUS_MONTH',
                    'title': {
                        'field': {
                            'description':
                                'Name of report in DV360, should be unique.',
                            'name':
                                'recipe_name',
                            'kind':
                                'string',
                            'order':
                                1,
                            'prefix':
                                'Monthly_Budget_Mover_'
                        }
                    },
                    'format': 'CSV'
                },
                'timezoneCode': {
                    'field': {
                        'description': 'Timezone for report dates.',
                        'name': 'recipe_timezone',
                        'default': 'America/Los_Angeles',
                        'kind': 'timezone'
                    }
                }
            }
        }
    }
}, {
    'monthly_budget_mover': {
        'out_changes': {
            'bigquery': {
                'table': {
                    'field': {
                        'prefix': 'SDF_BUDGET_MOVER_LOG_',
                        'name': 'recipe_name',
                        'kind': 'string',
                        'description': ''
                    }
                },
                'skip_rows': 0,
                'disposition': 'WRITE_TRUNCATE',
                'schema': [],
                'dataset': {
                    'field': {
                        'description':
                            'Dataset that you would like your output tables to'
                            ' be produced in.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            8
                    }
                }
            },
            'file': '/content/log.csv'
        },
        'out_old_sdf': {
            'bigquery': {
                'table': {
                    'field': {
                        'prefix': 'SDF_OLD_',
                        'name': 'recipe_name',
                        'kind': 'string',
                        'description': ''
                    }
                },
                'skip_rows': 0,
                'disposition': 'WRITE_TRUNCATE',
                'schema': [],
                'dataset': {
                    'field': {
                        'description':
                            'Dataset that you would like your output tables to'
                            ' be produced in.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            8
                    }
                }
            },
            'file': '/content/old_sdf.csv'
        },
        'out_new_sdf': {
            'bigquery': {
                'table': {
                    'field': {
                        'prefix': 'SDF_NEW_',
                        'name': 'recipe_name',
                        'kind': 'string',
                        'description': ''
                    }
                },
                'skip_rows': 0,
                'disposition': 'WRITE_TRUNCATE',
                'schema': [],
                'dataset': {
                    'field': {
                        'description':
                            'Dataset that you would like your output tables to'
                            ' be produced in.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            8
                    }
                }
            },
            'file': '/content/new_sdf.csv'
        },
        'sdf': {
            'time_partitioned_table': False,
            'create_single_day_table': False,
            'version': {
                'field': {
                    'order': 6,
                    'name': 'version',
                    'default': '5',
                    'description': 'The sdf version to be returned.',
                    'choices': ['SDF_VERSION_5', 'SDF_VERSION_5_1'],
                    'kind': 'choice'
                }
            },
            'read': {
                'filter_ids': {
                    'single_cell': True,
                    'values': {
                        'field': {
                            'description':
                                'Comma separated list of filter ids for the '
                                'request.',
                            'name':
                                'filter_ids',
                            'default': [],
                            'kind':
                                'integer_list',
                            'order':
                                4
                        }
                    }
                }
            },
            'auth': 'user',
            'file_types': 'INSERTION_ORDER',
            'table_suffix': '',
            'filter_type': 'FILTER_TYPE_ADVERTISER_ID',
            'dataset': {
                'field': {
                    'description': 'Dataset to be written to in BigQuery.',
                    'name': 'dataset',
                    'default': '',
                    'kind': 'string',
                    'order': 6
                }
            },
            'partner_id': {
                'field': {
                    'description': 'The sdf file types.',
                    'name': 'partner_id',
                    'kind': 'integer',
                    'order': 1
                }
            }
        },
        'auth': 'user',
        'budget_categories': {
            'field': {
                'description':
                    'A dictionary to show which IO Ids go under which '
                    'Category. {"CATEGORY1":[12345,12345,12345], '
                    '"CATEGORY2":[12345,12345]}',
                'name':
                    'budget_categories',
                'default':
                    '{}',
                'kind':
                    'json',
                'order':
                    3
            }
        },
        'excluded_ios': {
            'field': {
                'description':
                    'A comma separated list of Inserion Order Ids that should '
                    'be exluded from the budget calculations',
                'name':
                    'excluded_ios',
                'kind':
                    'integer_list',
                'order':
                    4
            }
        },
        'report_name': {
            'field': {
                'description': 'Name of report in DV360, should be unique.',
                'name': 'recipe_name',
                'kind': 'string',
                'order': 1,
                'prefix': 'Monthly_Budget_Mover_'
            }
        },
        'is_colab': {
            'field': {
                'description':
                    'Are you running this in Colab? (This will store the files'
                    ' in Colab instead of Bigquery)',
                'name':
                    'is_colab',
                'default':
                    True,
                'kind':
                    'boolean',
                'order':
                    7
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('monthly_budget_mover', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
