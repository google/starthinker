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

import os

UI_ROOT = os.environ.get('STARTHINKER_ROOT', 'MISSING RUN deploy.sh TO SET')
UI_CRON = os.environ.get('STARTHINKER_CRON', '')

DEVELOPMENT_MODE = bool(os.environ.get('STARTHINKER_DEVELOPMENT', '0') == '1')
INTERNAL_MODE = bool(os.environ.get('STARTHINKER_INTERNAL', '0') == '1')

# used to manage user credentials and UI data
UI_ZONE = os.environ.get('STARTHINKER_ZONE', 'MISSING RUN deploy.sh TO SET')
UI_PROJECT = os.environ.get('STARTHINKER_PROJECT', 'MISSING RUN deploy.sh TO SET')
UI_CLIENT = os.environ.get('STARTHINKER_CLIENT_WEB', 'MISSING RUN deploy.sh TO SET')
UI_SERVICE = os.environ.get('STARTHINKER_SERVICE', 'MISSING RUN deploy.sh TO SET')

# used to multiply all buffer sizes for scaling on larger or smaller machines, can be a float
BUFFER_SCALE = int(os.environ.get('STARTHINKER_SCALE', 1))
