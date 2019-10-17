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

""" Command line to execute all tasks in a recipe once. ( Common Entry Point )

This script dispatches all the tasks in a JSON recipe to handlers in sequence.
For each task, it calls a subprocess to execute the JSON instructions, waits
for the process to complete and dispatches the next task, until all tasks are 
complete or a critical failure ( exception ) is raised.

To execute a recipe run:

`python all/run.py [path to recipe file] [see optional arguments below] --force`

### Arguments

- path - run all tasks the specified recipe
- --project / -p - cloud id of project
- --user / -u - path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS
- --service / -s - path to service credentials json file
- --client / -c' - path to client credentials json file
- --verbose / -v - print all the steps as they happen.
- --force - execute all tasks regardless of schedule

### Notes

If an exception is raised in any task, all following tasks are not executed by design.
Obeys the schedule rules defined in /cron/README.md.
Uses credentials logic defined in /util/project/README.md.
For scheduled jobs this script is called by /cron/run.py.

### CAUTION

This script does NOT check if the last job finished, potentially causing overruns.

### Useful Development Features

To avoid running the entire script when debugging a single task, the command line 
can easily replace "all" with the name of any "task" in the json.  For example

`python all/run.py project/sample/say_hello.json`

Can be easily replaced with the following to run only the "hello" task:

`python task/hello/run.py project/sample/say_hello.json`

Or specified further to run only the second hello task:

`python task/hello/run.py project/sample/say_hello.json -i 2`

"""


import sys
import subprocess
import argparse

from starthinker.config import UI_ROOT
from starthinker.util.project import get_project, is_scheduled


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
  recipe = get_project(args.json)

  # track per task instance count
  instances = {}

  returncode = 0
  for task in recipe['tasks']:
    script, task = next(iter(task.items()))

    # count instance per task
    instances.setdefault(script, 0)
    instances[script] += 1

    # assemble command ( replace command, use all arguments passed, and add instance )
    command = 'python -W ignore %s/starthinker/task/%s/run.py %s -i %d' % (UI_ROOT, script, ' '.join(sys.argv[1:]), instances[script])

    # show command so user can run each task
    print(command)

    # execute command if schedule, return code
    if args.force or is_scheduled(recipe, task):
      returncode |= subprocess.Popen(command, shell=True).wait()

    # skip command if not schedule
    else:
      raise SystemExit("Schedule Skipping: run command manually or add --force to run all")

  # Set lowest return code from all tasks
  exit(returncode)
