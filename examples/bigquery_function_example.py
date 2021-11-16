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
from starthinker.task.bigquery.run import bigquery


def recipe_bigquery_function(config, auth, function, dataset):
  """Add a custom function or table to a dataset.

     Args:
       auth (authentication) - Credentials used for writing function.
       function (choice) - Function or table to create.
       dataset (string) - Existing BigQuery dataset.
  """

  bigquery(config, {
    'auth':auth,
    'function':function,
    'to':{
      'dataset':dataset
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Add a custom function or table to a dataset.

      1. Specify the dataset, and the function or table will be added.
      2. Pearson Significance Test: Check if a correlation is significant.
      3. RGB To HSV: Convert color values for analysis.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth", help="Credentials used for writing function.", default='service')
  parser.add_argument("-function", help="Function or table to create.", default='Pearson Significance Test')
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

  recipe_bigquery_function(config, args.auth, args.function, args.dataset)
