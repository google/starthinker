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

#https://storage.cloud.google.com/gdbm-public/entity/20161128.0.UniversalSite.json?_ga=1.166056958.1158224420.1495818894

import gzip
from datetime import timedelta

from util.project import project 
from util.excel import ExcelToCSV
from util.regexp import parse_filename, parse_yyyymmdd
from util.csv import csv_to_rows, rows_to_csv, rows_add_date, rows_null_to_value, rows_re_to_value
from util.data import get_files, put_files


def ias_out(project, sheet, filename, data):
  # write multiple sheets
  if 'sheets' in project.task:
    for s in project.task['sheets']:
      if s['sheet'] == sheet:
        if project.verbose: print 'SAVING:', sheet
        put_files(project.task['auth'], s['out'], filename, data)
        break;
  # write one object if no sheets specified
  else:
    if project.verbose: print 'SAVING:', filename
    put_files(project.task['auth'], project.task['out'], filename, data)


def ias():

  for filename, data in get_files(project.task['auth'], project.task['in'], project.date):

    if filename.endswith('.gz'):
      data = gzip.GzipFile(fileobj=data, mode='rb')
      filename = filename[:-3]

    if project.verbose: print 'PROCESSING:', filename

    if filename.endswith('.xlsx'):
      report_date = project.date - timedelta(days=1)
 
      if str(project.date) not in filename: continue

      excel = ExcelToCSV(data)
      excel.set_ignore(['Report Settings'])
      excel.set_header(True)
      excel.set_trim(True)
      excel.set_date(report_date)

      for sheet, data in excel.get_csv().items():
        #if report_sheets and sheet not in report_sheets: continue # save only sheets specified ( if specified )
        sheet_filename = parse_filename(sheet)
        filename = '%s/%s_%s.csv' % (sheet_filename, sheet_filename, str(report_date))
        #if project.verbose: print 'STORAGE:', filename
        #put_files(project.task['auth'], project.task['out'], filename, data)
        ias_out(project, sheet, filename, data)


    elif filename.endswith('.csv'):
      #if report_sheets and filename.split('_', 1)[0] not in report_sheets: continue # save only sheets specified ( if specified )

      if filename == 'site_report.csv':
        report_date = (project.date - timedelta(days=1))
        filename = 'site_report_%s.csv' % str(report_date)
      else:
        report_date = parse_yyyymmdd(filename)

      rows = csv_to_rows(data)
      rows = rows_add_date(rows, report_date)
      rows = rows_null_to_value(rows, '') # ias stores null as string 'null' not empty cell, breaks BQ import
      rows = rows_re_to_value(rows, r'\$\{.*\}', '') # ias stores ${....} in columns just for fun, breaks BQ import
      data = rows_to_csv(rows)

      filename = '%s/%s' % (filename.split('_', 1)[0], filename)
      #if project.verbose: print 'STORAGE:', filename
      #put_files(project.task['auth'], project.task['out'], filename, data)
      ias_out(project, None, filename, data)
   

if __name__ == "__main__":
  project.load('ias')
  ias()
