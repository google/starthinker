###########################################################################
#
#  Copyright 2017 Google Inc.
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

import pprint

from starthinker.util.project import project
from starthinker.util.bigquery import table_to_schema, table_to_rows, query_to_rows
from starthinker.util.sheets import sheets_read
from starthinker.util.csv import rows_to_type


# display results of list comparison
def object_compare(actual, expected):
  if actual == expected:
    print 'PASSED'
  else:
    print ''
    print 'FAILED *******************************************************'
    print 'ACTUAL'
    pprint.PrettyPrinter().pprint(actual)
    print 'EXPECTED'
    pprint.PrettyPrinter().pprint(expected)
    print '**************************************************************'
    print ''


# check if sheet matches given values
#    { "test": {
#      "auth":"user",
#      "sheets": {
#        "url":"https://docs.google.com/spreadsheets/d/1h-Ic-DlCv-Ct8-k-VJnpo_BAkqsS70rNe0KKeXKJNx0/edit?usp=sharing",
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

  rows = sheets_read(
    project.task['auth'], 
    project.task['sheets']['url'], 
    project.task['sheets']['tab'], 
    project.task['sheets']['range']
  )

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

  # check schema if given ( check independent of values )
  if 'schema' in project.task['bigquery']:
    schema = table_to_schema(
      project.task['auth'],
      project.id,
      project.task['bigquery']['dataset'],
      project.task['bigquery']['table']
    )
    object_compare(schema['fields'], project.task['bigquery']['schema'])

  # if query given check it
  if 'query' in project.task['bigquery']:
    rows = query_to_rows(
      project.task['auth'],
      project.id,
      project.task['bigquery']['dataset'],
      project.task['bigquery']['query']
    )

    object_compare(sorted(rows), sorted(project.task['bigquery']['values']))

  # simple table check ( unless query given )
  elif 'values' in project.task['bigquery']:
    rows = table_to_rows(
      project.task['auth'],
      project.id,
      project.task['bigquery']['dataset'],
      project.task['bigquery']['table']
    )

    object_compare(sorted(rows), sorted(project.task['bigquery']['values']))


# decide which test to run
@project.from_parameters
def test():
  if 'sheets' in project.task: sheets()
  elif 'bigquery' in project.task: bigquery()


# test should be run like any other task
# one test per task ( otherwise it gets confusing )
# calling script already indicates which test is being run
# print only PASS or FAIL 
if __name__ == "__main__":
  test()
