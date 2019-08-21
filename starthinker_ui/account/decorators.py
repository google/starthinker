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

from functools import wraps
from oauth2client import client
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login as django_login

from starthinker.util.auth import get_flow
from starthinker_ui.account.models import Account


def permission_admin():
  def _decorator(_view):
    @wraps(_view)
    def _wrapper(request, *args, **kwargs):

      # user is logged in
      if request.user.is_authenticated():
        return _view(request, *args, **kwargs)

      # multi user mode, log user in using oauth
      elif settings.UI_CLIENT:
        flow = get_flow(settings.UI_CLIENT, redirect_uri=settings.CONST_URL + '/oauth_callback/')
        flow.params['response_type'] = 'code'
        #flow.params['approval_prompt'] = 'auto'
        flow.params['prompt'] = 'consent'
        flow.params['access_type'] = 'offline'
        flow.params['include_granted_scopes'] = 'true'
        return HttpResponseRedirect(flow.step1_get_authorize_url())

      # single user mode, no oath, just log the user in
      else:

        # fetch the default account
        account = (Account.objects.filter(identifier=json.loads(settings.UI_USER)['id_token']['sub'])[:1] or (None))[0]
        
        # log the account in ( set cookie )
        if account:
          django_login(request, account, backend=settings.AUTHENTICATION_BACKENDS[0])
          messages.success(request, 'Welcome %s To StarThinker' % account.name.title())
          return _view(request, *args, **kwargs)

        # or display a friendly error
        else:
          messages.error(request, 'Missing Account, Run Deployment Again')
          return HttpResponseRedirect('/')

    return _wrapper
  return _decorator
