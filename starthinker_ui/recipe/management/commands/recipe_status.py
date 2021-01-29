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
from django.core import serializers


class Command(BaseCommand):
  help = 'Shows status of recipes'

  def add_arguments(self, parser):
    parser.add_argument(
        '--recipe',
        action='store',
        dest='recipe',
        default=None,
        help='Run a specific recipe.',
    )

    parser.add_argument(
        '--raw',
        action='store_true',
        dest='raw',
        default=False,
        help='Raw recipe log.',
    )

  def handle(self, *args, **kwargs):
    for recipe in (Recipe.objects.filter(
        pk=kwargs['recipe']) if kwargs['recipe'] else Recipe.objects.all()):
      status = json.loads(recipe.job_status)

      print('---------------------------------------')
      print('Name:', recipe.name)
      print('Account:', recipe.account.email)
      print('UUID:', recipe.uid())
      print('Reference:', recipe.reference)
      print('Active:', recipe.active)
      print('Week:', recipe.week)
      print('Hour:', recipe.hour)
      print('Timezone:', recipe.timezone)
      print('Manual:', recipe.manual)
      print('Done:', all(task['done'] for task in status['tasks']))

      if kwargs['raw']:
        print('Job Status:')
        print(json.dumps(status), indent=2)
        continue

      log = recipe.get_log()

      print('Tasks', len(log['tasks']))
      print('UTC', log['utc'])
      print('AGO', log['ago'])
      print('PK:', recipe.pk)
      print('Date Timezone', log['date_tz'])
      print('Forced', log.get('forced', False))
      print('Status', log['status'])
      print('Worker:', recipe.worker_uid)

      for task in log['tasks']:
        print('  ----------------')
        print('  Utc', task['utc'])
        print('  Ago', task['ago'])
        print('  Script', task['script'])
        print('  Instance', task['instance'])
        print('  Hour', task['hour'])
        print('  Event', task['event'])
        print('  Done', task['done'])
        print('  Output', task['stdout'])
        print('  Error', task['stderr'])
        print('')

      task = recipe.get_task()
      print('Next Task', task)
