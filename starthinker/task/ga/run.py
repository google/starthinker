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

from starthinker.util.project import project
from starthinker.util.data import put_rows
from starthinker.util.ga import GA_Report


@project.from_parameters
def ga():
  if project.verbose:
    print('GA')

  report = GA_Report(
    project.task['auth'],
    **project.task['kwargs']
  )

  # be sure to call before get_schema
  rows = report.get_rows()

  if 'bigquery' in project.task.get('out', {}):
    project.task['out']['bigquery']['schema'] = report.get_schema()
    project.task['out']['bigquery']['format'] = 'JSON'

  put_rows(
    project.task['auth'],
    project.task['out'],
    rows
  )


if __name__ == '__main__':
  ga()
