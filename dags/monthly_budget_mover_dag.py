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
#
#  This code generated (see starthinker/scripts for possible source):
#    - Command: "python starthinker_ui/manage.py airflow"
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

DV360 Monthly Budget Mover

Apply the previous month's budget/spend delta to the current month.  Aggregate up the budget and spend from the previous month of each category declared then apply the delta of the spend and budget equally to each Line Item under that Category.

  - No changes made can be made in DV360 from the start to the end of this process
  - Make sure there is budget information for the current and previous month's IOs in DV360
  - Make sure the provided spend report has spend data for every IO in the previous month
  - Spend report must contain 'Revenue (Adv Currency)' and 'Insertion Order ID'
  - There are no duplicate IO Ids in the categories outlined below
  - This process must be ran during the month of the budget it is updating
  - If you receive a 502 error then you must separate your jobs into two, because there is too much information being pulled in the sdf
  - Manually run this job
  - Once the job has completed go to the table for the new sdf and export to a csv
  - Take the new sdf and upload it into DV360

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_timezone':'America/Los_Angeles',  # Timezone for report dates.
  'recipe_name':'',  # Table to write to.
  'auth_write':'service',  # Credentials used for writing data.
  'auth_read':'user',  # Credentials used for reading data.
  'partner_id':'',  # The sdf file types.
  'budget_categories':'{}',  # A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}
  'filter_ids':[],  # Comma separated list of filter ids for the request.
  'excluded_ios':'',  # A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
  'version':'5',  # The sdf version to be returned.
  'is_colab':True,  # Are you running this in Colab? (This will store the files in Colab instead of Bigquery)
  'dataset':'',  # Dataset that you would like your output tables to be produced in.
}

RECIPE = {
  'setup':{
    'day':[
      'Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'
    ],
    'hour':[
      2,
      4,
      6,
      8,
      10,
      12,
      14,
      16,
      18,
      20,
      22,
      24
    ]
  },
  'tasks':[
    {
      'dataset':{
        'description':'Create a dataset where data will be combined and transfored for upload.',
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'dataset','kind':'string','order':1,'description':'Place where tables will be created in BigQuery.'}}
      }
    },
    {
      'dbm':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'report':{
          'timeout':90,
          'filters':{
            'FILTER_ADVERTISER':{
              'values':{'field':{'name':'filter_ids','kind':'integer_list','order':7,'default':'','description':'The comma separated list of Advertiser Ids.'}}
            }
          },
          'body':{
            'timezoneCode':{'field':{'name':'recipe_timezone','kind':'timezone','description':'Timezone for report dates.','default':'America/Los_Angeles'}},
            'metadata':{
              'title':{'field':{'name':'recipe_name','kind':'string','prefix':'Monthly_Budget_Mover_','order':1,'description':'Name of report in DV360, should be unique.'}},
              'dataRange':'PREVIOUS_MONTH',
              'format':'CSV'
            },
            'params':{
              'type':'TYPE_GENERAL',
              'groupBys':[
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_INSERTION_ORDER'
              ],
              'metrics':[
                'METRIC_REVENUE_ADVERTISER'
              ]
            }
          }
        },
        'delete':False
      }
    },
    {
      'monthly_budget_mover':{
        'auth':'user',
        'is_colab':{'field':{'name':'is_colab','kind':'boolean','default':True,'order':7,'description':'Are you running this in Colab? (This will store the files in Colab instead of Bigquery)'}},
        'report_name':{'field':{'name':'recipe_name','kind':'string','prefix':'Monthly_Budget_Mover_','order':1,'description':'Name of report in DV360, should be unique.'}},
        'budget_categories':{'field':{'name':'budget_categories','kind':'json','order':3,'default':'{}','description':'A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}'}},
        'excluded_ios':{'field':{'name':'excluded_ios','kind':'integer_list','order':4,'description':'A comma separated list of Inserion Order Ids that should be exluded from the budget calculations'}},
        'sdf':{
          'auth':'user',
          'version':{'field':{'name':'version','kind':'choice','order':6,'default':'5','description':'The sdf version to be returned.','choices':['SDF_VERSION_5','SDF_VERSION_5_1']}},
          'partner_id':{'field':{'name':'partner_id','kind':'integer','order':1,'description':'The sdf file types.'}},
          'file_types':'INSERTION_ORDER',
          'filter_type':'FILTER_TYPE_ADVERTISER_ID',
          'read':{
            'filter_ids':{
              'single_cell':True,
              'values':{'field':{'name':'filter_ids','kind':'integer_list','order':4,'default':[],'description':'Comma separated list of filter ids for the request.'}}
            }
          },
          'time_partitioned_table':False,
          'create_single_day_table':False,
          'dataset':{'field':{'name':'dataset','kind':'string','order':6,'default':'','description':'Dataset to be written to in BigQuery.'}},
          'table_suffix':''
        },
        'out_old_sdf':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':8,'default':'','description':'Dataset that you would like your output tables to be produced in.'}},
            'table':{'field':{'name':'recipe_name','kind':'string','prefix':'SDF_OLD_','description':'Table to write to.'}},
            'schema':[
            ],
            'skip_rows':0,
            'disposition':'WRITE_TRUNCATE'
          },
          'file':'/content/old_sdf.csv'
        },
        'out_new_sdf':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':8,'default':'','description':'Dataset that you would like your output tables to be produced in.'}},
            'table':{'field':{'name':'recipe_name','kind':'string','prefix':'SDF_NEW_','description':'Table to write to.'}},
            'schema':[
            ],
            'skip_rows':0,
            'disposition':'WRITE_TRUNCATE'
          },
          'file':'/content/new_sdf.csv'
        },
        'out_changes':{
          'bigquery':{
            'dataset':{'field':{'name':'dataset','kind':'string','order':8,'default':'','description':'Dataset that you would like your output tables to be produced in.'}},
            'table':{'field':{'name':'recipe_name','kind':'string','prefix':'SDF_BUDGET_MOVER_LOG_','description':'Table to write to.'}},
            'schema':[
            ],
            'skip_rows':0,
            'disposition':'WRITE_TRUNCATE'
          },
          'file':'/content/log.csv'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('monthly_budget_mover', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
