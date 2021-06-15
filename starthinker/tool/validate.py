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

import argparse
import textwrap

from json import JSONDecodeError

from starthinker.util.recipe import get_recipe


def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Evaluate the validity of a json file. Helps in debugging recipes.
    Print the line and character position of any errors in the given json file.

    Also provide ability to replace values in a recipe with fields and values.

    Examples:
      - python json.py scripts/say_hello.json
      - python json.py scripts/dv360_targeting_audit.json -target 'DV_Targeting_Audit.' -value '{dataset}.'
      - python json.py scripts/dv360_targeting_audit.json -target '"service"' -field "auth_bigquery" -order 3 -description "BigQuery read/ write credentials." -default "service" -kind "authentication"
      - python json.py scripts/dv360_targeting_audit.json -target '"Some_Dataset"' -field "recipe_slug" -order 5 -description "name of dataset in BigQuery." -default "" -kind "string"
  """))

  parser.add_argument('file', help='A JSON file.')
  parser.add_argument('-target', help='The string value to replace.')

  parser.add_argument('-delete', action='store_false')

  parser.add_argument('-value', help='The value to insert.', default='')

  parser.add_argument('-field', help='The field name to insert.')
  parser.add_argument('-kind', help='The field kind to insert.', default='string')
  parser.add_argument('-prefix', help='The field prefix to insert.', default='')
  parser.add_argument('-default', help='The field default to insert.', default='')
  parser.add_argument('-description', help='The field description to insert.', default='')
  parser.add_argument('-order', help='The field order to insert.', type=int, default=1)
  parser.add_argument('-choices', help='The field choices to insert.', default='')

  args = parser.parse_args()

  try:
    get_recipe(args.file)
    print('JSON OK:', args.file)
  except JSONDecodeError as e:
    print('JSON ERROR:', str(e))
    exit

  if args.target:
    with open(args.file) as recipe_file:
      recipe = recipe_file.read()

    value = args.value

    if args.field:
      value = '{"field":{ "name":"%s", "kind":"%s", "order":%d, "default":"%s"' % (
        args.field,
        args.kind,
        args.order,
        args.default
      )
      if args.prefix:
        value += ', "prefix":"%s"' % args.prefix

      if args.choices:
        value += ', "choices":[%s]' % args.coices

      value += ', "description":"%s" }}' % args.description

    elif args.delete:
      value = ''

    print('REPLACE:', args.target)
    print('WITH:', value)

    recipe = recipe.replace(args.target, value)

    try:
      get_recipe(stringcontent=recipe)
      print('NEW JSON OK:', args.file)
    except JSONDecodeError as e:
      print('NEW JSON ERROR:', str(e))
      exit

    if str(input('Commit change (y/n): ')).lower().strip() == 'y':
      with open(args.file, "w") as f:
        f.write(recipe)


if __name__ == '__main__':
  main()
