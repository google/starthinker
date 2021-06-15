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

import re
import json

from django import forms

from starthinker.util.recipe import json_get_fields
from starthinker_ui.recipe.forms_fields import CommaSeparatedCharField, CommaSeparatedIntegerField, JsonField, TimezoneField, SwitchField


def load_config_data(config, path, default):
  current = config
  if isinstance(path, str):
    path = path.split('.')  # accept string or list as path
  for key in path:
    if not isinstance(key, int) and key.isdigit():
      key = int(key)  # cast string indexes to int
    try:
      current = current[key]
    except:
      return default
  return current


def get_field_kind(field):
  if field['kind'] == 'string':
    return forms.CharField(max_length=255, required=False)
  elif field['kind'] == 'email':
    return forms.EmailField(max_length=255, required=False)
  elif field['kind'] == 'integer':
    return forms.IntegerField(required=False)
  elif field['kind'] == 'boolean':
    return forms.BooleanField(required=False)
  elif field['kind'] == 'text':
    return forms.CharField(widget=forms.Textarea(), required=False)
  elif field['kind'] == 'choice':
    return forms.ChoiceField(choices=map(lambda c: (c, c), field['choices']))
  elif field['kind'] == 'timezones':
    return TimezoneField()
  elif field['kind'] == 'authentication':
    return SwitchField('user', 'service', required=True)
  elif field['kind'] == 'json':
    return JsonField(required=False)
  elif field['kind'] == 'integer_list':
    return CommaSeparatedIntegerField(required=False)
  elif field['kind'] == 'string_list':
    return CommaSeparatedCharField(required=False)
  else:
    return forms.CharField(max_length=255, required=False)


class ScriptJsonForm(forms.Form):
  script_sequence = forms.IntegerField(
      widget=forms.HiddenInput(attrs={'class': 'form_sequence'}))
  script_delete = forms.IntegerField(
      widget=forms.HiddenInput(attrs={'class': 'form_delete'}), initial=0)

  def __init__(self, sequence, script, values, *args, **kwargs):
    self.script = script
    self.values = values
    super(ScriptJsonForm, self).__init__(*args, **kwargs)
    self.fields['script_sequence'].initial = sequence
    x = script.get_tag()
    self.variables = json_get_fields(script.get_tasks())
    for variable in self.variables:
      if variable['name'].startswith('recipe_'):
        continue  # skip inputs that come from recipe constants
      self.fields[variable['name']] = get_field_kind(variable)
      self.fields[variable['name']].initial = values.get(
          variable['name'], variable.get('value', variable.get('default', '')))
      self.fields[variable['name']].required = variable.get('required', False)
      self.fields[variable['name']].help_text = variable.get('description', '')

  def get_description(self):
    return self.script.get_description(self.values)

  def get_instructions(self):
    return self.script.get_instructions(self.values)

  def get_script(self):
    # if marked for delete return nothing, will be filtered up stream
    if self.cleaned_data.get('script_delete', 0) == 1:
      return None
    # if saving, return values ( constants are not stored as they come from the recipe )
    else:
      values = {}
      for variable in self.variables:
        if variable['name'].startswith('recipe_'):
          continue  # skip inputs that come from recipe constants
        values[variable['name']] = self.cleaned_data[variable['name']]
      return {
          'tag': self.script.get_tag(),
          'values': values,
          'sequence': self.cleaned_data['script_sequence']
      }
