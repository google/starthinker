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
from starthinker.task.archive.run import archive


def recipe_archive(config, auth_write, archive_days, archive_bucket, archive_path, archive_delete):
  """Wipe old information from a Storage bucket based on last update time.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       archive_days (integer) - NA
       archive_bucket (string) - NA
       archive_path (string) - NA
       archive_delete (boolean) - NA
  """

  archive(config, {
    'auth':auth_write,
    'days':archive_days,
    'storage':{
      'bucket':archive_bucket,
      'path':archive_path
    },
    'delete':archive_delete
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Wipe old information from a Storage bucket based on last update time.

      1. Specify how many days back to retain data and which buckets and paths to purge.
      2. Everything under a path will be moved to archive or deleted depending on your choice.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-archive_days", help="", default=7)
  parser.add_argument("-archive_bucket", help="", default='')
  parser.add_argument("-archive_path", help="", default='')
  parser.add_argument("-archive_delete", help="", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_archive(config, args.auth_write, args.archive_days, args.archive_bucket, args.archive_path, args.archive_delete)
