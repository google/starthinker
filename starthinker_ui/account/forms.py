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
from django.conf import settings
from django.contrib.auth import authenticate, login

from starthinker_ui.account.models import Account

class LoginForm(forms.Form):
  email = forms.EmailField(required=True)
  password = forms.CharField(required=True, widget=forms.PasswordInput())
  redirect = forms.CharField(required=False, widget=forms.HiddenInput())
  user = None

  def __init__(self, request, *args, **kwargs):
    self.request = request

    if request.method == 'GET':
      kwargs['initial'] = {'redirect':request.GET.get('redirect', '')}
    else:
      kwargs['data'] = request.POST

    super(LoginForm, self).__init__(*args, **kwargs)


  def clean(self):
    if 'email' in self.cleaned_data and 'password' in self.cleaned_data:
      self.user = authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
      if self.user is None: 
        self.user = None
        raise forms.ValidationError('Wrong email / password.')
      elif not self.user.is_active: 
        self.user = None
        raise forms.ValidationError('Account is not active.')
    return self.cleaned_data


  def get_redirect(self):
    if self.user: 
      login(self.request, self.user)
      return self.cleaned_data.get('redirect') or '/'
    else:
      return '/login/'
