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
import errno
from datetime import timedelta

import csv
import uuid

from io import BytesIO
#from google.cloud import storage

from util.project import project
from util.storage import parse_filename, parse_path, makedirs_safe, object_get, object_put, object_list, bucket_create
from util.regexp import parse_yyyymmdd, parse_dbm_report_id
from util.email import get_email_attachments, get_email_links, get_email_messages

from util.bigquery import local_file_to_table, datasets_create, csv_to_table
from util.bigquery.file_processor import FileProcessor

#def date_range(day, source):
#  if 'days' in source['email']: return day, day + timedelta(days=abs(source['email']['days']))
#  else: return None, None


def get_files(auth, source, day = None):
  if project.verbose: print 'LOADING FILES:', source 

  # not affected by day since explicitly defined
  if 'file' in source:
    if project.verbose: print 'OPENING', source['file']
    with open(source['file'], 'rb') as excel_file:
      return (source['file'], BytesIO(excel_file.read()))

  # can be day filtered
  elif 'directory' in source:
    files = []
    for file_in in glob.glob(source['directory']):
      if parse_filename(file_in).startswith('~'): continue # skip temporary files
      if day and parse_yyyymmdd(file_in) != day: continue # skip if day does not match
      if project.verbose: print 'OPENING', file_in
      with open(file_in, 'rb') as excel_file:
        files.append((file_in, BytesIO(excel_file.read())))
    return files

  elif 'storage' in source:
    # not affected by day since explicitly defined
    if 'blob' in source:
      if project.verbose: print 'OPENING', blob.name
      object_get(auth, source['storage']['blob'])
      return (source['blob'], blob.download_as_string())

    # can be day filtered
    elif 'bucket' in source:
      files = []
      for blob_name in object_list(auth, source['storage']['bucket'] + ':' + source['storage']['path']):
        if day and parse_yyyymmdd(blob_name) != day: continue # skip if day does not match
        if project.verbose: print 'OPENING', blob_name
        files.append((blob_name, object_get(auth, blob_name)))
      return files

  # can be day filtered ( pased in for aditional efficiency )
  elif 'email' in source:
    data = []

    #date_min, date_max = date_range(day, source)
    subject_regexp =  source['email'].get('subject', None)
    link_regexp =  source['email'].get('link', None)
    attachment_regexp =  source['email'].get('attachment', None)

    if attachment_regexp: data.extend(get_email_attachments(auth, source['email']['from'], source['email']['to'], day, day, subject_regexp, attachment_regexp))
    if link_regexp: data.extend(get_email_links(auth, source['email']['from'], source['email']['to'], day, day, subject_regexp, link_regexp, download=True))

    return data 


def get_emails(auth, source, day):
  #date_min, date_max = date_range(day, source)
  subject_regexp =  source['email'].get('subject', None)
  link_regexp =  source['email'].get('link', None)
  attachment_regexp =  source['email'].get('attachment', None)
  return get_email_messages(auth, source['email']['from'], source['email']['to'], day, day, subject_regexp, link_regexp, attachment_regexp, True)


def put_files(auth, target, filename, data):

  if 'directory' in target:
    file_out = target['directory'] + filename
    if project.verbose: print 'SAVING', file_out
    makedirs_safe(parse_path(file_out))
    with open(file_out, 'wb') as save_file:
      save_file.write(data.read())

  if 'storage' in target:
    # create the bucket
    bucket_create(auth, project.id, target['storage']['bucket'])

    # put the file
    file_out = target['storage']['bucket'] + ':' + target['storage']['path'] + filename
    if project.verbose: print 'SAVING', file_out
    object_put(auth, file_out, data)

  if 'bigquery' in target:
    if target['bigquery'].get('autodetect_schema', True):
      csv_to_table(auth, project.id, target['bigquery']['dataset'], target['bigquery']['table'], data, schema=target['bigquery'].get('schema', []), headers=1, structure='CSV')
    else:
      reader = csv.reader(data)
      rows = [item for item in reader]
      processor = FileProcessor()

      dataset = target['bigquery']['dataset']
      datasets_create(auth, project.id, dataset)

      table_name = target['bigquery']['table']
      replace = target['bigquery']['replace']
      schema = processor.field_list_to_schema(rows[0])
      temp_file_name = '/tmp/%s' % str(uuid.uuid1())
      f = open(temp_file_name, 'w')
      writer = csv.writer(f)

      if project.verbose: print 'SAVING', dataset, table_name

      for row in rows[1:]: writer.writerow(row)

      f.close()

      local_file_to_table(auth, dataset, table_name, schema, temp_file_name, replace=replace, file_type='CSV')
      os.remove(temp_file_name)

  if 'trix' in target:
    trix_update(auth, target['trix']['sheet_id'], target['trix']['sheet_range'], data, target['trix']['clear'])


  if 'email' in target:
    pass
