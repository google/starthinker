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

import re
import gzip
from datetime import timedelta
from StringIO import StringIO

from util.project import project 
from util.regexp import parse_filename, parse_yyyymmdd
from util.csv import excel_to_rows, rows_trim, csv_to_rows, rows_column_add, rows_null_to_value, rows_re_to_value, rows_header_sanitize
from util.data import put_rows
from util.email import get_email_messages

def ias():

  # ensures a seperate data write for each report ( file/storage = append number to file, bigquery = change mode to append )
  counter = 1

  # date of file is yesterday
  report_date = project.date - timedelta(days=1)

  for email in get_email_messages(
    project.task['auth'],
    project.task['email']['from'],
    project.task['email']['to'],
    report_date,
    report_date,
    project.task['email'].get('subject', None),
    project.task['email'].get('link', None),
    project.task['email'].get('attachment', None),
    download=True
  ):

    if project.verbose: print 'IAS EMAIL:', email['subject']

    # use only first attachment or link
    if len(email['attachments']) > 0:
      filename, data = email['attachments'][0]
      if project.verbose: print 'IAS ATTACHMENT:', filename
    elif len(email['links']) > 0:
      filename, data = email['links'][0]
      if project.verbose: print 'IAS LINK:', filename
    else:
      filename, data = '', None

    if filename.endswith('.gz'):
      data = gzip.GzipFile(fileobj=data, mode='rb')
      filename = filename[:-3]

    if filename.endswith('.xlsx'):

      # loop through IAS XLSX sheets...
      for sheet, rows in excel_to_rows(data):
        
        print 'IAS XLSX SHEET:', sheet
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
            rows = rows[:-1]
            #print data.read()
            #data.seek(0)

            sheet_filename = parse_filename(sheet)
            filename = '%s/%s_%s_%d.csv' % (sheet_filename, sheet_filename, str(report_date), counter)
            if counter > 1: s['out']['bigquery']['disposition'] = 'WRITE_APPEND' # if mutliple reports then make sure to append, ONLY WORKS FOR BQ

            if project.verbose: print 'IAS WRITE', filename
            put_rows(project.task['auth'], s['out'], filename, rows)
            counter += 1 # count the number of reports to keep them seperate

    elif filename.endswith('.csv'):

      rows = csv_to_rows(data)
      rows = rows_null_to_value(rows, '') # ias stores null as string 'null' not empty cell, breaks BQ import
      rows = rows_re_to_value(rows, r'\$\{.*\}', '') # ias stores ${....} in columns just for fun, breaks BQ import

      if project.verbose: print 'IAS WRITE', filename
      put_rows(project.task['auth'], project.task['sheets'][0]['out'], filename, rows)

    else:
      if project.verbose: print 'UNSUPPORTED FILE:', filename


if __name__ == "__main__":
  project.load('ias')
  ias()
