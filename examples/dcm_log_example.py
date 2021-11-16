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
from starthinker.task.dcm_log.run import dcm_log


def recipe_dcm_log(config, auth_read, auth_write, accounts, days, recipe_slug):
  """Downloads Campaign manager logs and allows audits.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Credentials used for writing data.
       accounts (integer_list) - Comma separated CM account ids.
       days (integer) - Number of days to backfill the log, works on first run only.
       recipe_slug (string) - Google BigQuery dataset to create tables in.
  """

  dataset(config, {
    'description':'The dataset will hold log table, Create it exists.',
    'hour':[
      1
    ],
    'auth':auth_write,
    'dataset':recipe_slug
  })

  dcm_log(config, {
    'description':'Will create tables with format CM_* to hold each endpoint via a call to the API list function. Exclude reports for its own task.',
    'hour':[
      2
    ],
    'auth':auth_read,
    'accounts':{
      'single_cell':True,
      'values':accounts
    },
    'days':days,
    'out':{
      'auth':auth_write,
      'dataset':recipe_slug
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Downloads Campaign manager logs and allows audits.

      1. Wait for BigQuery->->->CM_... to be created.
      2. Wait for BigQuery->->->Barnacle_... to be created, then copy and connect the following data sources.
      3. Join the 1-StarThinker Assets Group to access the following assets
         3.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      4. Copy 1-Barnacle Profile Advertiser Map and connect.
         4.1 - Barnacle Profile Advertiser Map: https://datastudio.google.com/open/1a6K-XdPUzCYRXZp1ZcmeOUOURc9wn2Jj
      5. Copy 1-Barnacle Profile Campaign Map and connect.
         5.1 - Barnacle Profile Campaign Map: https://datastudio.google.com/open/1NEzrQWWnPjkD90iUwN-ASKbVBzoeBdoT
      6. Copy 1-Barnacle Profile Site Map and connect.
         6.1 - Barnacle Profile Site Map: https://datastudio.google.com/open/1v_GRaitwPaHHKUzfJZYNBhzotvZ-bR7Y
      7. Copy 1-Barnacle Profiles Connections and connect.
         7.1 - Barnacle Profiles Connections: https://datastudio.google.com/open/14tWlh7yiqzxKJIppMFVOw2MoMtQV_ucE
      8. Copy 1-Barnacle Report Delivery Profiles and connect.
         8.1 - Barnacle Report Delivery Profiles: https://datastudio.google.com/open/1mavjxvHSEPfJq5aW4FYgCXsBCE5rthZG
      9. Copy 1-Barnacle Roles Duplicates and connect.
         9.1 - Barnacle Roles Duplicates: https://datastudio.google.com/open/1Azk_Nul-auinf4NnDq8T9fDyiKkUWD7A
      10. Copy 1-Barnacle Roles Not Used and connect.
         10.1 - Barnacle Roles Not Used: https://datastudio.google.com/open/1ogoofpKtqkLwcW9qC_Ju_JvJdIajsjNI
      11. Copy 1-Barnacle Site Contacts Profiles and connect.
         11.1 - Barnacle Site Contacts Profiles: https://datastudio.google.com/open/1xLgZPjOPDtmPyEqYMiMbWwMI8-WTslfj
      12. If reports checked, copy 1-Barnacle Profile Report Map and connect.
         12.1 - Barnacle Profile Report Map: https://datastudio.google.com/open/1-YGDiQPDnk0gD78_QOY5XdTXRlTrLeEq
      13. Copy 1-Barnacle Report.
         13.1 - Barnacle Report: https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT
      14. When prompted choose the new data sources you just created.
      15. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-accounts", help="Comma separated CM account ids.", default=[])
  parser.add_argument("-days", help="Number of days to backfill the log, works on first run only.", default=7)
  parser.add_argument("-recipe_slug", help="Google BigQuery dataset to create tables in.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dcm_log(config, args.auth_read, args.auth_write, args.accounts, args.days, args.recipe_slug)
