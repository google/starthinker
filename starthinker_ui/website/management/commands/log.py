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
from django.template.loader import render_to_string

from starthinker_worker.log import log_get

class Command(BaseCommand):
  help = 'Render Log HTML'

  def add_arguments(self, parser):
    parser.add_argument(
      '--recipe',
      action='store',
      dest='recipe',
      required=True,
      help='Recipe to pull log for.',
    )

  def handle(self, *args, **kwargs):
    log = log_get(kwargs['recipe'])
    print render_to_string('log.html', { 'log':log })
