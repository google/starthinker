###########################################################################
#
#  Copyright 2021 Google LLC
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

"""Handler that executes { "sa":{...}} task in recipe JSON.

Connects the Google Search Ads Reporting API to recipe JSON.  This task
is required because the reporting response needs additional processing.
"""

from starthinker.util.data import put_rows
from starthinker.util.sa import SA_Report


def sa(config, task):
  if config.verbose:
    print('SA')

  report = SA_Report(config, task['auth'])
  report.request(task['body'])
  rows = report.get_rows()

  if 'bigquery' in task.get('out', {}):
    task['out']['bigquery']['schema'] = report.get_schema()
    task['out']['bigquery']['format'] = 'CSV'

  return put_rows(
    config,
    task['auth'],
    task['out'],
    rows
  )
