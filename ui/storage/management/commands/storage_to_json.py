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


import json
import pprint

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker.ui.ui.pubsub import send_message
from starthinker.ui.account.models import Account
from starthinker.ui.storage.models import storage_list, storage_get


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
      '--json',
      action='store',
      dest='json',
      default=None,
      help='Run a specific json.',
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

        # skip all others if recipe specified
        if kwargs['json'] and kwargs['json'] != recipe.name: continue

        try:
          data = storage_get(account, recipe.name)
        
          print 'FILENAME:', recipe.filename_local
          #pprint.PrettyPrinter().pprint(data)
  
          # force by stripping time from setup
          if kwargs['force']:
            if 'day' in data['setup']: del data['setup']['day']
            if 'hour' in data['setup']: del data['setup']['hour']
          else:
            print "HAS SCHEDULE ( --force removes )"
  
          # run the recipe using pub sub
          if kwargs['remote']:
            print 'EXECUTE REMOTE'
            print send_message(settings.UI_PROJECT, settings.UI_TOPIC, json.dumps(data))
  
          # save the recipe to a local file
          else:
            with open(recipe.filename_local, 'w') as outfile:
              json.dump(data, outfile)

        except Exception, e:
          print 'JSON ERROR', str(e)
