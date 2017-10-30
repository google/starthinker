###########################################################################
#
#  Copyright 2017 Google Inc.
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

import pprint

from datetime import timedelta

from util.project import project 
from util.data import get_files, put_files
from util.ds import report_get, report_fetch, report_to_rows, report_to_csv, report_read_data
from util.auth import get_service

def ds_run(day):
  if project.verbose: print 'DS RUN'

  if 'id' in project.task['report']:
    return report_fetch(
      project.task['auth'], 
      project.task['report']['id'],)
  else:
    return report_get(
      project.task['auth'],
      project.task['report']['title'],
      project.task['report']['template'],
      project.task['report']['parameters'],
      day)


def _one_report(day):
  # retrieve the report meta-data
  reports = ds_run(day)

  # if a report exists
  for report in reports:
    for report_frag in report:
      if project.verbose: print 'DS FILE', report_frag['name']

      # read data and clean up the report
      rows = report_to_rows(report_read_data(project.task['auth'], report_frag['report_id'], report_frag['report_fragment']))
      data = report_to_csv(rows)

      # upload to cloud if data
      if rows: put_files(project.task['auth'], project.task['out'], report_frag['name'], data)


def ds():
  if project.verbose: print 'DS'

  if 'report' in project.task:
    day = project.date - timedelta(days=abs(project.task['days']))

    _one_report(day)


if __name__ == "__main__":
  project.load('ds')
  ds()
