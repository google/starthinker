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


def recipe_fred_regional_to_bigquery(config, auth, fred_api_key, fred_series_group, fred_region_type, fred_units, fred_frequency, fred_season, fred_aggregation_method, project, dataset):
  """Download federal reserve region.

     Args:
       auth (authentication) - Credentials used for writing data.
       fred_api_key (string) - 32 character alpha-numeric lowercase string.
       fred_series_group (string) - The ID for a group of seriess found in GeoFRED.
       fred_region_type (choice) - The region you want want to pull data for.
       fred_units (choice) - A key that indicates a data value transformation.
       fred_frequency (choice) - An optional parameter that indicates a lower frequency to aggregate values to.
       fred_season (choice) - The seasonality of the series group.
       fred_aggregation_method (choice) - A key that indicates the aggregation method used for frequency aggregation.
       project (string) - Existing BigQuery project.
       dataset (string) - Existing BigQuery dataset.
  """

  fred(config, {
    'auth':auth,
    'api_key':fred_api_key,
    'frequency':fred_frequency,
    'region_type':fred_region_type,
    'regions':[
      {
        'series_group':fred_series_group,
        'units':fred_units,
        'season':fred_season,
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
      Download federal reserve region.

      1. Specify the values for a 1-Fred observations API call.
         1.1 - Fred observations API call: https://research.stlouisfed.org/docs/api/geofred/regional_data.html
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
  parser.add_argument("-fred_series_group", help="The ID for a group of seriess found in GeoFRED.", default='')
  parser.add_argument("-fred_region_type", help="The region you want want to pull data for.", default='county')
  parser.add_argument("-fred_units", help="A key that indicates a data value transformation.", default='lin')
  parser.add_argument("-fred_frequency", help="An optional parameter that indicates a lower frequency to aggregate values to.", default='')
  parser.add_argument("-fred_season", help="The seasonality of the series group.", default='SA')
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

  recipe_fred_regional_to_bigquery(config, args.auth, args.fred_api_key, args.fred_series_group, args.fred_region_type, args.fred_units, args.fred_frequency, args.fred_season, args.fred_aggregation_method, args.project, args.dataset)
