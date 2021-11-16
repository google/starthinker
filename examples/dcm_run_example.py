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
from starthinker.task.dcm.run import dcm


def recipe_dcm_run(config, auth_read, account, report_id, report_name):
  """Trigger a CM report run

     Args:
       auth_read (authentication) - Credentials used for reading data.
       account (integer) - CM network id.
       report_id (integer) - CM report id, empty if using name.
       report_name (string) - CM report name, empty if using id instead.
  """

  dcm(config, {
    'auth':auth_read,
    'report_run_only':True,
    'report':{
      'account':account,
      'report_id':report_id,
      'name':report_name
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Trigger a CM report run

      1. Specify an account id.
      2. Specify either report name or report id to run.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-account", help="CM network id.", default='')
  parser.add_argument("-report_id", help="CM report id, empty if using name.", default='')
  parser.add_argument("-report_name", help="CM report name, empty if using id instead.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dcm_run(config, args.auth_read, args.account, args.report_id, args.report_name)
