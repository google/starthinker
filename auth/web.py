###########################################################################
# 
#  Copyright 2018 Google Inc.
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

"""Sample code for Google OAuth designed for a web application and pub/sub.

### Problem

User credentials typically need to be downloaded from a web application, and
then refreshed periodically.  When jobs are run in a distributed pub/sub,
multiple processes may need a refreshed user token at once.  Refreshing the
token for one job but not others will invalidate the token for the other jobs.

### Solution

Store the downloaded user credentials in a Google Cloud Bucket and let multiple 
jobs fetch and update the token in a central location.  This sample shows how to
get, store, and retrieve the user credentials in a token refresh safe way. The key 
is using BucketCredentials, it does all the token management under the hood.

### Sample Google Auth Used As Login

User hits a web flow that requires authentication, instead of calling app login logic
call toauth_star to begin the Google Web Login Process. For safety, only trivial values
should be added as parameters to the auth URL, DO NOT USE THIS TO PASSACCOUNT KEYS.

`oauth_start()`

User will be presented with a Google Login Flow, which will request all scopes defined 
in SCOPES.  Future plan is to leverage incremental scoping. 

Once user completes the Google Login flow, by either cancelling or authenticating, 
the redirect comes back.  Now the application needs to verify the auth, and request
the actual credentials. Somwhere in the app the redirect_uri passed above needs to
point to:

`oauth_callback(request):`

Thats it, user is now created or logged in, the BucketCredentials will load, update, 
and store the token as necessary under the hood. In your application and pub/sub
always use BucketCredentials, for example see get_profile(...) for a typical API
call using distributed bucket credentials:

```
credentials = get_credentials(user_id)
service = discovery.build('oauth2', 'v2', credentials.authorize(httplib2.Http()))
profile = service.userinfo().get().execute()
```

"""

import httplib2

from apiclient import discovery
from oauth2client import client
from django.http import HttpResponseRedirect
from django.conf import settings

from util.auth.google_bucket_auth import BucketCredentials
from util.auth import APPLICATION_NAME, SCOPES


def oauth_start():
  extra = '?manager=true' if request.GET.get('manager') == 'true' else ''
  flow = client.flow_from_clientsecrets(settings.UI_CLIENT, SCOPES[:2] if extra else SCOPES, redirect_uri=settings.CONST_URL + '/oauth_callback/' + extra)
  flow.user_agent = APPLICATION_NAME,
  flow.params['response_type'] = 'code'
  #flow.params['approval_prompt'] = 'auto'
  flow.params['prompt'] = 'consent'
  flow.params['access_type'] = 'offline'
  flow.params['include_granted_scopes'] = 'true'
  return HttpResponseRedirect(flow.step1_get_authorize_url())


def oauth_callback(request):
  try:
    extra = '?manager=true' if request.GET.get('manager') == 'true' else ''
    flow = client.flow_from_clientsecrets(
      settings.UI_CLIENT, SCOPES[:2] if extra else SCOPES, 
      redirect_uri=settings.CONST_URL + '/oauth_callback/' + extra
    )
    credentials = flow.step2_exchange(request.GET['code'])

    # if using Google Auth as a login, create your app user here 
    # create local user object, get user_id
    # call get_profile(user_id, credentials) to get user information
    # save user

    set_credentials(user_id, credentials)

    # if using Google Auth as a login, set your app login state here

  except Exception, e:
    import traceback
    traceback.print_exc()

  return HttpResponseRedirect('/')


def get_credentials_path(user_id):
  return '%s:ui/%s.json' % (settings.UI_BUCKET_AUTH, user_id)


def set_credentials(user_id, credentials):
  BucketCredentials.from_oauth(get_credentials_path(user_id), credentials).to_bucket()


def get_credentials(user_id):
  return BucketCredentials.from_bucket(get_credentials_path(user_id))


def get_profile(user_id, credentials=None):
  if credentials is None: credentials = get_credentials(user_id)

  # pull user information for account 
  service = discovery.build('oauth2', 'v2', credentials.authorize(httplib2.Http()))
  profile = service.userinfo().get().execute()

  return profile
