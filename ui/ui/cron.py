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

import subprocess
from time import sleep

from starthinker.config import EXECUTE_PATH

ONE_HOUR_AND_ONE_SECOND = (60 * 60) + 1 # ensures no repeat in a single hour but never runs over in 24 hours

if __name__ == "__main__":

  try:
    while True:
      subprocess.call("python manage.py recipe_to_json --remote --settings=ui.settings_internal", shell=True, cwd=EXECUTE_PATH + "ui/")
      subprocess.call("python manage.py client_to_json --remote --settings=ui.settings_internal", shell=True, cwd=EXECUTE_PATH + "ui/")
      print 'SLEEP:', ONE_HOUR_AND_ONE_SECOND
      sleep(ONE_HOUR_AND_ONE_SECOND)

  except KeyboardInterrupt:
    exit()
