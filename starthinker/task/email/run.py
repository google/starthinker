###########################################################################
#
#  Copyright 2020 Google LLC
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

from starthinker.util.project import project
from starthinker.util.data import put_rows, get_rows
from starthinker.util.csv import excel_to_rows, csv_to_rows, rows_trim, rows_header_sanitize, column_header_sanitize
from starthinker.util.email import get_email_messages, get_email_links, get_email_attachments, get_subject, send_email
from starthinker.util.dbm import report_to_rows as dv360_report_to_rows, report_clean as dv360_report_clean
from starthinker.util.dcm import report_to_rows as cm_report_to_rows, report_clean as cm_report_clean, report_schema as cm_report_schema


def email_read():

  # process only most recent message
  try:
    message = next(
        get_email_messages(project.task['auth'], project.task['read']['from'],
                           project.task['read']['to'],
                           project.task['read'].get('subject', None)))
  except StopIteration as e:
    if project.verbose:
      print('NO EMAILS FOUND')
    exit()

  if project.verbose:
    print('EMAIL:', get_subject(message))

  files = []

  if project.task['read'].get('attachment'):
    files.extend(
        get_email_attachments(project.task['auth'], message,
                              project.task['read']['attachment']))

  if project.task['read'].get('link'):
    files.extend(
        get_email_links(
            project.task['auth'],
            message,
            project.task['read']['link'],
            download=True))

  for filename, data in files:

    if project.verbose:
      print('EMAIL FILENAME:', filename)

    # decompress if necessary
    if filename.endswith('.gz'):
      data = gzip.GzipFile(fileobj=data, mode='rb')
      filename = filename[:-3]

    # if excel file, save each sheet individually
    if filename.endswith('.xlsx'):

      for sheet, rows in excel_to_rows(data):
        rows = rows_trim(rows)
        rows = rows_header_sanitize(rows)
        put_rows(project.task['read']['out'].get('auth', project.task['auth']),
                 project.task['read']['out'], rows, sheet)

    # if CM report
    elif project.task['read']['from'] == 'noreply-cm@google.com':
      rows = cm_report_to_rows(data.read().decode())
      rows = cm_report_clean(rows)

      # if bigquery, remove header and determine schema
      schema = None
      if 'bigquery' in project.task['read']['out']:
        schema = cm_report_schema(next(rows))
        project.task['read']['out']['bigquery']['schema'] = schema
        project.task['read']['out']['bigquery']['skip_rows'] = 1

      put_rows(project.task['read']['out'].get('auth', project.task['auth']),
               project.task['read']['out'], rows)

    # if dv360 report
    elif project.task['read']['from'] == 'noreply-dv360@google.com':
      rows = dv360_report_to_rows(data.getvalue().decode())
      rows = dv360_report_clean(rows)
      put_rows(project.task['read']['out'].get('auth', project.task['auth']),
               project.task['read']['out'], rows)

    # if csv
    elif filename.endswith('.csv'):
      rows = csv_to_rows(data.read().decode())
      rows = rows_header_sanitize(rows)
      put_rows(project.task['read']['out'].get('auth', project.task['auth']),
               project.task['read']['out'], rows)

    else:
      if project.verbose:
        print('UNSUPPORTED FILE:', filename)


def email_send():
  if project.verbose:
    print('EMAIL SEND')

  send_email(
      'user',
      project.task['send']['from'],
      project.task['send']['to'],
      project.task['send'].get('cc', ''),
      project.task['send']['subject'],
      project.task['send']['text'],
      project.task['send']['html'],
      project.task['send']['attachment']['filename'],
      get_rows('user', project.task['send']['attachment']),
  )


@project.from_parameters
def email():
  if 'read' in project.task:
    email_read()
  elif 'send' in project.task:
    email_send()


if __name__ == '__main__':
  email()
