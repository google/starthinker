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
from util.dbm import report_delete, report_create, report_file, report_bigquery, report_to_rows, report_clean, accounts_split, DBM_CHUNKSIZE
from util.csv import rows_to_csv, rows_print


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
    report_delete(
      project.task['auth'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None)
    )

  # check if report is to be created
  if 'type' in project.task['report']: 
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
      project.task['report'].get('timezone', 'America/Los Angeles')
    )

  # moving a report
  if 'out' in project.task:

    # if cleaning is required
    #if project.task.get('datastudio', False) and 'bigquery' in project.task.get('out', {}):

    filename, report = report_file(
      project.task['auth'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None),
      project.task['report'].get('timeout', 60),
      DBM_CHUNKSIZE
    )

    # if a report exists
    if report:
      if project.verbose: print 'DBM FILE', filename
  
      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows, datastudio=project.task.get('datastudio', False) == True, nulls=True)
  
      #rows = rows_print(rows, 0, 3)

      # upload to cloud if data
      if rows: put_files(project.task['auth'], project.task['out'], filename, rows_to_csv(rows))

    # if storage copy ( DOES NOT WORK BECAUSE SERVICE OR USER NEEDS TO BE ADDED TO EVERY BILLING PROJECT! )
    #else:
    #  report_bigquery(
    #    project.task['auth'],
    #    project.task['report'].get('report_id', None),
    #    report_name,
    #    project.task['out']['bigquery']['dataset'],
    #    project.task['out']['bigquery']['table'],
    #    project.task['out']['bigquery'].get('schema', [])
    #  )

if __name__ == "__main__":
  project.load('dbm')
  dbm()
