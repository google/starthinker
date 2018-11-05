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

import gzip

from util import flag_last
from util.project import project 
from util.csv import excel_to_rows, csv_to_rows, rows_trim, rows_header_sanitize, column_header_sanitize
from util.email import get_email_messages
from util.data import put_rows
import traceback


def email_files(email):

  # loop attachment, outside it looks like one iteration
  for filename, data in email['attachments']:
    if project.verbose: print 'EMAIL ATTACHMENT:', filename
    yield filename, data

  # loop links, outside it looks like one iteration
  for filename, data in email['links']:
    if project.verbose: print 'EMAIL LINK:', filename
    yield filename, data


def email():

  # process only most recent message
  email = get_email_messages(
    project.task['auth'],
    project.task['from'],
    project.task['to'],
    project.task.get('subject', None),
    project.task.get('link', None),
    project.task.get('attachment', None),
    download=True
  )

  # only take the most recent email
  try: email = email.next()
  except:
    traceback.print_exc()
    if project.verbose: print 'NO EMAILS FOUND'
    exit()

  if project.verbose: print 'EMAIL:', email['subject']

  # loop all attached files
  for filename, data in email_files(email):

    if project.verbose: print 'EMAIL FILENAME:', filename

    # decompress if necessary
    if filename.endswith('.gz'):
      data = gzip.GzipFile(fileobj=data, mode='rb')
      filename = filename[:-3]

    # if excel file, save each sheet individually
    if filename.endswith('.xlsx'):

      for sheet, rows in excel_to_rows(data):
        rows = rows_trim(rows)
        rows = rows_header_sanitize(rows)

        if project.verbose: print 'EMAIL WRITE', filename
        put_rows(project.task['auth'], project.task['out'], filename, rows, column_header_sanitize(sheet))

    # if csv, save directly
    elif filename.endswith('.csv'):
      rows = csv_to_rows(data)
      rows = rows_header_sanitize(rows)

      if project.verbose: print 'EMAIL WRITE', filename
      put_rows(project.task['auth'], project.task['out'], filename, rows)

    else:
      if project.verbose: print 'UNSUPPORTED FILE:', filename


if __name__ == "__main__":
  project.load('email')
  email()
