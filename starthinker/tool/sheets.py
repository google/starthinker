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

from starthinker.util.csv import excel_to_sheets
from starthinker.util.csv import excel_to_rows
from starthinker.util.csv import rows_to_csv
from starthinker.util.configuration import commandline_parser, Configuration


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
    Command line to transform excel sheets into csv files.

    Prints to STDOUT, user is expected to pipe output into file.
    Typically used for BigQuery data imports.

    Examples:
      List sheets in workbook: python helper.py [EXCEL FILE] --list
      Convert excel to CSV: python helper.py [EXCEL FILE] --sheet [SHEET NAME] > results.csv

  """))

  parser.add_argument('workbook', help='name of file to pull the rows.')
  parser.add_argument('--sheet', help='Sheet to pull the rows.', default=None)
  parser.add_argument('--list', help='List reports.', action='store_true')

  # initialize project
  parser = commandline_parser(parser, arguments=('-v'))
  args = parser.parse_args()
  config = Configuration(
    verbose=args.verbose
  )

  with open(args.workbook, 'rb') as excel_file:
    if args.list:
      for sheet in excel_to_sheets(excel_file):
        print(sheet)
    elif args.sheet:
      for sheet, row in excel_to_rows(excel_file, args.sheet):
        print(rows_to_csv(row).read())


if __name__ == '__main__':
  main()
