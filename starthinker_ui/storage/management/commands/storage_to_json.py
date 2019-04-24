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


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker_ui.account.models import Account
from starthinker_ui.storage.models import storage_list, storage_run


class Command(BaseCommand):
  help = 'Moves storage recipes to json files for cron consumption'

  def add_arguments(self, parser):
    parser.add_argument(
      '--remote',
      action='store_true',
      dest='remote',
      default=False,
      help='Run jobs remotely using pub sub.',
    )

    parser.add_argument(
      '--account',
      action='store',
      dest='account',
      default=None,
      help='Run a specific account.',
    )

    parser.add_argument(
      '--recipe',
      action='store',
      dest='recipe',
      default=None,
      help='Run a specific recipe.',
    )

    parser.add_argument(
      '--force',
      action='store_true',
      dest='force',
      default=False,
      help='Force execution regardless of schedule.',
    )


  def handle(self, *args, **kwargs):
    
    for account in Account.objects.filter(pk=kwargs['account']) if kwargs['account'] else Account.objects.all():
      for recipe in storage_list(account):
        try:
          # skip all others if recipe specified
          if kwargs['recipe'] and kwargs['recipe'] != recipe.name: continue

          if kwargs['remote']: print 'Dispatch: %s' % recipe.name
          else: print 'Write: %s/storage_%d_%s' % (settings.UI_CRON, account.pk, recipe.name)

          storage_run(account, recipe.name, force=kwargs['force'], topic=settings.UI_TOPIC if kwargs['remote'] else '')

        except (KeyboardInterrupt, SystemExit):
          raise
        except Exception, e:
          print 'DEPLOY ERROR:', str(e)
