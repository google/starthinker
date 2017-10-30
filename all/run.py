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
from util.project import get_project
from worker.log import log_project

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('project', help='[project] is one of the * in starthinker/project/*.json.')
  parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
  parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
  args = parser.parse_args()

  project = get_project(args.project)
  verbose = args.verbose
  date = args.date

  instances = {}

  return_code = 0

  for task in project['tasks']:
    task = [t for t in task.keys() if t != 'script'][0] # ui scripts have an extra script tag that needs to be removed

    # count instance per task
    instances.setdefault(task, 0)
    instances[task] += 1

    # assemble command
    command = 'python2.7 %s%s/run.py %s -i %d' % (EXECUTE_PATH, task, args.project, instances[task])
    if date != 'TODAY': command += ' --date "%s"' % date
    if verbose: command += ' --verbose'

    # execute command
    print command

    log_project(project) # writes running if UUID is present

    child = subprocess.Popen(command, shell=True, cwd=EXECUTE_PATH, stderr=subprocess.PIPE)
    outputs, errors = child.communicate()

    log_project(project, outputs, errors) # writes status if UUID is present

    #print errors
    if errors:
      sys.stderr.write(errors)
      return_code = 1

  sys.exit(return_code)
