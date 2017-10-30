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

import httplib2
from datetime import datetime
from io import BytesIO

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.http import MediaIoBaseUpload
from apiclient import discovery
from google.cloud import storage

from setup import UI_SERVICE, UI_BUCKET_LOG


def get_service():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(UI_SERVICE, ['https://www.googleapis.com/auth/devstorage.full_control'])
  http = credentials.authorize(httplib2.Http())
  return discovery.build('storage', 'v1', http=http)


def log_put(uid, data):
  service = get_service()
  media = MediaIoBaseUpload(BytesIO(str(data)), mimetype="text/plain")
  service.objects().insert(bucket=UI_BUCKET_LOG, name='%s.txt' % uid, media_body=media).execute()


def log_get(uid):
  service = get_service()
  data = service.objects().get_media(bucket=UI_BUCKET_LOG, object='%s.txt' % uid).execute()
  return data


def log_project(project, output=None, errors=None):
  if 'uuid' in project['setup']:
    data = 'DATE:%s\n' % str(datetime.now())
    if output is None and errors is None: data += 'STATUS:RUNNING\n'
    else:
      if errors: data += 'STATUS:ERROR\n' + (output or '')+ '\n' + (errors or '')
      else: data += 'STATUS:FINISHED\n' + (output or '')
    log_put(project['setup']['uuid'], data)


def log_status(uid):
  try:
    log_datetime, log_status, log_data = log_get(uid).split('\n', 2)
    log_datetime = log_datetime.split(':', 1)[1]
    log_status = log_status.split(':', 1)[1]
  except:
    log_datetime = ''
    log_status = 'UNKNOWN'
    log_data = ''
  return { 'datetime':log_datetime, 'status':log_status, 'data':log_data }
