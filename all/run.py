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

import sys
import subprocess
import argparse

from setup import EXECUTE_PATH
from util.project import get_project, is_scheduled
from worker.log import log_project

if __name__ == "__main__":

  # this is a helper function, these inputs mirror util.project.Project singleton used by tasks because they are pass through to each task
  parser = argparse.ArgumentParser()
  parser.add_argument('json', help='path to tasks json file')

  parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
  parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
  parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
  parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

  parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
  parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
  parser.add_argument('--force', '-force', help='execute all scripts once then exit.', action='store_true')
  args = parser.parse_args()

  # load json to get each task
  project = get_project(args.json)
  # track per task instance count
  instances = {}
  # return code changes if a task fails
  return_code = 0

  for task in project['tasks']:
    script, task = task.items()[0]

    # count instance per task
    instances.setdefault(script, 0)
    instances[script] += 1

    # assemble command ( replace command, use all arguments passed, and add instance )
    command = 'python2.7 %s%s/run.py %s -i %d' % (EXECUTE_PATH, script, ' '.join(sys.argv[1:]), instances[script])

    # show command so user can run each task
    print command

    # execute command if schedule
    if args.force or is_scheduled(project, task):

      # writes running if UUID is present
      log_project(project)

      child = subprocess.Popen(command, shell=True, cwd=EXECUTE_PATH, stderr=subprocess.PIPE)
      outputs, errors = child.communicate()

      # writes status if UUID is present
      log_project(project, outputs, errors)

      #print errors
      if errors:
        sys.stderr.write(errors)
        return_code = 1
        sys.exit(return_code)

    # skip command if not schedule
    else:
      print "Schedule Skipping: run command manually or add --force to run all"

  sys.exit(return_code)
