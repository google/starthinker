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
from starthinker.task.sheets.run import sheets


def recipe_sheets_clear(config, auth_read, sheets_sheet, sheets_tab, sheets_range):
  """Clear data from a sheet.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       sheets_sheet (string) - NA
       sheets_tab (string) - NA
       sheets_range (string) - NA
  """

  sheets(config, {
    'auth':auth_read,
    'sheet':sheets_sheet,
    'tab':sheets_tab,
    'range':sheets_range,
    'clear':True
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Clear data from a sheet.

      1. For the sheet, provide the full edit URL.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-sheets_sheet", help="", default='')
  parser.add_argument("-sheets_tab", help="", default='')
  parser.add_argument("-sheets_range", help="", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_sheets_clear(config, args.auth_read, args.sheets_sheet, args.sheets_tab, args.sheets_range)
