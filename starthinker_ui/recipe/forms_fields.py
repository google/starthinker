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

import csv
import io
import json

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from starthinker_ui.recipe.timezones import TIMEZONES


class CommaSeparatedCharField(forms.CharField):

  def prepare_value(self, value):
    return ', '.join(value or [])

  def clean(self, value):
    try:
      v = [str(v.strip()) for v in value.split(',') if v.strip()]
      json.dumps(v)  # only do a check if valid
      return v
    except:
      raise ValidationError


class CommaSeparatedIntegerField(forms.Field):
  default_error_messages = {
      'invalid': 'Enter comma separated numbers only.',
  }

  def prepare_value(self, value):
    return ', '.join(
        str(v)
        for v in (json.loads(value or '[]') if isinstance(value, str) else (
            value or [])))

  def clean(self, value):
    try:
      v = [int(v.strip()) for v in value.split(',') if v.strip()]
      json.dumps(v)  # only do a check if valid
      return v
    except:
      raise ValidationError


class ListChoiceField(forms.MultipleChoiceField):

  def prepare_value(self, value):
    return json.loads(value or '[]') if isinstance(value, str) else value

  def to_python(self, value):
    return json.dumps(value)

  def validate(self, value):
    try:
      json.loads(value)
      return True
    except:
      return False


class ListChoiceIntegerField(forms.MultipleChoiceField):

  def prepare_value(self, value):
    return json.loads(value or '[]') if isinstance(value, str) else value

  def to_python(self, value):
    return json.dumps([int(v) for v in value])

  def validate(self, value):
    try:
      json.loads(value)
      return True
    except:
      return False


class ListChoiceIntegerField(forms.MultipleChoiceField):

  def prepare_value(self, value):
    return json.loads(value or '[]') if isinstance(value, str) else value

  def to_python(self, value):
    return json.dumps([int(v) for v in value])

  def validate(self, value):
    try:
      json.loads(value)
      return True
    except:
      return False


class JsonField(forms.CharField):
  widget = forms.Textarea

  def prepare_value(self, value):
    if isinstance(value, str):
      if value:
        try:
          return json.dumps(json.loads(value))
        except ValueError:
          return value
      else:
        return None
    else:
      return json.dumps(value)

  def clean(self, value):
    if isinstance(value, str):
      if value:
        try:
          return json.loads(value.strip())
        except ValueError as e:
          raise ValidationError(str(e))
      else:
        return None
    else:
      return value


class TimezoneField(forms.ChoiceField):

  def __init__(self, *args, **kwargs):
    kwargs['choices'] = map(lambda t: (t, t.replace('_', ' ')), TIMEZONES)
    kwargs['initial'] = 'America/Los_Angeles'
    super(TimezoneField, self).__init__(*args, **kwargs)


class SwitchField(forms.ChoiceField):
  widget = forms.CheckboxInput

  def __init__(self, value_false, value_true, *args, **kwargs):
    self.value_true = value_true
    self.value_false = value_false
    kwargs['choices'] = [value_true, value_false]
    super(SwitchField, self).__init__(*args, **kwargs)

  def prepare_value(self, value):
    return value == self.value_true

  def clean(self, value):
    if value == True:
      return self.value_true
    else:
      return self.value_false
