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

"""StarThinker generator for Colab Notebooks.

Includes both the command line and librarires used by UI.
See main for usage description.
"""

import json
import argparse
import textwrap

from starthinker.util.configuration import commandline_parser
from starthinker.util.recipe import dict_to_string
from starthinker.util.recipe import fields_to_string
from starthinker.util.recipe import get_recipe
from starthinker.util.recipe import json_get_fields
from starthinker.util.recipe import json_set_auths
from starthinker.util.colab import Colab


def recipe_to_colab(name, description, instructions, tasks, parameters={}, project=None, client_credentials=None, user_credentials=None, service_credentials=None):
  """ Converts a JSON recipe into a Jupyter Notebook for Colabs.

  Sets up multiple steps to execute recipe:
    1. Install starthinker from repository
    2. Get Cloud Project ID.
    3. Get Client Credentials ( optional if User Credentials exist ).
    4. Enter Recipe parameters if fields present.
    5. Execute recipe tasks.

  Args:
    * name: (string) The name of the notebook.
    * description: (string) A description fo the recipe.
    * instructions: (string) Recipe manual instructions, for example connecting datastudios.
    * tasks: (list) The task JSON to execute.
    * parameters: (dict) Values for field parameters in tasks, optional.
    * project: (string) The GCP project id.
    * client_credentials: (string) The GCP Desktop Client Credentials in JSON string.
    * user_credentials: (string) Not used, placeholder.
    * service_credentials: (string) Not used, placeholder.

  Returns:
    * (string) Rendered notebook source code to be written to a ipynb file.
  """

  colab = Colab(name)

  colab.header(name)
  colab.paragraph(description)

  colab.header('License')
  colab.paragraph(textwrap.dedent('''
    Copyright 2020 Google LLC,

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
  '''))

  colab.header('Disclaimer')
  colab.paragraph('This is not an officially supported Google product. It is a reference implementation. There is absolutely NO WARRANTY provided for using this code. The code is Apache Licensed and CAN BE fully modified, white labeled, and disassembled by your team.')
  colab.paragraph(textwrap.dedent('''
    This code generated (see starthinker/scripts for possible source):
      - **Command**: "python starthinker_ui/manage.py colab"
      - **Command**: "python starthinker/tools/colab.py [JSON RECIPE]"
  '''))

  colab.header('1. Install Dependencies')
  colab.paragraph('First install the libraries needed to execute recipes, this only needs to be done once, then click play.')
  colab.code('!pip install git+https://github.com/google/starthinker')

  colab.header('2. Set Configuration')
  colab.paragraph(textwrap.dedent('''
    This code is required to initialize the project. Fill in required fields and press play.

    1. If the recipe uses a Google Cloud Project:
      - Set the configuration **project** value to the project identifier from [these instructions](https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md).

    1. If the recipe has **auth** set to **user**:
      - If you have user credentials:
        - Set the configuration **user** value to your user credentials JSON.
      - If you DO NOT have user credentials:
        - Set the configuration **client** value to [downloaded client credentials](https://github.com/google/starthinker/blob/master/tutorials/cloud_client_installed.md).

    1. If the recipe has **auth** set to **service**:
      - Set the configuration **service** value to [downloaded service credentials](https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md).
  '''))

  #colab.image('Client Project ID', 'https://github.com/google/starthinker/raw/master/tutorials/images/cloud_project.png')
  #colab.image('Client Credentials', 'https://github.com/google/starthinker/raw/master/tutorials/images/cloud_client_installed.png')

  colab.code('from starthinker.util.configuration import Configuration')
  colab.code('')
  colab.code(textwrap.dedent('''
    CONFIG = Configuration(
      project="",
      client={},
      service={},
      user="/content/user.json",
      verbose=True
    )
  '''))

  fields = json_get_fields(tasks)
  if fields:
    colab.header('3. Enter %s Recipe Parameters' % name)
    colab.list(instructions)
    colab.paragraph('Modify the values below for your use case, can be done multiple times, then click play.')
    colab.code('FIELDS = %s' % fields_to_string(fields, parameters))
    colab.code('\nprint("Parameters Set To: %s" % FIELDS)')

  colab.header('%d. Execute %s' % (4 if fields else 3, name))
  colab.paragraph('This does NOT need to be modified unless you are changing the recipe, click play.')

  colab.code('from starthinker.util.configuration import execute')
  colab.code('from starthinker.util.recipe import json_set_fields')
  colab.code('')
  colab.code('TASKS = %s' % dict_to_string(json_set_auths(tasks, 'user'), skip=('field',)))
  colab.code('')

  if fields:
    colab.code('json_set_fields(TASKS, FIELDS)')
  colab.code('')

  colab.code('execute(CONFIG, TASKS, force=True)')

  return colab.render()


def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Command line to turn StarThinker Recipe into Colab Notebook.

    Example:
      python colab.py [path to existing recipe.json] --fo [path to new jupyter file.ipynb]

  """))

  parser.add_argument('json', help='Path to recipe json file to load.')

  parser.add_argument(
    '--file_out',
    '-fo',
    help='Path to recipe file to be written if replacing fields.',
    default=None
  )

  # initialize project
  parser = commandline_parser(parser, arguments=('-p', '-c', '-u', '-s'))

  args = parser.parse_args()

  # load json to get each task
  recipe = get_recipe(args.json)

  # create Jupyter Notebook (Colab)
  notebook = recipe_to_colab(
    name=(args.file_out or args.json).rsplit('/', 1)[-1].split('.')[0], # take filename without extension of destination or source
    description=recipe.get('description'),
    instructions=recipe.get('instructions'),
    tasks=recipe['tasks'],
    project=args.project,
    client_credentials=args.client,
    user_credentials=args.user,
    service_credentials=args.service
  )

  # check to write converted fields to stdout
  if args.file_out:
    print('Writing to:', args.file_out)
    f = open(args.file_out, 'w')
    f.write(notebook)
    f.close()
  else:
    print(notebook)


if __name__ == '__main__':
  main()
