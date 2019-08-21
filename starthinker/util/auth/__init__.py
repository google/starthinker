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

#https://github.com/google/oauth2client/blob/master/oauth2client/client.py
#https://developers.google.com/android-publisher/authorization#generating_a_refresh_token

import os
import re
import json
import httplib2
import threading

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery_cache.base import Cache

from starthinker.config import APPLICATION_NAME, APPLICATION_SCOPES
from starthinker.util.project import project
from starthinker.util.auth.google_bucket_auth import BucketCredentials


MAX_TOKEN_LIFETIME_SECS = 6 * 60 * 60 # 6 hours
SERVICE_CACHE = {}

RE_CREDENTIALS_BUCKET = re.compile(r'[a-z0-9_\-\.]+:.+\.json')
RE_CREDENTIALS_JSON = re.compile(r'^\s*\{.*\}\s*$', re.DOTALL)


def get_flow(client_json_or_filepath, redirect_uri=None):
  if RE_CREDENTIALS_JSON.match(client_json_or_filepath):
    client_json = json.loads(client_json_or_filepath)
    flow = client.OAuth2WebServerFlow(
      client_id=client_json.values()[0]['client_id'],
      client_secret=client_json.values()[0]['client_secret'],
      scope=APPLICATION_SCOPES,
      redirect_uri=redirect_uri
    )
  else:
    flow = client.flow_from_clientsecrets(
      filename=client_json_or_filepath,
      scope=APPLICATION_SCOPES,
      redirect_uri=redirect_uri
    )
  
  flow.user_agent = APPLICATION_NAME
  return flow


def get_credentials():

  try:
    auth = project.recipe['setup']['auth']['user']

    # if credentials are stored in a bucket
    if RE_CREDENTIALS_BUCKET.match(auth):
      credentials = BucketCredentials.from_bucket(auth)

    # if credentials are embeded as JSON
    elif RE_CREDENTIALS_JSON.match(auth):
      return Credentials.from_json_keyfile_dict(
        json.loads(auth),
        scopes or APPLICATION_SCOPES
      )

    # if credentials are local path ( remember this runs as command line )
    else:
      store = Storage(auth)
      credentials = store.get()

      if not credentials or credentials.invalid:
        flow = get_flow(project.recipe['setup']['auth']['client'])
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=['--noauth_local_webserver'])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + auth)

    return credentials

  except (KeyError, ValueError): 
    raise KeyError("Either specify a -u [user credentials path] parameter on the command line or include setup->auth->user->[JSON OR PATH] in the recipe.")


def get_service_credentials(scopes=None):

  try:
    auth = project.recipe['setup']['auth']['service']

    # if credentials are embeded as JSON
    if RE_CREDENTIALS_JSON.match(auth):
      return ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(auth),
        scopes or APPLICATION_SCOPES
      )
  
    # if credentials are local path then check if they exist ( used by command line )
    else:
      return ServiceAccountCredentials.from_json_keyfile_name(
        auth,
        scopes or APPLICATION_SCOPES
      )

  except (KeyError, ValueError): 
    raise KeyError("Either specify a -s [service credentials path] parameter on the command line or include setup->auth->service->[JSON OR PATH] in the recipe.")


#auth = 'user' or 'service'
def get_service(api='gmail', version='v1', auth='service', scopes=None, uri_file=None):
  global SERVICE_CACHE # for some reason looking this up too frequently sometimes errors out

  # Cache service based on:
  # api/version - different API and version
  # auth - different for service or user
  # thread - multiple threads cannot use the same service credentials or headers get confused
  key = api + version + auth + str(threading.current_thread().ident)
  if key not in SERVICE_CACHE:
    credentials = get_service_credentials(scopes) if auth == 'service' else get_credentials()
    http = credentials.authorize(httplib2.Http())
    http.MAX_TOKEN_LIFETIME_SECS = MAX_TOKEN_LIFETIME_SECS

    # if using alterante version ( for example internal )
    if uri_file:
      
      class FakeCache(Cache):
        buffer = {}
        def get(self, url): return self.buffer[url]
        def set(self, url, content): self.buffer[url] = content

      # load local file ( not supported, so faking url to read from cache )
      with open(uri_file, 'r') as cache_file:
        uri = 'http://localhost/dummy'
        cache = FakeCache()
        cache.set(uri, cache_file.read())
        service = discovery.build(api, version, http=http, discoveryServiceUrl=uri, cache_discovery=True, cache=cache)
        
    # normal call to default service version
    else:

      service = discovery.build(api, version, http=http, cache_discovery=False)

    SERVICE_CACHE[key] = service

  return SERVICE_CACHE[key]


def get_client(api='storage', auth='user'):
  '''Translates discovery credentials into client credentials.
  
  Used to connect client API from StarThinker.

  For example:

  ```
    credentials_client = get_client('storage', 'service)
    api = storage.Client(project=project.recipe['setup']['id'], credentials=credentials_client)
  ```
  '''

  credentials_service = get_credentials() if auth == 'user' else get_service_credentials()
  credentials_service.get_access_token() # force acccess refresh check here ( custom client refresh isn't implemented )
                                         # not perect, single job can still time out, may need to write custom BucketClient
  credentials_client = Credentials(
    credentials_service.access_token,
    credentials_service.refresh_token,
    credentials_service.token_uri,
    credentials_service.client_id,
    credentials_service.client_secret
  )
  return credentials_client


def get_profile():
  service = get_service('oauth2', 'v2', 'user')
  return service.userinfo().get().execute()


def set_iam(auth, project_id, role, email=None, service=None):
  service = get_service('cloudresourcemanager', 'v1', auth, ['https://www.googleapis.com/auth/cloud-platform'])
  policy = service.projects().getIamPolicy(resource=project_id, body={}).execute()

  if email: member = 'user:%s' % email
  elif service: member = 'service:%s' % service
  else: member = None

  if member:
    for r in policy['bindings']:
      if r['role'] == role and member not in r['members']:
        if project.verbose: print 'Settings Role:', member, role
        r['members'].append(member)
        policy = service.projects().setIamPolicy(resource=project_id, body={ "policy":policy }).execute()
