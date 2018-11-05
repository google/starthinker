###########################################################################
# 
#  Copyright 2018 Google Inc.
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

Scripts are JSON templates that define a workflow.  Files in the format script_*.json.
Each script can be converted to a recipe by replacing { field:{...}} elements with
actual vaues.

This program reads {{ field:{...}} values from the script JSON, translates them into 
command line arguments, and uses those arguments to fill in the JSON {{ field:{...}} values
and produce a specific recipe as STDOUT.  Which can be piped to a file.

Example:

  `python script/run.py dcm/script_dcm_to_bigquery.json`

  Will produce the following because it expects the arguments in the json script.

  `
  usage: run.py [-h] json account report_id report_name dataset table
  run.py: error: too few arguments
  `

  To see a detailed list of arguments run with the -h option:

  `
  python script/run.py dcm/script_dcm_to_bigquery.json -h
  usage: run.py [-h] json account report_id report_name dataset table
  
  positional arguments:
    json         JSON recipe file to script.
    account      DCM network id.
    report_id    DCM report id from the UI.
    report_name  DCM report name, pass '' if using id instead.
    dataset      Dataset to be written to in BigQuery.
    table        Table to be written to in BigQuery.
  
  optional arguments:
    -h, --help   show this help message and exit
    --datastudio  Alter columns for datastudio, fixes nulls and date format.
  `

  Then to turn the script into a recipe run:

  `python script/run.py dcm/script_dcm_to_bigquery.json 7880 1234567 "" "Test_Dataset" "Test_Table" --datastudio > test_recipe.json`

  To perform the work of the script for the now filled in recipe:
 
  `python all/run.py test_recipe.json`

"""

import sys
import json
import argparse

from parse import json_get_fields, json_set_fields, json_set_instructions, json_set_description


def parser_add_field(parser, field):
  """Translates JOSN field specification into a command line argument.

    Args:
      parser: (ArgumentParser) An existing initalized argument parser to add fields to.
      field: (dict) A filed structured as: { "name":"???", "kind":"???", "default":???, "description":"???" }}

    Returns:
      Nothing.  Modifies parser in place.

    Raises:
      NotImplementedError: If field cannot be found.

  """

  if field['kind'] == 'string':
    parser.add_argument(field['name'], help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  elif field['kind'] == 'email':
    parser.add_argument(field['name'], help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  elif field['kind'] == 'integer':
    parser.add_argument(field['name'], type=int, help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  elif field['kind'] == 'boolean':
    parser.add_argument('--' + field['name'], help=field.get('description', 'No instructions.'), action='store_%s' % str(field.get('default', 'false')).lower())
  elif field['kind'] == 'text':
    parser.add_argument(field['name'], help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  elif field['kind'] == 'choice':
    parser.add_argument(field['name'], nargs='?', choices=field['choices'], help=field.get('description', 'No instructions'), default=field.get('default', ''))
  elif field['kind'] == 'timezone':
    parser.add_argument(field['name'], help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  elif field['kind'] == 'json':
    raise NotImplementedError("JSON is not a suported field type")
  elif field['kind'] == 'integer_list':
    parser.add_argument(field['name'], type=int, nargs='+', help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  elif field['kind'] == 'string_list':
    parser.add_argument(field['name'], nargs='+', help=field.get('description', 'No instructions.'), default=field.get('default', ''))
  else:
    raise NotImplementedError("%s is not a suported field type" % field)


if __name__ == "__main__":

  if len(sys.argv) == 0:
    print "usage: run.py json"

  # load json
  with open(sys.argv[1]) as data_file:
    data = data_file.read()
    data = data.replace('\n', ' ')
    script = json.loads(data)

  # assemble parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('json', help='JSON recipe file to script.', default=None)

  # parse fields and constants into parameters
  for field in json_get_fields(script):
    parser_add_field(parser, field)

  # run new arg parser with parameters from script
  args = vars(parser.parse_args())

  # insert fields into json
  json_set_fields(script, args)

  # insert variables into instructions
  json_set_instructions(script, args)

  # insert variables into description
  json_set_description(script, args)

  # produce output or run task 
  print json.dumps(script, indent=2)
