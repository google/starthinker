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
from starthinker.task.fred.run import fred


def recipe_fred_series_to_bigquery(config, auth, fred_api_key, fred_series_id, fred_units, fred_frequency, fred_aggregation_method, project, dataset):
  """Download federal reserve series.

     Args:
       auth (authentication) - Credentials used for writing data.
       fred_api_key (string) - 32 character alpha-numeric lowercase string.
       fred_series_id (string) - Series ID to pull data from.
       fred_units (choice) - A key that indicates a data value transformation.
       fred_frequency (choice) - An optional parameter that indicates a lower frequency to aggregate values to.
       fred_aggregation_method (choice) - A key that indicates the aggregation method used for frequency aggregation.
       project (string) - Existing BigQuery project.
       dataset (string) - Existing BigQuery dataset.
  """

  fred(config, {
    'auth':auth,
    'api_key':fred_api_key,
    'frequency':fred_frequency,
    'series':[
      {
        'series_id':fred_series_id,
        'units':fred_units,
        'aggregation_method':fred_aggregation_method
      }
    ],
    'out':{
      'bigquery':{
        'project':project,
        'dataset':dataset
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Download federal reserve series.

      1. Specify the values for a 1-Fred observations API call.
         1.1 - Fred observations API call: https://fred.stlouisfed.org/docs/api/fred/series_observations.html
      2. A table will appear in the dataset.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth", help="Credentials used for writing data.", default='service')
  parser.add_argument("-fred_api_key", help="32 character alpha-numeric lowercase string.", default='')
  parser.add_argument("-fred_series_id", help="Series ID to pull data from.", default='')
  parser.add_argument("-fred_units", help="A key that indicates a data value transformation.", default='lin')
  parser.add_argument("-fred_frequency", help="An optional parameter that indicates a lower frequency to aggregate values to.", default='')
  parser.add_argument("-fred_aggregation_method", help="A key that indicates the aggregation method used for frequency aggregation.", default='avg')
  parser.add_argument("-project", help="Existing BigQuery project.", default='')
  parser.add_argument("-dataset", help="Existing BigQuery dataset.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_fred_series_to_bigquery(config, args.auth, args.fred_api_key, args.fred_series_id, args.fred_units, args.fred_frequency, args.fred_aggregation_method, args.project, args.dataset)
