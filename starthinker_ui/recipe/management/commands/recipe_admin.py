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

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker_ui.recipe.models import Recipe


class Command(BaseCommand):
  help = 'Perform admin operations on recipes'

  def add_arguments(self, parser):
    parser.add_argument(
        '--recipe',
        action='store',
        dest='recipe',
        default=None,
        help='Run a specific recipe.',
    )

    parser.add_argument(
        '--activate',
        action='store_true',
        dest='activate',
        default=False,
        help='Activate specified recipe.',
    )

    parser.add_argument(
        '--deactivate',
        action='store_true',
        dest='deactivate',
        default=False,
        help='Deactivate specified recipe.',
    )

  def handle(self, *args, **kwargs):
    for recipe in (Recipe.objects.filter(pk=kwargs['recipe'])
                   if kwargs['recipe'] else Recipe.objects.filter(active=True)):
      try:
        if kwargs['activate'] == kwargs['deactivate']:
          raise Exception(
              'Specify one of the supported flags --activate or --deactivate')
        elif kwargs['activate']:
          recipe.activate()
        elif kwargs['deactivate']:
          recipe.deactivate()
        else:
          raise Exception('Unexpected exception')

        print('---------------------------------------')
        print('Name:', recipe.name)
        print('Account:', recipe.account.email)
        print('UUID:', recipe.uid())
        print('Reference:', recipe.reference)
        print('Active:', recipe.active)
        print('Week:', recipe.week)
        print('Hour:', recipe.hour)
        print('Timezone:', recipe.timezone)
        print('---------------------------------------')

      except (KeyboardInterrupt, SystemExit):
        raise

      except Exception as e:
        print('DEPLOY ERROR:', str(e))
