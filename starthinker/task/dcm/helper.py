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

This is a helper to help developers debug and create reports. Prints using JSON for
copy and paste compatibility. The following command lines are available:

- To get list of reports: `python dcm/helper.py --account [id] --list -u [credentials]`
- To get report: `python dcm/helper.py --account [id] --report [id] -u [credentials]`
- To get report files: `python dcm/helper.py --account [id] --files [id] -u [credentials]`
- To get report sample: `python dcm/helper.py --account [id] --sample [id] -u [credentials]`
- To get report schema: `python dcm/helper.py --account [id] --schema [id] -u [credentials]`

"""

import json
import argparse

from starthinker.util.project import project
from starthinker.util.google_api import API_DCM
from starthinker.util.dcm import get_profile_for_api, report_to_rows, report_clean, report_file, report_schema
from starthinker.util.csv import rows_to_type, rows_print

if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--account', help='account ID to use to pull the report', default=None)
  parser.add_argument('--report', help='report ID to pull JSON definition', default=None)
  parser.add_argument('--schema', help='report ID to pull achema definition', default=None)
  parser.add_argument('--sample', help='report ID to pull sample data', default=None)
  parser.add_argument('--files', help='report ID to pull file list', default=None)
  parser.add_argument('--list', help='list reports', action='store_true')

  # initialize project
  project.from_commandline(parser=parser)
  auth = 'service' if project.args.service else 'user'

  is_superuser, profile = get_profile_for_api(auth, project.args.account)
  kwargs = { 'profileId':profile, 'accountId':project.args.account } if is_superuser else { 'profileId':profile }

  # get report list
  if project.args.report:
    kwargs['reportId'] = project.args.report
    report = API_DCM(auth, internal=is_superuser).reports().get(**kwargs).execute()
    print(json.dumps(report, indent=2, sort_keys=True))

  # get report files
  elif project.args.files:
    kwargs['reportId'] = project.args.files
    for report_file in API_DCM(auth, internal=is_superuser).reports().files().list(**kwargs).execute():
      print(json.dumps(report_file, indent=2, sort_keys=True))

  # get schema
  elif project.args.schema:
    filename, report = report_file(auth, project.args.account, project.args.schema, None, 10)
    rows = report_to_rows(report)
    rows = report_clean(rows)
    print(json.dumps(report_schema(next(rows)), indent=2, sort_keys=True))

  # get sample
  elif project.args.sample:
    filename, report = report_file(auth, project.args.account, project.args.sample, None, 10)
    rows = report_to_rows(report)
    rows = report_clean(rows)
    rows = rows_to_type(rows)
    for r in rows_print(rows, row_min=0, row_max=20): pass

  # get list
  else:
    for report in API_DCM(auth, internal=is_superuser).reports().list(**kwargs).execute():
      print(json.dumps(report, indent=2, sort_keys=True))
