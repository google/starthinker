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

from django import forms

from starthinker_ui.recipe.scripts import Script
from starthinker_ui.recipe.models import Recipe
from starthinker_ui.recipe.forms import SetupForm
from starthinker_ui.recipe.forms_json import ScriptJsonForm


class ScriptForm(forms.Form):
  users = None

  def __init__(self, manual, recipe, account, *args, **kwargs):
    post = args[0] if len(args) > 0 else None

    # load scripts ( used when creating new recipe )
    if 'scripts' in kwargs:
      scripts = [s for s in kwargs.pop('scripts').split(',') if s]
    else:
      scripts = []

    # fetch the instance and load initial data
    self.instance = recipe or Recipe()
    self.setup = SetupForm(manual, account, post, instance=self.instance)
    super(ScriptForm, self).__init__(*args, **kwargs)

    # create blank forms
    self.blanks = []
    for s in Script.get_scripts(account.email):
      if s.is_manual() == manual:
        self.blanks.append(
            ScriptJsonForm('[BLANK]', s, {}, prefix='%s_[BLANK]' % s.get_tag()))

    # processing incoming form
    self.forms = []
    if post:
      for prefix in post.getlist('form_prefix'):
        tag, sequence = prefix.rsplit('_', 1)
        sequence = int(sequence) - 1
        s = Script(tag)
        self.forms.append(
            ScriptJsonForm(
                sequence,
                s,
                self.instance.get_values()[sequence]['values']
                if self.instance and sequence < len(self.instance.get_values())
                else {},
                post,
                prefix=prefix))

    # loading from existing recipe
    elif self.instance:
      for sequence, script in enumerate(self.instance.get_values()):
        s = Script(script['tag'])
        self.forms.append(
            ScriptJsonForm(
                sequence + 1,
                s,
                script['values'],
                prefix='%s_%d' % (s.get_tag(), sequence + 1)))

    # starting a new recipe
    else:
      for sequence, script in enumerate(scripts):
        s = Script(script)
        self.forms.append(
            ScriptJsonForm(
                sequence + 1,
                s, [],
                prefix='%s_%d' % (s.get_tag(), sequence + 1)))

  def is_valid(self):
    return super(ScriptForm, self).is_valid() & self.setup.is_valid() & all(
        [script.is_valid() for script in self.forms])

  def get_errors(self):
    errors = list(['%s: %s' % (k, v) for k, v in self.setup.errors.items()])
    for script in self.forms:
      errors.extend(['%s: %s' % (k, v) for k, v in script.errors.items()])
    return errors

  def get_scripts(self):
    scripts = [script.get_script() for script in self.forms
              ]  # fetch sequence and scripts
    return sorted([script for script in scripts if script],
                  key=lambda k: k['sequence']
                 )  # sort and return script ( if delete sript will be None )

  def save(self):
    self.instance = self.setup.save()
    self.instance.set_values(self.get_scripts())
    self.instance.save()
    self.instance.update()
