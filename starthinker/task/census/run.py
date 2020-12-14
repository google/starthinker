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
from starthinker.util.bigquery import query_to_table, query_to_view
from starthinker.task.census.fields import CENSUS_FIELDS


def census_normalize(census_geography, census_year, census_span):

  query = 'SELECT\n'
  for segment in CENSUS_FIELDS:
    if segment['denominator'] is None:
      for column in segment['columns']:
        query += '  %s AS %s,\n' % (column, column.title())
    else:
      query += '\n  /* %s */\n' % segment['category']
      for column in segment['columns']:
        query += '  SAFE_DIVIDE(%s, %s) AS %s,\n' % (
            column, segment['denominator'], column.title())

  query += 'FROM `bigquery-public-data.census_bureau_acs.%s_%s_%s`;' % (
      census_geography, census_year, census_span)

  return query


def census_pivot(dataset, table):
  query = 'SELECT Geo_Id, [\n'

  for segment in CENSUS_FIELDS:
    if segment['category']:
      for column_a in segment['columns']:
        query += '    STRUCT(\n'
        query += '      "%s" AS Percentage,\n' % column_a.title()
        query += '      "%s" AS Dimension,\n' % segment['category']
        query += '      "%s" AS Segment\n' % column_a.title()
        query += '      ),\n'

  query = query[:-2] + '\n  ] AS Correlation\n'
  query += 'FROM `%s.%s`;' % (dataset, table)

  return query


def census_correlate(column_join, column_pass, column_sum, column_correlate,
                     dataset, table):

  query = 'SELECT\n'

  for column in column_pass:
    query += '  A.%s,\n' % column

  for column in column_sum:
    query += '  SUM(A.%s) AS %s,\n' % (column, column)

  query += '  COUNT(*) AS Locations,\n'

  for segment in CENSUS_FIELDS:
    if segment['category']:
      for column_a in segment['columns']:
        for column_b in column_correlate:
          query += '  CORR(A.%s, B.%s) AS %s_%s_Correlation,\n' % (
              column_b, column_a.title(), column_a.title(), column_b)

  query += 'FROM `%s.%s.%s` AS A\n' % (project.id, dataset, table)
  query += 'LEFT JOIN `%s.%s.Census_Normalized` AS B\n' % (project.id, dataset)
  query += 'ON A.%s=B.Geo_Id\n' % column_join
  query += 'GROUP BY %s' % ','.join(map(str, range(1, len(column_pass) + 1)))

  return query


def census_significance(column_join, column_pass, column_sum, column_correlate,
                        dataset, significance):

  query = 'SELECT\n'

  for column in column_pass:
    query += '  %s,\n' % column

  for column in column_sum:
    query += '  %s,\n' % column

  query += '  Locations,\n'

  for segment in CENSUS_FIELDS:
    if segment['category']:
      for column_a in segment['columns']:
        for column_b in column_correlate:
          query += ('%s.pearson_significance_test(%s_%s_Correlation, Locations,'
                    ' %s, 0.5) AS %s_%s_Correlation,\n') % (
              dataset,
              column_a.title(),
              column_b,
              significance,
              column_a.title(),
              column_b,
          )

  query += 'FROM `%s.%s.Census_Correlated`;' % (project.id, dataset)

  return query


def census_join(column_join, column_pass, column_sum, column_correlate,
                 dataset):

  query = 'SELECT\n'

  for column in column_pass:
    query += '  %s,\n' % column

  for column in column_sum:
    query += '  %s,\n' % column

  query += '  Locations,\n'

  query += '  [\n'

  for segment in CENSUS_FIELDS:
    if segment['category']:
      for column_a in segment['columns']:
        query += '    STRUCT(\n'
        for column_b in column_correlate:
          query += '      %s_%s_Correlation AS %s,\n' % (column_a.title(),
                                                         column_b, column_b)
        query += '      "%s" AS Dimension,\n' % segment['category']
        query += '      "%s" AS Segment\n' % column_a.title()
        query += '      ),\n'

  query = query[:-2] + '\n  ] AS Correlation\n'
  query += 'FROM `%s.%s.Census_Significant`;' % (project.id, dataset)

  return query


def census_write(query, table):

  if project.verbose:
    print('%s: %s' % (table, query))

  if project.task['to']['type'] == 'table':
    query_to_table(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        table,
        query,
        legacy=False)

  elif project.task['to']['type'] == 'view':
    query_to_view(
        project.task['auth'],
        project.id,
        project.task['to']['dataset'],
        table,
        query,
        legacy=False)


@project.from_parameters
def census():
  if 'normalize' in project.task:
    query = census_normalize(
        project.task['normalize']['census_geography'],
        project.task['normalize']['census_year'],
        project.task['normalize']['census_span'],
    )
    census_write(query, 'Census_Normalized')

  if project.task.get('pivot'):
    query = census_pivot(project.task['to']['dataset'], 'Census_Normalized')
    census_write(query, 'Census_Pivoted')

  if 'correlate' in project.task:
    query = census_correlate(
        project.task['correlate']['join'],
        project.task['correlate']['pass'],
        project.task['correlate']['sum'],
        project.task['correlate']['correlate'],
        project.task['correlate']['dataset'],
        project.task['correlate']['table'],
    )
    census_write(query, 'Census_Correlated')

    query = census_significance(
        project.task['correlate']['join'],
        project.task['correlate']['pass'],
        project.task['correlate']['sum'],
        project.task['correlate']['correlate'],
        project.task['correlate']['dataset'],
        project.task['correlate']['significance'],
    )
    census_write(query, 'Census_Significant')

    query = census_join(project.task['correlate']['join'],
                         project.task['correlate']['pass'],
                         project.task['correlate']['sum'],
                         project.task['correlate']['correlate'],
                         project.task['correlate']['dataset'])
    census_write(query, 'Census_Join')


#WITH data AS (
#  SELECT ST_GEOGPOINT(-122.4194, 37.7749) point
#  UNION ALL
#  SELECT ST_GEOGPOINT(-74.0060, 40.7128) point
#)
#SELECT zip_code, city, county
#FROM `bigquery-public-data.geo_us_boundaries.zip_codes`
#JOIN data
#ON ST_WITHIN(point, zip_code_geom)

if __name__ == '__main__':
  census()
