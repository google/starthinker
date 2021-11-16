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
from starthinker.task.bigquery.run import bigquery


def recipe_bigquery_to_sheet(config, auth_read, sheet, tab, range, dataset, query, legacy):
  """Copy the contents of a query into a Google Sheet.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       sheet (string) - Either sheet url or sheet name.
       tab (string) - Name of the tab where to put the data.
       range (string) - Range in the sheet to place the data, leave blank for whole sheet.
       dataset (string) - Existing BigQuery dataset.
       query (text) - Query to pull data from the table.
       legacy (boolean) - Use Legacy SQL
  """

  bigquery(config, {
    'auth':auth_read,
    'from':{
      'auth':'service',
      'dataset':dataset,
      'query':query,
      'legacy':legacy
    },
    'to':{
      'sheet':sheet,
      'tab':tab,
      'range':range
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Copy the contents of a query into a Google Sheet.

      1. Specify the sheet and the query.
      2. Leave range blank or set to A2 to insert one line down.
      3. The range is cleared before the sheet is written to.
      4. To select a table use SELECT * FROM table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-sheet", help="Either sheet url or sheet name.", default='')
  parser.add_argument("-tab", help="Name of the tab where to put the data.", default='')
  parser.add_argument("-range", help="Range in the sheet to place the data, leave blank for whole sheet.", default='')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-query", help="Query to pull data from the table.", default='')
  parser.add_argument("-legacy", help="Use Legacy SQL", default=True)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_bigquery_to_sheet(config, args.auth_read, args.sheet, args.tab, args.range, args.dataset, args.query, args.legacy)
