###########################################################################
#
#  Copyright 2020 Google LLC
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

import json
import argparse
import textwrap

from starthinker.util.auth import get_profile
from starthinker.util.configuration import commandline_parser, Configuration


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Creates USER credentials from Google Cloud Project CLIENT Credentials and displays profile information if it worked.
      CLIENT credentials are required to run this script, to obtain the JSON file...

        Step 1: Configure Authentication Consent Screen ( do only once )
        ----------------------------------------
          A. Visit: https://console.developers.google.com/apis/credentials/consent
          B. Choose Internal if you have GSuite, otherwise choose External.
          C. For Application Name enter: StarThinker
          D. All other fields are optional, click Save.

        Step 2: Create CLIENT Credentials ( do only once )
        ----------------------------------------
          A. Visit: https://console.developers.google.com/apis/credentials/oauthclient
          B. Choose Desktop.
          C. For Name enter: StarThinker.
          D. Click Create and ignore the confirmation pop-up.

        Step 3: Download CLIENT Credentials File ( do only once )"
        ----------------------------------------"
          A. Visit: https://console.developers.google.com/apis/credentials"
          B. Find your newly created key under OAuth 2.0 Client IDs and click download arrow on the right."
          C. The downloaded file is the CLIENT credentials, use its path for the --client -c parameter.

        Step 4: Generate USER Credentials File ( do only once )"
        ----------------------------------------"
          A. Run this command with parameters -c [CLIENT file path] and -u [USER file path].
          B. The USER file will be created and can be used to access Google APIs.
          C. The user profile will be printed to the screen.

        Example: python helper.py -c [CLIENT file path] -u [USER file path]
"""))

  # initialize project
  parser = commandline_parser(parser, arguments=('-c', '-u'))
  args = parser.parse_args()
  config = Configuration(
    user=args.user,
    client=args.client
  )

  # get profile to verify everything worked
  print('Profile:', json.dumps(get_profile(config), indent=2, sort_keys=True))


if __name__ == '__main__':
  main()
