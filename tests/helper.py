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


"""Command line to set up and run all the necessary test files for Starthinker.

  The test helper creates and checks a starthinker_assets/tests.json harness
  file with all the variables required to run each test.  It then runs each test
  in a process and polls for completion.  Tests run in parallel.

  Examples:
    To configure: python tests/helper.py --configure
    To run all: python tests/helper.py
    To run some: python tests/helper.py --tests dt entity

  Args:
    -c', --configure: Configure test in starthinker_assets/tests.json only. No run.
    -t', --tests: Run only these tests, name of test from scripts.
    -s', --skips: Skip these tests, name of test from scripts.
    -i', --include: Used for namespacing test files and avoiding collisions.
    -r', --test_run_id: Specify a test run ID to inject into the test config fields.

  Returns:
    Writes data to tests/logs/ as [FAILED][OK]_test_name.log.
    The files contain all STDOUT and STDERR output from each task.
"""

import argparse
import fcntl
import glob
import json
import os
import subprocess
import re
from time import sleep

from starthinker.config import UI_PROJECT
from starthinker.config import UI_ROOT
from starthinker.config import UI_SERVICE
from starthinker.script.parse import json_get_fields
from starthinker.script.parse import json_set_fields
from starthinker.util.project import get_project

CONFIG_FILE = UI_ROOT + '/starthinker_assets/tests.json'
TEST_DIRECTORY = UI_ROOT + '/tests/scripts/'
RECIPE_DIRECTORY = UI_ROOT + '/tests/recipes/'
LOG_DIRECTORY = UI_ROOT + '/tests/logs/'
RE_TEST = re.compile(r'test.*\.json')


def make_non_blocking(file_io):
  fd = file_io.fileno()
  fl = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def json_expand_includes(script):
  expanded_tasks = []
  for task in script['tasks']:
    function, parameters = next(iter(task.items()))

    if function == 'include':
      tasks = get_project(UI_ROOT + '/' + parameters['script'])['tasks']
      json_set_fields(tasks, parameters['parameters'])
      for t in tasks:
        function, parameters = next(iter(t.items()))
        expanded_tasks.append({function: parameters})

    else:
      expanded_tasks.append({function: parameters})

  script['tasks'] = expanded_tasks

  return script


def load_tests():
  for root, dirs, files in os.walk(TEST_DIRECTORY):
    for filename in files:
      if filename.endswith('.json'):
        print('LOADING', filename)
        yield filename, get_project(TEST_DIRECTORY + filename)


def configure_tests(tests, runs, skips, test_run_id):
  """Initialize the starthinker_assets/tests.json variable harness.

  Read all existing tests from tests/scripts/*.json and create a dictionary of
  each script and fields.  Save that dictionary to a test harness file where
  developer can configure tests.

  Then read the test harness and create recipe files to that can be run.  Write
  those files to tests/recipes/*.json for execution in a later step.

  Args:
    test: List of (filename, json) pairs containing all the tests.
    runs: List of test names that will be run, all will run if blank.
    skips: List of tests to skip.
    test_run_id: String added as a field to each test, used for namespacing.

  Returns:
    List of JSON recpies, where all fields have values from the test harness.

  """

  # Get old fields from the config file

  print('UPDATE CONFIG')

  old_fields = {}
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
      old_fields = json.load(f)

  # Get new fields from test files and merge in old values

  fields = {}
  for filename, script in tests:
    script_fields = json_get_fields(script)
    script_name = filename.split('.')[0]

    for field in script_fields:
      if field['name'] == 'test_run_id': continue
      fields.setdefault(script_name, {})
      fields[script_name][field['name']] = old_fields.get(script_name, {}).get(
          field['name'], field.get('default', ''))
      fields[script_name][
          '%s_description' % field['name']] = '(%s) %s' % (field.get(
              'kind', 'string'), field.get('description', 'No description.'))

      if field['name'] not in old_fields.get(script_name, {}):
        print('NEW FIELD ADDED', script_name, field['name'])

  # Save field values to config file

  if fields:
    f = open(CONFIG_FILE, 'w')
    f.write(json.dumps(fields, sort_keys=True, indent=2))
    f.close()

    if test_run_id:
      # Inject the test run ID to the list of field values that were read from the
      # test config file. This is done in memory only, so that concrete test run
      # value are replaced every time a test runs.
      for script in fields:
        fields[script]['test_run_id'] = test_run_id
  else:
    print('WARNING CONFIGURATION IS EMPTY, CHECK YOUR PATHS!')

  # Create recipe directory

  print('GENERATE RECIPES')
  os.makedirs(RECIPE_DIRECTORY, exist_ok=True)

  # Create recipes from tests

  recipes = []
  for filename, script in tests:
    name = filename.split('.')[0]
    if runs and name not in runs:
      continue
    if name in skips:
      continue

    # Set config field values into the script
    json_set_fields(script, fields.get(name, {}))

    # Expand all includes to full recipe
    json_expand_includes(script)

    with open(RECIPE_DIRECTORY + filename, 'w') as f:
      f.write(json.dumps(script, sort_keys=True, indent=2))

    recipes.append(filename)

  # Create log directory and clear old logs

  os.makedirs(LOG_DIRECTORY, exist_ok=True)

  # Display instructions

  print('')
  print('------')
  print('------------')
  print('------------------------')
  print(
      'Some tests require custom values. Update the necessary fields for the tests you wish to run.'
  )
  print('EDIT: ' + CONFIG_FILE)
  print('------------------------')
  print(
      'Some tests require external assets.  Join the following group to gain access.'
  )
  print('VISIT: https://groups.google.com/forum/#!forum/starthinker-assets')
  print('------------------------')
  print('------------')
  print('------')
  print('')
  sleep(3)

  return recipes

