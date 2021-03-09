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

import json

from django import forms
from django.utils.html import mark_safe

from starthinker_ui.project.models import Project


class ProjectForm(forms.ModelForm):
  share = forms.ChoiceField()

  class Meta:
    model = Project
    fields = ['identifier', 'service', 'key', 'share']

  def __init__(self, account, *args, **kwargs):
    super(ProjectForm, self).__init__(*args, **kwargs)
    self.instance.account = account

    self.fields['identifier'].label = 'Project Identifier'
    self.fields['identifier'].required = False
    self.fields['identifier'].help_text = mark_safe(
      'Project to bill for data transfers.'
    )


    self.fields['service'].label = 'Service JSON'
    self.fields['service'].required = False
    self.fields['service'].help_text = mark_safe(
      'Optional, paste service JSON here.'
    )

    self.fields['key'].label = 'API Key'
    self.fields['key'].required = False
    self.fields['key'].help_text = mark_safe(
      'Optional, ensures access and may be required for some API calls.'
    )

    self.fields['share'].label = 'Share'
    self.fields['share'].help_text = mark_safe(
      'WARNING: Sharing with DOMAIN or GLOBAL will allow other users to use, but not view, your service credentials and project permissions.'
    )

    domain = account.get_domain()
    self.fields['share'].choices = ((
        'user', 'USER | SAFE: Only you can use it.'
    ), ('domain',
        'DOMAIN ( %s ) | CAUTION: Only people in your verified domain can use it.'
        % domain), ('global', 'GLOBAL | CAUTION: Anyone logging in can use it.'
                   )) if domain else (('user', 'User'), ('global', 'Global'))


  def clean_service(self):
    if self.cleaned_data['service']:
      try:
        service_json = json.loads(self.cleaned_data['service'])['project_id']
      except:
        raise 'Service credentials must be proper JSON.'
    return self.cleaned_data['service']


  def get_errors(self):
    return self.errors
