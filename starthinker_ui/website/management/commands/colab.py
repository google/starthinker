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
import json
from random import choice

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker.script.parse import json_get_fields, json_set_auths
from starthinker_ui.recipe.scripts import Script

class Colab:

  def __init__(self, name, version="4.0"):
    self.markdown_lines = []
    self.code_lines = []
    self.colab = {
      "license":"Apache License, Version 2.0",
      "copyright":"Copyright 2018 Google Inc.",
      "nbformat": version.split('.', 1)[0],
      "nbformat_minor": version.split('.', 1)[1],
      "metadata": {
        "colab": {
          "name": name,
          "provenance": [],
          "collapsed_sections": [],
          "toc_visible": True
        },
        "kernelspec": {
          "name": "python3",
          "display_name": "Python 3"
        }
      },
      "cells": []
    }


  def _code(self):
    if self.code_lines:
      self.colab['cells'].append({
        "cell_type": "code",
        "metadata": {
          "id": ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(12)]),
          "colab_type": "code"
        },
        "source": self.code_lines
      })
      self.code_lines = []


  def _markdown(self):
    if self.markdown_lines:
      self.colab['cells'].append({
        "cell_type": "markdown",
        "metadata": {
          "id": ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(12)]),
          "colab_type": "text"
        },
        "source": self.markdown_lines
      })
      self.markdown_lines = []


  def code(self, code):
    self._markdown()
    self.code_lines.extend(["%s\n" % c for c in code.split('\n')])


  def header(self, text, level=1, indent=0):
    self._code()
    self.markdown_lines.append("%s%s%s\n" % ('>' * indent, '#' * level, text))


  def paragraph(self, text, indent=0):
    self._code()
    self.markdown_lines.extend(["%s%s\n" % ('>' * indent, t) for t in text.split('\n')])


  def image(self, name, link):
    self._code()
    self.markdown_lines.append('![%s](%s)\n' % (name, link))


  def list(self, items, ordered=True, indent=0):
    self._code()
    self.markdown_lines.extend(["%s %s %s\n" % ('>' * indent, '1.' if ordered else '*', t) for t in items])


  def render(self):
    self._code()
    self._markdown()
    return json.dumps(self.colab, indent=2)


class Command(BaseCommand):
  help = 'Generate Templates For Colab'

  def handle(self, *args, **kwargs):
     
    with open('%s/tutorials/deploy_colab.md' % settings.UI_ROOT, 'w') as readme_file:
      readme_file.write('# Using Scripts As A Colab Notebook\n')
      readme_file.write('\n')
      readme_file.write('All StarThinker recipes and solutions can be run from Google\'s Collaboratory.\n')
      readme_file.write('Click the link below or visit the [Solution Gallery](https://google.github.io/starthinker/) to deploy a notebook.\n')
      readme_file.write('\n')
      readme_file.write('## List Of Notebooks\n')

      for script in Script.get_scripts():
        if script.get_open_source():
          readme_file.write('* [%s](%s) - %s\n' % (script.get_name(), script.get_link_colab(), script.get_description()))

      readme_file.write('---\n')
      readme_file.write('&copy; 2019 Google Inc. - Apache License, Version 2.0\n')

    for script in Script.get_scripts():
      if script.get_open_source():

        colab = Colab(script.get_name())

        colab.header("1. Install Dependencies")
        colab.paragraph("First install the libraries needed to execute recipes, this only needs to be done once, then click play.")
        colab.code("!pip install git+https://github.com/google/starthinker")

        colab.header("2. Get Cloud Project ID")
        colab.paragraph("To run this recipe [requires a Google Cloud Project](https://github.com/google/starthinker/blob/master/tutorials/cloud_client_installed.md), this only needs to be done once, then click play.")
        #colab.image('Client Project ID', 'https://github.com/google/starthinker/raw/master/tutorials/images/cloud_client_installed.png')
        colab.code('CLOUD_PROJECT = \'PASTE PROJECT ID HERE\'')
        colab.code('\nprint("Cloud Project Set To: %s" % CLOUD_PROJECT)')

        colab.header("3. Get Client Credentials")
        #colab.image('Client Credentials', 'https://github.com/google/starthinker/raw/master/tutorials/images/cloud_client_installed.png')
        colab.paragraph('To read and write to various endpoints requires [downloading client credentials](https://github.com/google/starthinker/blob/master/tutorials/cloud_client_installed.md), this only needs to be done once, then click play.')
        colab.code('CLIENT_CREDENTIALS = \'PASTE CREDENTIALS HERE\'')
        colab.code('\nprint("Client Credentials Set To: %s" % CLIENT_CREDENTIALS)')

        colab.header('4. Enter %s Parameters' % script.get_name())
        colab.paragraph(script.get_description())
        colab.list(script.get_instructions())
        colab.paragraph('Modify the values below for your use case, can be done multiple times, then click play.')

        fields = json_get_fields(script.get_tasks())
        colab.code('FIELDS = {')
        for field in fields:

          if field['kind'] in ('string', 'email', 'text'):
            value = '"%s"' % field.get('default', '') 
          elif field['kind'] in ('integer', 'boolean'):
            value = field.get('default', 'None') 
          elif field['kind'] in ('choice', 'integer_list', 'string_list'):
            value = field.get('default', '[]') 
          elif field['kind'] in ('json'):
            value = field.get('default', '{}') 
          elif field['kind'] == 'timezone':
            value = field.get('default', 'America/Phoenix') 
            field['description'] = '%s https://github.com/google/starthinker/blob/master/starthinker_ui/ui/timezones.py' % field.get('description', '')
          else:
            raise NotImplementedError("%s is not a suported field type" % field)

          if 'description' in field: 
            colab.code('  "%s":%s, # %s' % (field['name'], value, field['description']))
          else:
            colab.code('  "%s":%s,' % (field['name'], field.get('default')))

        colab.code('}')
        colab.code('\nprint("Parameters Set To: %s" % FIELDS)')

        colab.header('4. Execute %s' % script.get_name())
        colab.paragraph('This does NOT need to be modified unles you are changing the recipe, click play.')
        colab.code('''from starthinker.util.project import project
from starthinker.script.parse import json_set_fields

USER_CREDENTIALS = '/content/user.json'

TASKS = %s

json_set_fields(TASKS, FIELDS)

project.initialize(_recipe={ 'tasks':TASKS }, _project=CLOUD_PROJECT, _user=USER_CREDENTIALS, _client=CLIENT_CREDENTIALS, _verbose=True)
project.execute()''' % json.dumps(json_set_auths(script.get_tasks(), 'user'), indent=2))

        with open('%s/colab/%s.ipynb' % (settings.UI_ROOT, script.get_tag()), 'w') as colab_file:
          colab_file.write(colab.render())
