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

from starthinker_ui.recipe.scripts import Script
from starthinker_ui.recipe.dag import script_to_dag


class Command(BaseCommand):
  help = 'Generate Templates For Airflow'

  def handle(self, *args, **kwargs):
    for script in Script.get_scripts():
      if script.get_open_source():
        print('Writing: %s_dag.py' % script.get_tag())
        with open(
          '%s/dags/%s_dag.py' % (
            settings.UI_ROOT,
            script.get_tag()
          ),
          'w'
        ) as dag_file:
          dag_file.write(
            script_to_dag(
              script.get_tag(),
              script.get_name(),
              script.get_description(),
              script.get_instructions(),
              script.get_tasks_and_setup()
            )
          )
