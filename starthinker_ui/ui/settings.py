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


# Load all technical settings
from starthinker_ui.ui.framework import *

# Replace local auth with web auth
UI_CLIENT = os.environ.get('STARTHINKER_CLIENT_WEB', '') # blank to deploy single user mode

def domain_to_host(domain):
  return  domain.split('://', 1)[-1].split(':', 1)[0].split('/', 1)[0]

# Currently StarThinker is in English, internationalization TBD
LANGUAGE_CODE = 'en-us'

# Only affects logging on local server, all times in UI are recipe specific.
TIME_ZONE = 'America/Los_Angeles'

# If sendmail is set up, will email if site failure or error occurs.
ADMINS = [('User Name', 'email@domain.com')]

# Store your logo and front end website graphics here.
STATIC_URL = 'https://storage.googleapis.com/starthinker-ui/'

CONST_URL = os.environ.get('STARTHINKER_UI_DOMAIN') or 'http://localhost:8000'
SECRET_KEY = os.environ.get('STARTHINKER_UI_SECRET') or 'safetyandcivilreassuranceadministrationofficials'
ALLOWED_HOSTS = [domain_to_host(os.environ.get('STARTHINKER_UI_DOMAIN', '')) or 'localhost', '127.0.0.1']

DATABASES = {
  'default': {
    'ENGINE': os.environ.get('STARTHINKER_UI_DATABASE_ENGINE', 'MISSING RUN deploy.sh TO SET'),
    'HOST': os.environ.get('STARTHINKER_UI_DATABASE_HOST', ''),
    'PORT': os.environ.get('STARTHINKER_UI_DATABASE_PORT', ''),
    'NAME': os.environ.get('STARTHINKER_UI_DATABASE_NAME', 'MISSING RUN deploy.sh TO SET'),
    'USER': os.environ.get('STARTHINKER_UI_DATABASE_USER', ''),
    'PASSWORD': os.environ.get('STARTHINKER_UI_DATABASE_PASSWORD', ''),
    'TEST': { 'NAME': 'starthinker_test' }
  }
}
