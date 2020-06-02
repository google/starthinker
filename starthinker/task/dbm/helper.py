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

This is a helper to help developers debug and create reports. The following
calls are valid:

- To get list of reports: `python dbm/helper.py --list -u $STARTHINKER_USER`
- To get report json: `python dbm/helper.py --report [id] -u $STARTHINKER_USER`
- To get report schema: `python dbm/helper.py --schema [id] -u $STARTHINKER_USER`
- To get report sample: `python dbm/helper.py --sample [id] -u$STARTHINKER_USER`

Prerequisite: https://github.com/google/starthinker/blob/master/tutorials/deploy_developer.md#command-line-deploy

"""


import json
import argparse

from starthinker.util.project import project
from starthinker.util.google_api import API_DBM
from starthinker.util.dbm import report_file, report_to_rows, report_clean
from starthinker.util.bigquery import get_schema
from starthinker.util.csv import rows_to_type, rows_print

if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--report', help='report ID to pull json definition', default=None)
  parser.add_argument('--schema', help='report ID to pull schema format', default=None)
  parser.add_argument('--sample', help='report ID to pull sample data', default=None)
  parser.add_argument('--list', help='list reports', action='store_true')

  # initialize project
  project.from_commandline(parser=parser)
  auth = 'service' if project.args.service else 'user'

  # get report
  if project.args.report:
    report = API_DBM(auth).queries().getquery(queryId=project.args.report).execute()
    print(json.dumps(report, indent=2, sort_keys=True))

  # get schema
  elif project.args.schema:
    filename, report = report_file(auth, project.args.schema, None, 10)
    rows = report_to_rows(report)
    rows = report_clean(rows)
    rows = rows_to_type(rows)
    print(json.dumps(get_schema(rows)[1], indent=2, sort_keys=True))

  # get sample
  elif project.args.sample:
    filename, report = report_file(auth, project.args.sample, None, 10)
    rows = report_to_rows(report)
    rows = report_clean(rows)
    rows = rows_to_type(rows)
    for r in rows_print(rows, row_min=0, row_max=20): pass

  # get list
  else:
    for report in API_DBM(auth, iterate=True).queries().listqueries().execute():
      print(json.dumps(report, indent=2, sort_keys=True))

