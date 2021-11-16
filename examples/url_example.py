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
from starthinker.task.url.run import url


def recipe_url(config, auth, status, read, dataset, table):
  """Pull URL list from a table, fetch them, and write the results to another table.

     Args:
       auth (authentication) - Credentials used for rading and writing data.
       status (boolean) - Pull status of HTTP request.
       read (boolean) - Pull data from HTTP request.
       dataset (string) - Name of Google BigQuery dataset to write.
       table (string) - Name of Google BigQuery table to write.
  """

  url(config, {
    'auth':auth,
    'status':status,
    'read':read,
    'urls':{
      'bigquery':{
        'dataset':dataset,
        'query':table,
        'legacy':False
      }
    },
    'to':{
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
      Pull URL list from a table, fetch them, and write the results to another table.

      1. Specify a table with only two columns URL, URI (can be null).
      2. Check bigquery destination for results of fetching each URL.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth", help="Credentials used for rading and writing data.", default='service')
  parser.add_argument("-status", help="Pull status of HTTP request.", default=True)
  parser.add_argument("-read", help="Pull data from HTTP request.", default=False)
  parser.add_argument("-dataset", help="Name of Google BigQuery dataset to write.", default='')
  parser.add_argument("-table", help="Name of Google BigQuery table to write.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_url(config, args.auth, args.status, args.read, args.dataset, args.table)
