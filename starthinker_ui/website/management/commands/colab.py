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

from starthinker.tool.colab import recipe_to_colab
from starthinker_ui.recipe.scripts import Script


class Command(BaseCommand):
  help = 'Generate Templates For Colab'

  def handle(self, *args, **kwargs):

    with open('%s/tutorials/deploy_colab.md' % settings.UI_ROOT,
              'w') as readme_file:
      readme_file.write('# Using Scripts As A Colab Notebook\n')
      readme_file.write('\n')
      readme_file.write(
          'All StarThinker recipes and solutions can be run from [Google Collaboratory](https://colab.research.google.com/github/google/starthinker/blob/master). '
      )
      readme_file.write(
          'Also visit the [Solution Gallery](google.github.io/starthinker/) or click a link below to deploy a notebook.\n'
      )
      readme_file.write('\n')
      readme_file.write('## List Of Notebooks\n')

      for script in Script.get_scripts():
        if script.get_tag() in ['airflow']: continue
        if script.get_open_source():
          readme_file.write('* [%s](%s) - %s\n' %
                            (script.get_name(), script.get_link_colab(),
                             script.get_description()))

      readme_file.write('---\n')
      readme_file.write(
          '&copy; 2019 Google LLC - Apache License, Version 2.0\n')

    for script in Script.get_scripts():
      if script.get_tag() in ['airflow']: continue
      if script.get_open_source():
        print('Writing: %s/colabs/%s.ipynb' %
              (settings.UI_ROOT, script.get_tag()))
        with open('%s/colabs/%s.ipynb' % (settings.UI_ROOT, script.get_tag()),
                  'w') as colab_file:
          colab_file.write(
              recipe_to_colab(
                  script.get_name(),
                  script.get_description(),
                  script.get_instructions(),
                  script.get_tasks(),
              ))
