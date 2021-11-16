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
from starthinker.task.drive.run import drive


def recipe_cm_campaign_audit(config, recipe_name):
  """A tool for rapidly bulk checking Campaign Manager campaigns

     Args:
       recipe_name (string) - Name of document to deploy to.
  """

  drive(config, {
    'auth':'user',
    'hour':[
    ],
    'copy':{
      'source':'https://docs.google.com/spreadsheets/d/1tt597dMsAaxYXaJdifwKYNVzJrIl6E9Pe8GysfVrWOs/',
      'destination':recipe_name
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      A tool for rapidly bulk checking Campaign Manager campaigns

      1. See all 1-Bulkdozer Lite related tools and instructions.
         1.1 - Bulkdozer Lite: https://github.com/google/bulkdozer-lite#installation
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_name", help="Name of document to deploy to.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm_campaign_audit(config, args.recipe_name)
