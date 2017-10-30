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
import csv
from StringIO import StringIO

from util.bigquery import bigquery_date


def csv_to_rows(csv_string):
  return  list(csv.reader(csv_string, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL))


def rows_to_csv(rows):
  csv_string = StringIO()
  writer = csv.writer(csv_string, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for row_number, row in enumerate(rows):
    try: writer.writerow(row)
    except Exception, e: print 'Error:', row_number, str(e), row
  csv_string.seek(0) # important otherwise contents is zero
  return csv_string


def rows_add_date(rows, date, header=True):
  if header:
    rows[0].insert(0, 'Report_Day')
    for row in rows[1:]: row.insert(0, bigquery_date(date))
  else:
    for row in rows: row.insert(0, bigquery_date(date))
  return rows

def rows_null_to_value(rows, value):
  for r  in xrange(len(rows)):
    rows[r] = map(lambda c: value if c.strip().lower() == 'null' else c, rows[r])
  return rows

def rows_re_to_value(rows, regexp, value):
  regexp = re.compile(regexp)
  for r  in xrange(len(rows)):
    rows[r] = map(lambda c: regexp.sub(value, c), rows[r])
  return rows

def rows_column_delete(rows, column):
  for row in rows:
    del row[column:column+1]
