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

from time import sleep

from starthinker.util.project import project 
from starthinker.util.data import put_rows
from starthinker.util.dcm import report_delete, report_create, report_file, report_to_rows, report_clean, get_account_name
from starthinker.util.csv import rows_column_add

CHUNKSIZE = 200 * 1024 * 1024

def dcm(account_id, disposition):
  name = '%s %s ( StarThinker )' % (project.task['name'], account_id)

  if project.verbose: print 'DCM REPORT', name

  # check if report is to be deleted
  if project.task.get('delete', False):
    report_delete(
      project.task['auth'],
      account_id,
      None,
      name
    )

  # check if report is to be created
  if 'type' in project.task['report']:
    report_create(
      project.task['auth'],
      account_id,
      name,
      project.task['report']
    )

  # moving a report
  if 'out' in project.task:
    filename, report = report_file(
      project.task['auth'],
      account_id,
      None,
      name,
      project.task['report'].get('timeout', 0),
      CHUNKSIZE
    )

    if report:
      if project.verbose: print 'DCM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows,  project.task.get('datastudio', False))
      rows = rows_column_add(rows, 'Account_Id', account_id)
      rows = rows_column_add(rows, 'Account_Name', get_account_name(project.task['auth'], account_id))

      # if BigQuery set to append ( storage will automatically file namespace )
      if project.task.get('out', {}).get('bigquery', {}).get('table'):
        project.task['out']['bigquery']['disposition'] = disposition 

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows: put_rows(project.task['auth'], project.task['out'], filename, rows)


@project.from_parameters
def dcm_bulk():
  if project.verbose: print 'DCM BULK'
  disposition = 'WRITE_TRUNCATE'
  for count, account in enumerate(project.task['accounts']):
    if project.verbose: print 'DCM BULK %d of %d' % (count, len(project.task['accounts']))
    dcm(account, disposition)
    disposition = 'WRITE_APPEND'
    sleep(3)


if __name__ == "__main__":
  dcm_bulk()
