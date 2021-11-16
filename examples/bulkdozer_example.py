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
from starthinker.task.traffic.run import traffic


def recipe_bulkdozer(config, recipe_timezone, account_id, dcm_profile_id, sheet_url):
  """Bulkdozer is a tool that can reduce trafficking time in Campaign Manager by up
     to 80%% by providing automated bulk editing capabilities.

     Args:
       recipe_timezone (timezone) - Timezone for report dates.
       account_id (string) - Campaign Manager Network ID (optional if profile id provided)
       dcm_profile_id (string) - Campaign Manager Profile ID (optional if account id provided)
       sheet_url (string) - Feed Sheet URL
  """

  traffic(config, {
    'hour':[
    ],
    'account_id':account_id,
    'dcm_profile_id':dcm_profile_id,
    'auth':'user',
    'sheet_url':sheet_url,
    'timezone':recipe_timezone
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Bulkdozer is a tool that can reduce trafficking time in Campaign Manager by up to 80%% by providing automated bulk editing capabilities.

      1. Open the 1-Bulkdozer feed.
         1.1 - Bulkdozer: https://docs.google.com/spreadsheets/d/1EjprWTDLWOvkV7znA0P4uciz0_E5_TNn3N3f8J4jTwA/edit?usp=sharing&resourcekey=0-jVCGjrPdnUnJ0rk7nQCFBQ
      2. Make your own copy of the feed by clicking the File -> Make a copy... menu in the feed.
      3. Give it a meaninful name including the version, your name, and team to help you identify it and ensure you are using the correct version.
      4. Under the Account ID field below, enter the your Campaign Manager Network ID.
      5. Under Sheet URL, enter the URL of your copy of the feed that you just created in the steps above.
      6. Go to the Store tab of your new feed, and enter your profile ID in the profileId field (cell B2). Your profile ID is visible in Campaign Manager by clicking your avatar on the top right corner.
      7. Click the Save button below.
      8. After clicking Save, copy this page's URL from your browser address bar, and paste it in the Store tab for the recipe_url field (cell B5) your sheet.
      9. Bulkdozer is ready for use
      10. Review the 1-Bulkdozer documentation.
         10.1 - Bulkdozer documentation: https://github.com/google/starthinker/blob/master/tutorials/Bulkdozer/Installation_and_User_guides.md
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_timezone", help="Timezone for report dates.", default='America/Chicago')
  parser.add_argument("-account_id", help="Campaign Manager Network ID (optional if profile id provided)", default=None)
  parser.add_argument("-dcm_profile_id", help="Campaign Manager Profile ID (optional if account id provided)", default=None)
  parser.add_argument("-sheet_url", help="Feed Sheet URL", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_bulkdozer(config, args.recipe_timezone, args.account_id, args.dcm_profile_id, args.sheet_url)
