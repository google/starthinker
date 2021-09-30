###########################################################################
#
#  Copyright 2021 Google LLC
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

"""StarThinker generator for python examples.

Includes both the command line and libraries used by UI.
See main for usage description.
"""

import argparse
import textwrap

from starthinker.util.configuration import commandline_parser
from starthinker.util.recipe import dict_to_python
from starthinker.util.recipe import get_recipe
from starthinker.util.recipe import json_get_fields
from starthinker.util.recipe import json_expand_queries

DISCLAIMER = '''###########################################################################
#
#  Copyright 2021 Google LLC
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
#
#  This code generated (see scripts folder for possible source):
#    - Command: "python starthinker_ui/manage.py example"
#
###########################################################################

'''

def parameters_to_argparse(description, instructions, parameters):
  code =  '  parser = argparse.ArgumentParser(\n'
  code += '    formatter_class=argparse.RawDescriptionHelpFormatter,\n'
  code += '    description=textwrap.dedent("""\n'

  if description:
    code += '      %s\n' % description

  if instructions:
    code += '\n'
    for step, instruction in enumerate(instructions, 1):
      code += '        %d. %s\n' % (step, instruction)

  code += '  """))\n\n'

  code += '  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)\n'
  code += '  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)\n'
  code += '  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)\n'
  code += '  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)\n'
  code += '  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)\n'
  code += '  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")\n'

  code += '\n'

  for parameter in parameters:
    code += '  parser.add_argument("-%s", help="%s", default=%s)\n' % (parameter['name'], parameter.get('description', ''), repr(parameter.get('default')))

  code += '\n'

  return code


def recipe_to_python(name, description, instructions, tasks, parameters={}, project=None, client_credentials=None, user_credentials=None, service_credentials=None):
  """ Converts a JSON recipe into a python stand alone example.

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
    * (string) Rendered example source code to be written to a py file.
  """

  # Expand all queries
  tasks = json_expand_queries(tasks)

  # Add imports
  code = DISCLAIMER
  code += 'import argparse\n'
  code += 'import textwrap\n\n'
  code += 'from starthinker.util.configuration import Configuration\n'

  imported = set()
  for task in tasks:
    script, task = next(iter(task.items()))
    if script not in imported:
      code += 'from starthinker.task.%s.run import %s\n' % (script, script)
      imported.add(script)
  code += '\n'
  code += '\n'

  # Create function for recipe
  fields = json_get_fields(tasks)
  if fields:
    code += 'def recipe_%s(config, %s):\n' % (name, ', '.join([f['name'] for f in fields]))
  else:
    code += 'def recipe_%s(config):\n' % name

  # Add docstring
  if description or fields:
    code += '  """' + textwrap.fill(
      description,
      width=80,
      subsequent_indent="     "
    ) + '\n'

    if fields:
      code += '\n     Args:\n'
      for field in fields:
        code += '       %s (%s) - %s\n' % (field['name'], field['kind'], field.get('description', 'NA'))

    code += '  """\n\n'

  # Add calls
  for task in tasks:
    script, task = next(iter(task.items()))
    code += '  %s(config, %s)\n\n' % (script, dict_to_python(task, indent=1))

  code += '\n'
  code += '\n'
  code += 'if __name__ == "__main__":\n'

  # Add argparse for each field
  code += parameters_to_argparse(description, instructions, fields)

  code += '\n'
  code += '  args = parser.parse_args()\n'
  code += '\n'

  code += '''  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )'''

  code += '\n\n'

  if fields:
    code += '  recipe_%s(config, %s)\n' % (name, ', '.join(['args.%s' % f['name'] for f in fields]))
  else:
    code += '  recipe_%s(config)\n' % name

  return code


def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Command line to turn StarThinker Recipe into Python script.

    Example:
      python example.py [path to existing recipe.json] --fo [path to new python file.py]

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

  # create Python file
  example = recipe_to_python(
    name=(args.file_out or args.json).rsplit('/', 1)[-1].split('.')[0], # take filename without extension of destination or source
    description=recipe['script'].get('description'),
    instructions=recipe['script'].get('instructions'),
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
    f.write(example)
    f.close()
  else:
    print(example)


if __name__ == '__main__':
  main()
