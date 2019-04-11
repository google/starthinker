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

from website.views import code

class Command(BaseCommand):
  help = 'Generate Code HTML'

  def add_arguments(self, parser):
    parser.add_argument(
      '--filename',
      action='store',
      dest='filename',
      required=True,
      help='HTML file to create.',
    )

  def handle(self, *args, **kwargs):
    
    print 'Writing:', kwargs['filename']

    with open(kwargs['filename'], 'w') as index_file:
      index_file.write(code(request=None))
