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
from starthinker.task.floodlight_monitor.run import floodlight_monitor


def recipe_floodlight_monitor(config, auth_read, dcm_account, sheet):
  """Monitor floodlight impressions specified in sheet and send email alerts.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       dcm_account (string) - Specify an account_id as a number.
       sheet (string) - Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.
  """

  floodlight_monitor(config, {
    'auth':auth_read,
    'account':dcm_account,
    'template':{
      'template':{
        'sheet':'https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing',
        'tab':'Floodlight Monitor',
        'range':'A1'
      }
    },
    'sheet':{
      'sheet':sheet,
      'tab':'Floodlight Monitor',
      'range':'A2:B'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Monitor floodlight impressions specified in sheet and send email alerts.

      1. Specify an account_id or account_id:subaccount_id.
      2. Will copy 1-Floodlight Monitor Sheet to the sheet you specify.
         2.1 - Floodlight Monitor Sheet: https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/
      3. Follow instructions on sheet.
      4. Emails are sent once a day.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-dcm_account", help="Specify an account_id as a number.", default='')
  parser.add_argument("-sheet", help="Full Name or URL to Google Sheet, Floodlight Monitor tab will be added.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_floodlight_monitor(config, args.auth_read, args.dcm_account, args.sheet)
