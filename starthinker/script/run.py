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
"""Command line to convert script with fields into a recipe with specific values.

Scripts are JSON templates that define a workflow.  Files in the format
script_*.json.
Each script can be converted to a recipe by replacing { field:{...}} elements
with
actual vaues.

This program reads {{ field:{...}} values from the script JSON, translates them
into
command line arguments, and uses those arguments to fill in the JSON {{
field:{...}} values
and produce a specific recipe as STDOUT.  Which can be piped to a file.

Example:

  `python starthinker/script/run.py scripts/script_dcm_to_bigquery.json`

  Will produce the following because it expects the arguments in the json
  script.

  ```
  usage: run.py [-h] json account report_id report_name dataset table
  run.py: error: too few arguments
  ```

  To see a detailed list of arguments run with the -h option:

  ```
  python starthinker/script/run.py scripts/script_dcm_to_bigquery.json -h
  usage: run.py [-h] json account report_id report_name dataset table

  positional arguments:
    json         JSON input recipe template file to onfigure.
    account      DCM network id.
    report_id    DCM report id from the UI.
    report_name  DCM report name, pass '' if using id instead.
    dataset      Dataset to be written to in BigQuery.
    table        Table to be written to in BigQuery.

  optional arguments:
    -h, --help   show this help message and exit
    --output JSON file to write resulting recipe.
  ```

  Then to turn the script into a recipe run:

  `python starthinker/script/run.py scripts/script_dcm_to_bigquery.json 7880
  1234567 "" "Test_Dataset" "Test_Table" > test_recipe.json`

  To perform the work of the script for the now filled in recipe:

  `python starthinker/all/run.py test_recipe.json`

"""

import sys
import json
import argparse

from starthinker.util.project import get_project
from starthinker.script.parse import json_get_fields, json_set_fields, json_set_instructions, json_set_description


def parser_add_field(parser, field):
  """Translates JOSN field specification into a command line argument.

    Args:
      parser: (ArgumentParser) An existing initalized argument parser to add
        fields to.
      field: (dict) A filed structured as: { "name":"???", "kind":"???",
        "default":???, "description":"???" }}

    Returns:
      Nothing.  Modifies parser in place.

    Raises:
      NotImplementedError: If field cannot be found.

  """

  if field['kind'] == 'string':
    parser.add_argument(
        '--' + field['name'],
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  elif field['kind'] == 'email':
    parser.add_argument(
        '--' + field['name'],
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  elif field['kind'] == 'authentication':
    parser.add_argument(
        '--' + field['name'],
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''),
        choices=['user', 'service'])
  elif field['kind'] == 'integer':
    parser.add_argument(
        '--' + field['name'],
        type=int,
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  elif field['kind'] == 'boolean':
    parser.add_argument(
        '--' + field['name'],
        help=field.get('description', 'No instructions.'),
        action='store_%s' % str(field.get('default', 'false')).lower())
  elif field['kind'] == 'text':
    parser.add_argument(
        '--' + field['name'],
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  elif field['kind'] == 'choice':
    parser.add_argument(
        '--' + field['name'],
        nargs='?',
        choices=field['choices'],
        help=field.get('description', 'No instructions'),
        default=field.get('default', ''))
  elif field['kind'] == 'timezone':
    parser.add_argument(
        '--' + field['name'],
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  elif field['kind'] == 'json':
    raise NotImplementedError('JSON is not a suported field type')
  elif field['kind'] == 'integer_list':
    parser.add_argument(
        '--' + field['name'],
        type=int,
        nargs='+',
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  elif field['kind'] == 'string_list':
    parser.add_argument(
        '--' + field['name'],
        nargs='+',
        help=field.get('description', 'No instructions.'),
        default=field.get('default', ''))
  else:
    raise NotImplementedError('%s is not a suported field type' % field)


def script_write(script, args, filepath=None):
  # insert fields into json
  json_set_fields(script, args)

  # insert variables into instructions
  json_set_instructions(script, args)

  # insert variables into description
  json_set_description(script, args)

  # produce output or run task
  if filepath:
    with open(filepath, 'w') as data_file:
      data_file.write(json.dumps(script, indent=2))
      print('JSON Written To: ', filepath)
  else:
    print(json.dumps(script, indent=2))


def script_interactive():
  args = {}

  from_json = sys.argv[1]
  to_json = sys.argv[2] if len(sys.argv) == 3 else ''

  script = get_project(sys.argv[1])

  # parse fields and constants into parameters
  fields = json_get_fields(script)

  print('-' * 60)
  if to_json:
    print('(1 of %d) From %s template create recipe: %s\n' %
          (len(fields), from_json, to_json))
  else:
    print('(1 of %d) Recipe file to create from %s template.\n' %
          (len(fields), sys.argv[1]))
    to_json = input('Full Path TO JSON File:')

  for count, field in enumerate(fields):
    print('')
    print('-' * 60)
    print('(%d of %d) %s%s%s' % (
        count + 2,
        len(fields),
        field['description'],
        ','.join(field['choices']) if 'choices' in field else '',
        (' Default to "%s" if blank.' %
         field['default']) if 'default' in field else '',
    ))
    args[field['name']] = input('%s ( %s ): ' % (field['name'], field['kind']))

    # remove blanks ( they should have defaults )
    if not args[field['name']]:
      del args[field['name']]

  script_write(script, args, to_json)


def script_commandline():

  script = get_project(sys.argv[1])

  # assemble parameters
  parser = argparse.ArgumentParser()
  parser.add_argument(
      'json', help='JSON recipe template to configure.', default=None)

  # parse fields and constants into parameters
  for field in json_get_fields(script):
    parser_add_field(parser, field)

  # run new arg parser with parameters from script
  args = vars(parser.parse_args())

  # always write to STDOUT, caller should rediect output to a JSON file
  script_write(script, args)


def main():
  # invalid command line
  if len(sys.argv) < 2:
    print('USAGE: run.py [json recipe template file path] [-h]')

  # only script, json and optional destination supplied, assume interactive
  elif len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2] != '-h'):
    script_interactive()

  # parameters supplied, assume command line
  else:
    script_commandline()


if __name__ == '__main__':
  main()
