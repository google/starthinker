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


def recipe_dbm_to_sheets(config, auth_read, report_id, report_name, sheet, tab):
  """Move existing DV360 report into a Sheets tab.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       report_id (integer) - DV360 report ID given in UI, not needed if name used.
       report_name (string) - Name of report, not needed if ID used.
       sheet (string) - Full URL to sheet being written to.
       tab (string) - Existing tab in sheet to write to.
  """

  dbm(config, {
    'auth':auth_read,
    'report':{
      'report_id':report_id,
      'name':report_name
    },
    'out':{
      'sheets':{
        'sheet':sheet,
        'tab':tab,
        'range':'A1'
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move existing DV360 report into a Sheets tab.

      1. Specify either report name or report id to move a report.
      2. The most recent valid file will be moved to the sheet.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-report_id", help="DV360 report ID given in UI, not needed if name used.", default='')
  parser.add_argument("-report_name", help="Name of report, not needed if ID used.", default='')
  parser.add_argument("-sheet", help="Full URL to sheet being written to.", default='')
  parser.add_argument("-tab", help="Existing tab in sheet to write to.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dbm_to_sheets(config, args.auth_read, args.report_id, args.report_name, args.sheet, args.tab)
