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

"""Handler that executes { "ga":{...}} task in recipe JSON.

Connects the Google Analytics Reporting API to recipe JSON.  This task
is required because the reporting response needs additional processing.
"""

from starthinker.util.data import put_rows
from starthinker.util.ga import GA_Report


def ga(config, task):
  if config.verbose:
    print('GA')

  report = GA_Report(
    config,
    task['auth'],
    **task['kwargs']
  )

  # be sure to call before get_schema
  rows = report.get_rows()

  if 'bigquery' in task.get('out', {}):
    task['out']['bigquery']['schema'] = report.get_schema()
    task['out']['bigquery']['format'] = 'JSON'

  return put_rows(
    config,
    task['auth'],
    task['out'],
    rows
  )
