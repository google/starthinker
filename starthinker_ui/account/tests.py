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

from starthinker.util.configuration import Configuration
from starthinker.util.auth import clear_credentials_cache, get_credentials, get_service
from starthinker.config import UI_CLIENT, UI_SERVICE
from starthinker_ui.account.models import Account

UI_USER = os.environ.get('STARTHINKER_USER', '')


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
    self.user_file = '/tmp/test_user.json'
    self.service_file = '/tmp/test_service.json'
    self.config = Configuration(service=self.service_file, user=self.user_file)
    shutil.copyfile(UI_USER, self.user_file)
    shutil.copyfile(UI_SERVICE, self.service_file)

  def tearDown(self):
    os.remove(self.user_file)
    os.remove(self.service_file)

  def helper_refresh(self):
    credentials = get_credentials(self.config, 'user')
    token = credentials.token
    expiry = credentials.expiry

    # wait a bit before refreshing token, multiple tests go too fast and same token is returned
    sleep(1)

    # test refresh ( not expired cache, not expired file )
    credentials.refresh()
    self.assertEqual(token, credentials.token)
    self.assertEqual(expiry, credentials.expiry)

    # wait a bit before refreshing token, multiple tests go too fast and same token is returned
    sleep(1)

    # test refresh ( expired cache, not expired file )
    credentials.expiry = (datetime.now() - timedelta(days=5))
    credentials.refresh()
    self.assertEqual(token, credentials.token)
    self.assertEqual(expiry, credentials.expiry)

    # wait a bit before refreshing token, multiple tests go too fast and same token is returned
    sleep(1)

    # test refresh ( expired cache, expired file )
    credentials.expiry = (datetime.now() - timedelta(days=5))
    credentials.save()
    credentials.refresh()
    self.assertNotEqual(token, credentials.token)
    self.assertNotEqual(expiry, credentials.expiry)

  def test_file_credentials_user(self):
    config = Configuration(user=self.user_file)
    service = get_service(config, 'oauth2', 'v2', 'user')
    response = service.userinfo().get().execute()

    self.assertIn('email', response)
    self.helper_refresh()

  def test_file_credentials_service(self):
    config = Configuration(service=self.service_file)
    service = get_service(config, 'cloudresourcemanager', 'v1', 'service')
    response = service.projects().list().execute()

    self.assertIn('projects', response)

  def test_string_credentials_user(self):
    with open(self.user_file, 'r') as json_file:
      config = Configuration(user=json_file.read())

    service = get_service(config, 'oauth2', 'v2', 'user')
    response = service.userinfo().get().execute()

    self.assertIn('email', response)
    self.helper_refresh()

  def test_string_credentials_service(self):
    with open(self.service_file, 'r') as json_file:
      config = Configuration(service=json_file.read())

    service = get_service(config, 'cloudresourcemanager', 'v1', 'service')
    response = service.projects().list().execute()

    self.assertIn('projects', response)

  def test_dictionary_credentials_user(self):
    with open(self.user_file, 'r') as json_file:
      config = Configuration(user=json.load(json_file))

    service = get_service(config, 'oauth2', 'v2', 'user')
    response = service.userinfo().get().execute()

    self.assertIn('email', response)
    self.helper_refresh()

  def test_dictionary_credentials_service(self):
    with open(self.service_file, 'r') as json_file:
      config = Configuration(service=json.load(json_file))

    service = get_service(config, 'cloudresourcemanager', 'v1', 'service')
    response = service.projects().list().execute()

    self.assertIn('projects', response)

  def test_remote_credentials_user(self):
    config = Configuration(user=self.user_file)
    credentials = get_credentials(config, 'user')
    account = Account.objects.get_or_create_user(credentials, 'password')

    clear_credentials_cache()

    config = Configuration(user=account.get_credentials_path())
    self.assertEqual(config.recipe['setup']['auth']['user'], account.get_credentials_path())

    service = get_service(config, 'oauth2', 'v2', 'user')
    response = service.userinfo().get().execute()

    self.assertIn('email', response)
    self.helper_refresh()
