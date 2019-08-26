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

import getpass

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker.util.project import project
from starthinker.util.auth import get_profile, get_credentials
from starthinker_ui.account.models import Account
from starthinker_ui.project.models import Project
from starthinker_ui.recipe.models import Recipe


class Command(BaseCommand):
  help = 'Add user credentials to master account.'

  def add_arguments(self, parser):
    parser.add_argument(
      '--user',
      action='store',
      dest='user',
      default=None,
      help='Path to user credentials.',
    )

    parser.add_argument(
      '--password',
      action='store',
      dest='password',
      default=None,
      help='Login password for account.',
    )

    parser.add_argument(
      '--write',
      action='store_true',
      dest='write',
      default=False,
      help='Safety check for a dangerous operation.',
    )

  def handle(self, *args, **kwargs):
    
    if kwargs.get('write'):

      # create or update master account credentials from installed user credentials
      project.initialize(_user=kwargs['user'])

      # if password not given on command line, ask for it inline
      if not kwargs.get('password'):
        print('Enter password for UI account access ( DO NOT USE YOUR GSUITE PASSWORD ):')
        kwargs['password'] = getpass.getpass()

      account = Account.objects.get_or_create_user(get_profile(), get_credentials(), kwargs['password'])

      # move all recipes to this account and remove all other accounts ( there can be ONLY one )
      #Project.objects.exclude(account=account).update(account=account)
      #Recipe.objects.exclude(account=account).update(account=account)
      #Account.objects.exclude(pk=account.pk).delete()

      print 'ACCOUNT SET UP:', account.email 

    else:
      print '\nDANGER: Use only with the Data Scientist Setup. This will...'
      print ' - Overwrite the users credentials with local credentials.'
      print ''
