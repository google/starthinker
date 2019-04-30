###########################################################################
# 
#  Copyright 2019 Google Inc.
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
from django.test import TestCase

from starthinker.util.project import project
from starthinker.util.auth import get_profile, get_credentials
from starthinker_ui.account.models import  Account


def account_create():
  UI_CLIENT = os.environ.get('STARTHINKER_CLIENT_INSTALLED', 'MISSING RUN deploy.sh TO SET')
  UI_SERVICE = os.environ.get('STARTHINKER_SERVICE', 'MISSING RUN deploy.sh TO SET')
  UI_USER = os.environ.get('STARTHINKER_USER', 'MISSING RUN deploy.sh TO SET')

  project.initialize(_client=UI_CLIENT, _service=UI_SERVICE, _user=UI_USER)
  credentials = get_credentials()
  profile = get_profile()

  account = Account.objects.create_user(profile, credentials, 'password')
