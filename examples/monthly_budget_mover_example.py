###########################################################################
#
#  Copyright 2021 Google LLC
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
#  This code generated (see scripts folder for possible source):
#    - Command: "python starthinker_ui/manage.py example"
#
###########################################################################

import argparse
import textwrap

from starthinker.util.configuration import Configuration
from starthinker.task.dataset.run import dataset
from starthinker.task.dbm.run import dbm
from starthinker.task.monthly_budget_mover.run import monthly_budget_mover


def recipe_monthly_budget_mover(config, recipe_timezone, recipe_name, auth_write, auth_read, partner_id, budget_categories, filter_ids, excluded_ios, version, is_colab, dataset):
  """Apply the previous month's budget/spend delta to the current month.  Aggregate
     up the budget and spend from the previous month of each category declared
     then apply the delta of the spend and budget equally to each Line Item
     under that Category.

     Args:
       recipe_timezone (timezone) - Timezone for report dates.
       recipe_name (string) - Table to write to.
       auth_write (authentication) - Credentials used for writing data.
       auth_read (authentication) - Credentials used for reading data.
       partner_id (integer) - The sdf file types.
       budget_categories (json) - A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}
       filter_ids (integer_list) - Comma separated list of filter ids for the request.
       excluded_ios (integer_list) - A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
       version (choice) - The sdf version to be returned.
       is_colab (boolean) - Are you running this in Colab? (This will store the files in Colab instead of Bigquery)
       dataset (string) - Dataset that you would like your output tables to be produced in.
  """

  dataset(config, {
    'description':'Create a dataset where data will be combined and transfored for upload.',
    'auth':auth_write,
    'dataset':dataset
  })

  dbm(config, {
    'auth':auth_read,
    'report':{
      'timeout':90,
      'filters':{
        'FILTER_ADVERTISER':{
          'values':filter_ids
        }
      },
      'body':{
        'timezoneCode':recipe_timezone,
        'metadata':{
          'title':recipe_name,
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
  })

  monthly_budget_mover(config, {
    'auth':'user',
    'is_colab':is_colab,
    'report_name':recipe_name,
    'budget_categories':budget_categories,
    'excluded_ios':excluded_ios,
    'sdf':{
      'auth':'user',
      'version':version,
      'partner_id':partner_id,
      'file_types':'INSERTION_ORDER',
      'filter_type':'FILTER_TYPE_ADVERTISER_ID',
      'read':{
        'filter_ids':{
          'single_cell':True,
          'values':filter_ids
        }
      },
      'time_partitioned_table':False,
      'create_single_day_table':False,
      'dataset':dataset,
      'table_suffix':''
    },
    'out_old_sdf':{
      'bigquery':{
        'dataset':dataset,
        'table':recipe_name,
        'schema':[
        ],
        'skip_rows':0,
        'disposition':'WRITE_TRUNCATE'
      },
      'file':'/content/old_sdf.csv'
    },
    'out_new_sdf':{
      'bigquery':{
        'dataset':dataset,
        'table':recipe_name,
        'schema':[
        ],
        'skip_rows':0,
        'disposition':'WRITE_TRUNCATE'
      },
      'file':'/content/new_sdf.csv'
    },
    'out_changes':{
      'bigquery':{
        'dataset':dataset,
        'table':recipe_name,
        'schema':[
        ],
        'skip_rows':0,
        'disposition':'WRITE_TRUNCATE'
      },
      'file':'/content/log.csv'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Apply the previous month's budget/spend delta to the current month.  Aggregate up the budget and spend from the previous month of each category declared then apply the delta of the spend and budget equally to each Line Item under that Category.

      1. No changes made can be made in DV360 from the start to the end of this process
      2. Make sure there is budget information for the current and previous month's IOs in DV360
      3. Make sure the provided spend report has spend data for every IO in the previous month
      4. Spend report must contain 'Revenue (Adv Currency)' and 'Insertion Order ID'
      5. There are no duplicate IO Ids in the categories outlined below
      6. This process must be ran during the month of the budget it is updating
      7. If you receive a 502 error then you must separate your jobs into two, because there is too much information being pulled in the sdf
      8. Manually run this job
      9. Once the job has completed go to the table for the new sdf and export to a csv
      10. Take the new sdf and upload it into DV360
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_timezone", help="Timezone for report dates.", default='America/Los_Angeles')
  parser.add_argument("-recipe_name", help="Table to write to.", default=None)
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-partner_id", help="The sdf file types.", default=None)
  parser.add_argument("-budget_categories", help="A dictionary to show which IO Ids go under which Category. {"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}", default='{}')
  parser.add_argument("-filter_ids", help="Comma separated list of filter ids for the request.", default=[])
  parser.add_argument("-excluded_ios", help="A comma separated list of Inserion Order Ids that should be exluded from the budget calculations", default=None)
  parser.add_argument("-version", help="The sdf version to be returned.", default='5')
  parser.add_argument("-is_colab", help="Are you running this in Colab? (This will store the files in Colab instead of Bigquery)", default=True)
  parser.add_argument("-dataset", help="Dataset that you would like your output tables to be produced in.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_monthly_budget_mover(config, args.recipe_timezone, args.recipe_name, args.auth_write, args.auth_read, args.partner_id, args.budget_categories, args.filter_ids, args.excluded_ios, args.version, args.is_colab, args.dataset)
