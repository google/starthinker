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
import re
import json
from copy import deepcopy

from django.conf import settings

from starthinker.config import EXECUTE_PATH
from starthinker.script.parse import json_set_fields, json_set_instructions, json_set_description
from starthinker.util.project import get_project

RE_SCRIPT = re.compile(r'^script_.*\.json$')

# cache scripts and authors in memory
AUTHORS = {}
SCRIPTS = {}
for root, dirs, files in os.walk(EXECUTE_PATH):
  for filename in files:
    if RE_SCRIPT.match(filename):
      try:
        script = get_project(root + '/' + filename)
        if not 'script' in script: continue
        SCRIPTS[filename.replace('script_', '').replace('.json', '')] = script
        # authors ( for solution lookup )
        container = root.rsplit('/', 1)[-1]
        AUTHORS[container] = AUTHORS.get(container, set()) | set(script['script'].get('authors', []))
        print 'OK', filename
      except Exception, e:
        print 'ERROR:', filename, str(e) 

class Script:

  @staticmethod
  def get_scripts(account_email=None):
    for tag in SCRIPTS.keys():
      if account_email in SCRIPTS[tag]['script'].get('private', (account_email,)):
        yield Script(tag)

  def __init__(self, tag):
    self.tag = tag
    self.script = SCRIPTS.get(tag, {})

  def exists(self):
    return self.script != {}

  def get_link(self):
    return '%s/solution/%s/' % (settings.CONST_URL, self.tag, )

  def get_tag(self):
    return self.tag

  def get_open(self):
    return self.script.get('script', {}).get('open', False)

  def get_name(self):
    return self.script.get('script', {}).get('title', '')

  def get_icon(self):
    return self.script.get('script', {}).get('icon', '')

  def get_product(self):
    return self.script.get('script', {}).get('product', 'Other')

  def get_description(self, constants = {}):
    json_set_description(self.script, constants)
    return self.script['script'].get('description', '')

  def get_instructions(self, constants = {}):
    json_set_instructions(self.script, constants)
    return self.script['script'].get('instructions', [])

  def get_authors(self):
    return set(deepcopy(self.script.get('script', {}).get('authors', []))) | AUTHORS.get(self.tag, set())

  def get_image(self):
    return self.script.get('script', {}).get('image', None)

  def get_sample(self):
    return self.script.get('script', {}).get('sample', None)

  def get_open_source(self):
    return self.script.get('script', {}).get('open_source', None)

  def get_requirements(self):
    return self.script.get('script', {}).get('requirements', {})

  def get_categories(self):
    return self.script.get('script', {}).get('categories', [])

  def get_pitches(self):
    return self.script.get('script', {}).get('pitches', [])

  def get_impacts(self):
    return self.script.get('script', {}).get('impacts', {})

  def get_task(self):
    task = deepcopy(self.script['tasks'])
    return task

  def is_solution(self):
    return 'impacts' in self.script.get('script', {})

  @staticmethod
  def get_json(uuid, project_id, credentials_user, credentials_service, days, hours, values, constants):
    tasks = []
    for v in values:
      task = Script(v['tag']).get_task()
      json_set_fields(task, v['values'])
      tasks.extend(task)

    data = {
      "setup":{
        "uuid":uuid,
        "id":project_id,
        "timezone":constants['timezone'],
        "day":days,
        "hour":hours,
        "auth":{
          "source":"ui",
          "user":credentials_user,
          "service":credentials_service,
        }
      },
      "tasks":tasks,
    }

    return data
