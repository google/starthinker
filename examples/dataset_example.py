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


def recipe_dataset(config, auth_write, dataset_dataset, dataset_emails, dataset_groups):
  """Create and permission a dataset in BigQuery.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       dataset_dataset (string) - Name of Google BigQuery dataset to create.
       dataset_emails (string_list) - Comma separated emails.
       dataset_groups (string_list) - Comma separated groups.
  """

  dataset(config, {
    'auth':auth_write,
    'dataset':dataset_dataset,
    'emails':dataset_emails,
    'groups':dataset_groups
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Create and permission a dataset in BigQuery.

      1. Specify the name of the dataset.
      2. If dataset exists, it is inchanged.
      3. Add emails and / or groups to add read permission.
      4. CAUTION: Removing permissions in StarThinker has no effect.
      5. CAUTION: To remove permissions you have to edit the dataset.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-dataset_dataset", help="Name of Google BigQuery dataset to create.", default='')
  parser.add_argument("-dataset_emails", help="Comma separated emails.", default=[])
  parser.add_argument("-dataset_groups", help="Comma separated groups.", default=[])


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dataset(config, args.auth_write, args.dataset_dataset, args.dataset_emails, args.dataset_groups)
