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

import os
import json
from difflib import Differ
from time import sleep

from starthinker.util.project import project
from starthinker.util.bigquery import table_to_rows
from starthinker.util.bigquery import table_to_schema
from starthinker.util.bigquery import query_parameters
from starthinker.util.bigquery import query_to_rows
from starthinker.util.sheets import sheets_read
from starthinker.util.storage import object_exists, object_delete
from starthinker.util.drive import file_exists, file_delete
from starthinker.util.csv import rows_to_type
from starthinker.task.traffic.test import bulkdozer_test
from starthinker.task.weather_gov.test import weather_gov_test


EXIT_ERROR = 1
EXIT_SUCCESS = 0


def test_failed():
  print('FAILED')
  return EXIT_ERROR


def test_passed():
  print('PASSED')
  return EXIT_SUCCESS


def schema_compare(expected, actual, path=''):
  delta = {}
  matched = set()

  make_path = lambda name: path + ('.' if path else '') + name

  # find matches
  for expected_column in expected:
    for actual_column in actual:
      if expected_column['name'] == actual_column['name']:
        matched.add(expected_column['name'])
        if expected_column.get('type') != actual_column.get('type'):
          delta[make_path(expected_column['name'])] = { 'path': make_path(expected_column['name']), 'error': 'type', 'expected': expected_column.get('type'), 'actual': actual_column.get('type')}
        if expected_column.get('mode') != actual_column.get('mode'):
          delta[make_path(expected_column['name'])] = { 'path': make_path(expected_column['name']), 'error': 'mode', 'expected': expected_column.get('mode'), 'actual': actual_column.get('mode')}
        delta.update(schema_compare(expected_column.get('fields', []), actual_column.get('fields', []), make_path(expected_column['name'])))

  # find missing
  for expected_column in expected:
    if expected_column['name'] not in matched:
      delta[make_path(expected_column['name'])] = { 'path': make_path(expected_column['name']), 'error': 'missing', 'expected': expected_column['name'], 'actual': ''}

  # find extra
  for actual_column in actual:
    if actual_column['name'] not in matched:
      delta[make_path(actual_column['name'])] = { 'path': make_path(actual_column['name']), 'error': 'extra', 'expected': '', 'actual': actual_column['name']}

  return delta


def deep_compare(actual, expected):

  if type(actual) != type(expected):
    return 'EXPECTED %s BUT ACTUAL %s' % (type(expected), type(actual))

  elif isinstance(expected, (dict, tuple, list)):
    expected_str = json.dumps(expected, indent=2, sort_keys=True, default=str)
    actual_str = json.dumps(actual, indent=2, sort_keys=True, default=str)

    delta = list(Differ().compare(expected_str.splitlines(),
                                  actual_str.splitlines()))

    if sum(1 for d in delta if d[0] in ['-', '+', '?']):
      return ('%s\nEXPECTED '
              '*******************************************************\n%s\nACTUAL'
              ' *******************************************************\n%s') % (
          '\n'.join(delta), expected_str, actual_str)

  elif actual != expected:
    return 'EXPECTED %s != ACTUAL %s' % (expected, actual)

  return None


# display results of list comparison
def object_compare(actual, expected):
  errors = deep_compare(actual, expected)

  if errors:
    print('\nOBJECT DELTA *************************************************\n')
    print(errors)
    print('\n**************************************************************\n')
    test_failed()
  else:
    test_passed()


# check if sheet matches given values
#    { "test": {
#      "auth":"user",
#      "sheets": {
#        "sheet":"https://docs.google.com/spreadsheets/d/1h-Ic-DlCv-Ct8-k-VJnpo_BAkqsS70rNe0KKeXKJNx0/edit?usp=sharing",
#        "tab":"Sheet_Clear",
#        "range":"A1:C",
#        "values":[
#          ["Animal", "Age", "Weight ( lbs )"],
#          ["dog", 7, 67],
#          ["cat", 5, 1.5],
#          ["bird", 12, 0.44],
#          ["lizard", 22, 1],
#          ["dinosaur", 1600, 273.97]
#        ]
#      }
#    }}


def sheets():
  print('TEST: sheets')

  rows = sheets_read(project.task['auth'], project.task['sheets']['sheet'],
                     project.task['sheets']['tab'],
                     project.task['sheets']['range'])

  rows = rows_to_type(rows)
  object_compare(list(rows), project.task['sheets']['values'])


