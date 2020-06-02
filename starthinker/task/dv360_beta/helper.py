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

from starthinker.util.project import project
from starthinker.util.google_api import API_DV360_Beta

"""Command line to get a DV360 Line Item lists.

This is a helper demonstrate the use of the new DV360 API.

`python helper.py --advertiser # -u $STARTHINKER_USER -c $STARTHINKER_CLIENT`
`python helper.py --advertiser 3721733 --user $STARTHINKER_USER`

Prerequisite: https://github.com/google/starthinker/blob/master/tutorials/deploy_developer.md#command-line-deploy

"""


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--advertiser', help='advertiser ID to pull', default=None)

  # initialize project
  project.from_commandline(parser=parser)
  auth = 'service' if project.args.service else 'user'

  # pull the line items
  lineitems =  API_DV360_Beta(auth, iterate=True).advertisers().lineItems().list(advertiserId=project.args.advertiser).execute()

  for lineitem in lineitems:
    print(json.dumps(lineitem, indent=2, sort_keys=True))
