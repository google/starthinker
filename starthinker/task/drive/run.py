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
"""Handler that executes { "drive":{...}} task in recipe JSON.

This script perfroms various drive operations like copy and create.
"""

from starthinker.util.drive import file_copy, file_create, file_delete


def drive(config, task):
  if config.verbose:
    print('Drive')

  if 'delete' in task:
    if config.verbose:
      print('Drive Delete', task['delete'])
    file_delete(config, task['auth'], task['delete'])

  if 'copy' in task:
    if config.verbose:
      print('Drive Copy', task['copy']['source'],
            task['copy']['destination'])
    file_copy(config, task['auth'], task['copy']['source'],
              task['copy']['destination'])
