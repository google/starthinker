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

  parser = argparse.ArgumentParser()
  parser.add_argument('project', help='path to project json file')
  parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
  parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
  parser.add_argument('--force', '-force', help='execute all scripts once then exit.', action='store_true')
  args = parser.parse_args()

  project = get_project(args.project)
  verbose = args.verbose
  date = args.date

  instances = {}

  return_code = 0

  for task in project['tasks']:
    script, task = task.items()[0]

    # count instance per task
    instances.setdefault(script, 0)
    instances[script] += 1
  
    # assemble command
    command = 'python2.7 %s%s/run.py %s -i %d' % (EXECUTE_PATH, script, args.project, instances[script])
    if date != 'TODAY': command += ' --date "%s"' % date
    if verbose: command += ' --verbose'
  
    print command

    # execute command if schedule
    if args.force or is_scheduled(project, task):
      log_project(project) # writes running if UUID is present
  
      child = subprocess.Popen(command, shell=True, cwd=EXECUTE_PATH, stderr=subprocess.PIPE)
      outputs, errors = child.communicate()
 
      log_project(project, outputs, errors) # writes status if UUID is present
  
      #print errors
      if errors:
        sys.stderr.write(errors)
        return_code = 1

    # skip command if not schedule
    else:
      print "Schedule Skipping: run command manually or add --force to run all"

  sys.exit(return_code)
