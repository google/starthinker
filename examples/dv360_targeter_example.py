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
from starthinker.task.dataset.run import dataset
from starthinker.task.drive.run import drive
from starthinker.task.dv_targeter.run import dv_targeter


def recipe_dv360_targeter(config, auth_dv, auth_sheet, auth_bigquery, recipe_name, recipe_slug, command, first_and_third):
  """Allows bulk targeting DV360 through Sheets and BigQuery.

     Args:
       auth_dv (authentication) - Credentials used for dv.
       auth_sheet (authentication) - Credentials used for sheet.
       auth_bigquery (authentication) - Credentials used for bigquery.
       recipe_name (string) - Name of Google Sheet to create.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
       command (choice) - Action to take.
       first_and_third (boolean) - Load first and third party data (may be slow). If not selected, enter audience identifiers into sheet manually.
  """

  dataset(config, {
    '__comment__':'Ensure dataset exists.',
    'auth':auth_bigquery,
    'dataset':recipe_slug
  })

  drive(config, {
    '__comment__':'Copy the default template to sheet with the recipe name',
    'auth':auth_sheet,
    'copy':{
      'source':'https://docs.google.com/spreadsheets/d/1ARkIvh0D-gltZeiwniUonMNrm0Mi1s2meZ9FUjutXOE/',
      'destination':recipe_name
    }
  })

  dv_targeter(config, {
    '__comment':'Depending on users choice, execute a different part of the solution.',
    'auth_dv':auth_dv,
    'auth_sheets':auth_sheet,
    'auth_bigquery':auth_bigquery,
    'sheet':recipe_name,
    'dataset':recipe_slug,
    'command':command,
    'first_and_third':first_and_third
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Allows bulk targeting DV360 through Sheets and BigQuery.

      1. Select Load, click Save + Run, a sheet called  DV Targeter will be created.
      2. In the Partners sheet tab, fill in Filter column then select Load, click Save + Run.
      3. In the Advertisers sheet tab, fill in Filter column. then select Load, click Save + Run.
      4. Check the First And Third Party option to load audiences, which may be slow.  If not loaded, user will enter audience ids into the sheet manually.
      5. On the Line Items sheet tab, the Filter is used only to limit drop down choices in the rest of the tool.
      6. Optionally edit or filter the Targeting Options or Inventory Sources sheets to limit choices.
      7. Make targeting updates, fill in changes on all tabs with colored fields (RED FIELDS ARE NOT IMPLEMENTED, IGNORE).
      8. Select Preview, click Save + Run then check the Preview tabs.
      9. Select Update, click Save + Run then check the Success and Error tabs.
      10. Load and Update can be run multiple times.
      11. If an update fails, all parts of the update failed, break it up into multiple updates.
      12. To refresh the Partner, Advertiser, or Line Item list, remove the filters and run load.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_dv", help="Credentials used for dv.", default='user')
  parser.add_argument("-auth_sheet", help="Credentials used for sheet.", default='user')
  parser.add_argument("-auth_bigquery", help="Credentials used for bigquery.", default='service')
  parser.add_argument("-recipe_name", help="Name of Google Sheet to create.", default='')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')
  parser.add_argument("-command", help="Action to take.", default='Load')
  parser.add_argument("-first_and_third", help="Load first and third party data (may be slow). If not selected, enter audience identifiers into sheet manually.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dv360_targeter(config, args.auth_dv, args.auth_sheet, args.auth_bigquery, args.recipe_name, args.recipe_slug, args.command, args.first_and_third)
