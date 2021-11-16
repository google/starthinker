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
from starthinker.task.census.run import census


def recipe_bigquery_census_normalize(config, auth, census_geography, census_year, census_span, dataset, type):
  """Convert given census table to percent of population, normalizing it.

     Args:
       auth (authentication) - Credentials used for writing data.
       census_geography (choice) - Census table to get data from.
       census_year (choice) - Census table to get data from.
       census_span (choice) - Census table to get data from.
       dataset (string) - Existing BigQuery dataset.
       type (choice) - Write Census_Percent as table or view.
  """

  census(config, {
    'auth':auth,
    'normalize':{
      'census_geography':census_geography,
      'census_year':census_year,
      'census_span':census_span
    },
    'to':{
      'dataset':dataset,
      'type':type
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Convert given census table to percent of population, normalizing it.

      1. Specify the geography, year, and span that make up the 1-census table names.
         1.1 - census table names: https://pantheon.corp.google.com/bigquery?redirect_from_classic=true&p=bigquery-public-data&d=census_bureau_acs&page=dataset
      2. Not every combination of geography, year, and span exists or contains all the required fields.
      3. Every time the query runs it will overwrite the table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth", help="Credentials used for writing data.", default='service')
  parser.add_argument("-census_geography", help="Census table to get data from.", default='zip_codes')
  parser.add_argument("-census_year", help="Census table to get data from.", default='2018')
  parser.add_argument("-census_span", help="Census table to get data from.", default='5yr')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-type", help="Write Census_Percent as table or view.", default='table')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_bigquery_census_normalize(config, args.auth, args.census_geography, args.census_year, args.census_span, args.dataset, args.type)
