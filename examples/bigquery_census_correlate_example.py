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


def recipe_bigquery_census_correlate(config, auth, join, pass, sum, correlate, from_dataset, from_table, significance, to_dataset, type):
  """Correlate another table with US Census data.  Expands a data set dimensions by
     finding population segments that correlate with the master table.

     Args:
       auth (authentication) - Credentials used for writing data.
       join (string) - Name of column to join on, must match Census Geo_Id column.
       pass (string_list) - Comma seperated list of columns to pass through.
       sum (string_list) - Comma seperated list of columns to sum, optional.
       correlate (string_list) - Comma seperated list of percentage columns to correlate.
       from_dataset (string) - Existing BigQuery dataset.
       from_table (string) - Table to use as join data.
       significance (choice) - Select level of significance to test.
       to_dataset (string) - Existing BigQuery dataset.
       type (choice) - Write Census_Percent as table or view.
  """

  census(config, {
    'auth':auth,
    'correlate':{
      'join':join,
      'pass':pass,
      'sum':sum,
      'correlate':correlate,
      'dataset':from_dataset,
      'table':from_table,
      'significance':significance
    },
    'to':{
      'dataset':to_dataset,
      'type':type
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Correlate another table with US Census data.  Expands a data set dimensions by finding population segments that correlate with the master table.

      1. Pre-requisite is Census Normalize, run that at least once.
      2. Specify JOIN, PASS, SUM, and CORRELATE columns to build the correlation query.
      3. Define the DATASET and TABLE for the joinable source. Can be a view.
      4. Choose the significance level.  More significance usually means more NULL results, balance quantity and quality using this value.
      5. Specify where to write the results.
      6. IMPORTANT:** If you use VIEWS, you will have to delete them manually if the recipe changes.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth", help="Credentials used for writing data.", default='service')
  parser.add_argument("-join", help="Name of column to join on, must match Census Geo_Id column.", default='')
  parser.add_argument("-pass", help="Comma seperated list of columns to pass through.", default=[])
  parser.add_argument("-sum", help="Comma seperated list of columns to sum, optional.", default=[])
  parser.add_argument("-correlate", help="Comma seperated list of percentage columns to correlate.", default=[])
  parser.add_argument("-from_dataset", help="Existing BigQuery dataset.", default='')
  parser.add_argument("-from_table", help="Table to use as join data.", default='')
  parser.add_argument("-significance", help="Select level of significance to test.", default='80')
  parser.add_argument("-to_dataset", help="Existing BigQuery dataset.", default='')
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

  recipe_bigquery_census_correlate(config, args.auth, args.join, args.pass, args.sum, args.correlate, args.from_dataset, args.from_table, args.significance, args.to_dataset, args.type)
