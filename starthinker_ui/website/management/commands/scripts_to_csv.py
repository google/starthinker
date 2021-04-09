###########################################################################
#
#  Copyright 2021 Google LLC
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

from starthinker_ui.recipe.scripts import Script
from starthinker.util.csv import rows_to_csv

class Command(BaseCommand):
  """ Command used to generate a simple list of solutions.

  Nothing depends on this, just a quick implementation, feel
  free to pivot as necessary.

  Current version returns a CSV with:
    - Name
    - Description
    - Global
    - Product List
    - Owners List
    - Year Active
    - Status
    - Link ( local, may need to regexp into production after running )

  Call without arguments using: python manage.py scripts_to_csv

  """

  help = 'Generate CSV Of Scripts'

  def get_scripts(self):
    for script in Script.get_scripts():
      yield (
        script.get_name(), # solution
        script.get_description().replace('"', '\''), # description
        'Global', # region
        ', '.join(script.get_products()), # entity
        ', '.join(x.replace('@google.com', '') for x in script.get_authors()), # POC
        '%s - current' % script.get_released().year, # year
        script.get_status() or 'Live', # status
        script.get_link(), # link
      )

  def handle(self, *args, **kwargs):
    print(rows_to_csv(self.get_scripts()).read())
