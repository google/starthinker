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
from time import sleep

from datetime import timedelta

from util.project import project 
from util.data import get_files, put_files
from util.dcm import report_get, report_file, report_to_rows, report_clean, report_to_csv, get_profile_id, report_delete
from util.auth import get_service
from util.regexp import strip_yyymmdd


def dcm_copy():
  if project.verbose: print 'DCM COPY'

  report = True
  while report == True:
    filename, report = report_file(
      project.task['auth'],
      project.task['report']['account_id'],
      project.task['report']['report_id'],
      project.task['report']['collate'],
      project.task['report']['file'],
      project.date
    )
    if report == True: sleep(30)

  # report will be False or ByteIO
  return filename, report


def dcm_run():
  if project.verbose: print 'DCM RUN'

  return report_get(
    project.task['auth'],
    project.task['report']
  )


def dcm_delete():
  if project.verbose: print 'DCM DELETE'

  return report_delete(
    project.task['auth'],
    project.task['title'],
    project.task['account_id']
  )


def dcm():
  if project.verbose: print 'DCM'

  # check if delete flag is set
  if project.task.get('delete', False):
    dcm_delete()

  if 'report' in project.task:
    # retrieve the report data
    filename, report = dcm_copy() if 'report_id' in project.task['report'] else dcm_run()

    # if a report exists
    if report:

      # collate using filename ( remove the date and bam, what you pull is the latest )
      #if project.task['collate'] == 'LATEST':
      #  filename = strip_yyymmdd(filename)

      if project.verbose: print 'DCM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows, project.date, project.task.get('datastudio', False), project.task['report'].get('humanName', False))
      data = report_to_csv(rows)

      # upload to cloud if data
      if rows: put_files(project.task['auth'], project.task['out'], filename, data)


if __name__ == "__main__":
  project.load('dcm')
  dcm()
