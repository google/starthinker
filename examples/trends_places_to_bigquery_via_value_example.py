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


def recipe_trends_places_to_bigquery_via_value(config, auth_write, secret, key, woeids, destination_dataset, destination_table):
  """Move using hard coded WOEID values.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       secret (string) - NA
       key (string) - NA
       woeids (integer_list) - NA
       destination_dataset (string) - NA
       destination_table (string) - NA
  """

  twitter(config, {
    'auth':auth_write,
    'secret':secret,
    'key':key,
    'trends':{
      'places':{
        'single_cell':True,
        'values':woeids
      }
    },
    'out':{
      'bigquery':{
        'dataset':destination_dataset,
        'table':destination_table
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
      3. Specify BigQuery dataset and table to write API call results to.
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
  parser.add_argument("-woeids", help="", default=[])
  parser.add_argument("-destination_dataset", help="", default='')
  parser.add_argument("-destination_table", help="", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_trends_places_to_bigquery_via_value(config, args.auth_write, args.secret, args.key, args.woeids, args.destination_dataset, args.destination_table)
