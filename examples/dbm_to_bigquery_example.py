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
from starthinker.task.dbm.run import dbm


def recipe_dbm_to_bigquery(config, auth_read, auth_write, dbm_report_id, dbm_report_name, dbm_dataset, dbm_table, dbm_schema, is_incremental_load):
  """Move existing DV360 reports into a BigQuery table.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Authorization used for writing data.
       dbm_report_id (integer) - DV360 report ID given in UI, not needed if name used.
       dbm_report_name (string) - Name of report, not needed if ID used.
       dbm_dataset (string) - Existing BigQuery dataset.
       dbm_table (string) - Table to create from this report.
       dbm_schema (json) - Schema provided in JSON list format or empty value to auto detect.
       is_incremental_load (boolean) - Clear data in destination table during this report's time period, then append report data to destination table.
  """

  dbm(config, {
    'auth':auth_read,
    'report':{
      'report_id':dbm_report_id,
      'name':dbm_report_name
    },
    'out':{
      'bigquery':{
        'auth':auth_write,
        'dataset':dbm_dataset,
        'table':dbm_table,
        'schema':dbm_schema,
        'header':True,
        'is_incremental_load':is_incremental_load
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move existing DV360 reports into a BigQuery table.

      1. Specify either report name or report id to move a report.
      2. A schema is recommended, if not provided it will be guessed.
      3. The most recent valid file will be moved to the table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Authorization used for writing data.", default='service')
  parser.add_argument("-dbm_report_id", help="DV360 report ID given in UI, not needed if name used.", default='')
  parser.add_argument("-dbm_report_name", help="Name of report, not needed if ID used.", default='')
  parser.add_argument("-dbm_dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-dbm_table", help="Table to create from this report.", default='')
  parser.add_argument("-dbm_schema", help="Schema provided in JSON list format or empty value to auto detect.", default=None)
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

  recipe_dbm_to_bigquery(config, args.auth_read, args.auth_write, args.dbm_report_id, args.dbm_report_name, args.dbm_dataset, args.dbm_table, args.dbm_schema, args.is_incremental_load)
