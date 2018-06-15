###########################################################################
# 
#  Copyright 2018 Google Inc.
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


"""Command line to get a DCM report or show list of report or files.

This is a helper to help developers debug and create reports.

To get list: python dcm/helper.py --account [id] --profile [id] --list -u [credentials]
To get report: python dcm/helper.py --account [id] --profile [id] --report [id] -u [credentials]
To get files: python dcm/helper.py --account [id] --profile [id] --report [id] --list -u [credentials]

"""

import argparse
import pprint

from util.project import project
from util.google_api import API_DCM


if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--account', help='account ID to use to pull the report.', default=None)
  parser.add_argument('--profile', help='profile ID to use to pull the report.', default=None)
  parser.add_argument('--report', help='report ID to pull the achema.', default=None)
  parser.add_argument('--list', help='list reports or files.', action='store_true')

  # initialize project
  project.load(parser=parser)
  auth = 'service' if project.args.service else 'user'

  kwargs = {}
  if project.args.account: kwargs['accountId'] = project.args.account
  if project.args.profile: kwargs['profileId'] = project.args.profile

  # get report
  if project.args.report:
    kwargs['reportId'] = project.args.report
    if project.args.list:
      for report_file in API_DCM(auth).reports().files().list(**kwargs).execute():
        pprint.PrettyPrinter().pprint(report_file)
    else:
      report = API_DCM(auth).reports().get(**kwargs).execute()
      pprint.PrettyPrinter().pprint(report)
  else:
    for report in API_DCM(auth).reports().list(**kwargs).execute():
      pprint.PrettyPrinter().pprint(report)
