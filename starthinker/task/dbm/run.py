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
"""Handler that executes { "dbm":{...}} task in recipe JSON.

This script translates JSON instructions into operations on DBM reporting.
It deletes, or creates, and/or downloads DBM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in config.py.

"""

from starthinker.util.data import put_rows
from starthinker.util.dv import report_delete, report_filter, report_build, report_file, report_to_rows, report_clean


def dbm(config, task):
  if config.verbose:
    print('DBM')

  # name is redundant if title is given, allow skipping use of name for creating reports
  if 'body' in task['report'] and 'name' not in task['report']:
    task['report']['name'] = task['report']['body']['metadata'][
        'title']

  # check if report is to be deleted
  if task.get('delete', False):
    if config.verbose:
      print('DBM DELETE')
    report_delete(config, task['auth'],
                  task['report'].get('report_id', None),
                  task['report'].get('name', None))

  # check if report is to be created
  if 'body' in task['report']:
    if config.verbose:
      print('DBM BUILD', task['report']['body']['metadata']['title'])

    # ceck if filters given ( returns new body )
    if 'filters' in task['report']:
      task['report']['body'] = report_filter(
          config, task['auth'], task['report']['body'],
          task['report']['filters'])

    # create the report
    report = report_build(config, task['auth'], task['report']['body'])

  # moving a report
  if 'out' in task:

    filename, report = report_file(
        config, task['auth'], task['report'].get('report_id', None),
        task['report'].get('name', None),
        task['report'].get('timeout', 10))

    # if a report exists
    if report:
      if config.verbose:
        print('DBM FILE', filename)

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows)

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows:
        return put_rows(config, task['auth'], task['out'], rows)
