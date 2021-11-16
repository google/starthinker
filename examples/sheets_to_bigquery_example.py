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
from starthinker.task.sheets.run import sheets


def recipe_sheets_to_bigquery(config, auth_read, auth_write, sheets_url, sheets_tab, sheets_range, dataset, table, sheets_header):
  """Import data from a sheet and move it to a BigQuery table.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Credentials used for writing data.
       sheets_url (string) - NA
       sheets_tab (string) - NA
       sheets_range (string) - NA
       dataset (string) - NA
       table (string) - NA
       sheets_header (boolean) - NA
  """

  sheets(config, {
    'auth':auth_read,
    'sheet':sheets_url,
    'tab':sheets_tab,
    'range':sheets_range,
    'header':sheets_header,
    'out':{
      'auth':auth_write,
      'bigquery':{
        'dataset':dataset,
        'table':table
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Import data from a sheet and move it to a BigQuery table.

      1. For the sheet, provide the full edit URL.
      2. If the tab does not exist it will be created.
      3. Empty cells in the range will be NULL.
      4. Check Sheets header if first row is a header
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-sheets_url", help="", default='')
  parser.add_argument("-sheets_tab", help="", default='')
  parser.add_argument("-sheets_range", help="", default='')
  parser.add_argument("-dataset", help="", default='')
  parser.add_argument("-table", help="", default='')
  parser.add_argument("-sheets_header", help="", default=True)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_sheets_to_bigquery(config, args.auth_read, args.auth_write, args.sheets_url, args.sheets_tab, args.sheets_range, args.dataset, args.table, args.sheets_header)
