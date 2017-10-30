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

import os
import csv
import re
from StringIO import StringIO
from datetime import datetime

from third_party.xlsx import Workbook
from util.project import project
from util.bigquery import bigquery_date

RE_HEADER = re.compile('[^0-9a-zA-Z_]+')

class ExcelToCSV():

  def __init__(self, file_in):
    self.file_in = file_in
    self.header = False
    self.trim = False
    self.date = None
    self.date_cell = None 
    self.ignore = []
    
  def set_header(self, on_off):
    self.header = on_off
  
  def set_trim(self, on_off):
    self.trim = on_off
  
  def set_date(self, date_value):
    self.date = date_value
  
  def set_date_cell(self, column, row, date_format): 
    self.date_cell = (column, row, date_format)
  
  def set_ignore(self, sheet_names):
    self.ignore = set(sheet_names)
  
  def _sheet_open(self, sheet):
    if project.verbose: print 'SHEET', sheet.name
    rows = []

    # load all rows from sheet
    for row_number, cells in sheet.rowsIter():
      rows.append(map(lambda cell: cell.value or cell.formula, cells))
      if self.date_cell:
        if row_number == self.date_cell[0]:
          self.date = datetime.strptime(cells[self.date_cell[1] - 1].value, self.date_cell[2]).date()
          if project.verbose: print 'DATE FROM SHEET', self.date

    return rows


  def _sheet_trim(self, rows):
    if project.verbose: print 'TRIMMING'
  
    # find most common continous length
    histogram = {}
    prior = None
    for row in rows:
      length = len(row)
      if length != prior: histogram[length] = 1
      else: histogram[length] += 1
      prior = length
    common_length = sorted(histogram.iterkeys(), key=lambda k: histogram[k], reverse=True)[0]

    # strip any columns not in common length
    rows = [row for row in rows if len(row) == common_length]

    # replace any special characters in the header
    if self.header:
      try: rows[0] = [RE_HEADER.sub('', cell.replace(' ', '_')).strip('_') for cell in rows[0]]
      except: pass

    return rows


  def _sheet_date(self, rows):
    if project.verbose: print 'DATING', self.date

    # add header for first row, then date for all others
    if self.header:
      rows[0].insert(0, 'Report_Day')
      for row in rows[1:]: row.insert(0, bigquery_date(self.date))
    else:
      for row in rows: row.insert(0, bigquery_date(self.date))

    return rows


  #  return a raw {sheet:[][]} of cells
  def get_sheets(self):
    sheets = {}
    book = Workbook(self.file_in)
    for sheet in book:
      if sheet.name in self.ignore: continue # ignore specified sheets
      rows = self._sheet_open(sheet) # open sheet
      if self.trim: rows = self._sheet_trim(rows) # trim if flagged
      if self.date: rows = self._sheet_date(rows) # apply date if set
      sheets[sheet.name] = rows
    return sheets


  #  return a raw {sheet:csv} of cells
  def get_csv(self):
    sheets = {}
    book = Workbook(self.file_in)
    for sheet in book:
      if sheet.name in self.ignore: continue # ignore specified sheets
      rows = self._sheet_open(sheet) # open sheet
      if self.trim: rows = self._sheet_trim(rows) # trim if flagged
      if self.date: rows = self._sheet_date(rows) # apply date if set

      # create csv buffer
      csv_string = StringIO()
      writer = csv.writer(csv_string, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for row_number, row in enumerate(rows): 
        try: writer.writerow(row)
        except Exception, e: print 'Error:', row_number, str(e), row
      csv_string.seek(0) # important otherwise contents is zero
      sheets[sheet.name] = csv_string
    return sheets
