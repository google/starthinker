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
from starthinker.task.salesforce.run import salesforce


def recipe_salesforce_to_bigquery(config, domain, client, secret, username, password, query, auth_read, dataset, table, schema):
  """Move query results into a BigQuery table.

     Args:
       domain (string) - Retrieve from a Salesforce Domain.
       client (string) - Retrieve from a Salesforce App.
       secret (string) - Retrieve from a Salesforce App.
       username (email) - Your Salesforce user email.
       password (password) - Your Salesforce login password.
       query (string) - The query to run in Salesforce.
       auth_read (authentication) - Credentials used for reading data.
       dataset (string) - Existing BigQuery dataset.
       table (string) - Table to create from this report.
       schema (json) - Schema provided in JSON list format or empty list.
  """

  salesforce(config, {
    'auth':auth_read,
    'domain':domain,
    'client':client,
    'secret':secret,
    'username':username,
    'password':password,
    'query':query,
    'out':{
      'bigquery':{
        'dataset':dataset,
        'table':table,
        'schema':schema
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move query results into a BigQuery table.

      1. Specify 1-Salesforce credentials.
         1.1 - Salesforce: https://developer.salesforce.com/
      2. Specify the query youd like to execute.
      3. Specify a 1-SCHEMA for that query (optional).
         3.1 - SCHEMA: https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-domain", help="Retrieve from a Salesforce Domain.", default='login.salesforce.com')
  parser.add_argument("-client", help="Retrieve from a Salesforce App.", default='')
  parser.add_argument("-secret", help="Retrieve from a Salesforce App.", default='')
  parser.add_argument("-username", help="Your Salesforce user email.", default='')
  parser.add_argument("-password", help="Your Salesforce login password.", default='')
  parser.add_argument("-query", help="The query to run in Salesforce.", default='')
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-table", help="Table to create from this report.", default='')
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

  recipe_salesforce_to_bigquery(config, args.domain, args.client, args.secret, args.username, args.password, args.query, args.auth_read, args.dataset, args.table, args.schema)
