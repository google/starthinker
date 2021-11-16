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
from starthinker.task.sa.run import sa


def recipe_sa_report(config, auth_sa, auth_bq, dataset, table, report, is_incremental_load):
  """Move SA360 report to BigQuery.

     Args:
       auth_sa (authentication) - Credentials used for writing data.
       auth_bq (authentication) - Authorization used for writing data.
       dataset (string) - Existing BigQuery dataset.
       table (string) - Table to create from this report.
       report (json) - Body part of report request API call.
       is_incremental_load (boolean) - Clear data in destination table during this report's time period, then append report data to destination table.
  """

  sa(config, {
    'description':'Create a dataset for bigquery tables.',
    'auth':auth_sa,
    'body':report,
    'out':{
      'bigquery':{
        'auth':auth_bq,
        'dataset':dataset,
        'table':table,
        'is_incremental_load':is_incremental_load,
        'header':True
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move SA360 report to BigQuery.

      1. Fill in the report definition and destination table.
      2. Wait for BigQuery->->-> to be created.
      3. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_sa", help="Credentials used for writing data.", default='service')
  parser.add_argument("-auth_bq", help="Authorization used for writing data.", default='service')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-table", help="Table to create from this report.", default='')
  parser.add_argument("-report", help="Body part of report request API call.", default={})
  parser.add_argument("-is_incremental_load", help="Clear data in destination table during this report's time period, then append report data to destination table.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_sa_report(config, args.auth_sa, args.auth_bq, args.dataset, args.table, args.report, args.is_incremental_load)
