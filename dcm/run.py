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
from util.dcm import report_delete, report_create, report_file, report_to_rows, report_clean, DCM_CHUNKSIZE
from util.csv import rows_to_csv

def dcm():
  if project.verbose: print 'DCM'

  # check if report is to be deleted
  if project.task.get('delete', False):
    report_delete(
      project.task['auth'],
      project.task['report']['account_id'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None)
    )

  # check if report is to be created
  if 'type' in project.task['report']:
    report_create(
      project.task['auth'],
      project.task['report']['account_id'],
      project.task['report']['name'],
      project.task['report']
    )

  # moving a report
  if 'out' in project.task:
    filename, report = report_file(
      project.task['auth'],
      project.task['report']['account_id'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None),
      project.task['report'].get('timeout', 10),
      DCM_CHUNKSIZE
    )

    if report:
      if project.verbose: print 'DCM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows,  project.task.get('datastudio', False))
      data = rows_to_csv(rows)

      # upload to cloud if data
      if rows: put_files(project.task['auth'], project.task['out'], filename, data)


if __name__ == "__main__":
  project.load('dcm')
  dcm()
