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

from starthinker.util.configuration import Configuration
from starthinker.util.configuration import commandline_parser
from starthinker.util.configuration import execute
from starthinker.util.recipe import get_recipe
from starthinker.util.recipe import json_get_fields
from starthinker.util.recipe import json_set_fields


def prompt(fields):
  args = {}

  print()
  print('-' * 60)
  print('This recipe contains fields that have not been set.')
  print('To remove this prompt, replace all { field:{...}} entries with actual values.')
  print('To proceed with execution, user input is required...')
  print('-' * 60)

  for count, field in enumerate(fields):
    print()
    print('(%d of %d) %s%s%s' % (
      count + 1,
      len(fields),
      field.get('description', ''),
      ','.join(str(c) for c in field['choices']) if 'choices' in field else '',
      (' Default to "%s" if blank.' %
       field['default']) if 'default' in field else '',
    ))
    args[field['name']] = input('%s ( %s ): ' % (field['name'], field['kind']))

  # remove blanks ( they should have defaults )
  if not args[field['name']]:
    del args[field['name']]

  return args


def validate(recipe, no_input):
  # query for fields if they exist
  fields = json_get_fields(recipe)

  # parse fields and constants into parameters
  if fields:
    if no_input:
      raise NameError(
        'Edit the recipie and convert these fields into values:\n  - %s\n' % ' \n  - '.join('%s: %s' % (f['name'], f['description']) for f in fields)
      )
    else:
      parameters = prompt(fields)
      json_set_fields(recipe, parameters)


def main():

  # load standard parameters
  parser = commandline_parser()

  parser.add_argument(
    '--recipe_out',
    '-rc',
    help='Path to recipe file to be written if replacing fields.',
    default=None
  )

  args = parser.parse_args()

  # load json to get each task
  recipe = get_recipe(args.json)

  # check if all fields have been converted to values
  validate(recipe, args.no_input)

  # check to write converted fields to stdout
  if args.recipe_out:
    print()
    print('Writing to:', args.recipe_out)
    f = open(args.recipe_out, 'w')
    f.write(json.dumps(recipe, sort_keys=True, indent=2))
    f.close()
    exit()

  # initialize the project singleton with passed in parameters
  configuration = Configuration(
    recipe,
    args.project,
    args.user,
    args.service,
    args.client,
    args.json,
    args.key,
    args.verbose,
    args.trace_print,
    args.trace_file
  )

  execute(configuration, recipe['tasks'], args.force, args.instance)


if __name__ == '__main__':
  main()
