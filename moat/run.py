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

from datetime import timedelta

from util.project import project 
from util.regexp import date_to_str
from util.data import get_emails, put_files
from util.csv import csv_to_rows, rows_to_csv, rows_add_date
from util.bigquery import storage_to_table

def moat():


  # find emails with reports
  for email in get_emails(project.task['auth'], project.task['in'], project.date):
    # moat reports are always one day back
    report_date = project.date - timedelta(days=1)
    if date_to_str(report_date) in email['subject']:
      if project.verbose: print 'PROCESSING:', email['subject']
      if len(email['attachments']) == 0: continue

      # use only first attachment
      attachment = email['attachments'][0]
      rows = csv_to_rows(attachment[1])
      rows_add_date(rows, report_date)
      data = rows_to_csv(rows)

      # split files into storage [ 'advertiser', 'display|video', 'moat', 'report.csv']
      path = attachment[0].lower().replace('-openx', '').rsplit('-', 3)
      path = '%s/%s-%s.csv' % (path[1], path[0], date_to_str(report_date))

      print 'STORAGE:', path
      put_files(project.task['auth'], project.task['out'], path, data)

if __name__ == "__main__":
  project.load('moat')
  moat()
