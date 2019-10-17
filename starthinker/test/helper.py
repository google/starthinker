###########################################################################
# 
#  Copyright 2019 Google Inc.
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

To initialize: python test/helper.py --init
To run all: python test/helper.py
To run some: python test/helper.py --tests dt entity

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
from starthinker.script.run import script_read

CONFIG_FILE = UI_ROOT + '/starthinker/test/config.json'
TEST_DIRECTORY = UI_ROOT + '/starthinker/test/scripts/'
RECIPE_DIRECTORY = UI_ROOT + '/starthinker/test/recipes/'
LOG_DIRECTORY = UI_ROOT + '/starthinker/test/logs/'
RE_TEST = re.compile(r'test.*\.json')


def load_tests():
  for root, dirs, files in os.walk(TEST_DIRECTORY):
    for filename in files:
      print('LOADING', filename)
      yield filename, script_read(TEST_DIRECTORY + filename)


def initialize_tests():
  """Initialize all the necessary test files for Starthinker
  
  Args:
    None
  
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
  for filename, script in load_tests():
    script_fields = json_get_fields(script)
    script_name = filename.split('.')[0]

    for field in script_fields:
      fields.setdefault(script_name, {})
      fields[script_name][field["name"]] = old_fields.get(script_name, {}).get(field["name"], field.get("default", ''))
      fields[script_name]['%s_description' % field["name"]] = '(%s) %s' % (field.get('kind', 'string'), field.get('description', 'No description.'))

      if field["name"] not in old_fields.get(script_name, {}):
        print('NEW FIELD ADDED', script_name, field["name"])

  # Save field values to config file

  if fields:
    f = open(CONFIG_FILE,"w")
    f.write(json.dumps(fields, sort_keys=True, indent=2))
    f.close()  
  else:
    print('WARNING CONFIGURATION IS EMPTY, CHECK YOUR PATHS!')

  # Display instructions

  print("")
  print("------")
  print("------------")
  print("------------------------")
  print("Some tests require custom values. Update the necessary fields for the tests you wish to run.")
  print("EDIT: " + CONFIG_FILE)
  print("------------------------")
  print("Some tests require external assets.  Join the following group to gain access.")
  print("VISIT: https://groups.google.com/forum/#!forum/starthinker-assets")
  print("------------------------")
  print("------------")
  print("------")
  print("")
  sleep(3)


def run_tests(tests):

  # Load values from config file

  fields = {}
  if (os.path.exists(CONFIG_FILE)):
    with open(CONFIG_FILE, 'r') as f:
      fields = json.load(f)

  # Create recipe directory

  print('GENERATE RECIPES')
  os.makedirs(RECIPE_DIRECTORY, exist_ok=True)

  # Create recipes from scripts

  recipes = []
  for filename, script in load_tests():
    name = filename.split('.')[0]
    if tests and name not in tests: continue

    # Set cal config field values into the script
    json_set_fields(script, fields.get(name, {}))

    with open(RECIPE_DIRECTORY + filename, 'w') as f:
      f.write(json.dumps(script, sort_keys=True, indent=2))
    
    recipes.append(filename)

  # Create log directory and clear old logs

  os.makedirs(LOG_DIRECTORY, exist_ok=True)

  if not tests:
    print('CLEAR LOGS')
    for f in glob.glob(LOG_DIRECTORY + '*.log'):
      os.remove(f)

  # Create a process for each recipe execution

  jobs = []
  for recipe in recipes:
    if tests and recipe.split('.')[0] not in tests: continue
    command = [
      '%s/starthinker_virtualenv/bin/python' % UI_ROOT,
      '-W', 'ignore',
      '%s/starthinker/all/run.py' % UI_ROOT,
      RECIPE_DIRECTORY + recipe,
      '-u $STARTHINKER_USER',
      '-s $STARTHINKER_SERVICE',
      '-p $STARTHINKER_PROJECT',
      '--verbose',
      '--force',
    ]

    print('LAUNCHED:', ' '.join(command))

    jobs.append({
      'recipe':recipe,
      'process':subprocess.Popen(command, shell=False, cwd=UI_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

      print('\nOK:' if poll == 0 else '\nFAILED:', job['recipe'], 'REMAINING:', len(jobs))

      output, errors = job['process'].communicate()
      with open(LOG_DIRECTORY + ('OK_' if poll == 0 else 'FAILED_') + job['recipe'].replace('.json', '.log'), 'w') as f:
        f.write(output.decode())
        f.write(errors.decode())

    # Start checking jobs from end again
    if i == 0:
      i = len(jobs)

  print("")
  print("------")
  print("------------")
  print("------------------------")
  print('TEST RESULTS: ls -1 %s*.log' % LOG_DIRECTORY)
  print("------------------------")
  print("------------")
  print("------")
  print("")


def tests():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--init', help='Initialize test config.json only.', action='store_true')
  parser.add_argument('-t', '--tests', nargs='*', help='Run only these tests, name of test from scripts without .json part.')

  args = parser.parse_args()

  if args.init:
    initialize_tests()
  else:
    initialize_tests()
    run_tests(args.tests or [])


if __name__ == "__main__":
  tests()
