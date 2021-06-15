# -*- coding: utf-8 -*-

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

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponseRedirect

from starthinker.util.auth_wrapper import CredentialsFlowWrapper
from starthinker_ui.account.models import Account


def oauth_callback(request):

  # get the credentials from the Google redirect
  flow = CredentialsFlowWrapper(
      settings.UI_CLIENT, redirect_uri=settings.CONST_URL + '/oauth_callback/')
  flow.code_verifier = request.session.get('code_verifier')
  flow.fetch_token(code=request.GET['code'])

  # get or create the account
  account = Account.objects.get_or_create_user(flow.credentials)

  # log the account in ( set cookie )
  django_login(request, account, backend=settings.AUTHENTICATION_BACKENDS[0])

  messages.success(request, 'Welcome To StarThinker')

  return HttpResponseRedirect('/')


def logout(request):
  django_logout(request)
  messages.success(request, 'You Are Logged Out')
  return HttpResponseRedirect('/')
