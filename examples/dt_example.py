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
from starthinker.task.dt.run import dt


def recipe_dt(config, auth_read, auth_write, bucket, paths, days, hours, dataset):
  """Move data from a DT bucket into a BigQuery table.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Credentials used for writing data.
       bucket (string) - Name of bucket where DT files are stored.
       paths (string_list) - List of prefixes to pull specific DT files.
       days (integer) - Number of days back to synchronize.
       hours (integer) - Number of hours back to synchronize.
       dataset (string) - Existing dataset in BigQuery.
  """

  dt(config, {
    'auth':auth_read,
    'from':{
      'bucket':bucket,
      'paths':paths,
      'days':days,
      'hours':hours
    },
    'to':{
      'auth':auth_write,
      'dataset':dataset
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Move data from a DT bucket into a BigQuery table.

      1. Ensure your user has 1-access to the bucket.
         1.1 - access to the bucket: https://developers.google.com/doubleclick-advertisers/dtv2/getting-started
      2. Provide the DT bucket name to read from.
      3. Provide the path of the files to read.
      4. Each file is synchronized to a unique table.  Use a view or aggregate select.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-bucket", help="Name of bucket where DT files are stored.", default='')
  parser.add_argument("-paths", help="List of prefixes to pull specific DT files.", default=[])
  parser.add_argument("-days", help="Number of days back to synchronize.", default=2)
  parser.add_argument("-hours", help="Number of hours back to synchronize.", default=0)
  parser.add_argument("-dataset", help="Existing dataset in BigQuery.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dt(config, args.auth_read, args.auth_write, args.bucket, args.paths, args.days, args.hours, args.dataset)
