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

from django import forms

from starthinker.ui.recipe.models import Recipe
from starthinker.ui.recipe.forms_fields import ListChoiceField, TimezoneField

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
HOURS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# This form is always constructed with an object, so initial data doesn't really work here, need to set defaults at the model
class SetupForm(forms.ModelForm):
  week = ListChoiceField(choices=map(lambda d: (d[:3],d), DAYS), initial=map(lambda d: d[:3], DAYS))
  hour = ListChoiceField(choices=map(lambda h: (h,h), HOURS), initial=[3])

  timezone = TimezoneField(required=False)

  class Meta:
    model = Recipe
    fields = ['name', 'project', 'timezone', 'week', 'hour', 'active']
 
  def __init__(self, account, *args, **kwargs):
    super(SetupForm, self).__init__(*args, **kwargs)
    self.instance.account = account
    self.fields['active'].required = False
    self.fields['project'].queryset = account.project_set.all()

    self.structure = [
      { 'title':'Cloud Project',
        'description':'Provide a cloud project where data will be stored.  The service level authentication will be used where possible in lieu of your user credentials.',
        'fields':[
          self['name'],
          self['project'],
        ]
      },
      { 'title':'Task Schedule',
        'description':'Tasks in this project will be run on the day and hours specified below.  To pause all the tesks uncheck the cron option.',
        'fields':[
          self['timezone'],
          self['week'],
          self['hour'],
          self['active'],
        ]
      },
    ]
