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
import textwrap
import argparse

from starthinker.util.bigquery import get_schema
from starthinker.util.bigquery import rows_to_table
from starthinker.util.bigquery import table_to_schema
from starthinker.util.configuration import Configuration
from starthinker.util.configuration import commandline_parser
from starthinker.util.csv import csv_to_rows
from starthinker.util.csv import excel_to_rows
from starthinker.util.google_api import API_BigQuery
from starthinker.util.recipe import json_to_string


def task_template(table):
  """ Helper for translating a view into a StarThinker task.

  Removes project refrence and adds {dataset} parameters where possible.

  """

  task =  {
    "bigquery":{
      "auth":{"field":{ "name":"auth_bq", "kind":"authentication", "order":0, "default":"user", "description":"Credentials used for reading data." }},
      "from":{
        "query":table['view']['query'].replace(table['tableReference']['projectId'] + '.', '').replace(table['tableReference']['datasetId'] + '.', '{dataset}.'),
        "legacy":table['view']['useLegacySql'],
        "parameters":{
          "dataset":{"field":{ "name":"dataset", "kind":"string", "order":3, "description":"Place where tables will be written in BigQuery." }}
        }
      },
      "to":{
        "dataset":{"field":{ "name":"dataset", "kind":"string", "order":1, "default":"", "description":"Existing BigQuery dataset." }},
        "view":{"field":{ "name":"view", "kind":"string", "order":2, "default":"", "description":"View to create from this query." }}
      }
    }
  }
  return task


def main():
  # get parameters
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Command line to get table schema from BigQuery.

    Helps developers upload data to BigQuery and pull schemas.  These are the
    most common BigQuery tasks when developing solutions.

    Examples:
      Display table schema: `python bigquery.py --project [id] --dataset [name] --table [name] -s [credentials]`
      Create view task: `python bigquery.py --project [id] --dataset [name] --view [name] -s [credentials]`
      Upload csv table: `python bigquery.py --project [id] --dataset [name] --table [name] --csv [file] --schema [file] -s [credentials]`
      Upload excel sheet: `python bigquery.py --project [id] --dataset [name] --table [name] --excel_file [file] --excel_sheet [name] --schema [file] -s [credentials]`

  """))

  parser.add_argument(
    '--dataset',
    help='name of BigQuery dataset',
    default=None
  )
  parser.add_argument(
    '--table',
    help='name of BigQuery table',
    default=None
  )
  parser.add_argument(
    '--view',
    help='name of view to turn into StarThinker task',
    default=None
  )
  parser.add_argument(
    '--csv',
    help='CSV file path',
    default=None
  )
  parser.add_argument(
    '--schema',
    help='SCHEMA file path',
    default=None
  )
  parser.add_argument(
    '--excel_workbook',
    help='Excel file path',
    default=None
  )
  parser.add_argument(
    '--excel_sheet',
    help='Excel sheet name',
    default=None
  )

  # initialize project
  parser = commandline_parser(parser, arguments=('-u', '-c', '-s', '-v', '-p'))
  args = parser.parse_args()
  config = Configuration(
    user=args.user,
    client=args.client,
    service=args.service,
    verbose=args.verbose,
    project=args.project
  )

  auth = 'service' if args.service else 'user'

  schema = json.loads(args.schema) if args.schema else None

  if args.view:
    print(json_to_string(
      task_template(API_BigQuery(config, auth).tables().get(projectId=config.project, datasetId=args.dataset, tableId=args.view).execute()),
      skip=('field',)
    ).replace('\\n', '\n      ')
  )

  elif args.csv:

    with open(args.csv, 'r') as csv_file:
      rows = csv_to_rows(csv_file.read())

      if not schema:
        rows, schema = get_schema(rows)
        print('DETECETED SCHEMA', json.dumps(schema))
        print('Please run again with the above schema provided.')
        exit()

      rows_to_table(
        config,
        auth,
        config.project,
        args.dataset,
        args.table,
        rows,
        schema
      )

  elif args.excel_workbook and args.excel_sheet:
    with open(args.excel_workbook, 'r') as excel_file:
      rows = excel_to_rows(excel_file, args.excel_sheet)

      if not schema:
        rows, schema = get_schema(rows)
        print('DETECETED SCHEMA', json.dumps(schema))
        print('Please run again with the above schema provided.')
        exit()

      rows_to_table(
        config,
        auth,
        config.project,
        args.dataset,
        args.table,
        rows,
        schema
      )

  else:
    # print schema
    print(json.dumps(
      table_to_schema(
        config,
        auth,
        config.project,
        args.dataset,
        args.table
      ),
      indent=2
    ))

if __name__ == '__main__':
  main()
