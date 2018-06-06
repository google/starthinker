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
from util.data import put_rows
from util.dbm import report_delete, report_create, report_file, report_to_rows, report_clean, accounts_split, DBM_CHUNKSIZE


def dbm():
  if project.verbose: print 'DBM'

  # legacy translations ( changed report title to name )
  if 'title' in project.task['report']:
    project.task['report']['name'] = project.task['report']['title']

  # legacy translations ( changed partners, advertisers to accounts with "partner_id:advertiser_id" )
  if 'accounts' in project.task['report']:
    project.task['report']['partners'], project.task['report']['advertisers'] = accounts_split(project.task['report']['accounts'])

  # check if report is to be deleted
  if project.task.get('delete', False):
    if project.verbose: print 'DBM DELETE',
    report_delete(
      project.task['auth'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None)
    )

  # check if report is to be created
  if 'type' in project.task['report']:
    if project.verbose: print 'DBM CREATE',
    report_create(
      project.task['auth'],
      project.task['report']['name'],
      project.task['report']['type'],
      project.task['report'].get('partners'),
      project.task['report'].get('advertisers'),
      project.task['report'].get('filters'),
      project.task['report'].get('dimensions'),
      project.task['report'].get('metrics'),
      project.task['report'].get('data_range'),
      project.task['report'].get('timezone', 'America/Los Angeles'),
      project.id,
      project.task['report'].get('dataset_id', None)
    )

  # moving a report
  if 'out' in project.task:

    filename, report = report_file(
      project.task['auth'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None),
      project.task['report'].get('timeout', 10),
      DBM_CHUNKSIZE
    )

    # if a report exists
    if report:
      if project.verbose: print 'DBM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows, datastudio=project.task.get('datastudio', False), nulls=True)

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows: put_rows(project.task['auth'], project.task['out'], filename, rows)

if __name__ == "__main__":
  project.load('dbm')
  dbm()
