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

from starthinker.util.project import project
from starthinker.util.google_api import API_DV360_Beta


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Command line utility to download and print line items from the DV360 Beta API.

      Example: python helper.py --advertiser 3721733 --user user.json
               python helper.py --advertiser 3721733 --service service.json
  """))

  # lineitem list requires an advertiser id
  parser.add_argument(
      '--advertiser', help='Advertiser ID to pull line items from.')

  # initialize project
  project.from_commandline(parser=parser, arguments=('-u', '-c', '-s', '-v'))

  # determine auth based on parameters
  auth = 'service' if project.args.service else 'user'

  # pull the line items
  lineitems = API_DV360_Beta(
      auth, iterate=True).advertisers().lineItems().list(
          advertiserId=project.args.advertiser).execute()

  # print line items
  for lineitem in lineitems:
    print(json.dumps(lineitem, indent=2, sort_keys=True))


if __name__ == '__main__':
  main()
