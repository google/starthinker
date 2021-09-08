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

  The test helper creates and checks a starthinker_assets/tests/ harness
  file with all the variables required to run each test.  It then runs each test
  in a process and polls for completion.  Tests run in parallel.

  Examples:
    To configure: python tests/helper.py --configure
    To run all: python tests/helper.py
    To run some: python tests/helper.py --tests dt entity

  Args:
    -c', --configure: Configure test harness in starthinker_assets/tests/ only. No run.
    -t', --tests: Run only these tests, name of test from scripts.
    -s', --skips: Skip these tests, name of test from scripts.
    -i', --include: Used for namespacing test files and avoiding collisions.
    -r', --test_run_id: Specify a test run ID to inject into the test config fields.

  Returns:
    Writes data to starthinker_assets/logs/ as [FAILED][OK]_test_name.log.
    The files contain all STDOUT and STDERR output from each task.
"""

import argparse
import glob
import json
import os
import subprocess
import re
from time import sleep

# does not exist on WINDOWS, ignore
try:
  import fcntl
except ImportError:
  pass

from starthinker.config import UI_ROOT
from starthinker.util.recipe import json_get_fields
from starthinker.util.recipe import json_set_fields
from starthinker.util.recipe import get_recipe

INCLUDES_DIRECTORY = UI_ROOT
HARNESS_DIRECTORY = UI_ROOT + '/starthinker_assets/tests/'
TEST_DIRECTORY = UI_ROOT + '/tests/'
LOG_DIRECTORY = UI_ROOT + '/starthinker_assets/logs/'


def make_non_blocking(file_io):
  # does not exist on WINDOWS, ignore
  try:
    fd = file_io.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
  except:
     pass


def load_tests():
  for root, dirs, files in os.walk(TEST_DIRECTORY):
    for filename in files:
      if filename.endswith('.json'):
        print('LOADING', filename)
        yield filename, get_recipe(TEST_DIRECTORY + filename, INCLUDES_DIRECTORY)


def configure_tests(tests, test_run_id):
  """Initialize the starthinker_assets/tests.json variable harness.

  Read all existing tests from tests/*.json and create a harness file in
  starthinker_assets/tests/*.json so developer can configure tests.

  Args:
    test: List of (filename, json) pairs containing all the tests.

  Returns:
    None

  """

  # Get old fields from the config file

  print('UPDATE CONFIG')

  # Create harness directory and clear old logs
  os.makedirs(HARNESS_DIRECTORY, exist_ok=True)

  # Get new fields from test files and merge in old values
  for filename, script in tests:

    # load script fields
    script_fields = json_get_fields(script)
    script_name = filename.split('.')[0]

    # load harness fields
    harness_fields = {}
    harness_path = HARNESS_DIRECTORY + script_name + '.json'
    if os.path.exists(harness_path):
      with open(harness_path, 'r') as f:
        harness_fields = json.load(f)

    # merge harness and script fields
    new_fields = {}
    for field in script_fields:
      if field['name'] == 'test_run_id':
        new_fields['test_run_id'] = test_run_id
      else:
        new_fields[field['name']] = harness_fields.get(field['name'], field.get('default'))
        new_fields['%s_description' % field['name']] = '(%s) %s' % (field.get('kind', 'string'), field.get('description', 'No description.'))
        if field['name'] not in harness_fields:
          print('NEW FIELD ADDED', script_name, field['name'])

    # save fields to harness
    if new_fields:
      with open(harness_path, 'w') as f:
        json.dump(new_fields, f, indent=2)
    elif os.path.exists(harness_path):
      os.remove(harness_path)

  # Display instructions
  print('')
  print('------')
  print('------------')
  print('------------------------')
  print(
      'Some tests require custom values. Update the necessary fields for the tests you wish to run.'
  )
  print('EDIT: ' + HARNESS_DIRECTORY)
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


def run_tests(tests):
  """Run tests tests/*.json and parameters starthinker_assets/tests/*.json.

  Each test will execute in a unique process and allowing parallel execution.
  Each process is monitored for exit status.

  If status is OK, all tasks OK, writes to starthinker_assets/logs/OK_*.json.
  If status is ERROR, any task ERROR, writes to starthinker_assets/logs/OK_*.json.

  Args:
    test: List of (filename, json) pairs containing test definitions.

  Returns:
    Writes data to starthinker_assets/logs/ as [FAILED][OK]_test_name.log.
    The files contain all STDOUT and STDERR output from each task.

  """

  # Create a process for each recipe execution

  jobs = []
  for filename, script in tests:

    parameters = '%s%s' % (HARNESS_DIRECTORY, filename)

    command = [
      'python',
      '%s/starthinker/tool/recipe.py' % UI_ROOT,
      '%s%s' % (TEST_DIRECTORY, filename),
      '-u $STARTHINKER_USER',
      '-s $STARTHINKER_SERVICE',
      '-c $STARTHINKER_CLIENT',
      '-p $STARTHINKER_PROJECT',
      #'-pi "%s%s"' % (HARNESS_DIRECTORY, filename),
      '-i %s' % INCLUDES_DIRECTORY,
      '--verbose',
      '--force',
    ]

    # only add parameters if they are required and configured
    if os.path.isfile(parameters):
      command.insert(6, '-pi "%s"' % parameters)

    print('LAUNCHED:', ' '.join(command))

    jobs.append({
        'recipe': filename,
        'output': '',
        'errors': '',
        'process': subprocess.Popen(
          ' '.join(command), #use join if shell=True
          shell=True,
          cwd=UI_ROOT,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE
       )
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
  script = get_recipe(script_file)

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
    help='Configure test in starthinker_assets/tests/ only.', action='store_true'
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

    if runs:
      tests = [t for t in tests if t[0].split('.')[0] in runs]

    if skips:
      tests = [t for t in tests if t[0].split('.')[0] not in skips]

    configure_tests(tests, args.test_run_id)

    if not args.configure:
      # Create log directory and clear old logs
      os.makedirs(LOG_DIRECTORY, exist_ok=True)

      if not runs:
        print('CLEAR LOGS')
        for f in glob.glob(LOG_DIRECTORY + '*.log'):
          os.remove(f)
      run_tests(tests)


if __name__ == '__main__':
  tests()
