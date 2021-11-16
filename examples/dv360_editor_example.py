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
from starthinker.task.dv_editor.run import dv_editor


def recipe_dv360_editor(config, auth_dv, auth_sheet, auth_bigquery, recipe_name, recipe_slug, command):
  """Allows bulk editing DV360 through Sheets and BigQuery.

     Args:
       auth_dv (authentication) - Credentials used for dv.
       auth_sheet (authentication) - Credentials used for sheet.
       auth_bigquery (authentication) - Credentials used for bigquery.
       recipe_name (string) - Name of Google Sheet to create.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
       command (choice) - Action to take.
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
      'source':'https://docs.google.com/spreadsheets/d/18G6cGo4j5SsY08H8P53R22D_Pm6m-zkE6APd3EDLf2c/',
      'destination':recipe_name
    }
  })

  dv_editor(config, {
    '__comment':'Depending on users choice, execute a different part of the solution.',
    'auth_dv':auth_dv,
    'auth_sheets':auth_sheet,
    'auth_bigquery':auth_bigquery,
    'sheet':recipe_name,
    'dataset':recipe_slug,
    'command':command
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Allows bulk editing DV360 through Sheets and BigQuery.

      1. Select Load Partners, then click Save + Run, then a sheet called DV Editor  will be created.
      2. In the Partners sheet tab, fill in Filter column then select Load Advertisers, click Save + Run.
      3. In the Advertisers sheet tab, fill in Filter column then select Load Campaigns, click Save + Run.
      4. In the Campaigns sheet tab, fill in Filter column, optional.
      5. Then select Load Insertion Orders And Line Items, click Save + Run.
      6. To update values, make changes on all Edit columns.
      7. Select Preview, then Save + Run.
      8. Check the Audit and Preview tabs to verify commit.
      9. To commit changes, select Update, then Save + Run.
      10. Check the Success and Error tabs.
      11. Update can be run multiple times.
      12. Update ONLY changes fields that do not match their original value.
      13. Insert operates only on Edit columns, ignores orignal value columns.
      14. Carefull when using drag to copy rows, values are incremented automatically.
      15. Modify audit logic by visting BigQuery and changing the views.
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
  parser.add_argument("-command", help="Action to take.", default='Load Partners')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dv360_editor(config, args.auth_dv, args.auth_sheet, args.auth_bigquery, args.recipe_name, args.recipe_slug, args.command)