def run_tests(tests, recipes, runs, skips):
  """Run tests derived from tests/scripts/*.json.

  Each test was written to a file in tests/recipes/*.json, which will spin
  up a process allowing parallel execution. Each process is monitored for exit
  status.

  If status is OK, all tasks OK, writes to tests/logs/OK_*.json.
  If status is ERROR, any task ERROR, writes to tests/logs/OK_*.json.

  Args:
    test: List of (filename, json) pairs containing test definitions.
    recipes: List of (filename, json) pairs containing executable recipes.
    runs: List of test names that will be run, all will run if blank.
    skips: List of tests to skip.

  Returns:
    Writes data to tests/logs/ as [FAILED][OK]_test_name.log.
    The files contain all STDOUT and STDERR output from each task.

  """

  if not runs:
    print('CLEAR LOGS')
    for f in glob.glob(LOG_DIRECTORY + '*.log'):
      os.remove(f)

  # Create a process for each recipe execution

  jobs = []
  for recipe in recipes:
    if runs and recipe.split('.')[0] not in runs: continue
    if recipe.split('.')[0] in skips: continue

    command = [
        'python',
        '-W',
        'ignore',
        '%s/starthinker/all/run.py' % UI_ROOT,
        RECIPE_DIRECTORY + recipe,
        '-u $STARTHINKER_USER',
        '-s $STARTHINKER_SERVICE',
        '-c $STARTHINKER_CLIENT',
        '-p $STARTHINKER_PROJECT',
        '--verbose',
        '--force',
    ]

    print('LAUNCHED:', ' '.join(command))

    jobs.append({
        'recipe':
            recipe,
        'output':
            '',
        'errors':
            '',
        'process':
            subprocess.Popen(
                command,
                shell=False,
                cwd=UI_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    })

    # give ability to read buffers without locking process
    make_non_blocking(jobs[-1]['process'].stdout)
    make_non_blocking(jobs[-1]['process'].stderr)

  # Monitor each job for completion and write to log

  i = len(jobs)
  while i:
    print('.', end='', flush=True)
    sleep(10)

    i = i - 1

    # read output every time as buffer may fill up and lock process
    stdout = jobs[i]['process'].stdout.read()
    if stdout is not None:
      jobs[i]['output'] += stdout.decode()

    stderr = jobs[i]['process'].stderr.read()
    if stderr is not None:
      jobs[i]['errors'] += stderr.decode()

    poll = jobs[i]['process'].poll()

    if poll is not None:
      job = jobs.pop(i)

      print('\nOK:' if poll == 0 else '\nFAILED:', job['recipe'], 'REMAINING:',
            len(jobs), [j['recipe'].replace('.json', '') for j in jobs])

      with open(
          LOG_DIRECTORY + ('OK_' if poll == 0 else 'FAILED_') +
          job['recipe'].replace('.json', '.log'), 'w') as f:
        f.write(job['output'])
        f.write(job['errors'])

    # Start checking jobs from end again
    if i == 0:
      i = len(jobs)

  print('')
  print('------')
  print('------------')
  print('------------------------')
  print('TEST RESULTS: ls -1 %s*.log' % LOG_DIRECTORY)
  print('------------------------')
  print('------------')
  print('------')
  print('')


def generate_include(script_file):
  script = get_project(script_file)

  # parse fields and constants into parameters
  print('    { "include":{')
  print('      "script":"%s",' % script_file)
  print('      "parameters":{')
  print(',\n'.join([
      '        "%s":{"field":{ "name":"%s", "kind":"%s", "description":"%s" }}'
      % (field['name'], field['name'], field['kind'],
         field.get('description', '')) for field in json_get_fields(script)
  ]))
  print('      }')
  print('    }}')
  print('')


def tests():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-c',
    '--configure',
    help='Configure test in starthinker_assets/tests.json only.', action='store_true'
  )
  parser.add_argument(
    '-t',
    '--tests',
    nargs='*',
    help='Run only these tests, name of test from tests/scripts/*.json.'
  )
  parser.add_argument(
    '-s',
    '--skips',
    nargs='*',
    help='Skip these tests, name of test from tests/scripts/*.json.'
  )
  parser.add_argument(
    '-i',
    '--include',
    default=None,
    help='Used for namespacing test files and avoiding collisions.'
  )
  parser.add_argument(
    '-r',
    '--test_run_id',
    default='Manual',
    help='Specify a test run ID to inject into the test config fields.'
  )

  args = parser.parse_args()

  print('')

  if args.include:
    generate_include(args.include)

  else:
    tests = list(load_tests())
    runs = [t.split('.')[0] for t in (args.tests or [])]
    skips = [t.split('.')[0] for t in (args.skips or [])]

    if args.configure:
      configure_tests(tests, runs, skips, args.test_run_id)
    else:
      recipes = configure_tests(tests, runs, skips, args.test_run_id)
      run_tests(tests, recipes, runs, skips)


if __name__ == '__main__':
  tests()
