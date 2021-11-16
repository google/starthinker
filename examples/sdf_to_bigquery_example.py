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
from starthinker.task.sdf.run import sdf


def recipe_sdf_to_bigquery(config, auth_write, partner_id, file_types, filter_type, filter_ids, dataset, version, table_suffix, time_partitioned_table, create_single_day_table):
  """Download SDF reports into a BigQuery table.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       partner_id (integer) - The sdf file types.
       file_types (string_list) - The sdf file types.
       filter_type (choice) - The filter type for the filter ids.
       filter_ids (integer_list) - Comma separated list of filter ids for the request.
       dataset (string) - Dataset to be written to in BigQuery.
       version (choice) - The sdf version to be returned.
       table_suffix (string) - Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)
       time_partitioned_table (boolean) - Is the end table a time partitioned
       create_single_day_table (boolean) - Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.
  """

  dataset(config, {
    'auth':auth_write,
    'dataset':dataset
  })

  sdf(config, {
    'auth':'user',
    'version':version,
    'partner_id':partner_id,
    'file_types':file_types,
    'filter_type':filter_type,
    'read':{
      'filter_ids':{
        'single_cell':True,
        'values':filter_ids
      }
    },
    'time_partitioned_table':time_partitioned_table,
    'create_single_day_table':create_single_day_table,
    'dataset':dataset,
    'table_suffix':table_suffix
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Download SDF reports into a BigQuery table.

      1. Select your filter types and the filter ideas.
      2. Enter the 1-file types using commas.
         2.1 - file types: https://developers.google.com/bid-manager/v1.1/sdf/download
      3. SDF_ will be prefixed to all tables and date appended to daily tables.
      4. File types take the following format: FILE_TYPE_CAMPAIGN, FILE_TYPE_AD_GROUP,...
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-partner_id", help="The sdf file types.", default=None)
  parser.add_argument("-file_types", help="The sdf file types.", default=[])
  parser.add_argument("-filter_type", help="The filter type for the filter ids.", default='')
  parser.add_argument("-filter_ids", help="Comma separated list of filter ids for the request.", default=[])
  parser.add_argument("-dataset", help="Dataset to be written to in BigQuery.", default='')
  parser.add_argument("-version", help="The sdf version to be returned.", default='5')
  parser.add_argument("-table_suffix", help="Optional: Suffix string to put at the end of the table name (Must contain alphanumeric or underscores)", default='')
  parser.add_argument("-time_partitioned_table", help="Is the end table a time partitioned", default=False)
  parser.add_argument("-create_single_day_table", help="Would you like a separate table for each day? This will result in an extra table each day and the end table with the most up to date SDF.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_sdf_to_bigquery(config, args.auth_write, args.partner_id, args.file_types, args.filter_type, args.filter_ids, args.dataset, args.version, args.table_suffix, args.time_partitioned_table, args.create_single_day_table)
