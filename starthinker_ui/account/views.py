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
from oauth2client import client

from django.contrib.auth import login as django_login, logout as django_logout#, authenticate
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages

from starthinker.util.auth import get_flow
from starthinker.util.project import project
from starthinker.util.storage import bucket_create, bucket_access
from starthinker_ui.account.models import Account
from starthinker_ui.account.decorators import permission_admin


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


@permission_admin()
def storage(request):
  bucket = request.user.get_bucket(full_path=False)

  # create and permission bucket ( will do nothing if it exists )
  project.initialize(_project=settings.RECIPE_PROJECT, _service=settings.RECIPE_SERVICE)
  bucket_create('service', settings.RECIPE_PROJECT, bucket)
  bucket_access('service', settings.RECIPE_PROJECT, bucket, 'OWNER', emails=[request.user.email])

  return HttpResponseRedirect(request.user.get_bucket())
