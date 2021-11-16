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
from starthinker.task.hello.run import hello


def recipe_test(config):
  """Used by tests.
  """

  hello(config, {
    'auth':'user',
    'hour':[
      1
    ],
    'say':'Hello At 1',
    'sleep':0
  })

  hello(config, {
    'auth':'user',
    'hour':[
      3
    ],
    'say':'Hello At 3',
    'sleep':0
  })

  hello(config, {
    'auth':'user',
    'hour':[
    ],
    'say':'Hello Manual',
    'sleep':0
  })

  hello(config, {
    'auth':'user',
    'hour':[
      23
    ],
    'say':'Hello At 23 Sleep',
    'sleep':30
  })

  hello(config, {
    'auth':'user',
    'say':'Hello At Anytime',
    'sleep':0
  })

  hello(config, {
    'auth':'user',
    'hour':[
      1,
      3,
      23
    ],
    'say':'Hello At 1, 3, 23',
    'sleep':0
  })

  hello(config, {
    'auth':'user',
    'hour':[
      3
    ],
    'say':'Hello At 3 Reordered',
    'sleep':0
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Used by tests.

      1. This should be called by the tests scripts only.
      2. When run will generate a say hello log.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")



  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_test(config)
