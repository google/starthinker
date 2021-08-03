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
  colab.paragraph(
      'First install the libraries needed to execute recipes, this only needs to be done once, then click play.'
  )
  colab.code('!pip install git+https://github.com/google/starthinker')

  colab.header('2. Get Cloud Project ID')
  colab.paragraph(
      'To run this recipe [requires a Google Cloud Project](https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md), this only needs to be done once, then click play.'
  )
  #colab.image('Client Project ID', 'https://github.com/google/starthinker/raw/master/tutorials/images/cloud_project.png')
  colab.code('CLOUD_PROJECT = \'%s\'' % (project or 'PASTE PROJECT ID HERE'))
  colab.code('\nprint("Cloud Project Set To: %s" % CLOUD_PROJECT)')

  colab.header('3. Get Client Credentials')
  #colab.image('Client Credentials', 'https://github.com/google/starthinker/raw/master/tutorials/images/cloud_client_installed.png')
  colab.paragraph(
      'To read and write to various endpoints requires [downloading client credentials](https://github.com/google/starthinker/blob/master/tutorials/cloud_client_installed.md), this only needs to be done once, then click play.'
  )
  colab.code('CLIENT_CREDENTIALS = \'%s\'' % (client_credentials or 'PASTE CLIENT CREDENTIALS HERE'))
  colab.code('\nprint("Client Credentials Set To: %s" % CLIENT_CREDENTIALS)')

  fields = json_get_fields(tasks)
  if fields:
    colab.header('4. Enter %s Parameters' % name)
    colab.list(instructions)
    colab.paragraph(
        'Modify the values below for your use case, can be done multiple times, then click play.'
    )
    colab.code('FIELDS = %s' % fields_to_string(fields, parameters))
    colab.code('\nprint("Parameters Set To: %s" % FIELDS)')

  colab.header('%d. Execute %s' % (5 if fields else 4, name))
  colab.paragraph(
      'This does NOT need to be modified unless you are changing the recipe, click play.'
  )

  colab.code('from starthinker.util.configuration import Configuration')
  colab.code('from starthinker.util.configuration import execute')
  colab.code('from starthinker.util.recipe import json_set_fields')
  colab.code('')
  colab.code("USER_CREDENTIALS = '/content/user.json'")
  colab.code('')
  colab.code('TASKS = %s' %
             dict_to_string(json_set_auths(tasks, 'user'), skip=('field',)))
  colab.code('')

  if fields:
    colab.code('json_set_fields(TASKS, FIELDS)')
  colab.code('')

  colab.code('execute(Configuration(project=CLOUD_PROJECT, client=CLIENT_CREDENTIALS, user=USER_CREDENTIALS, verbose=True), TASKS, force=True)')

  return colab.render()


def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Command line to turn recipe into Jupyter Notebook.

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
