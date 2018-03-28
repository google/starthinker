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
import sys
import re
import argparse
import subprocess

from setup import EXECUTE_PATH

RE_TEST = re.compile(r'test\.json')

if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
  parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
  parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
  parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

  parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
  parser.add_argument('--list', '-l', help='list all tests that will be discovered and run.', action='store_true')

  args = parser.parse_args()

  for root, dirs, files in os.walk(EXECUTE_PATH):
    for filename in files:
      if RE_TEST.match(filename) and '/project/' not in root:

        if args.list:
          print '%s/%s' % (root, filename)
        else:
          # assemble command ( replace command, use all arguments passed, and add instance )
          command = 'python2.7 %s/all/run.py %s/%s %s' % (EXECUTE_PATH, root, filename, ' '.join(sys.argv[1:]))
          print ''
          print 'TEST:', command
          subprocess.call(command, shell=True, cwd=EXECUTE_PATH, stderr=subprocess.PIPE)
