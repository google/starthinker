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

import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker_ui.recipe.models import Recipe


class Command(BaseCommand):
  help = 'Moves database recipes to json files or pub/sub topic'

  def add_arguments(self, parser):
    parser.add_argument(
        '--remote',
        action='store_true',
        dest='remote',
        default=False,
        help='Run jobs remotely using pub sub.',
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

    for recipe in (Recipe.objects.filter(pk=kwargs['recipe'])
                   if kwargs['recipe'] else Recipe.objects.filter(active=True)):
      try:
        if kwargs['remote']:
          print('Dispatch: %s' % recipe.uid())
          if kwargs['force']:
            recipe.force()
        elif settings.UI_CRON:
          print('Write: %s/recipe_%d.json' % (settings.UI_CRON, recipe.pk))
          with open(settings.UI_CRON + '/recipe_%d.json' % recipe.pk, 'w') as f:
            f.write(json.dumps(recipe.get_json()))
        else:
          raise Exception('Neither UI_CRON configured nor remote specified.')

      except (KeyboardInterrupt, SystemExit):
        raise

      except Exception as e:
        print('DEPLOY ERROR:', str(e))
