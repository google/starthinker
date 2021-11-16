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
from starthinker.task.dynamic_costs.run import dynamic_costs


def recipe_dynamic_costs(config, dcm_account, auth_read, configuration_sheet_url, auth_write, bigquery_dataset):
  """Calculate DV360 cost at the dynamic creative combination level.

     Args:
       dcm_account (string) - NA
       auth_read (authentication) - Credentials used for reading data.
       configuration_sheet_url (string) - NA
       auth_write (authentication) - Credentials used for writing data.
       bigquery_dataset (string) - NA
  """

  dynamic_costs(config, {
    'auth':auth_read,
    'account':dcm_account,
    'sheet':{
      'template':{
        'url':'https://docs.google.com/spreadsheets/d/19J-Hjln2wd1E0aeG3JDgKQN9TVGRLWxIEUQSmmQetJc/edit?usp=sharing',
        'tab':'Dynamic Costs',
        'range':'A1'
      },
      'url':configuration_sheet_url,
      'tab':'Dynamic Costs',
      'range':'A2:B'
    },
    'out':{
      'auth':auth_write,
      'dataset':bigquery_dataset
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Calculate DV360 cost at the dynamic creative combination level.

      1. Add a sheet URL. This is where you will enter advertiser and campaign level details.
      2. Specify the CM network ID.
      3. Click run now once, and a tab called Dynamic Costs will be added to the sheet with instructions.
      4. Follow the instructions on the sheet; this will be your configuration.
      5. StarThinker will create two or three (depending on the case) reports in CM named Dynamic Costs - ....
      6. Wait for BigQuery->->->Dynamic_Costs_Analysis to be created or click Run Now.
      7. Copy 1-Dynamic Costs Sample Data.
         7.1 - Dynamic Costs Sample Data: https://datastudio.google.com/open/1vBvBEiMbqCbBuJTsBGpeg8vCLtg6ztqA
      8. Click Edit Connection, and Change to BigQuery->->->Dynamic_Costs_Analysis.
      9. Copy 1-Dynamic Costs Sample Report.
         9.1 - Dynamic Costs Sample Report: https://datastudio.google.com/open/1xulBAdx95SnvjnUzFP6r14lhkvvVbsP8
      10. When prompted, choose the new data source you just created.
      11. Edit the table to include or exclude columns as desired.
      12. Or, give the dashboard connection intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-dcm_account", help="", default='')
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-configuration_sheet_url", help="", default='')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-bigquery_dataset", help="", default='dynamic_costs')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dynamic_costs(config, args.dcm_account, args.auth_read, args.configuration_sheet_url, args.auth_write, args.bigquery_dataset)
