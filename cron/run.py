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

import sys
import subprocess
import argparse

from glob import glob
from time import sleep

from util.project import get_project, is_scheduled
from setup import EXECUTE_PATH

ONE_HOUR_AND_ONE_SECOND = (60 * 60) + 1 # ensures no repeat in a single hour but never runs over in 24 hours

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('path', help='run all json files in the specified path', action="store")

  parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
  parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
  parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
  parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

  parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
  parser.add_argument('--force', '-force', help='execute all scripts once then exit.', action='store_true')

  args = parser.parse_args()
  verbose = args.verbose

  try:

    while True:
      for filepath in glob('%s*.json' % args.path):
        if verbose: print 'PROJECT:', filepath

        project = get_project(filepath)

        if args.force or is_scheduled(project):

          script = 'all' if project.get('setup', {}).get('local', True) else 'remote'
          #command = 'python %s/run.py %s --date TODAY' % (script, filepath)
          command = 'python %s/run.py %s %s' % (script, filepath, ' '.join(sys.argv[2:]))

          if verbose: print 'COMMAND:', command

          subprocess.Popen(command, shell=True, cwd=EXECUTE_PATH)

      if args.force: break
      if verbose: print 'SLEEP:', ONE_HOUR_AND_ONE_SECOND
      sleep(ONE_HOUR_AND_ONE_SECOND)

  except KeyboardInterrupt:
    exit()
