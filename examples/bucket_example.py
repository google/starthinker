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
from starthinker.task.bucket.run import bucket


def recipe_bucket(config, auth_write, bucket_bucket, bucket_emails, bucket_groups):
  """Create and permission a bucket in Storage.

     Args:
       auth_write (authentication) - Credentials used for writing data.
       bucket_bucket (string) - Name of Google Cloud Bucket to create.
       bucket_emails (string_list) - Comma separated emails.
       bucket_groups (string_list) - Comma separated groups.
  """

  bucket(config, {
    'auth':auth_write,
    'bucket':bucket_bucket,
    'emails':bucket_emails,
    'groups':bucket_groups
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Create and permission a bucket in Storage.

      1. Specify the name of the bucket and who will have owner permissions.
      2. Existing buckets are preserved.
      3. Adding a permission to the list will update the permissions but removing them will not.
      4. You have to manualy remove grants.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-bucket_bucket", help="Name of Google Cloud Bucket to create.", default='')
  parser.add_argument("-bucket_emails", help="Comma separated emails.", default='')
  parser.add_argument("-bucket_groups", help="Comma separated groups.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_bucket(config, args.auth_write, args.bucket_bucket, args.bucket_emails, args.bucket_groups)
