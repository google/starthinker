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

import re
import json
import base64
from time import sleep
from io import BytesIO

from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

from starthinker.config import UI_SERVICE

RE_CREDENTIALS_JSON = re.compile(r'^\s*\{.*\}\s*$', re.DOTALL)


def _credentials_storage_service():

  if RE_CREDENTIALS_JSON.match(UI_SERVICE):
    credentials = Credentials.from_service_account_info(json.loads(UI_SERVICE))
  else:
    credentials = Credentials.from_service_account_file(UI_SERVICE)

  return discovery.build('storage', 'v1', credentials=credentials)


def _credentials_retry(job, retries=3, wait=1):
  try:
    return job.execute()
  except HttpError as e:
    if e.resp.status == 429 and retries > 0:
      sleep(wait)
      return _credentials_retry(job, retries - 1, wait * 2)
    else:
      raise


def credentials_storage_get(cloud_path):
  bucket, filename = cloud_path.split(':', 1)
  data = _credentials_retry(_credentials_storage_service().objects().get_media(
      bucket=bucket, object=filename))
  return json.loads(base64.b64decode(data.decode()).decode())


def credentials_storage_put(cloud_path, credentials):
  bucket, filename = cloud_path.split(':', 1)
  data = BytesIO(base64.b64encode(json.dumps(credentials).encode()))
  media = MediaIoBaseUpload(data, mimetype='text/json')
  _credentials_retry(_credentials_storage_service().objects().insert(
      bucket=bucket, name=filename, media_body=media))
