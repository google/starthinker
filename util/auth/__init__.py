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
import json
import httplib2
import pprint

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery, storage
from google.oauth2.credentials import Credentials

from util.project import project
from util.auth.google_bucket_auth import BucketCredentials

from setup import CLOUD_SERVICE

APPLICATION_NAME = 'StarThinker Client'
SCOPES = [
  'https://www.googleapis.com/auth/userinfo.profile', # must be first for manager login
  'https://www.googleapis.com/auth/userinfo.email', # must be first for manager login
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/gmail.send', 
  'https://www.googleapis.com/auth/doubleclickbidmanager',
  'https://www.googleapis.com/auth/cloudplatformprojects',
  'https://www.googleapis.com/auth/devstorage.full_control',
  'https://www.googleapis.com/auth/bigquery',
  'https://www.googleapis.com/auth/dfareporting',
  'https://www.googleapis.com/auth/dfatrafficking',
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/doubleclicksearch'
]
SERVICE_CACHE = {}


def get_credentials():

  # if credentials are UI generated ( remember this runs as worker )
  if project.configuration['setup']['auth'].get('source', 'local') == 'ui':
    credentials = BucketCredentials.from_bucket(project.configuration['setup']['auth']['user'])

  # if credentials are UI generated ( remember this runs as worker )
  elif project.configuration['setup']['auth'].get('source', 'local') == 'remote':
    credentials = BucketCredentials.from_bucket(project.configuration['setup']['auth']['user'])

  # if credentials are local path ( remember this runs as command line )
  else:
    credential_path = project.configuration['setup']['auth']['user']
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(project.configuration['setup']['auth']['client'], SCOPES)
      flow.user_agent = APPLICATION_NAME
      flags = tools.argparser.parse_args(args=['--noauth_local_webserver'])
      credentials = tools.run_flow(flow, store, flags)
      print('Storing credentials to ' + credential_path)

  return credentials


def get_service_credentials(scopes=None):

  # if credentials are embeded as JSON ( used by ui )
  if project.configuration['setup']['auth'].get('source', 'local') == 'ui':
    return ServiceAccountCredentials.from_json_keyfile_dict(
      json.loads(project.configuration['setup']['auth']['service']),
      scopes or SCOPES)

  # if credentials are local path then check if they exist ( used by command line )
  else:
    return ServiceAccountCredentials.from_json_keyfile_name(
      project.configuration['setup']['auth']['service'],
      scopes or SCOPES)

#auth = 'user' or 'service'
def get_service(api='gmail', version='v1', auth='service', scopes=None):
  global SERVICE_CACHE # for some reason looking this up too frequently sometimes errors out

  # FIX: does not work in threads, need to add pool specifier to key?
  key = api + version + auth
  if key not in SERVICE_CACHE:
    credentials = get_service_credentials(scopes) if auth == 'service' else get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(api, version, http=http)
    SERVICE_CACHE[key] = service

  return SERVICE_CACHE[key]


def get_client(api='storage', auth='user'):
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
  if api == 'storage': return storage.Client(project=project.configuration['setup']['id'], credentials=credentials_client)
  elif api == 'bigquery': return bigquery.Client(project=project.configuration['setup']['id'], credentials=credentials_client)
  else: return None


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
