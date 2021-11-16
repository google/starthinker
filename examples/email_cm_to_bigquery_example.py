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


def recipe_email_cm_to_bigquery(config, auth_read, email, subject, dataset, table, is_incremental_load):
  """Pulls a CM Report from a gMail powered email account into BigQuery.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       email (string) - Email address report was sent to.
       subject (string) - Regular expression to match subject. Double escape backslashes.
       dataset (string) - Existing dataset in BigQuery.
       table (string) - Name of table to be written to.
       is_incremental_load (boolean) - Append report data to table based on date column, de-duplicates.
  """

  email(config, {
    'auth':auth_read,
    'read':{
      'from':'noreply-cm@google.com',
      'to':email,
      'subject':subject,
      'attachment':'.*'
    },
    'write':{
      'bigquery':{
        'dataset':dataset,
        'table':table,
        'header':True,
        'is_incremental_load':is_incremental_load
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Pulls a CM Report from a gMail powered email account into BigQuery.

      1. The person executing this recipe must be the recipient of the email.
      2. Schedule a CM report to be sent to .
      3. Or set up a redirect rule to forward a report you already receive.
      4. The report must be sent as an attachment.
      5. Ensure this recipe runs after the report is email daily.
      6. Give a regular expression to match the email subject.
      7. Configure the destination in BigQuery to write the data.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-email", help="Email address report was sent to.", default='')
  parser.add_argument("-subject", help="Regular expression to match subject. Double escape backslashes.", default='.*')
  parser.add_argument("-dataset", help="Existing dataset in BigQuery.", default='')
  parser.add_argument("-table", help="Name of table to be written to.", default='')
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

  recipe_email_cm_to_bigquery(config, args.auth_read, args.email, args.subject, args.dataset, args.table, args.is_incremental_load)
