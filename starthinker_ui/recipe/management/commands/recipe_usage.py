###########################################################################
#
#  Copyright 2022 Google LLC
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

class Command(BaseCommand):
  help = 'Prints recipe count and age by account.'

  def handle(self, *args, **kwargs):
    usage = []

    for account in Account.objects.all():
      usage.append({
        'email':account.email,
        'recipes':list(account.recipe_set.all().values_list('birthday', flat=True))
      })

    usage.sort(key=lambda u: len(u['recipes']), reverse=True)

    for u in usage:
      print ('{}, {}, {}'.format(u['email'], len(u['recipes']), max(u['recipes']) if u['recipes'] else ''))
