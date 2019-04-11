###########################################################################
#
#  Copyright 2018 Google Inc.
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

from starthinker.util.project import project 
from starthinker.util.data import get_rows, put_rows
from starthinker.util.dcm import report_delete, report_build, report_create, report_file, report_to_rows, report_clean, report_schema


@project.from_parameters
def dcm():
  if project.verbose: print 'DCM'

  # stores existing report json
  report = None

  # check if report is to be deleted
  if project.task.get('delete', False):
    if project.verbose: print 'DCM DELETE'
    report_delete(
      project.task['auth'],
      project.task['report']['account'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None)
    )

  # check if report is to be created - DEPRECATED
  if 'type' in project.task['report']:
    if project.verbose: print 'DCM CREATE'
    report = report_create(
      project.task['auth'],
      project.task['report']['account'],
      project.task['report']['name'],
      project.task['report']
    )

  # check if report is to be created
  if 'body' in project.task['report']:
    if project.verbose: print 'DCM BUILD', project.task['report']['body']['name']

    # filters can be passed using special get_rows handler, allows reading values from sheets etc...
    if 'filters' in project.task['report']:
      for f, d in project.task['report']['filters'].items():
        for v in get_rows(project.task['auth'], d):
          # accounts are specified in a unique part of the report json
          if f in 'accountId':
            project.task['report']['body']['accountId'] = v
          # activities are specified in a unique part of the report json
          elif f in 'dfa:activity':
            project.task['report']['body']['reachCriteria']['activities'].setdefault('filters', []).append({
              "kind":"dfareporting#dimensionValue",
              "dimensionName": f,
              "id": v
            })
          # all other filters go in the same place
          else:
            project.task['report']['body']['criteria'].setdefault('dimensionFilters', []).append({
              "kind":"dfareporting#dimensionValue",
              "dimensionName": f,
              "id": v,
              "matchType": "EXACT"
            })

    report = report_build(
      project.task['auth'],
      project.task['report']['body'].get('accountId') or project.task['report']['account'],
      project.task['report']['body']
    )

  # moving a report
  if 'out' in project.task:
    filename, report = report_file(
      project.task['auth'],
      project.task['report']['account'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None) or project.task['report'].get('body', {}).get('name', None),
      project.task['report'].get('timeout', 10),
    )

    if report:
      if project.verbose: print 'DCM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows,  project.task.get('datastudio', False))

      # if bigquery, remove header and determine schema
      schema = None
      if 'bigquery' in project.task['out']:
        schema = report_schema(rows.next()) 
        project.task['out']['bigquery']['schema'] = schema
        project.task['out']['bigquery']['skip_rows'] = 0

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows: put_rows(project.task['auth'], project.task['out'], filename, rows)

if __name__ == "__main__":
  dcm()
