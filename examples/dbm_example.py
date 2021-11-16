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


def recipe_dbm(config, auth_read, report, delete):
  """Create a DV360 report.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       report (json) - Report body and filters.
       delete (boolean) - If report exists, delete it before creating a new one.
  """

  dbm(config, {
    'auth':auth_read,
    'report':report,
    'delete':delete
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Create a DV360 report.

      1. Reference field values from the 1-DV360 API to build a report.
         1.1 - DV360 API: https://developers.google.com/bid-manager/v1/reports
      2. Copy and paste the JSON definition of a report, 1-sample for reference.
         2.1 - sample for reference: https://github.com/google/starthinker/blob/master/tests/dbm_to_bigquery.json
      3. The report is only created, a seperate script is required to move the data.
      4. To reset a report, delete it from DV360 reporting.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-report", help="Report body and filters.", default='{}')
  parser.add_argument("-delete", help="If report exists, delete it before creating a new one.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dbm(config, args.auth_read, args.report, args.delete)
