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

from starthinker.util.project import project
from starthinker.util.data import put_rows, get_rows
from starthinker.util.dbm import lineitem_read, lineitem_write
from starthinker.util.dbm.schema import LineItem_Read_Schema


@project.from_parameters
def lineitem():
  if project.verbose:
    print('LINEITEM')

  if 'read' in project.task:
    advertisers = []
    insertion_orders = []
    line_items = []

    if 'advertisers' in project.task['read']:
      advertisers = get_rows(project.task['auth'],
                             project.task['read']['advertisers'])

    elif 'insertion_orders' in project.task['read']:
      insertion_orders = get_rows(project.task['auth'],
                                  project.task['read']['insertion_orders'])

    elif 'line_items' in project.task['read']:
      line_items = list(
          get_rows(project.task['auth'], project.task['read']['line_items']))
      print('LI', line_items)

    rows = lineitem_read(project.task['auth'], advertisers, insertion_orders,
                         line_items)

    if rows:
      if 'bigquery' in project.task['read']['out']:
        project.task['read']['out']['bigquery']['schema'] = LineItem_Read_Schema
        project.task['read']['out']['bigquery']['skip_rows'] = 0

      put_rows(project.task['auth'], project.task['read']['out'], rows)

  elif 'write' in project.task:
    rows = get_rows(project.task['auth'], project.task['write'])
    lineitem_write(project.task['auth'], rows,
                   project.task['write'].get('dry_run', True))


if __name__ == '__main__':
  lineitem()
