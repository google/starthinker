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

# General StarThinker constants that can also be used from the command line interface
from starthinker.config import UI_ROOT, UI_PROJECT, UI_CLIENT, UI_SERVICE, UI_CRON, UI_ZONE, DEVELOPMENT_MODE

# See available translations (this is just the default if browser does not provide)
LANGUAGE_CODE = 'en-us'

# Load all technical settings
from starthinker_ui.ui.framework import *

# Used by workers to manage instance group
WORKER_MAX = int(os.environ.get('STARTHINKER_WORKER_MAX', 0))
WORKER_JOBS = int(os.environ.get('STARTHINKER_WORKER_JOBS', 1))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEVELOPMENT_MODE

# Optional tracking parameter
GOOGLE_ANALYTICS = os.environ.get('STARTHINKER_ANALYTICS', '')

# Only affects logging on local server, all times in UI are recipe specific.
TIME_ZONE = 'America/Los_Angeles'

# If sendmail is set up, will email if site failure or error occurs.
ADMINS = [('User Name', 'email@domain.com')]

# Store your logo and front end website graphics here.
STATIC_URL = 'https://storage.googleapis.com/starthinker-ui/'


def domain_to_host(domain):
  return domain.split('://', 1)[-1].split(':', 1)[0].split('/', 1)[0]


CONST_URL = os.environ.get('STARTHINKER_UI_DOMAIN') or 'http://localhost:8000'
SECRET_KEY = os.environ.get(
    'STARTHINKER_UI_SECRET'
) or 'safetyandcivilreassuranceadministrationofficials'
ALLOWED_HOSTS = [
    domain_to_host(os.environ.get('STARTHINKER_UI_DOMAIN', '')) or 'localhost',
    '127.0.0.1'
]

DATABASES = {
    'default': {
        'ENGINE':
            os.environ.get('STARTHINKER_UI_DATABASE_ENGINE',
                           'MISSING RUN deploy.sh TO SET'),
        'HOST':
            os.environ.get('STARTHINKER_UI_DATABASE_HOST', ''),
        'PORT':
            os.environ.get('STARTHINKER_UI_DATABASE_PORT', ''),
        'NAME':
            os.environ.get('STARTHINKER_UI_DATABASE_NAME',
                           'MISSING RUN deploy.sh TO SET'),
        'USER':
            os.environ.get('STARTHINKER_UI_DATABASE_USER', ''),
        'PASSWORD':
            os.environ.get('STARTHINKER_UI_DATABASE_PASSWORD', ''),
        'TEST': {
            'NAME': 'starthinker_test'
        }
    }
}
