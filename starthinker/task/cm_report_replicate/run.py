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

from starthinker.util.data import put_rows, get_rows
from starthinker.util.csv import pivot_column_to_row
from starthinker.util.bigquery import table_name_sanitize, query_to_table
from starthinker.util.cm import report_get, report_delete, report_filter, report_build, report_file, report_to_rows, report_clean, report_schema

"""Copies a report from one CM360 account to others.

Use a single CM360 report as a template and replicate it for multiple accounts or advertisers.
  1. Provide the CM Template account and report.
  2. Provide a list of accounts and optionally advertisers to replicate for.

When run the reports are created in CM360 and downloaded to BigQuery. The soluton:
  1. Creates copies of the CM tempalte report for each account and runs them at least once.
  2. Checks if the report has run and downloads each report.
  3. An Account_ID column is added to each report to help distinguish accounts.
  4. The data is stored in a singlle BigQuery table for all accounts and advertisers specified.

Known limitations and processes:
  1. The solution will not update the copies if the template is updated unless delete is set to True.
  2. All report types are supported including whatever schedule is set in the template.
  3. The template report name or id can be used.
  4. Is Incremental Load requires a date partition in the report and will de-dupe dates.
  5. Edits to the reports in CM360 are possible, ensure schema across all copies is consistent.

Parameters:

  Entry point is cm_report_replicate(config, task).
  All {"field":{...}} entries are parameters used by the python function.

  config = see: starthinker/util/configuration.py

  task = { "cm_report_replicate":{
    "auth":{"field":{ "name":"auth_read", "kind":"authentication", "order":0, "default":"user", "description":"Credentials used for reading data." }},
    "report":{
      "account":{"field":{ "name":"account", "kind":"integer", "order":3, "default":"", "description":"CM network id." }},
      "id":{"field":{ "name":"report_id", "kind":"integer", "order":4, "default":"", "description":"CM template report id, for template" }},
      "name":{"field":{ "name":"report_name", "kind":"string", "order":5, "default":"", "description":"CM template report name, empty if using id instead." }},
      "delete":{"field":{ "name":"delete", "kind":"boolean", "order":6, "default":false, "description":"Use only to reset the reports if setup changes." }}
    },
    "in":{ SEE: starthinker/util/data.py - get_rows(...) },
    "out":{
      "bigquery":{
        "dataset":{"field":{ "name":"recipe_slug", "kind":"string", "order":4, "default":"" }},
        "is_incremental_load":{"field":{ "name":"Aggregate", "kind":"boolean", "order":7, "default":false, "description":"Append report data to existing table, requires Date column." }}
      }
    }
  }}

"""

def cm_report_replicate_template(config, task):
  if config.verbose:
    print('DCM REPLICATE TEMPLATE')

  report = report_get(
    config,
    task['auth'],
    task['report']['account'],
    task['report'].get('id'),
    task['report'].get('name'),
  )

  report['criteria']['dimensionFilters'] = []
  del report['id']
  del report['lastModifiedTime']
  del report['ownerProfileId']

  #print(json.dumps(report, indent=2))
  return report


def cm_report_replicate_create(config, task, account, advertisers, name, template):
  print('DCM REPLICATE CREATE', name)

  # check if report is to be deleted
  if task['report'].get('delete', False):
    report_delete(config, task['auth'], account, None, name)

  # add account and advertiser filters ( return new disctionary)
  body = report_filter(config, task['auth'], template, {
    'accountId': {'values': account},
    'advertiser': {'values': advertisers}
  })
  body['name'] = name

  #print('BODY', body)

  # create and run the report if it does not exist
  report = report_build(config, task['auth'], account, body)


def cm_report_replicate_download(config, task, account, name):

  filename, report = report_file(config, task['auth'], account, None, name)

  if report:
    if config.verbose:
      print('DCM FILE', filename)

    # clean up the report
    rows = report_to_rows(report)
    rows = report_clean(rows)

    # if bigquery, remove header and determine schema
    schema = None
    if 'bigquery' in task['write']:
      task['write']['bigquery']['table'] = table_name_sanitize(name)
      task['write']['bigquery']['schema'] = report_schema(next(rows))
      task['write']['bigquery']['skip_rows'] = 0

    # write rows using standard out block in json ( allows customization across all scripts )
    if rows:
      put_rows(config, task['auth'], task['write'], rows)


def cm_report_replicate(config, task):
  if config.verbose:
    print('DCM REPLICATE')

  template = cm_report_replicate_template(config, task)

  rows = list(get_rows(config, task['auth'], task['replicate']))
  if 'sheets' in task['replicate']: rows = pivot_column_to_row([row[1:] for row in rows])

  # create or update reports
  for row in rows:
    account = row[0]
    advertisers = row[1:]
    name = '%s - Account %s' % (template['name'], account)
    cm_report_replicate_create(config, task, account, advertisers, name, template)

  # if destination provided, otherwise just copy report
  if 'write' in task:
    # download reports
    for row in rows:
      account = row[0]
      name = '%s - Account %s' % (template['name'], account)
      cm_report_replicate_download(config, task, account, name)

    # summary table ( combine all data into one table for fast load )
    if rows:
      query_to_table(
        config,
        task['auth'],
        config.project,
        task['write']['bigquery']['dataset'],
        table_name_sanitize('%s - All' % template['name']),
        "SELECT CAST(REPLACE(_TABLE_SUFFIX, '_', '') AS INT64) AS Account_Id, * FROM `%s.%s.%s*`" % (
          config.project,
          task['write']['bigquery']['dataset'],
          table_name_sanitize('%s - Account ' % template['name'])
        ),
        disposition='WRITE_TRUNCATE',
        legacy=False
      )
