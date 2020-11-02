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

from starthinker.util.project import project
from starthinker.util.bigquery import get_schema
from starthinker.util.bigquery import rows_to_table
from starthinker.util.bigquery import table_to_schema
from starthinker.util.csv import csv_to_rows
from starthinker.util.csv import excel_to_rows


def main():
  # get parameters
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Command line to get table schema from BigQuery.

    Helps developers upload data to BigQuery and pull schemas.  These are the
    most common BigQuery tasks when developing solutions.

    Examples:
      Display table schema: `python helper.py --project [id] --dataset [name] --table [name] -s [credentials]`
      Upload csv table: `python helper.py --project [id] --dataset [name] --table [name] --csv [file] --schema [file] -s [credentials]`
      Upload excel sheet: `python helper.py --project [id] --dataset [name] --table [name] --excel_file [file] --excel_sheet [name] --schema [file] -s [credentials]`

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
  project.from_commandline(
    parser=parser,
    arguments=('-u', '-c', '-s', '-v', '-p')
  )

  auth = 'service' if project.args.service else 'user'

  schema = json.loads(project.args.schema) if project.args.schema else None

  if project.args.csv:

    with open(project.args.csv, 'r') as csv_file:
      rows = csv_to_rows(csv_file.read())

      if not schema:
        rows, schema = get_schema(rows)
        print('DETECETED SCHEMA', json.dumps(schema))
        print('Please run again with the above schema provided.')
        exit()

      rows_to_table(
        auth,
        project.id,
        project.args.dataset,
        project.args.table,
        rows,
        schema
      )

  elif project.args.excel_workbook and project.args.excel_sheet:
    with open(project.args.excel_workbook, 'r') as excel_file:
      rows = excel_to_rows(excel_file, project.args.excel_sheet)

      if not schema:
        rows, schema = get_schema(rows)
        print('DETECETED SCHEMA', json.dumps(schema))
        print('Please run again with the above schema provided.')
        exit()

      rows_to_table(
        auth,
        project.id,
        project.args.dataset,
        project.args.table,
        rows,
        schema
      )

  else:
    # print schema
    print(json.dumps(
      table_to_schema(
        auth,
        project.id,
        project.args.dataset,
        project.args.table
      ),
      indent=2
    ))

if __name__ == '__main__':
  main()
