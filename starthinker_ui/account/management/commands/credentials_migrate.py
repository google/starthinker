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

import base64
import jsonpickle
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import encoding

from starthinker.util.project import project
from starthinker.util.auth import get_profile
from starthinker.util.auth.wrapper import CredentialsUserWrapper
from starthinker.util.auth.storage import _credentials_storage_service
from starthinker_ui.account.models import Account

LEGACY_BUCKET_PREFIX = settings.UI_PROJECT.split(':', 1)[-1] # remove domain: part

def legacy_credentials_path(identifier):
  return '%s:ui/%s.json' % (LEGACY_BUCKET_PREFIX + "-starthinker-users", identifier)

def legacy_auth_decode(value):
  return jsonpickle.decode(base64.b64decode(encoding.smart_bytes(value)))

def legacy_credentails_get(cloud_path):
  service = _credentials_storage_service()
  bucket, filename = cloud_path.split(':',1)
  data = service.objects().get_media(bucket=bucket, object=filename).execute()
  return legacy_auth_decode(data)


class Command(BaseCommand):
  help = 'Migrate credentials to new format.'

  def add_arguments(self, parser):
    parser.add_argument(
      '--test',
      action='store_true',
      dest='test',
      default=False,
      help='Test conversion.',
    )

  def handle(self, *args, **kwargs):
    
    # loop through accounts
    for account in Account.objects.all():
      print('CONVERTING', account.email)

      try:
        # load legacy credentials
        credentials = legacy_credentails_get(legacy_credentials_path(account.identifier))

        # convert to new format
        new_credentials = CredentialsUserWrapper(credentials)

        # save new credentials
        account.set_credentials(new_credentials)

        if kwargs['test']:
          project.initialize(_user=account.get_credentials_path())
          profile = get_profile()
          print(profile)
          exit()

      except Exception as e:
        print(str(e))
