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
import json
import shutil
from time import sleep
from datetime import datetime, timedelta
from django.test import TestCase

from starthinker.util.auth import get_credentials, get_service
from starthinker.util.configuration import Configuration
from starthinker.util.storage import bucket_create, object_delete
from starthinker.util.secret_manager import SecretManager
from starthinker.config import UI_PROJECT, UI_ZONE, UI_CLIENT, UI_SERVICE
from starthinker_ui.account.models import Account


UI_USER = os.environ.get('STARTHINKER_USER', '')
USER_BUCKET = '%s-starthinker-credentials' % UI_PROJECT.replace(':', '-')
USER_LOCATION = UI_ZONE.rsplit('-', 1)[0]  # take only region part of zone
USER_STORAGE = '%s:ui/%s.json' % (USER_BUCKET, 'test_user')
USER_SECRET = 'secret://123'
USER_FILE = '/tmp/test_user.json'
SERVICE_FILE = '/tmp/test_service.json'


def account_create():

  accounts = Account.objects.all()
  if len(accounts) > 0:
    account = accounts[0]
  else:
    config = Configuration(client=UI_CLIENT, user=UI_USER)
    credentials = get_credentials(config, 'user')
    account = Account.objects.get_or_create_user(credentials, 'password')

  return account


class CredentialsTest(TestCase):

  def setUp(self):
    shutil.copyfile(UI_USER, USER_FILE)
    shutil.copyfile(UI_SERVICE, SERVICE_FILE)

    # make sure credentials are fresh for all tests, many tests assume token is valid to start
    get_credentials(Configuration(user=USER_FILE), 'user').refresh()


  def tearDown(self):
    os.remove(USER_FILE)
    os.remove(SERVICE_FILE)


  def helper_api(self, config):
    service = get_service(config, 'oauth2', 'v2', 'user')
    response = service.userinfo().get().execute()
    self.assertIn('email', response)


  def helper_refresh(self, config):
    # test use of configuration
    self.helper_api(config)

    credentials = get_credentials(config, 'user')
    token = credentials.token
    expiry = credentials.expiry

    # wait a bit before refreshing token, multiple tests go too fast and same token is returned
    sleep(1)

    #print(token, expiry)

    # test refresh ( not expired cache, not expired file )
    credentials.refresh()
    self.assertEqual(token, credentials.token)
    self.assertEqual(expiry, credentials.expiry)

    # test after refresh
    self.helper_api(config)

    # wait a bit before refreshing token, multiple tests go too fast and same token is returned
    sleep(1)

    # test refresh ( expired cache, not expired file )
    credentials.expiry = (datetime.now() - timedelta(days=5))
    credentials.refresh()
    self.assertEqual(token, credentials.token)
    self.assertEqual(expiry, credentials.expiry)

    # test after refresh
    self.helper_api(config)

    # wait a bit before refreshing token, multiple tests go too fast and same token is returned
    sleep(1)

    # test refresh ( expired cache, expired file )
    credentials.expiry = (datetime.now() - timedelta(days=5))
    credentials.save()
    credentials.refresh()
    self.assertNotEqual(token, credentials.token)
    self.assertNotEqual(expiry, credentials.expiry)

    # test after refresh
    self.helper_api(config)


  def test_file_credentials_user(self):
    config = Configuration(user=USER_FILE)
    self.helper_refresh(config)


  def test_file_credentials_service(self):
    config = Configuration(service=SERVICE_FILE)
    service = get_service(config, 'cloudresourcemanager', 'v1', 'service')
    response = service.projects().list().execute()
    self.assertIn('projects', response)


  def test_string_credentials_user(self):
    with open(USER_FILE, 'r') as json_file:
      config = Configuration(user=json_file.read())
    self.helper_refresh(config)


  def test_string_credentials_service(self):
    with open(SERVICE_FILE, 'r') as json_file:
      config = Configuration(service=json_file.read())

    # cannot use helper for service
    service = get_service(config, 'cloudresourcemanager', 'v1', 'service')
    response = service.projects().list().execute()
    self.assertIn('projects', response)


  def test_dictionary_credentials_user(self):
    with open(USER_FILE, 'r') as json_file:
      config = Configuration(user=json.load(json_file))
    self.helper_refresh(config)


  def test_storage_credentials_user(self):

    # create bucket
    config_service = Configuration(service=UI_SERVICE, project=UI_PROJECT)
    bucket_create(config_service, 'service', UI_PROJECT, USER_BUCKET, USER_LOCATION)

    # load file credentials and save to storage bucket
    config_file = Configuration(user=USER_FILE)
    credentials = get_credentials(config_file, 'user')
    credentials.save(USER_STORAGE)

    # use configuration
    config = Configuration(user=USER_STORAGE)
    self.helper_refresh(config)

    # clean up storage credentials
    object_delete(config_service, 'service', USER_STORAGE)


  def test_secret_credentials_user(self):

    # load file credentials and save to secret manager
    config_file = Configuration(user=USER_FILE)
    credentials = get_credentials(config_file, 'user')
    credentials.save(USER_SECRET)

    #print('DOWNLOAD EXISTING SECRET', SecretManager(
    #  Configuration(
    #    service=UI_SERVICE,
    #    project=UI_PROJECT
    #  ),
    #  'service'
    #  ).access(
    #    UI_PROJECT,
    #    USER_SECRET.replace('secret://', '')
    #  )
    #)

    # use configuration
    config = Configuration(user=USER_SECRET)
    self.helper_refresh(config)

    # clean up secret credentials
    SecretManager(
      Configuration(
        service=UI_SERVICE,
        project=UI_PROJECT
      ),
      'service'
    ).delete(
       UI_PROJECT,
       USER_SECRET.replace('secret://', '')
    )


  def test_dictionary_credentials_service(self):
    with open(SERVICE_FILE, 'r') as json_file:
      config = Configuration(service=json.load(json_file))

    service = get_service(config, 'cloudresourcemanager', 'v1', 'service')
    response = service.projects().list().execute()

    self.assertIn('projects', response)


  def test_ui_credentials_user(self):
    config = Configuration(user=USER_FILE)
    credentials = get_credentials(config, 'user')
    account = Account.objects.get_or_create_user(credentials, 'password')

    config = Configuration(user=account.get_credentials_path())
    self.assertEqual(config.recipe['setup']['auth']['user'], account.get_credentials_path())
    self.helper_refresh(config)
