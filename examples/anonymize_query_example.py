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
from starthinker.task.anonymize.run import anonymize


def recipe_anonymize_query(config, auth_read, from_project, from_dataset, from_query, to_project, to_dataset, to_table):
  """Runs a query and anynonamizes all rows.  Used to create sample table for
     dashboards.

     Args:
       auth_read (authentication) - Credentials used.
       from_project (string) - Original project to read from.
       from_dataset (string) - Original dataset to read from.
       from_query (string) - Query to read data.
       to_project (string) - Anonymous data will be writen to.
       to_dataset (string) - Anonymous data will be writen to.
       to_table (string) - Anonymous data will be writen to.
  """

  anonymize(config, {
    'auth':auth_read,
    'bigquery':{
      'from':{
        'project':from_project,
        'dataset':from_dataset,
        'query':from_query
      },
      'to':{
        'project':to_project,
        'dataset':to_dataset,
        'table':to_table
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Runs a query and anynonamizes all rows.  Used to create sample table for dashboards.

      1. Ensure you have user access to both datasets.
      2. Provide the source project, dataset and query.
      3. Provide the destination project, dataset, and table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used.", default='service')
  parser.add_argument("-from_project", help="Original project to read from.", default=None)
  parser.add_argument("-from_dataset", help="Original dataset to read from.", default=None)
  parser.add_argument("-from_query", help="Query to read data.", default=None)
  parser.add_argument("-to_project", help="Anonymous data will be writen to.", default=None)
  parser.add_argument("-to_dataset", help="Anonymous data will be writen to.", default=None)
  parser.add_argument("-to_table", help="Anonymous data will be writen to.", default=None)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_anonymize_query(config, args.auth_read, args.from_project, args.from_dataset, args.from_query, args.to_project, args.to_dataset, args.to_table)
