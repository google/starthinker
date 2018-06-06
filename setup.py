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

EXECUTE_PATH = os.environ.get('STARTHINKER_PATH', "/home/starthinker") + '/'

# In production simply create this file: touch /mnt/SERVER
DEVELOPMENT_MODE = not os.path.isfile('/mnt/SERVER')

# This is always set to False ( setting it to True does nothing productive )
INTERNAL_MODE = False

# Used for local testing, 
if DEVELOPMENT_MODE:
 
  # credentials used to manage universal information such as logs, and project that does NOT store data
  UI_PROJECT = 'cloud-project-id-test'
  UI_CLIENT = '/home/credentials/test/starthinker_client.json'
  UI_SERVICE = '/home/credentials/test/starthinker_service.json'
  UI_BUCKET_LOG = 'starthinker-test-log'
  UI_TOPIC = 'test_worker'

  # credentials used to store data ( for security reasons not same project as logs and credentials )
  CLOUD_PROJECT = 'cloud-project-id-data-test'
  CLOUD_SERVICE = '/home/credentials/test/starthinker_data_service.json'

  # used to multiply all buffer sizes for scaling on larger or smaller machines, can be a float
  BUFFER_SCALE = 1

else:
  # credentials used to manage universal infomation such as logs, and project that does NOT store data
  UI_PROJECT = 'cloud-project-id'
  UI_CLIENT = '/home/credentials/starthinker_client.json'
  UI_SERVICE = '/home/credentials/starthinker_service.json'
  UI_BUCKET_LOG = 'starthinker-log'
  UI_TOPIC = 'prod_worker'

  # credentials used to store data ( for security reasons not same project as logs and credentials )
  CLOUD_PROJECT = 'cloud-project-id-data'
  CLOUD_SERVICE = '/home/credentials/starthinker_data_service.json'

 # used to multiply all buffer sizes for scaling on larger or smaller machines, can be a float
  BUFFER_SCALE = 5
