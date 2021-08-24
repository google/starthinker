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
import argparse
import textwrap

from starthinker.util.cm import get_profile_for_api, report_to_rows, report_clean, report_file, report_schema
from starthinker.util.configuration import commandline_parser, Configuration
from starthinker.util.csv import rows_to_type, rows_print
from starthinker.util.google_api import API_DCM
from starthinker.util.recipe import json_to_string


def task_template(report):
  """Helper to create a StarThinker compatible task JSON from CM report."""

  task = {
    "dcm":{
      "auth":{"field":{ "name":"auth_cm", "kind":"authentication", "order":0, "default":"user", "description":"Credentials used for reading data." }},
      "report": {
        "name":{"field":{ "name":"report_name", "kind":"string", "order":3, "prefix":"CM Report ", "default":"", "description":"Name of report." }},
        "account":{"field":{ "name":"account", "kind":"integer", "order":1, "default":12345, "description":"Campaign Manager Account ID" }},
        "body":report
      },
      "out":{
        "bigquery":{
          "auth":{"field":{ "name":"auth_bq", "kind":"authentication", "order":0, "default":"service", "description":"Authorization used for writing data." }},
          "dataset":{"field":{ "name":"dataset", "kind":"string", "order":4, "default":"", "description":"Name of Google BigQuery dataset to create." }},
          "table":"CM360_Report",
          "header":True
        }
      }
    }
  }

  if 'dimensionFilters' in report['criteria']:
    task['dcm']['report']['filters'] = {}
    for df in report['criteria']['dimensionFilters']:
      task['dcm']['report']['filters'][df['dimensionName']] = {
        "values": {"field":{ "name":df['dimensionName'], "kind":"integer_list", "order":3, "default":[], "description":"Comma delimited list of ids." }}
      }

  del tasks['dcm']['report']['body']['criteria']['dimensionFilters']
  del tasks['dcm']['report']['body']['lastModifiedTime']
  del tasks['dcm']['report']['body']['ownerProfileId']
  del tasks['dcm']['report']['body']['accountId']
  del tasks['dcm']['report']['body']['fileName']
  del tasks['dcm']['report']['body']['name']
  del tasks['dcm']['report']['body']['etag']
  del tasks['dcm']['report']['body']['id']

  return tasks


def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
      Command line to help debug CM reports and build reporting tools.

      Examples:
        To get list of reports: python cm.py --account [id] --list -u [user credentials path]
        To get report: python cm.py --account [id] --report [id] -u [user credentials path]
        To get report files: python cm.py --account [id] --files [id] -u [user credentials path]
        To get report sample: python cm.py --account [id] --sample [id] -u [user credentials path]
        To get report schema: python cm.py --account [id] --schema [id] -u [user credentials path]

    """
  ))

  parser.add_argument('--account', help='Account ID to use to pull the report.', default=None)
  parser.add_argument('--report', help='Report ID to pull JSON definition.', default=None)
  parser.add_argument('--schema', help='Report ID to pull achema definition.', default=None)
  parser.add_argument('--sample', help='Report ID to pull sample data.', default=None)
  parser.add_argument('--files', help='Report ID to pull file list.', default=None)
  parser.add_argument('--list', help='List reports.', action='store_true')
  parser.add_argument('--task', help='Report ID to pull task definition.', default=None)

  # initialize project
  parser = commandline_parser(parser, arguments=('-u', '-c', '-s', '-v'))
  args = parser.parse_args()
  config = Configuration(
    user=args.user,
    client=args.client,
    service=args.service,
    verbose=args.verbose
  )

  auth = 'service' if args.service else 'user'

  is_superuser, profile = get_profile_for_api(config, auth, args.account)
  kwargs = {
      'profileId': profile,
      'accountId': args.account
  } if is_superuser else {
      'profileId': profile
  }

  # get report json
  if args.report:
    kwargs['reportId'] = args.report
    report = API_DCM(config, auth, internal=is_superuser).reports().get(**kwargs).execute()
    print(json.dumps(report, indent=2, sort_keys=True))

  # get task json
  elif args.task:
    kwargs['reportId'] = args.task
    report = API_DCM(config, auth, internal=is_superuser).reports().get(**kwargs).execute()
    print(json_to_string(task_template(report), skip=('field',)))

  # get report files
  elif args.files:
    kwargs['reportId'] = args.files
    for rf in API_DCM(config,  auth, internal=is_superuser, iterate=True).reports().files().list(**kwargs).execute():
      print(json.dumps(rf, indent=2, sort_keys=True))

  # get schema
  elif args.schema:
    filename, report = report_file(config, auth, args.account,
                                   args.schema, None, 10)
    rows = report_to_rows(report)
    rows = report_clean(rows)
    print(json.dumps(report_schema(next(rows)), indent=2, sort_keys=True))

  # get sample
  elif args.sample:
    filename, report = report_file(config, auth, args.account, args.sample, None, 10)
    rows = report_to_rows(report)
    rows = report_clean(rows)
    rows = rows_to_type(rows)
    for r in rows_print(rows, row_min=0, row_max=20):
      pass

  # get list
  else:
    for report in API_DCM( config, auth, internal=is_superuser, iterate=True).reports().list(**kwargs).execute():
      print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
  main()
