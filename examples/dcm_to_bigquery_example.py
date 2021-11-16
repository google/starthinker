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
from starthinker.task.dcm.run import dcm


def recipe_dcm_to_bigquery(config, auth_read, auth_write, account, report_id, report_name, dataset, table, is_incremental_load):
  """Move existing CM report into a BigQuery table.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Credentials used for writing data.
       account (integer) - CM network id.
       report_id (integer) - CM report id, empty if using name .
       report_name (string) - CM report name, empty if using id instead.
       dataset (string) - Dataset to be written to in BigQuery.
       table (string) - Table to be written to in BigQuery.
       is_incremental_load (boolean) - Clear data in destination table during this report's time period, then append report data to existing table.
  """

  dcm(config, {
    'auth':auth_read,
    'report':{
      'account':account,
      'report_id':report_id,
      'name':report_name
    },
    'out':{
      'bigquery':{
        'auth':auth_write,
        'dataset':dataset,
        'table':table,
        'header':True,
        'is_incremental_load':is_incremental_load
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move existing CM report into a BigQuery table.

      1. Specify an account id.
      2. Specify either report name or report id to move a report.
      3. The most recent valid file will overwrite the table.
      4. Schema is pulled from the official CM specification.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-account", help="CM network id.", default='')
  parser.add_argument("-report_id", help="CM report id, empty if using name .", default='')
  parser.add_argument("-report_name", help="CM report name, empty if using id instead.", default='')
  parser.add_argument("-dataset", help="Dataset to be written to in BigQuery.", default='')
  parser.add_argument("-table", help="Table to be written to in BigQuery.", default='')
  parser.add_argument("-is_incremental_load", help="Clear data in destination table during this report's time period, then append report data to existing table.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dcm_to_bigquery(config, args.auth_read, args.auth_write, args.account, args.report_id, args.report_name, args.dataset, args.table, args.is_incremental_load)
