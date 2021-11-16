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
from starthinker.task.twitter.run import twitter


def recipe_trends_places_to_sheets_via_value(config, auth_write, secret, key, places_dataset, places_query, places_legacy, destination_sheet, destination_tab):
  """Move using hard coded WOEID values.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       secret (string) - NA
       key (string) - NA
       places_dataset (string) - NA
       places_query (string) - NA
       places_legacy (boolean) - NA
       destination_sheet (string) - NA
       destination_tab (string) - NA
  """

  twitter(config, {
    'auth':auth_write,
    'secret':secret,
    'key':key,
    'trends':{
      'places':{
        'single_cell':True,
        'bigquery':{
          'dataset':places_dataset,
          'query':places_query,
          'legacy':places_legacy
        }
      }
    },
    'out':{
      'sheets':{
        'sheet':destination_sheet,
        'tab':destination_tab,
        'range':'A1'
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move using hard coded WOEID values.

      1. Provide 1-Twitter Credentials.
         1.1 - Twitter Credentials: https://apps.twitter.com
      2. Provide a comma delimited list of WOEIDs.
      3. Specify Sheet url and tab to write API call results to.
      4. Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
      5. Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-secret", help="", default='')
  parser.add_argument("-key", help="", default='')
  parser.add_argument("-places_dataset", help="", default='')
  parser.add_argument("-places_query", help="", default='')
  parser.add_argument("-places_legacy", help="", default=False)
  parser.add_argument("-destination_sheet", help="", default='')
  parser.add_argument("-destination_tab", help="", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_trends_places_to_sheets_via_value(config, args.auth_write, args.secret, args.key, args.places_dataset, args.places_query, args.places_legacy, args.destination_sheet, args.destination_tab)
