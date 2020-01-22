###########################################################################
# 
#  Copyright 2019 Google Inc.
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
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'recipe_name': '',  # 
  'spend_report_id': '',  # The report Id for the DV360 spend report.
  'budget_categories': '{"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',  # A dictionary to show which IO Ids go under which Category. Please view the solutions page for information on format.
  'excluded_ios': '',  # A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
  'filter_type': '',  # The filter type for the filter ids.
  'filter_ids': '',  # The filter ids for the request.
  'dataset': '',  # Dataset that you would like your output tables to be produced in.
}

TASKS = [
  {
    'dataset': {
      'description': 'Create a dataset where data will be combined and transfored for upload.',
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'dataset',
          'kind': 'string',
          'order': 1,
          'description': 'Place where tables will be created in BigQuery.'
        }
      }
    }
  },
  {
    'monthly_budget_mover': {
      'auth': 'user',
      'spend_report_id': {
        'field': {
          'name': 'spend_report_id',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'The report Id for the DV360 spend report.'
        }
      },
      'budget_categories': {
        'field': {
          'name': 'budget_categories',
          'kind': 'json',
          'order': 3,
          'default': '{"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',
          'description': 'A dictionary to show which IO Ids go under which Category. Please view the solutions page for information on format.'
        }
      },
      'excluded_ios': {
        'field': {
          'name': 'excluded_ios',
          'kind': 'integer_list',
          'order': 4,
          'description': 'A comma separated list of Inserion Order Ids that should be exluded from the budget calculations'
        }
      },
      'sdf': {
        'auth': 'user',
        'file_types': 'INSERTION_ORDER',
        'filter_type': {
          'field': {
            'name': 'filter_type',
            'kind': 'choice',
            'order': 6,
            'default': '',
            'description': 'The filter type for the filter ids.',
            'choices': [
              'ADVERTISER_ID',
              'CAMPAIGN_ID',
              'INSERTION_ORDER_ID',
              'INVENTORY_SOURCE_ID',
              'LINE_ITEM_ID',
              'PARTNER_ID'
            ]
          }
        },
        'filter_ids': {
          'field': {
            'name': 'filter_ids',
            'kind': 'integer_list',
            'order': 7,
            'default': '',
            'description': 'The filter ids for the request.'
          }
        }
      },
      'out': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 8,
            'default': '',
            'description': 'Dataset that you would like your output tables to be produced in.'
          }
        },
        'old_sdf_table_name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'SDF_OLD_',
            'description': ''
          }
        },
        'new_sdf_table_name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'SDF_NEW_',
            'description': ''
          }
        },
        'changes_table_name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'SDF_BUDGET_MOVER_LOG_',
            'description': ''
          }
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
