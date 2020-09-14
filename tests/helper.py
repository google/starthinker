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
"""Command line to run all tests or list all runnable tests.

Meant to speed up automated testing of StarThinker.

To configure: python tests/helper.py --configure
To run all: python tests/helper.py
To run some: python tests/helper.py --tests dt entity

"""

import os
import re
import glob
import argparse
import subprocess
import json
from time import sleep

from starthinker.config import UI_ROOT, UI_SERVICE, UI_PROJECT
from starthinker.script.parse import json_get_fields, json_set_fields
from starthinker.util.project import get_project

CONFIG_FILE = UI_ROOT + '/starthinker_assets/tests.json'
TEST_DIRECTORY = UI_ROOT + '/tests/scripts/'
RECIPE_DIRECTORY = UI_ROOT + '/tests/recipes/'
LOG_DIRECTORY = UI_ROOT + '/tests/logs/'
RE_TEST = re.compile(r'test.*\.json')


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


def configure_tests(scripts, tests):
  """Initialize all the necessary test files for Starthinker

  Args: None

  Returns:
    None

  """

  # Get old fields from the config file

  print('UPDATE CONFIG')

  old_fields = {}
  if (os.path.exists(CONFIG_FILE)):
    with open(CONFIG_FILE, 'r') as f:
      old_fields = json.load(f)

  # Get new fields from test files and merge in old values

  fields = {}
  for filename, script in scripts:
    script_fields = json_get_fields(script)
    script_name = filename.split('.')[0]

    for field in script_fields:
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
  else:
    print('WARNING CONFIGURATION IS EMPTY, CHECK YOUR PATHS!')

  # Create recipe directory

  print('GENERATE RECIPES')
  os.makedirs(RECIPE_DIRECTORY, exist_ok=True)

  # Create recipes from scripts

  recipes = []
  for filename, script in scripts:
    name = filename.split('.')[0]
    if tests and name not in tests:
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


def run_tests(scripts, recipes, tests):

  if not tests:
    print('CLEAR LOGS')
    for f in glob.glob(LOG_DIRECTORY + '*.log'):
      os.remove(f)

  # Create a process for each recipe execution

  jobs = []
  for recipe in recipes:
    if tests and recipe.split('.')[0] not in tests:
      continue
    command = [
        '%s/starthinker_virtualenv/bin/python' % UI_ROOT,
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
        'process':
            subprocess.Popen(
                command,
                shell=False,
                cwd=UI_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    })

  # Monitor each job for completion and write to log

  i = len(jobs)
  while i:
    print('.', end='', flush=True)
    sleep(10)

    i = i - 1
    poll = jobs[i]['process'].poll()
    if poll is not None:
      job = jobs.pop(i)

      print('\nOK:' if poll == 0 else '\nFAILED:', job['recipe'], 'REMAINING:',
            len(jobs), [j['recipe'].replace('.json', '') for j in jobs])

      output, errors = job['process'].communicate()
      with open(
          LOG_DIRECTORY + ('OK_' if poll == 0 else 'FAILED_') +
          job['recipe'].replace('.json', '.log'), 'w') as f:
        f.write(output.decode())
        f.write(errors.decode())

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
      help='Configure test in starthinker_assets/tests.json only.',
      action='store_true')
  parser.add_argument(
      '-t',
      '--tests',
      nargs='*',
      help='Run only these tests, name of test from scripts without .json part.'
  )
  parser.add_argument(
      '-i',
      '--include',
      help='Create an include file for the script, used in tests.',
      default=None)

  args = parser.parse_args()

  print('')

  if args.include:
    generate_include(args.include)

  else:
    scripts = list(load_tests())
    tests = [t.split('.')[0] for t in (args.tests or [])]

    if args.configure:
      configure_tests(scripts, tests)
    else:
      recipes = configure_tests(scripts, tests)
      run_tests(scripts, recipes, tests)


if __name__ == '__main__':
  tests()
