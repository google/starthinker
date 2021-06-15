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

from starthinker.util.data import put_rows
from starthinker.util.sheets import sheets_read
from starthinker.util.csv import pivot_column_to_row
from starthinker.util.bigquery import table_name_sanitize, query_to_table
from starthinker.util.cm import report_get, report_delete, report_filter, report_build, report_file, report_to_rows, report_clean, get_account_name, report_schema


def dcm_replicate_accounts(config, task):
  if config.verbose:
    print('DCM REPLICATE ACCOUNTS')

  accounts = {}

  # read inputs
  if 'sheet' in task['in']:
    rows = sheets_read(
        config,
        task['auth'],
        task['in']['sheet'],
        task['in']['tab'],
    )
    # rotate rows so account, advertiser tuple is returned
    return pivot_column_to_row([row[1:] for row in rows])


def dcm_replicate_template(config, task):
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
  #del report['etag']
  del report['lastModifiedTime']
  del report['ownerProfileId']

  #print(json.dumps(report, indent=2))
  return report


def dcm_replicate_create(config, task, account, advertisers, name, template):
  print('DCM REPLICATE CREATE', name)

  # check if report is to be deleted
  if task['report'].get('delete', False):
    report_delete(config, task['auth'], account, None, name)

  # add account and advertiser filters ( return new disctionary)
  body = report_filter(config, task['auth'], template, {
      'accountId': {
          'values': account
      },
      'dfa:advertiser': {
          'values': advertisers
      }
  })
  body['name'] = name

  #print('BODY', body)

  # create and run the report if it does not exist
  report = report_build(config, task['auth'], account, body)


def dcm_replicate_download(config, task, account, name):

  filename, report = report_file(config, task['auth'], account, None, name)

  if report:
    if config.verbose:
      print('DCM FILE', filename)

    # clean up the report
    rows = report_to_rows(report)
    rows = report_clean(rows)

    # if bigquery, remove header and determine schema
    schema = None
    if 'bigquery' in task['out']:
      task['out']['bigquery']['table'] = table_name_sanitize(name)
      task['out']['bigquery']['schema'] = report_schema(next(rows))
      task['out']['bigquery']['skip_rows'] = 0

    # write rows using standard out block in json ( allows customization across all scripts )
    if rows:
      put_rows(config, task['auth'], task['out'], rows)


def dcm_replicate(config, task):
  if config.verbose:
    print('DCM REPLICATE')

  template = dcm_replicate_template(config, task)
  rows = dcm_replicate_accounts(config, task)

  # create or update reports
  for row in rows:
    account = row[0]
    advertisers = row[1:]
    name = '%s - Account %s' % (template['name'], account)
    dcm_replicate_create(config, task, account, advertisers, name, template)

  # download reports
  for row in rows:
    account = row[0]
    name = '%s - Account %s' % (template['name'], account)
    dcm_replicate_download(config, task, account, name)

  # summary table ( combine all data into one table for fast load )
  query_to_table(
      config,
      task['auth'],
      config.project,
      task['out']['bigquery']['dataset'],
      table_name_sanitize('%s - All' % template['name']),
      "SELECT CAST(REPLACE(_TABLE_SUFFIX, '_', '') AS INT64) AS Account_Id, * FROM `%s.%s.%s*`"
      % (config.project, task['out']['bigquery']['dataset'],
         table_name_sanitize('%s - Account ' % template['name'])),
      disposition='WRITE_TRUNCATE',
      legacy=False)
