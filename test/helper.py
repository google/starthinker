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


"""Command line to run all tests or list all runnable tests.

Meant to speed up an automate testing of StarThinker.

To get list: python test/helper.py --list -u [credentials] -s [credentials] -p [project_id]
To get report: python test/helper.py -u [credentials] -s [credentials] -p [project_id]

"""


import os
import sys
import re
import argparse
import subprocess

from starthinker.setup import EXECUTE_PATH
from starthinker.util.project import project


RE_TEST = re.compile(r'test.*\.json')


if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--report', help='report ID to pull the achema.', default=None)
  parser.add_argument('--list', help='list tests.', action='store_true')

  # initialize project
  project.load(parser=parser)
  auth = 'service' if project.args.service else 'user'

  for root, dirs, files in os.walk(EXECUTE_PATH):
    for filename in files:
      if RE_TEST.match(filename) and '/project/' not in root:

        if project.args.list:
          print '%s/%s' % (root, filename)
        else:
          # assemble command ( replace command, use all arguments passed, and add instance )
          command = 'python2.7 %s/all/run.py %s/%s %s' % (EXECUTE_PATH, root, filename, ' '.join(sys.argv[1:]))
          print ''
          print 'TEST:', command
          subprocess.call(command, shell=True, cwd=EXECUTE_PATH, stderr=subprocess.STDOUT)
