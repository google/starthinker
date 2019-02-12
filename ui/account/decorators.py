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

from functools import wraps
from oauth2client import client
from django.http import HttpResponseRedirect
from django.conf import settings

from starthinker.util.auth import APPLICATION_NAME, SCOPES

def permission_admin():
  def _decorator(_view):
    @wraps(_view)
    def _wrapper(request, *args, **kwargs):
      if request.user.is_authenticated():
        return _view(request, *args, **kwargs)
      else:
        extra = '?manager=true' if request.GET.get('manager') == 'true' else ''
        flow = client.flow_from_clientsecrets(settings.UI_CLIENT, SCOPES[:2] if extra else SCOPES, redirect_uri=settings.CONST_URL + '/oauth_callback/' + extra)
        flow.user_agent = APPLICATION_NAME,
        flow.params['response_type'] = 'code'
        #flow.params['approval_prompt'] = 'auto'
        flow.params['prompt'] = 'consent'
        flow.params['access_type'] = 'offline'
        flow.params['include_granted_scopes'] = 'true'
        return HttpResponseRedirect(flow.step1_get_authorize_url())
    return _wrapper
  return _decorator
