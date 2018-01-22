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

import re
import gzip
from datetime import timedelta

from StringIO import StringIO

from util.project import project 
from util.regexp import parse_filename, parse_yyyymmdd
from util.csv import excel_to_rows, rows_trim, csv_to_rows, rows_to_csv, rows_column_add, rows_null_to_value, rows_re_to_value, rows_header_sanitize
from util.data import get_files, put_files

RE_IAS_DATE = re.compile(r'\((\d+), (\d+), (\d+),.*')

def ias():

  # ensures a seperate data write for each report ( file/storage = append number to file, bigquery = change mode to append )
  counter = 1

  for filename, data in get_files(project.task['auth'], project.task['in'], project.date):

    if filename.endswith('.gz'):
      data = gzip.GzipFile(fileobj=data, mode='rb')
      filename = filename[:-3]

    if project.verbose: print 'PROCESSING:', filename

    if filename.endswith('.xlsx'):
      report_date = project.date - timedelta(days=1)
 
      if str(project.date) not in filename: continue

      # loop through IAS sheets...
      for sheet, rows in excel_to_rows(data):
        
        # if sheet is flagged for move...
        for s in project.task['sheets']:
          if s['sheet'] == sheet:
            rows = rows_trim(rows)
            rows = rows_header_sanitize(rows)

            # fix the date IAS sends into a format usable by BigQuery
            for r in xrange(len(rows)): 
              if r == 0: continue
              try: rows[r][0] = "{:04}{:02}{:02}".format(rows[r][0][0], rows[r][0][1], rows[r][0][2]) if rows[r][0] else None
              except: raise ValueError("The 1st column must be a date column in the format of (Year, Month, Day, Hour, Minute, Second ) not %s." % rows[r][0])

            # cut off last row before converting to csv, its always blank
            data = rows_to_csv(rows[:-1])
            #print data.read()
            #data.seek(0)

            sheet_filename = parse_filename(sheet)
            filename = '%s/%s_%s_%d.csv' % (sheet_filename, sheet_filename, str(report_date), counter)
            if counter > 1: s['out']['bigquery']['disposition'] = 'WRITE_APPEND' # if mutliple reports then make sure to append, ONLY WORKS FOR BQ
            put_files(project.task['auth'], s['out'], filename, data)
            counter += 1 # count the number of reports to keep them seperate

    elif filename.endswith('.csv'):
      if filename == 'site_report.csv':
        report_date = (project.date - timedelta(days=1))
        filename = 'site_report_%s.csv' % str(report_date)
      else:
        report_date = parse_yyyymmdd(filename)

      rows = csv_to_rows(data)
      rows = rows_column_add(rows, 'Report_Day', report_date)
      #rows = rows_add_date(rows, report_date)
      rows = rows_null_to_value(rows, '') # ias stores null as string 'null' not empty cell, breaks BQ import
      rows = rows_re_to_value(rows, r'\$\{.*\}', '') # ias stores ${....} in columns just for fun, breaks BQ import
      data = rows_to_csv(rows)

      filename = '%s/%s' % (filename.split('_', 1)[0], filename)
      put_files(project.task['auth'], project.task['out'], filename, data)
   

if __name__ == "__main__":
  project.load('ias')
  ias()
