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

import json

from django import forms

from starthinker.ui.project.models import Project

class ProjectForm(forms.ModelForm):

  class Meta:
    model = Project
    fields = ['service']

  def __init__(self, account, *args, **kwargs):
    super(ProjectForm, self).__init__(*args, **kwargs)
    self.instance.account = account

  def clean_service(self):
    try:
      service = self.cleaned_data['service']
      self.instance.identifier = json.loads(service)['client_email']
    except:
      raise forms.ValidationError('Service credentials must be proper JSON.')

    if Project.objects.filter(account=self.instance.account, identifier=self.instance.identifier).exclude(pk=self.instance.pk).exists():
      raise forms.ValidationError('You already have service credentails for %s, this is a duplicate.' % self.instance.identifier)

    return service

  def get_errors(self):
    return self.errors
