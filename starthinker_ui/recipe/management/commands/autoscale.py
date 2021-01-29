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

from starthinker_ui.recipe.views import autoscale
from starthinker_ui.recipe.models import Recipe, utc_milliseconds, JOB_LOOKBACK_MS


class Command(BaseCommand):
  help = 'Autoscale workers.'

  def handle(self, *args, **kwargs):
    print(json.dumps(json.loads(autoscale(None).content), indent=2))

    for recipe in Recipe.objects.filter(
        active=True, job_utm__lt=utc_milliseconds()).exclude(job_utm=0):
      print(recipe.id, recipe.name, recipe.get_days())
      print('---')

    for recipe in Recipe.objects.filter(
        active=True, worker_utm__gte=utc_milliseconds() - JOB_LOOKBACK_MS):
      print(recipe.id, recipe.name, recipe.worker_uid)
