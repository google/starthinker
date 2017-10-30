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

from util.project import project
from util.data import put_files
from util.dbm import report_download, report_to_rows, report_clean, report_to_csv

def dbm():
  if project.verbose: print 'DBM'

  if 'report' in project.task:
    # retrieve the report data ( latest or create )
    filename, report = report_download(
      project.task['auth'],
      project.task['report']['title'], # latest
      project.task['report'].get('type'), # create
      project.task['report'].get('partners'), # create
      project.task['report'].get('advertisers'), # create
      project.task['report'].get('filters'), # create
      project.task['report'].get('dimensions'), # create
      project.task['report'].get('metrics'), # create
      project.task['report'].get('data_range'), # create
    )

    # if a report exists
    if report:
      if project.verbose: print 'DBM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows, datastudio=project.task.get('datastudio', False) == True, nulls=True)
      data = report_to_csv(rows)

      if project.verbose: print 'DBM ROWS', len(rows)

      # upload to cloud if data
      if rows: put_files(project.task['auth'], project.task['out'], filename, data)

if __name__ == "__main__":
  project.load('dbm')
  dbm()
