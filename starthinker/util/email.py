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

# http://stackoverflow.com/questions/25832631/download-attachments-from-gmail-using-gmail-api

import re
import base64
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from io import BytesIO
from urllib.request import urlopen
from html.parser import HTMLParser
from datetime import timedelta

from googleapiclient.errors import HttpError

from starthinker.util.google_api import API_Gmail
from starthinker.util.regexp import parse_url, date_to_str
from starthinker.util.storage import parse_filename
from starthinker.util.csv import rows_to_csv


def _list_unique(seq):
  seen = set()
  seen_add = seen.add
  return [x for x in seq if not (x in seen or seen_add(x))]


def get_subject(message):
  for header in message['payload']['headers']:
    if header.get('name', '').lower() == 'subject':
      return header['value']
  return ''


def get_email_links(config, auth, message, link_regexp, download=False):
  links = []
  html_parser = HTMLParser()
  link_filter = re.compile(r'%s' % link_regexp) if link_regexp else None

  try:
    for part in message['payload'].get('parts', []) or [message['payload']]:
      if 'data' in part['body']:
        data = part['body']['data']
        content = base64.urlsafe_b64decode(data).decode('utf-8')
        # plain text may be different than html
        if part['mimeType'] == 'text/plain':
          links.extend(parse_url(content))
        # html needs to decode links
        elif part['mimeType'] == 'text/html':
          links.extend(
              map(lambda link: html_parser.unescape(link), parse_url(content)))

  except HttpError as error:
    print('EMAIL LINK ERROR: %s' % error)

  # remove duplicates
  links = _list_unique(links)

  # filter links
  if link_filter:
    links = [link for link in links if link_filter.match(link)]

  # for downloads convert links into files and data
  for link in links:
    if download:
      try:
        yield parse_filename(link, url=True), BytesIO(urlopen(link).read())
      except:
        'ERROR: Unable To Download', link
    else:
      yield link


def get_email_attachments(config, auth, message, attachment_regexp):

  file_filter = re.compile(r'%s' %
                           attachment_regexp) if attachment_regexp else None

  try:
    for part in message['payload'].get('parts', []):

      if part['filename']:

        # filter regexp
        if not file_filter or file_filter.match(part['filename']):

          if 'data' in part['body']:
            data = part['body']['data']

          else:
            att_id = part['body']['attachmentId']
            att = API_Gmail(config, auth).users().messages().attachments().get(
                userId='me', messageId=message['id'], id=att_id).execute()
            data = att['data']

          file_data = BytesIO(base64.urlsafe_b64decode(data.encode('UTF-8')))
          yield part['filename'], file_data

  except HttpError as e:
    print('EMAIL ATTACHMENT ERROR:', str(e))


def get_email_messages(config, auth,
                       email_from,
                       email_to,
                       subject_regexp=None,
                       date_min=None,
                       date_max=None):
  if config.verbose:
    print('GETTING EMAILS')

  query = 'from:%s AND to:%s' % (email_from, email_to)
  if date_min:
    query += ' AND after:%s' % date_to_str(date_min)
  if date_max:
    query += ' AND before:%s' % date_to_str(
        date_max + timedelta(days=1))  # make it inclusive
  if config.verbose:
    print('EMAIL SEARCH:', query)

  messages = API_Gmail(
      config, auth, iterate=True).users().messages().list(
          userId='me', q=query).execute()

  subject_filter = re.compile(r'%s' %
                              subject_regexp) if subject_regexp else None
  for message in messages:
    message = API_Gmail(config, auth).users().messages().get(
        userId='me', id=message['id']).execute()
    if subject_filter is None or subject_filter.match(get_subject(message)):
      yield message


def send_email(config, auth,
               email_to,
               email_from,
               email_cc,
               subject,
               text,
               html=None,
               attachment_filename=None,
               attachment_rows=None):
  if config.verbose:
    print('SENDING EMAIL', email_to)

  message = MIMEMultipart('alternative')
  message.set_charset('utf8')

  message['to'] = email_to
  message['cc'] = email_cc
  message['from'] = email_from
  message['subject'] = subject
  message.attach(MIMEText(text, 'plain', 'UTF-8'))

  if html:
    message.attach(MIMEText(html, 'html', 'UTF-8'))

  if attachment_filename and attachment_rows:
    attachment = MIMEBase('text', 'csv')
    attachment.set_payload(rows_to_csv(attachment_rows).read())
    attachment.add_header(
        'Content-Disposition', 'attachment', filename=attachment_filename)
    encode_base64(attachment)
    message.attach(attachment)

  #API_Gmail(config, auth).users().messages().send(userId='me', body={'raw': base64.urlsafe_b64encode(message.as_string())}).execute()
  API_Gmail(config, auth).users().messages().send(
      userId='me',
      body={
          'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
      }).execute()
