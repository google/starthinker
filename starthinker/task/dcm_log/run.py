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

from datetime import timedelta, datetime

from starthinker.util.google_api import API_DCM
from starthinker.util.bigquery import table_exists, rows_to_table, query_to_rows
from starthinker.util.cm import get_profile_for_api
from starthinker.util.data import get_rows

CHANGELOGS_TABLE = 'CM_Change_Logs'
CHANGELOGS_SCHEMA = [
    {
        'name': 'userProfileId',
        'type': 'INTEGER'
    },
    {
        'name': 'accountId',
        'type': 'INTEGER'
    },
    {
        'name': 'subaccountId',
        'type': 'INTEGER'
    },
    {
        'name': 'id',
        'type': 'INTEGER'
    },
    {
        'name': 'transactionId',
        'type': 'INTEGER'
    },
    {
        'name': 'objectType',
        'type': 'STRING'
    },
    {
        'name': 'objectId',
        'type': 'INTEGER'
    },
    {
        'name': 'action',
        'type': 'STRING'
    },
    {
        'name': 'fieldName',
        'type': 'STRING'
    },
    {
        'name': 'changeTime',
        'type': 'TIMESTAMP'
    },
    {
        'name': 'oldValue',
        'type': 'STRING'
    },
    {
        'name': 'newValue',
        'type': 'STRING'
    },
]


def get_changelogs(config, task, accounts, start):

  if config.verbose:
    print('CM CHANGE LOGS', accounts)

  for account_id in accounts:

    is_superuser, profile_id = get_profile_for_api(config, task['auth'],
                                                   account_id)
    kwargs = {'profileId': profile_id, 'minChangeTime': start}
    if is_superuser:
      kwargs['accountId'] = account_id

    for changelog in API_DCM(
        config, 'user', iterate=True,
        internal=is_superuser).changeLogs().list(**kwargs).execute():
      yield [
          changelog.get('userProfileId'),
          changelog['accountId'],
          changelog.get('subaccountId'),
          changelog['id'],
          changelog['transactionId'],
          changelog['objectType'],
          changelog['objectId'],
          changelog['action'],
          changelog.get('fieldName'),
          changelog['changeTime'],
          changelog.get('oldValue'),
          changelog.get('newValue'),
      ]


def dcm_log(config, task):
  if config.verbose:
    print('DCM LOG')

  accounts = list(get_rows(config, 'user', task['accounts']))

  # determine start log date
  if table_exists(config, task['out']['auth'], config.project,
                  task['out']['dataset'], CHANGELOGS_TABLE):
    start = next(
        query_to_rows(
            config, task['out']['auth'], config.project,
            task['out']['dataset'],
            'SELECT FORMAT_TIMESTAMP("%%Y-%%m-%%dT%%H:%%M:%%S-00:00", MAX(changeTime), "UTC") FROM `%s`'
            % CHANGELOGS_TABLE, 1, False))[0]
    disposition = 'WRITE_APPEND'

  else:
    start = (datetime.utcnow() - timedelta(days=int(task['days']))
            ).strftime('%Y-%m-%dT%H:%M:%S-00:00')
    disposition = 'WRITE_TRUNCATE'

  # load new logs
  rows = get_changelogs(config, task, accounts, start)
  if rows:
    rows_to_table(config, task['out']['auth'], config.project,
                  task['out']['dataset'], CHANGELOGS_TABLE, rows,
                  CHANGELOGS_SCHEMA, 0, disposition)
