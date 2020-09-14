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
import re

from starthinker.util.project import project
from starthinker.util.sheets import sheets_read, sheets_tab_copy
from starthinker.util.bigquery import get_schema, query_to_view
from starthinker.util.csv import rows_to_type, rows_to_csv

TEMPLATE_SHEET = 'https://docs.google.com/spreadsheets/d/1_faknNlaPlltLwsleMyQH0Gis5ixJODLGJHLovY3Ycg/edit?usp=sharing'
TEMPLATE_TAB = 'Mapping'
RE_SQLINJECT = re.compile(r'[^a-z0-9_\-, ]+', re.UNICODE | re.IGNORECASE)


@project.from_parameters
def mapping():
  if project.verbose:
    print('MAPPING')

  # create the sheet from template if it does not exist
  sheets_tab_copy(project.task['auth'], TEMPLATE_SHEET, TEMPLATE_TAB,
                  project.task['sheet'], project.task['tab'])

  # move if specified
  dimensions = {}
  defaults = {}
  rows = sheets_read(project.task['auth'], project.task['sheet'],
                     project.task['tab'], 'A1:D')

  # if rows don't exist, query is still created without mapping ( allows blank maps )
  if rows:
    # sanitize mapping
    # 0 = Dimension, 1 = Tag, 2 = Column, 3 = Keyword
    for row in rows[1:]:
      if project.verbose:
        print('ROW: ', row)
      # sanitize row
      #row = map(lambda c: RE_SQLINJECT.sub('', c.strip()), row)
      row = [RE_SQLINJECT.sub('', r.strip()) for r in row]
      if len(row) == 2:  # default
        defaults.setdefault(row[0], row[1])
      else:  # tag
        dimensions.setdefault(row[0], {})  # dimension
        dimensions[row[0]].setdefault(row[1], {})
        dimensions[row[0]].setdefault(row[1], {})  # tag
        dimensions[row[0]][row[1]].setdefault(row[2], [])  # column
        dimensions[row[0]][row[1]][row[2]].extend(
            [k.strip() for k in row[3].split(',') if k])  # keywords

  # construct query
  query = 'SELECT\n  *,\n'
  for dimension, tags in dimensions.items():
    query += '  CASE\n'
    for tag, columns in tags.items():
      query += '    WHEN '
      for column, keywords in columns.items():
        for count, keyword in enumerate(keywords):
          if count != 0:
            query += 'OR '
          query += '%s CONTAINS "%s" ' % (column, keyword)
      query += 'THEN "%s"\n' % tag
    query += '    ELSE "%s"\n  END AS %s,\n' % (defaults.get(dimension,
                                                             ''), dimension)
  query += 'FROM [%s.%s]' % (project.task['in']['dataset'],
                             project.task['in']['table'])

  if project.verbose:
    print('QUERY: ', query)

  # write to view
  query_to_view(
      project.task['out']['auth'],
      project.id,
      project.task['out']['dataset'],
      project.task['out']['view'],
      query,
      replace=True)


if __name__ == '__main__':
  mapping()
