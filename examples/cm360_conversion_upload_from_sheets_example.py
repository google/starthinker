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
from starthinker.task.conversion_upload.run import conversion_upload


def recipe_cm360_conversion_upload_from_sheets(config, dcm_account, auth_cm, floodlight_activity_id, auth_sheets, floodlight_conversion_type, encryption_entity_id, encryption_entity_type, encryption_entity_source, sheet, tab, range):
  """Move form Sheets to CM.

     Args:
       dcm_account (string) - NA
       auth_cm (authentication) - Credentials used for CM.
       floodlight_activity_id (integer) - NA
       auth_sheets (authentication) - Credentials to read sheet.
       floodlight_conversion_type (choice) - Must match the values specifed in the last column.
       encryption_entity_id (integer) - Typically the same as the account id.
       encryption_entity_type (choice) - NA
       encryption_entity_source (choice) - Where the ids are originating from.
       sheet (string) - NA
       tab (string) - Name of tab within sheet.
       range (string) - A1 Notation, for example A1:E
  """

  conversion_upload(config, {
    'auth':auth_cm,
    'account_id':dcm_account,
    'activity_id':floodlight_activity_id,
    'conversion_type':floodlight_conversion_type,
    'encryptionInfo':{
      'encryptionEntityId':encryption_entity_id,
      'encryptionEntityType':encryption_entity_type,
      'encryptionSource':encryption_entity_source
    },
    'from':{
      'sheets':{
        'auth':auth_sheets,
        'sheet':sheet,
        'tab':tab,
        'range':range
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move form Sheets to CM.

      1. Specify a CM Account ID, Floodligh Activity ID and Conversion Type.
      2. Include Sheets url, tab, and range, omit headers in range.
      3. Columns: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId | matchId | dclid
      4. Include encryption information if using encryptedUserId or encryptedUserIdCandidates.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-dcm_account", help="", default='')
  parser.add_argument("-auth_cm", help="Credentials used for CM.", default='user')
  parser.add_argument("-floodlight_activity_id", help="", default='')
  parser.add_argument("-auth_sheets", help="Credentials to read sheet.", default='user')
  parser.add_argument("-floodlight_conversion_type", help="Must match the values specifed in the last column.", default='encryptedUserId')
  parser.add_argument("-encryption_entity_id", help="Typically the same as the account id.", default='')
  parser.add_argument("-encryption_entity_type", help="", default='DCM_ACCOUNT')
  parser.add_argument("-encryption_entity_source", help="Where the ids are originating from.", default='DATA_TRANSFER')
  parser.add_argument("-sheet", help="", default='Name or URL of sheet.')
  parser.add_argument("-tab", help="Name of tab within sheet.", default='Conversions')
  parser.add_argument("-range", help="A1 Notation, for example A1:E", default='A1:E')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm360_conversion_upload_from_sheets(config, args.dcm_account, args.auth_cm, args.floodlight_activity_id, args.auth_sheets, args.floodlight_conversion_type, args.encryption_entity_id, args.encryption_entity_type, args.encryption_entity_source, args.sheet, args.tab, args.range)
