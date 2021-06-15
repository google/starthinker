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
"""Handler that executes { "hello":{...}} task in recipe JSON.

This is meant as an example only, it executes no useful tasks. Use this as
a template for how to connect a handler to a JSON recipe task.  It
illustrates how to use JOSN variables, access constants in the system, and
best practices for using this framework.  Credentials are not required for
this recipe handler.

Call from the command line using:

  - `python all/run.py scripts/say_hello.json`

Call from code using:

  - `hello(recipe, instance)`

"""

import json
import time

def hello(config, task):

  if config.verbose:
    print('HELLO')

  print('')
  print('-' * 80)
  print('Tasks are just python, you can do whatever.')
  print('This is a task being executed.')
  print('')
  print('SAY:', task['say'])
  print('')
  print('')

  print('-' * 80)
  print('Every task automatically gets a date parameter.')
  print('The parameter can be passed in, or defaults to today.')
  print('')
  print('PROJECT DATE:', config.date)
  print('')
  print('')

  print('-' * 80)
  print('Most tasks operate on top of Google Cloud infrastructure.')
  print("Every task specifies an 'auth' parameter as 'user' or 'service'.")
  print('Every config has its own credentails paths.')
  print(
      "If you provide 'client' credentials, the 'user' credentials will be populated as necessary."
  )
  print(
      "If you provde the 'user' credentails, the 'client' credentials are not necessary."
  )
  print("If you use the 'service' credentials, you must add them manually.")
  print('')
  print('PROJECT ID:', config.project)
  print(
      'PROJECT CLIENT CREDENTIALS:',
      config.recipe.get('setup', {}).get('auth', {}).get('client', 'MISSING'))
  print('PROJECT USER CREDENTIALS:',
        config.recipe.get('setup', {}).get('auth', {}).get('user', 'MISSING'))
  print(
      'PROJECT SERVICE CREDENTIALS:',
      config.recipe.get('setup', {}).get('auth', {}).get('service', 'MISSING'))
  print('')
  print('')

  print('-' * 80)
  print('Your entire recipe definition is accessible as a dictionary.')
  print('The task name must match a directory with a run.py inside it.')
  print(
      "For example, 'hello' is a task which will executed by 'task/hello/run.py'."
  )
  print('')
  print('PROJECT JSON:')
  print(json.dumps(config.recipe, indent=2, default=str))

  print('')
  print('')

  print('-' * 80)
  print('Each task is passed a nested subset of json.')
  print(
      'Different tasks should NOT share json. Security and readability reasons.'
  )
  print('Each task can execute as a service or a user independently.')
  print('Access structure data within a task as...')
  print('')
  print('PROJECT TASK:', task)
  print('PROJECT TASK AUTH:', task['auth'])
  print('PROJECT TASK SAY:', task['say'])
  print('')
  print('')

  if task.get('sleep'):
    print('PROJECT TASK SLEEP:', task['sleep'])
    time.sleep(task['sleep'])

  if task.get('error'):
    print('PROJECT TASK ERROR TRIGGERED:')
    raise Exception(task['error'])

  print('-' * 80)
  print("Take a look inside 'task/hello/run.py'.")
  print('Its a great skeleton for your first recipe.')
  print('')
  print('')


if __name__ == '__main__':
  hello()
