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


def recipe_bigquery_storage(config, auth_read, bucket, auth_write, path, dataset, table, schema):
  """Move using bucket and path prefix.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       bucket (string) - Google cloud bucket.
       auth_write (authentication) - Credentials used for writing data.
       path (string) - Path prefix to read from, no * required.
       dataset (string) - Existing BigQuery dataset.
       table (string) - Table to create from this query.
       schema (json) - Schema provided in JSON list format or empty list.
  """

  bigquery(config, {
    'auth':auth_read,
    'from':{
      'bucket':bucket,
      'path':path
    },
    'to':{
      'auth':auth_write,
      'dataset':dataset,
      'table':table
    },
    'schema':schema
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move using bucket and path prefix.

      1. Specify a bucket and path prefix, * suffix is NOT required.
      2. Every time the job runs it will overwrite the table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-bucket", help="Google cloud bucket.", default='')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-path", help="Path prefix to read from, no * required.", default='')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-table", help="Table to create from this query.", default='')
  parser.add_argument("-schema", help="Schema provided in JSON list format or empty list.", default='[]')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_bigquery_storage(config, args.auth_read, args.bucket, args.auth_write, args.path, args.dataset, args.table, args.schema)
