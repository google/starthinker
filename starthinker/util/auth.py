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

import sys
import socket
import threading

from googleapiclient import discovery
from googleapiclient.http import HttpRequest

from starthinker.util.auth_wrapper import CredentialsFlowWrapper
from starthinker.util.auth_wrapper import CredentialsServiceWrapper
from starthinker.util.auth_wrapper import CredentialsUserWrapper

# WARNING:  possible issue if switching user credentials mid recipe, not in scope but possible ( need to address using hash? )
CREDENTIALS_USER_CACHE = None
DISCOVERY_CACHE = {}

# set timeout to 10 minutes ( reduce socket.timeout: The read operation timed out )
socket.setdefaulttimeout(600)

def clear_credentials_cache():
  global CREDENTIALS_USER_CACHE
  CREDENTIALS_USER_CACHE = None


def get_credentials(config, auth):
  global CREDENTIALS_USER_CACHE

  if auth == 'user':
    if CREDENTIALS_USER_CACHE is None:
      try:
        CREDENTIALS_USER_CACHE = CredentialsUserWrapper(
          config.recipe['setup']['auth']['user'],
          config.recipe['setup']['auth'].get('client')
        )
      except (KeyError, ValueError):
        print('')
        print(
            'ERROR: You are attempting to access an API endpoiont that requires Google OAuth USER authentication but have not provided credentials to make that possible.'
        )
        print('')
        print(
            'SOLUTION: Specify a -u [user credentials path] parameter on the command line.'
        )
        print(
            '          Alternaitvely specify a -u [user credentials path to be created] parameter and a -c [client credentials path] parameter on the command line.'
        )
        print(
            '          Alternaitvely if running a recipe, include { "setup":{ "auth":{ "user":"[JSON OR PATH]" }}} in the JSON.'
        )
        print('')
        print(
            'INSTRUCTIONS: https://github.com/google/starthinker/blob/master/tutorials/cloud_client_installed.md'
        )
        print('')
        sys.exit(1)

    return CREDENTIALS_USER_CACHE

  elif auth == 'service':
    try:
      return CredentialsServiceWrapper(
        config.recipe['setup']['auth']['service']
      )
    except (KeyError, ValueError):
      print('')
      print(
          'ERROR: You are attempting to access an API endpoint that requires Google Cloud SERVICE authentication but have not provided credentials to make that possible.'
      )
      print('')
      print(
          'SOLUTION: Specify a -s [service credentials path] parameter on the command line.'
      )
      print(
          '          Alternaitvely if running a recipe, include { "setup":{ "auth":{ "service":"[JSON OR PATH]" }}} in the JSON.'
      )
      print('')
      print(
          'INSTRUCTIONS: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md'
      )
      print('')
      sys.exit(1)


def get_service(config,
  api='gmail',
  version='v1',
  auth='service',
  scopes=None,
  headers=None,
  key=None,
  uri_file=None
):
  global DISCOVERY_CACHE

  class HttpRequestCustom(HttpRequest):

    def __init__(self, *args, **kwargs):
      if headers:
        kwargs['headers'].update(headers)
      super(HttpRequestCustom, self).__init__(*args, **kwargs)

  if not key:
    key = config.recipe['setup'].get(key, '')

  cache_key = api + version + auth + str(key) + str(threading.current_thread().ident)

  if cache_key not in DISCOVERY_CACHE:
    credentials = get_credentials(config, auth)
    if uri_file:
      uri_file = uri_file.strip()
      if uri_file.startswith('{'):
        DISCOVERY_CACHE[cache_key] = discovery.build_from_document(
            uri_file,
            credentials=credentials,
            developerKey=key,
            requestBuilder=HttpRequestCustom
       )
      else:
        with open(uri_file, 'r') as cache_file:
          DISCOVERY_CACHE[cache_key] = discovery.build_from_document(
              cache_file.read(),
              credentials=credentials,
              developerKey=key,
              requestBuilder=HttpRequestCustom
          )
    else:
      try:
        DISCOVERY_CACHE[cache_key] = discovery.build(
          api,
          version,
          credentials=credentials,
          developerKey=key,
          requestBuilder=HttpRequestCustom,
          static_discovery=False
        )
      # PATCH: static_discovery not present in google-api-python-client < 2, default version in colab
      # ALTERNATE WORKAROUND: pip install update google-api-python-client==2.3 --no-deps --force-reinstall
      except TypeError:
        DISCOVERY_CACHE[cache_key] = discovery.build(
          api,
          version,
          credentials=credentials,
          developerKey=key,
          requestBuilder=HttpRequestCustom
        )

  return DISCOVERY_CACHE[cache_key]


def get_client_type(credentials):
  client_json = CredentialsFlowWrapper(credentials, credentials_only=True)
  return next(iter(client_json.keys()))


def get_profile(config):
  service = get_service(config, 'oauth2', 'v2', 'user')
  return service.userinfo().get().execute()


def set_iam(config, auth, project_id, role, email=None, service=None):
  service = get_service(config, 'cloudresourcemanager', 'v1', auth,
                        ['https://www.googleapis.com/auth/cloud-platform'])
  policy = service.projects().getIamPolicy(
      resource=project_id, body={}).execute()

  if email:
    member = 'user:%s' % email
  elif service:
    member = 'service:%s' % service
  else:
    member = None

  if member:
    for r in policy['bindings']:
      if r['role'] == role and member not in r['members']:
        print('Settings Role:', member, role)
        r['members'].append(member)
        policy = service.projects().setIamPolicy(
            resource=project_id, body={
                'policy': policy
            }).execute()
