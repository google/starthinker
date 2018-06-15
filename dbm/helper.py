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


"""Command line to get a DBM report or show list of reports.

This is a helper to help developers debug and create reports.

To get list: python dbm/helper.py --list -u [credentials]
To get report: python dbm/helper.py --report [id] -u [credentials]

"""


import argparse
import pprint

from util.project import project
from util.google_api import API_DBM


if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--report', help='report ID to pull the achema.', default=None)
  parser.add_argument('--list', help='list reports or files.', action='store_true')

  # initialize project
  project.load(parser=parser)
  auth = 'service' if project.args.service else 'user'

  # get report
  if project.args.report:
    report = API_DBM(auth).queries().getquery(queryId=project.args.report).execute()
    pprint.PrettyPrinter().pprint(report)
  else:
    for report in API_DBM(auth, iterate=True).queries().listqueries().execute():
      pprint.PrettyPrinter().pprint(report)
