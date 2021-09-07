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


def validate(recipe, parameters_in, no_input):

  if parameters_in:
    # use passed in parameters
    with open(parameters_in, 'r') as f:
      parameters = json.load(f)
      json_set_fields(recipe, parameters)

  else:
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

        # return modified parameters
        return parameters

  # assert: parameters have not been modified
  return None

def main():

  # load standard parameters
  parser = commandline_parser()

  parser.add_argument(
    '--recipe_out',
    '-ro',
    help='Path to recipe file to be written if replacing fields.',
    default=None
  )

  parser.add_argument(
    '--includes',
    '-i',
    help='Path to recipes defined in include blocks.',
    default=None
  )

  # only allow reading or writing parameters (both reading and writing is too confusing for now)
  parser_parameters = parser.add_mutually_exclusive_group()

  parser_parameters.add_argument(
    '--parameters_in',
    '-pi',
    help='Path to parameter json file to be read.',
    default=None
  )

  parser_parameters.add_argument(
    '--parameters_out',
    '-po',
    help='Path to parameter json file to write if not.',
    default=None
  )

  args = parser.parse_args()

  # load json to get each task
  recipe = get_recipe(args.json, args.includes)

  # check if all fields have been converted to values (modifies recipe in place)
  parameters = validate(recipe, args.parameters_in, args.no_input)

  # check to write parameters to file (add recipe path to parameters for usability)
  if args.parameters_out:
    parameters['__recipe__'] = args.json
    print()
    print('Writing to:', args.parameters_out)
    f = open(args.parameters_out, 'w')
    f.write(json.dumps(parameters, sort_keys=True, indent=2))
    f.close()

  # check to write filled in recipe to file
  if args.recipe_out:
    print()
    print('Writing to:', args.recipe_out)
    f = open(args.recipe_out, 'w')
    f.write(json.dumps(recipe, sort_keys=True, indent=2))
    f.close()

  # if executing, initialize configuration and execute recipe
  if not args.parameters_out and not args.recipe_out:
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

    execute(configuration, recipe['tasks'], args.force, args.task)


if __name__ == '__main__':
  main()
