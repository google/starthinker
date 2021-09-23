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

import os
import re
import json
import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.oauth2.credentials import Credentials as CredentialsUser
from google.oauth2.service_account import Credentials as CredentialsService

from starthinker.config import APPLICATION_NAME, APPLICATION_SCOPES
from starthinker.util.auth_storage import credentials_storage_get, credentials_storage_put

RE_CREDENTIALS_BUCKET = re.compile(r'[a-z0-9_\-\.]+:.+\.json')
RE_CREDENTIALS_JSON = re.compile(r'^\s*\{.*\}\s*$', re.DOTALL)


def CredentialsFlowWrapper(client, credentials_only=False, **kwargs):

  # relax scope comparison, order and default scopes are not critical
  os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

  # parse credentials from file or json
  if isinstance(client, dict):
    client_json = client
  elif RE_CREDENTIALS_JSON.match(client):
    client_json = json.loads(client)
  else:
    with open(client, 'r') as json_file:
      client_json = json.load(json_file)

  if credentials_only:
    return client_json
  else:
    if 'installed' in client_json:
      flow = InstalledAppFlow.from_client_config(client_json,
                                                 APPLICATION_SCOPES, **kwargs)
    else:
      flow = Flow.from_client_config(client_json, APPLICATION_SCOPES, **kwargs)

    flow.user_agent = APPLICATION_NAME

    return flow


def CredentialsServiceWrapper(service):
  if isinstance(service, dict):
    return CredentialsService.from_service_account_info(service)
  elif RE_CREDENTIALS_JSON.match(service):
    return CredentialsService.from_service_account_info(json.loads(service))
  else:
    return CredentialsService.from_service_account_file(service)


class CredentialsUserWrapper(CredentialsUser):

  def __init__(self, user=None, client=None):
    self.user = user
    self.client = client

    super(CredentialsUserWrapper, self).__init__(None)
    self.load()

  def from_credentials(self, credentials):
    self.token = credentials.token
    self.expiry = credentials.expiry
    self._refresh_token = credentials.refresh_token
    self._id_token = credentials.token_uri
    self._token_uri = credentials.token_uri
    self._client_id = credentials.client_id
    self._client_secret = credentials.client_secret
    self._scopes = credentials.scopes

  def from_json(self, data):
    self.token = data['access_token']
    self.expiry = datetime.datetime.strptime(
        data['token_expiry'][:19],
        '%Y-%m-%dT%H:%M:%S').replace(microsecond=0)  # this is always UTC
    self._refresh_token = data['refresh_token']
    self._id_token = data['id_token']
    self._token_uri = data['token_uri']
    self._client_id = data['client_id']
    self._client_secret = data['client_secret']

  def to_json(self):
    return {
        'access_token':
            self.token,
        'token_expiry':
            self.expiry.strftime('%Y-%m-%dT%H:%M:%SZ') if self.expiry else None,
        'refresh_token':
            self._refresh_token,
        'id_token':
            self._id_token,
        'token_uri':
            self._token_uri,
        'client_id':
            self._client_id,
        'client_secret':
            self._client_secret,
        'scopes':
            self._scopes,
    }

  def load_file(self):
    if os.path.exists(self.user):
      with open(self.user, 'r') as json_file:
        self.from_json(json.load(json_file))
    elif self.client:
      self.load_flow()

  def load_storage(self):
    return self.from_json(credentials_storage_get(self.user))

  def load_flow(self):
    flow = CredentialsFlowWrapper(self.client)
    flow.run_console()

    self.from_credentials(flow.credentials)
    self.save()

  def load(self):
    if self.user is None:
      pass
    elif isinstance(self.user, dict):
      self.from_json(self.user)
    elif RE_CREDENTIALS_JSON.match(self.user):
      self.from_json(json.loads(self.user))
    elif RE_CREDENTIALS_BUCKET.match(self.user):
      self.load_storage()
    elif self.user:
      self.load_file()

  def save_json(self):
    self.user = json.dumps(self.to_json())

  def save_file(self):
    with open(self.user, 'w') as json_file:
      json_file.write(json.dumps(self.to_json()))

  def save_storage(self):
    credentials_storage_put(self.user, self.to_json())

  def save(self, destination=None):
    if destination is not None:
      self.user = destination

    if self.user is None:
      pass
    elif isinstance(self.user, dict):
      self.user = self.to_json()
    elif RE_CREDENTIALS_BUCKET.match(self.user):
      self.save_storage()
    elif RE_CREDENTIALS_JSON.match(self.user):
      self.save_json()
    elif self.user:
      self.save_file()

  def refresh(self, request=None):
    self.load()
    if not self.valid:
      if request is None:
        request = Request()
      super(CredentialsUserWrapper, self).refresh(request)
      self.expiry = self.expiry.replace(
          microsecond=0
      )  # make parsing more consistent, microseconds are not essential
      self.save()
