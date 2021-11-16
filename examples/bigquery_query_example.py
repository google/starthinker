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


def recipe_bigquery_query(config, auth_write, query, dataset, table, legacy):
  """Save query results into a BigQuery table.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       query (text) - SQL with newlines and all.
       dataset (string) - Existing BigQuery dataset.
       table (string) - Table to create from this query.
       legacy (boolean) - Query type must match source tables.
  """

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':query,
      'legacy':legacy
    },
    'to':{
      'dataset':dataset,
      'table':table
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Save query results into a BigQuery table.

      1. Specify a single query and choose legacy or standard mode.
      2. For PLX use user authentication and: SELECT * FROM [plx.google:FULL_TABLE_NAME.all] WHERE...
      3. Every time the query runs it will overwrite the table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-query", help="SQL with newlines and all.", default='')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-table", help="Table to create from this query.", default='')
  parser.add_argument("-legacy", help="Query type must match source tables.", default=True)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_bigquery_query(config, args.auth_write, args.query, args.dataset, args.table, args.legacy)
