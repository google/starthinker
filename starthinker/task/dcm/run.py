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
"""Handler that executes { "dcm":{...}} task in recipe JSON.

This script translates JSON instructions into operations on DCM reporting.
It deletes, or creates, and/or downloads DCM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in config.py.
For superusers, this script will use the internal API, bypassing the
need for profiles.
Reports uploaded to BigQuery use automatic schema detection based on official
proto files.

"""

from starthinker.util.data import get_rows, put_rows
from starthinker.util.cm import report_delete, report_filter, report_build, report_file, report_to_rows, report_clean, report_schema, report_run


def dcm(config, task):
  if config.verbose:
    print('DCM')

  # report name can exist in 2 places
  report_name =  task['report'].get('name') or task['report'].get('body', {}).get('name')

  # check if report is to be deleted
  if task.get('delete', False):
    if config.verbose:
      print('DCM DELETE', report_name or task['report'].get('report_id'))

    report_delete(
      config,
      task['auth'],
      task['report']['account'],
      task['report'].get('report_id'),
      report_name
   )

  # check if report is to be run
  if task.get('report_run_only', False):
    if config.verbose:
      print('DCM REPORT RUN', report_name or  task['report'].get('report_id'))

    report_run(
      config,
      task['auth'],
      task['report']['account'],
      task['report'].get('report_id'),
      report_name
    )

  # check if report is to be created
  if 'body' in task['report']:
    if config.verbose:
      print('DCM BUILD', report_name)

    if 'filters' in task['report']:
      task['report']['body'] = report_filter(
        config,
        task['auth'], task['report']['body'],
        task['report']['filters']
      )

    # set name in case it was passed in report instead of body
    task['report']['body']['name'] = report_name
    report = report_build(
      config,
      task['auth'],
      task['report']['body'].get('accountId') or task['report']['account'],
      task['report']['body']
   )

  # moving a report
  if 'out' in task:
    filename, report = report_file(
      config,
      task['auth'],
      task['report']['account'],
      task['report'].get('report_id', None),
      report_name,
      task['report'].get('timeout', 10),
    )

    if report:
      if config.verbose:
        print('DCM FILE', filename)

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows)

      # if bigquery, remove header and determine schema
      schema = None
      if 'bigquery' in task['out']:
        schema = report_schema(next(rows))
        task['out']['bigquery']['schema'] = schema
        task['out']['bigquery']['skip_rows'] = 0

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows:
        return put_rows(config, task['auth'], task['out'], rows)