# check if bigquery table has given values or has data
#    { "test": {
#      "auth":"user",
#      "bigquery":{
#        "dataset":"Test",
#        "table":"Sheet_To_BigQuery",
#        "schema":[
#          {"name": "Animal", "type": "STRING"},
#          {"name": "Age", "type": "INTEGER"},
#          {"name": "Weight_lbs", "type": "FLOAT"}
#        ],
#        "values":[
#          ["dog", 7, 67],
#          ["cat", 5, 1.5],
#          ["bird", 12, 0.44],
#          ["lizard", 22, 1],
#          ["dinosaur", 1600, 273.97]
#        ]
#      }
#    }}


def bigquery():
  print('TEST: bigquery')

  # check schema if given ( check independent of values )
  if 'schema' in project.task['bigquery']:
    schema = table_to_schema(project.task['auth'], project.id,
                             project.task['bigquery']['dataset'],
                             project.task['bigquery']['table'])
    deltas = schema_compare(project.task['bigquery']['schema'], schema, path='')

    if deltas:
      print('\nFAILED *******************************************************\n')
      for delta in deltas.values():
        print('%(path)s: %(error)s ( %(expected)s - %(actual)s)' % delta)
      print('\n**************************************************************\n')
      test_failed()
    else:
      test_passed()


  # if query given check it
  if 'query' in project.task['bigquery']:
    rows = query_to_rows(
        project.task['auth'],
        project.id,
        project.task['bigquery']['dataset'],
        query_parameters(project.task['bigquery']['query'],
                         project.task['bigquery'].get('parameters')),
    )

    object_compare(sorted(rows), sorted(project.task['bigquery']['values']))

  # simple table check ( unless query given )
  elif 'values' in project.task['bigquery']:
    rows = table_to_rows(project.task['auth'], project.id,
                         project.task['bigquery']['dataset'],
                         project.task['bigquery']['table'])

    object_compare(sorted(rows), sorted(project.task['bigquery']['values']))


def asserts():
  print('TEST: asserts')
  print(project.task['assert'])
  test_passed()


def path_exists():
  print('TEST: path_exists')
  if os.path.exists(project.task['path']):
    if project.task.get('delete', False):
      os.remove(project.task['path'])
    test_passed()
  else:
    test_failed()


def storage_exists():
  print('TEST: storage_exists')
  if object_exists(
      project.task['auth'], '%s:%s' %
      (project.task['storage']['bucket'], project.task['storage']['file'])):
    if project.task.get('delete', False):
      object_delete(
          project.task['auth'], '%s:%s' %
          (project.task['storage']['bucket'], project.task['storage']['file']))
    test_passed()
  else:
    test_failed()


def drive_exists():
  print('TEST: drive')
  if file_exists(project.task['auth'], project.task['drive']['file']):
    if project.task.get('delete', False):
      file_delete(project.task['auth'], project.task['drive']['file'])
    test_passed()
  else:
    test_failed()


def test_sleep():
  print('TEST: sleep ', project.task['sleep'])
  sleep(project.task['sleep'])


def weather_gov():
  print('TEST: weather_gov')
  try:
    weather_gov_test()
    test_passed()
  except Exception as e:
    print(str(e))
    test_failed()


def traffic():
  print('TEST: Bulkdozer')
  try:
    bulkdozer_test()
    test_passed()
  except Exception as e:
    print(str(e))
    test_failed()


# decide which test to run
@project.from_parameters
def test():
  if 'assert' in project.task:
    return asserts()
  elif 'path' in project.task:
    return path_exists()
  elif 'storage' in project.task:
    storage_exists()
  elif 'sheets' in project.task:
    return sheets()
  elif 'bigquery' in project.task:
    return bigquery()
  elif 'drive' in project.task:
    return drive_exists()
  elif 'sleep' in project.task:
    return test_sleep()
  elif 'template' in project.task:
    return template()
  elif 'traffic' in project.task:
    return traffic()
  elif 'weather_gov' in project.task:
    return weather_gov()


# test should be run like any other task
# one test per task ( otherwise it gets confusing )
# calling script already indicates which test is being run
# print only PASS or FAIL
if __name__ == '__main__':
  test()
