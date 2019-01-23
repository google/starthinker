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

"""Handler that executes { "dbm":{...}} task in recipe JSON.

This script translates JSON instructions into operations on DBM reporting.
It deletes, or creates, and/or downloads DBM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in setup.py.

"""


from starthinker.util.project import project
from starthinker.util.data import put_rows, get_rows
from starthinker.util.dbm import report_delete, report_create, report_build, report_file, report_to_rows, report_clean, DBM_CHUNKSIZE


def dbm():
  if project.verbose: print 'DBM'

  # legacy translations ( changed report title to name )
  if 'title' in project.task['report']:
    project.task['report']['name'] = project.task['report']['title']

  # check if report is to be deleted
  if project.task.get('delete', False):
    if project.verbose: print 'DBM DELETE',
    report_delete(
      project.task['auth'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None)
    )

  # check if report is to be created ( LEGACY, DO NOT USE, SEE body format below )
  # REASON: this call tried to pass all parts of the json as parameters, this does not scale
  #         the new body call simply passes the report json in, leaving flexibility in the JSON recipe
  if 'type' in project.task['report']:

    if project.verbose: print 'DBM CREATE',

    partners = get_rows(project.task['auth'], project.task['report']['partners']) if 'partners' in project.task['report'] else []
    advertisers = get_rows(project.task['auth'], project.task['report']['advertisers']) if 'advertisers' in project.task['report'] else []

    report_create(
      project.task['auth'],
      project.task['report']['name'],
      project.task['report']['type'],
      partners,
      advertisers,
      project.task['report'].get('filters'),
      project.task['report'].get('dimensions'),
      project.task['report'].get('metrics'),
      project.task['report'].get('data_range'),
      project.task['report'].get('timezone', 'America/Los Angeles'),
      project.id,
      project.task['report'].get('dataset_id', None)
    )

  # check if report is to be created
  if 'body' in project.task['report']:
    if project.verbose: print 'DBM BUILD', project.task['report']['body']['metadata']['title']

    # filters can be passed using special get_rows handler, allows reading values from sheets etc...
    if 'filters' in project.task['report']:
      for f, d in project.task['report']['filters'].items():
        for v in get_rows(project.task['auth'], d):
          project.task['report']['body']['params'].setdefault('filters', []).append({"type": f, "value": v})

    # create the report
    report = report_build(
      project.task['auth'],
      project.task['report']['body']
    )

  # moving a report
  if 'out' in project.task:

    filename, report = report_file(
      project.task['auth'],
      project.task['report'].get('report_id', None),
      project.task['report'].get('name', None),
      project.task['report'].get('timeout', 10),
      DBM_CHUNKSIZE
    )

    # if a report exists
    if report:
      if project.verbose: print 'DBM FILE', filename

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows, datastudio=project.task.get('datastudio', False), nulls=True)

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows: put_rows(project.task['auth'], project.task['out'], filename, rows)

if __name__ == "__main__":
  project.load('dbm')
  dbm()
