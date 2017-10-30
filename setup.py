###########################################################################
#
#  Copyright 2017 Google Inc.
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

import os
import time
from datetime import time as localtime, date, timedelta


TIMEZONE_OFFSET = timedelta(hours=(-time.altzone if time.localtime(time.time()).tm_isdst and time.daylight else -time.timezone) / (60*60))
UTC_OFFSET = timedelta(hours=-7)

EXECUTE_PATH = os.environ.get('STARTHINKER_PATH', "/home/starthinker") + '/'

DEVELOPMENT_MODE = not os.path.isfile('/mnt/SERVER')
if DEVELOPMENT_MODE:
 
  # used to manage user credentials and UI data
  UI_PROJECT = 'google.com:starthinker-test'
  UI_CLIENT = '/home/credentials/test/starthinker_client.json'
  UI_SERVICE = '/home/credentials/test/starthinker_service.json'
  UI_BUCKET_AUTH = 'starthinker-test-auth'
  UI_BUCKET_UI = 'starthinker-test-ui'
  UI_BUCKET_LOG = 'starthinker-test-log'
  UI_TOPIC = 'default_test_worker'

  # used to store client data
  CLOUD_PROJECT = 'google.com:starthinker-test'
  CLOUD_SERVICE = '/home/credentials/test/starthinker_service.json'

else:
  # used to manage user credentials and UI data
  UI_PROJECT = 'google.com:starthinker'
  UI_CLIENT = '/home/credentials/starthinker_client.json'
  UI_SERVICE = '/home/credentials/starthinker_service.json'
  UI_BUCKET_AUTH = 'starthinker-auth'
  UI_BUCKET_UI = 'starthinker-ui'
  UI_BUCKET_LOG = 'starthinker-log'
  UI_TOPIC = 'default_worker'

  # used to store client data
  CLOUD_PROJECT = 'google.com:starthinker-42'
  CLOUD_SERVICE = '/home/credentials/starthinker_data_service.json'
