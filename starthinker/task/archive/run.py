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

from datetime import date, timedelta

from starthinker.util.project import project 
from starthinker.util.regexp import parse_yyyymmdd
from starthinker.util.storage import object_list, object_move, object_delete


@project.from_parameters
def archive():
  if project.verbose: print('ARCHIVE')

  day = project.date - timedelta(days=abs(project.task['days']))

  if 'storage' in project.task:
    for file_name in object_list(project.task['auth'], project.task['storage']['bucket'] + ':' + project.task['storage']['path'], files_only=True):
      file_day = parse_yyyymmdd(file_name)
      if file_day and file_day <= day:
        if project.task.get('delete', False) == False:
          if project.verbose: print('ARCHIVING FILE:', file_name)
          object_move(project.task['auth'], file_name, file_name.replace(':', ':archive/'))
        else:
          if project.verbose: print('DELETING FILE:', file_name)
          object_delete(project.task['auth'], file_name)


if __name__ == "__main__":
  archive()
