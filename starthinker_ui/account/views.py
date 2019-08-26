# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals

import httplib2

from apiclient import discovery

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponseRedirect

from starthinker.util.auth import get_flow
from starthinker_ui.account.models import Account
from starthinker_ui.account.forms import LoginForm


def oauth_callback(request):

  #try:
  # get the credentials from the Google redirect
  flow = get_flow(settings.UI_CLIENT, redirect_uri=settings.CONST_URL + '/oauth_callback/')
  credentials = flow.step2_exchange(request.GET['code'])

  # pull user information for account lookup or creation
  service = discovery.build('oauth2', 'v2', credentials.authorize(httplib2.Http()))
  profile = service.userinfo().get().execute()

  # get or create the account
  account = Account.objects.get_or_create_user(profile, credentials)
  #authenticate(username = username, password = password)

  # log the account in ( set cookie )
  django_login(request, account, backend=settings.AUTHENTICATION_BACKENDS[0])

  messages.success(request, 'Welcome To StarThinker')

  #except Exception, e: 
  #  messages.error(request, 'A Swing And A Miss')
  #  import traceback
  #  traceback.print_exc()


  return HttpResponseRedirect('/')


def logout(request):
  django_logout(request)
  messages.success(request, 'You Are Logged Out')
  return HttpResponseRedirect('/')


def login(request):

  if request.user.is_authenticated():
    messages.success(request, 'You Are Logged In')
    return HttpResponseRedirect('/')

  else:
    if request.method == 'POST':
      form_login = LoginForm(request)
      if form_login.is_valid():
        messages.success(request, 'Welcome To StarThinker')
        return HttpResponseRedirect(form_login.get_redirect())
      else:
        messages.error(request, 'Invalid Login')
    else:
      form_login = LoginForm(request)

  return render(request, "account/login.html", { 'form_login':form_login })
