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
  help = 'Replace task or field in recipes with new value.'

  def add_arguments(self, parser):
    parser.add_argument(
        '--task',
        action='store',
        dest='task',
        default=None,
        help='Task to edit.',
    )

    parser.add_argument(
        '--field',
        action='store',
        dest='field',
        default=None,
        help='Task to edit.',
    )

    parser.add_argument(
        '--replacement',
        action='store',
        dest='replacement',
        default=None,
        help='Key to replace with.',
    )

    parser.add_argument(
        '--write',
        action='store_true',
        dest='write',
        default=False,
        help='Key to replace with.')

  def handle(self, *args, **kwargs):
    for recipe in (Recipe.objects.all()):

      print('---------------------------------------')
      print('Name:', recipe.name)
      print('Account:', recipe.account.email)

      changed = False
      tasks = json.loads(recipe.tasks)

      if kwargs['replacement']:
        for task in tasks:
          if kwargs['field']:
            if kwargs['field'] in task['values']:
              task['values'][kwargs['replacement']] = task['values'][
                  kwargs['field']]
              del task['values'][kwargs['field']]
              changed = True
          else:
            if task['tag'] == kwargs['task']:
              task['tag'] = kwargs['replacement']
              changed = True

      if changed:
        print('OLD TASK', recipe.tasks)
        print('NEW TASK', tasks)
        if kwargs['write']:
          recipe.set_values(tasks)
          recipe.save(update_fields=['tasks'])
