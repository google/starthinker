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

from starthinker.util.csv import excel_to_rows, csv_to_rows, rows_trim, rows_header_sanitize, column_header_sanitize
from starthinker.util.cm import report_to_rows as cm_report_to_rows, report_clean as cm_report_clean, report_schema as cm_report_schema
from starthinker.util.data import put_rows, get_rows
from starthinker.util.dv import report_to_rows as dv360_report_to_rows, report_clean as dv360_report_clean
from starthinker.util.email import get_email_messages, get_email_links, get_email_attachments, get_subject, send_email


def email_read(config, task):

  # process only most recent message
  try:
    message = next(
        get_email_messages(config, task['auth'], task['read']['from'],
                           task['read']['to'],
                           task['read'].get('subject', None)))
  except StopIteration as e:
    if config.verbose:
      print('NO EMAILS FOUND')
    exit()

  if config.verbose:
    print('EMAIL:', get_subject(message))

  files = []

  if task['read'].get('attachment'):
    files.extend(
        get_email_attachments(config, task['auth'], message,
                              task['read']['attachment']))

  if task['read'].get('link'):
    files.extend(
        get_email_links(
            config,
            task['auth'],
            message,
            task['read']['link'],
            download=True))

  for filename, data in files:

    if config.verbose:
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
        put_rows(config, task['write'].get('auth', task['auth']),
                 task['write'], rows, sheet)

    # if CM report
    elif task['read']['from'] == 'noreply-cm@google.com':
      rows = cm_report_to_rows(data.read().decode())
      rows = cm_report_clean(rows)

      # if bigquery, remove header and determine schema
      schema = None
      if 'bigquery' in task['write']:
        schema = cm_report_schema(next(rows))
        task['write']['bigquery']['schema'] = schema
        task['write']['bigquery']['skip_rows'] = 1

      put_rows(config, task['write'].get('auth', task['auth']),
               task['write'], rows)

    # if dv360 report
    elif task['read']['from'] == 'noreply-dv360@google.com':
      rows = dv360_report_to_rows(data.getvalue().decode())
      rows = dv360_report_clean(rows)
      put_rows(config, task['write'].get('auth', task['auth']),
               task['write'], rows)

    # if csv
    elif filename.endswith('.csv'):
      rows = csv_to_rows(data.read().decode())
      rows = rows_header_sanitize(rows)
      put_rows(config, task['write'].get('auth', task['auth']),
               task['write'], rows)

    else:
      if config.verbose:
        print('UNSUPPORTED FILE:', filename)


def email_send(config, task):
  if config.verbose:
    print('EMAIL SEND')

  send_email(
      config,
      'user',
      task['send']['from'],
      task['send']['to'],
      task['send'].get('cc', ''),
      task['send']['subject'],
      task['send']['text'],
      task['send']['html'],
      task['send']['attachment']['filename'],
      get_rows(config, 'user', task['send']['attachment']),
  )


def email(config, task):
  if 'read' in task:
    email_read(config, task)
  elif 'send' in task:
    email_send(config, task)
