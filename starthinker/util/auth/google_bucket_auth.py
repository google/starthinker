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
import json
import base64
import jsonpickle
import httplib2
import datetime
from io import BytesIO

from oauth2client.client import Credentials, OAuth2Credentials, GoogleCredentials, Storage, EXPIRY_FORMAT
from oauth2client.file import Storage as LocalStorage
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import _helpers
from googleapiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload
from apiclient import discovery

from django.utils import encoding

from starthinker.config import UI_PROJECT, UI_SERVICE, UI_ZONE

RE_CREDENTIALS_JSON = re.compile(r'^\s*\{.*\}\s*$', re.DOTALL)

def get_service():
  '''Loads service credentials for storing the user credentials in a bucket.

  Sometimes UI_SERVICE is a json file, sometimes its a file path, accomodate both.

  '''

  # if credentials are embeded as JSON
  if RE_CREDENTIALS_JSON.match(UI_SERVICE):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
      json.loads(UI_SERVICE),
      'https://www.googleapis.com/auth/devstorage.full_control'
    )

  # if credentials are local path then check if they exist ( used by command line )
  else:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
      UI_SERVICE,
      'https://www.googleapis.com/auth/devstorage.full_control'
    )

  http = credentials.authorize(httplib2.Http())
  return discovery.build('storage', 'v1', http=http, cache_discovery=False)


def auth_decode(value):
  return jsonpickle.decode(base64.b64decode(encoding.smart_bytes(value)))


def auth_encode(value):
  return encoding.smart_text(base64.b64encode(jsonpickle.encode(value).encode()))


def credentails_get(cloud_path):
  service = get_service()
  bucket, filename = cloud_path.split(':',1)
  data = service.objects().get_media(bucket=bucket, object=filename).execute()
  return auth_decode(data)


def credentails_put(cloud_path, credentials):
  service = get_service()
  bucket, filename = cloud_path.split(':',1)

  # create bucket if it does not exist
  try:
    body = {
      "kind": "storage#bucket",
      "name":bucket,
      "storageClass":"REGIONAL",
      "location":UI_ZONE.rsplit('-', 1)[0] # take only region part of zone
    }
    service.buckets().insert(project=UI_PROJECT, body=body).execute()
  except HttpError, e:
    if json.loads(e.content)['error']['code'] == 409: pass 
    else: raise e

  data = auth_encode(credentials)
  media = MediaIoBaseUpload(BytesIO(str(data)), mimetype="text/json")
  service.objects().insert(bucket=bucket, name=filename, media_body=media).execute()
  return filename


class BucketStorage(Storage):
  def __init__(self, cloud_path):
    super(BucketStorage, self).__init__()
    self.cloud_path = cloud_path

  def locked_get(self):
    return BucketCredentials.from_json(credentails_get(self.cloud_path))

  def locked_put(self, credentials):
    credentails_put(self.cloud_path, credentials.to_json())

  def locked_delete(self):
    return # skip for now until tested well
    #service = get_service()
    #bucket, filename = self.cloud_path.split(':',1)
    #service.objects().delete(bucket=bucket, object=filename).execute()

class BucketCredentials(OAuth2Credentials):


  def __init__(self, *args, **kwargs):
    self.cloud_path = kwargs.pop('cloud_path')
    super(BucketCredentials, self).__init__(*args, **kwargs)
    self.store = BucketStorage(self.cloud_path)

  def set_cloud_path(self, cloud_path):
    self.cloud_path = cloud_path

  @classmethod
  def from_json(cls, json_data):
    data = json.loads(_helpers._from_bytes(json_data))
    if (data.get('token_expiry') and not isinstance(data['token_expiry'], datetime.datetime)):
      try: data['token_expiry'] = datetime.datetime.strptime(data['token_expiry'], EXPIRY_FORMAT)
      except ValueError: data['token_expiry'] = None

    retval = cls(
      data['access_token'],
      data['client_id'],
      data['client_secret'],
      data['refresh_token'],
      data['token_expiry'],
      data['token_uri'],
      data['user_agent'],
      revoke_uri=data.get('revoke_uri', None),
      id_token=data.get('id_token', None),
      id_token_jwt=data.get('id_token_jwt', None),
      token_response=data.get('token_response', None),
      scopes=data.get('scopes', None),
      token_info_uri=data.get('token_info_uri', None),
      cloud_path=data.get('cloud_path', None)
    )
    retval.invalid = data['invalid']
    return retval

  @classmethod
  def from_oauth(cls, cloud_path, credentials):
    # converts an OAuthCredentials into a BucketCredentials
    return BucketCredentials(
      credentials.access_token,
      credentials.client_id,
      credentials.client_secret,
      credentials.refresh_token,
      credentials.token_expiry,
      credentials.token_uri,
      credentials.user_agent,
      revoke_uri=credentials.revoke_uri,
      id_token=credentials.id_token,
      id_token_jwt=None, #credentials.id_token_jwt,
      token_response=credentials.token_response,
      scopes=credentials.scopes,
      token_info_uri=credentials.token_info_uri,
      cloud_path=cloud_path
    )

  @classmethod
  def from_local(cls, cloud_path, credentials_path):
    credentials = LocalStorage(credentials_path).get()
    return BucketCredentials.from_oauth(cloud_path, credentials)
  
  @classmethod
  def from_bucket(cls, cloud_path):
    return BucketCredentials.from_json(credentails_get(cloud_path))

  def to_bucket(self):
    credentails_put(self.cloud_path, self.to_json())

  # add from file

  # add to file
