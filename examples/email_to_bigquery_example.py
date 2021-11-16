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
from starthinker.task.email.run import email


def recipe_email_to_bigquery(config, auth_read, email_from, email_to, subject, link, attachment, dataset, table, schema, header, is_incremental_load):
  """Import emailed CM report, Dv360 report, csv, or excel into a BigQuery table.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       email_from (string) - Must match from field.
       email_to (string) - Must match to field.
       subject (string) - Regular expression to match subject.
       link (string) - Regular expression to match email.
       attachment (string) - Regular expression to match atttachment.
       dataset (string) - Existing dataset in BigQuery.
       table (string) - Name of table to be written to.
       schema (json) - Schema provided in JSON list format or empty list.
       header (boolean) - Does the csv contain a header row.
       is_incremental_load (boolean) - Append report data to table based on date column, de-duplicates.
  """

  email(config, {
    'auth':auth_read,
    'read':{
      'from':email_from,
      'to':email_to,
      'subject':subject,
      'link':link,
      'attachment':attachment
    },
    'write':{
      'bigquery':{
        'dataset':dataset,
        'table':table,
        'schema':schema,
        'header':header,
        'is_incremental_load':is_incremental_load
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Import emailed CM report, Dv360 report, csv, or excel into a BigQuery table.

      1. The person executing this recipe must be the recipient of the email.
      2. Give a regular expression to match the email subject, link or attachment.
      3. The data downloaded will overwrite the table specified.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-email_from", help="Must match from field.", default='')
  parser.add_argument("-email_to", help="Must match to field.", default='')
  parser.add_argument("-subject", help="Regular expression to match subject.", default='')
  parser.add_argument("-link", help="Regular expression to match email.", default='')
  parser.add_argument("-attachment", help="Regular expression to match atttachment.", default='')
  parser.add_argument("-dataset", help="Existing dataset in BigQuery.", default='')
  parser.add_argument("-table", help="Name of table to be written to.", default='')
  parser.add_argument("-schema", help="Schema provided in JSON list format or empty list.", default='[]')
  parser.add_argument("-header", help="Does the csv contain a header row.", default=False)
  parser.add_argument("-is_incremental_load", help="Append report data to table based on date column, de-duplicates.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_email_to_bigquery(config, args.auth_read, args.email_from, args.email_to, args.subject, args.link, args.attachment, args.dataset, args.table, args.schema, args.header, args.is_incremental_load)
