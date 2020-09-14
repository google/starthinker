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
from django.db.models import Q

from starthinker_ui.recipe.models import Recipe
from starthinker_ui.project.models import Project
from starthinker_ui.recipe.forms_fields import ListChoiceField, ListChoiceIntegerField, TimezoneField

DAYS = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]
HOURS = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23
]


# This form is always constructed with an object, so initial data doesn't really work here, need to set defaults at the model
class SetupForm(forms.ModelForm):
  week = ListChoiceField(
      choices=map(lambda d: (d[:3], d), DAYS),
      initial=map(lambda d: d[:3], DAYS))
  hour = ListChoiceIntegerField(
      choices=map(lambda h: (h, h), HOURS), initial=[3])
  timezone = TimezoneField(required=False)
  project = forms.ModelChoiceField(queryset=None, required=False)

  class Meta:
    model = Recipe
    fields = ['name', 'project', 'timezone', 'week', 'hour', 'active']

  def __init__(self, manual, account, *args, **kwargs):
    super(SetupForm, self).__init__(*args, **kwargs)
    self.instance.account = account
    self.fields['active'].required = False

    query = Q(account=account) | Q(share='global')
    if account.get_domain():
      query |= (
          Q(share='domain') & ~Q(account__domain='')
          & Q(account__domain=account.get_domain()))
    self.fields['project'].queryset = Project.objects.filter(query).order_by(
        'share', 'identifier')

    self.fields['name'].help_text = 'Identify this recipe in list of recipes.'
    self.fields[
        'project'].help_text = ('Choose a <b>Google Cloud Project Service '
                                'Credential</b> uploaded to Projects.')
    self.fields[
        'timezone'].help_text = 'Frame of reference for all recipe times.'
    self.fields['week'].help_text = 'Days of week to execute recipe.'
    self.fields['hour'].help_text = 'Hours of day to execute recipe.'
    self.fields['active'].help_text = 'To pause recipe, uncheck this.'

    self.structure = [{
        'title': '%s Recipe' % self.instance.name.title(),
        'description': '',
        'fields': [self['name'], self['project']]
    }]

    if manual:
      del self.fields['week']
      del self.fields['hour']
      del self.fields['active']

      self.instance.week = []
      self.instance.hour = []
      self.instance.active = True
      self.instance.manual = True

      self.structure[0]['fields'].append(self['timezone'])

    else:
      self.structure.append({
          'title':
              'Schedule',
          'description':
              '',
          'fields': [
              self['timezone'],
              self['week'],
              self['hour'],
              self['active'],
          ]
      })
