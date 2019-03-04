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
from starthinker.ui.ui.settings import *

# connect to loaded application
WSGI_APPLICATION = 'starthinker.ui.ui.wsgi_open.application'

# Currently StarThinker is in English, internationalization TBD
LANGUAGE_CODE = 'en-us'

# Only affects logging on local server, all times in UI are recipe specific.
TIME_ZONE = 'America/Los_Angeles'

# If sendmail is set up, will email if site failure or error occurs.
ADMINS = [('User Name', 'email@domain.com')]

# Store your logo and front end website graphics here.
STATIC_URL = 'https://storage.googleapis.com/starthinker-ui/'

# Each user in the UI will receive a bucket in the cloud project, this creates [BUCKET_PREFIX]-userid for storing recipes.
BUCKET_PREFIX = '[Usually Name Of Company]-'

# SECURITY WARNING: keep the secret key used in production secret!
if DEVELOPMENT_MODE:
  CONST_URL = 'http://localhost:8000'
  SECRET_KEY = 'safetyandcivilreassuranceadministrationofficials'
  ALLOWED_HOSTS = [] 
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database_name',
    }
  }
else:
  CONST_URL = 'https://starthinker.domain.com'
  SECRET_KEY = 'THIS_MUST_BE_A_RANDOM_ALPHA_NUMERIC_STRING_YOU_GENERATE'
  ALLOWED_HOSTS = ['starthinker.domain.com', 'AND/OR IP ADDRESS']
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'HOST': 'localhost',
      'NAME': 'database_name',
      'USER': 'database_user',
      'PASSWORD': 'database_password',
    }
  }
