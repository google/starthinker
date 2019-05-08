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

import os

from django.core.management.base import BaseCommand, CommandError

from starthinker_ui.recipe.scripts import Script
from website.views import code, solutions, solution


class Command(BaseCommand):
  help = 'Generate HTML For GitHub'

  def add_arguments(self, parser):
    parser.add_argument(
      '--path',
      action='store',
      dest='path',
      required=True,
      help='Open Source Directory',
    )

  def handle(self, *args, **kwargs):
    
    print 'Writing:', kwargs['path']

    with open(kwargs['path'] + '/docs/index.html', 'w') as index_file:
      index_file.write(solutions(request=None))

    with open(kwargs['path'] + '/docs/code.html', 'w') as code_file:
      code_file.write(code(request=None))

    for s in Script.get_scripts():
      if s.is_solution() and s.get_open_source():
        os.mkdir('%s/docs/%s/' % (kwargs['path'], s.get_tag()))
        with open('%s/docs/%s/index.html' % (kwargs['path'], s.get_tag()), 'w') as solution_file:
          solution_file.write(solution(request=None, tag=s.get_tag()))
