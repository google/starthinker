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
import os

from starthinker.util.project import project
from starthinker.util.bigquery import query_to_table, query_to_rows, rows_to_table, table_create
from starthinker.util.csv import rows_to_type
from starthinker.util.sheets import sheets_read, sheets_clear, sheets_write
from starthinker.task.itp_audit.queries import Queries

# Output Tables
BROWSER_PERFORMANCE_2YEARS_TABLE = 'DV3_Browser'
SAFARI_DISTRIBUTION_90DAYS_TABLE = 'DV3_Safari'
DV360_BROWSER_SHARES_MULTICHART_TABLE = 'DV3_MultiChart'
CM_BROWSER_REPORT_CLEAN_TABLE = 'CM_Browser'
CM_FLOODLIGHT_MULTICHART_TABLE = 'CM_Floodlight_Multichart'

# Tables
CLEAN_BROWSER_REPORT_TABLE = 'z_DV360_Browser_Report_Clean'
DV360_CUSTOM_SEGMENTS_TABLE = 'z_Custom_Segments'
DV360_CUSTOM_SEGMENTS_SHEET_TABLE = 'z_Custom_Segments_Sheet'
CM_SITE_SEGMENTATION_SHEET_TABLE = 'z_CM_Site_Segmentation_Sheet'
CM_SITE_SEGMENTATION_TABLE = 'z_CM_Site_Segmentation'
CM_BROWSER_REPORT_DIRTY_TABLE = 'z_CM_Browser_Report_Dirty'
CM_FLOODLIGHT_TABLE = 'z_CM_Floodlight'


@project.from_parameters
def itp_audit():
  if project.verbose:
    print('ITP Audit Run Queries')

  # Run DV360 related queries
  run_dv_360_queries(project)

  # Create CM Site Segmentation Table and Sheet
  create_cm_site_segmentation(project)

  # CM Segmentation Query
  if project.verbose:
    print('RUN CM Segmentation Query')
  run_query_from_file(Queries.cm_segmentation, CM_BROWSER_REPORT_CLEAN_TABLE)

  run_cm_queries(project)


def run_cm_queries(project):
  # CM Floodlight Lookup Table
  run_query_from_file(Queries.cm_floodlight_join, CM_FLOODLIGHT_TABLE)

  # Floodlight Multichart
  if project.verbose:
    print('RUN CM Floodlight Multichart')
  run_query_from_file(Queries.cm_floodlight_multichart, CM_FLOODLIGHT_MULTICHART_TABLE)


def run_dv_360_queries(project):
  # Create empty DV360 Custom Segments table for join until sheet is created
  table_create('service', project.id, project.task['dataset'],
               DV360_CUSTOM_SEGMENTS_TABLE)

  # Create DV360 Segments Table
  create_dv360_segments(project)

  # Clean DV360 Browser Report
  run_query_from_file(Queries.clean_browser_report, CLEAN_BROWSER_REPORT_TABLE)

  # Browser Performance 2 years
  if project.verbose:
    print('RUN Browser Performance 2 years Query')
  run_query_from_file(Queries.browser_2_year, BROWSER_PERFORMANCE_2YEARS_TABLE)

  #Safari Distribution 90 days
  if project.verbose:
    print('RUN Safari Distribution 90 days Query')
  run_query_from_file(Queries.safari_distribution_90days, SAFARI_DISTRIBUTION_90DAYS_TABLE)

  # Browser Shares Multichart
  if project.verbose:
    print('RUN Dv360 Browser Share Multichart')
  run_query_from_file(Queries.browser_share_multichart, DV360_BROWSER_SHARES_MULTICHART_TABLE)


def create_dv360_segments(project):
  a1_notation = 'A:M'
  schema = [{
      'type': 'STRING',
      'name': 'Advertiser',
      'mode': 'NULLABLE'
  }, {
      'type': 'INTEGER',
      'name': 'Advertiser_Id',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Campaign',
      'mode': 'NULLABLE'
  }, {
      'type': 'INTEGER',
      'name': 'Campaign_Id',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Insertion_Order',
      'mode': 'NULLABLE'
  }, {
      'type': 'INTEGER',
      'name': 'Insertion_Order_Id',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Line_Item',
      'mode': 'NULLABLE'
  }, {
      'type': 'INTEGER',
      'name': 'Line_Item_Id',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Line_Item_Type',
      'mode': 'NULLABLE'
  }, {
      'type': 'INTEGER',
      'name': 'Impressions',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Segment1',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Segment2',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Segment3',
      'mode': 'NULLABLE'
  }]

  sheet_rows = sheets_read(
      'user', project.task['sheet'], 'DV3 Segments', a1_notation, retries=10)

  if not sheet_rows:
    sheet_rows = []

  print('DV360 SEGMENT SHEET TABLE WRITE')

  rows_to_table(
      auth='service',
      project_id=project.id,
      dataset_id=project.task['dataset'],
      table_id=DV360_CUSTOM_SEGMENTS_SHEET_TABLE,
      rows=sheet_rows,
      schema=schema,
      skip_rows=1,
      disposition='WRITE_TRUNCATE')

  # Run Query
  if project.verbose:
    print('RUN DV360 Custom Segments Query')
  run_query_from_file(Queries.dv360_custom_segments, DV360_CUSTOM_SEGMENTS_TABLE)

  # Move Table back to sheets
  query = 'SELECT * from `' + project.id + '.' + project.task[
      'dataset'] + '.' + DV360_CUSTOM_SEGMENTS_TABLE + '`'
  rows = query_to_rows(
      'service', project.id, project.task['dataset'], query, legacy=False)

  # makes sure types are correct in sheet
  a1_notation = a1_notation[:1] + '2' + a1_notation[1:]
  rows = rows_to_type(rows)
  sheets_clear('user', project.task['sheet'], 'DV3 Segments', a1_notation)
  sheets_write('user', project.task['sheet'], 'DV3 Segments', a1_notation, rows)


"""This method will update the BQ table and update the Google sheet
"""


def create_cm_site_segmentation(project):
  # Read sheet to bq table
  sheet_rows = sheets_read(
      'user', project.task['sheet'], 'CM_Site_Segments', 'A:C', retries=10)
  if not sheet_rows:
    sheet_rows = []

  schema = [{
      'type': 'STRING',
      'name': 'Site_Dcm',
      'mode': 'NULLABLE'
  }, {
      'type': 'INTEGER',
      'name': 'Impressions',
      'mode': 'NULLABLE'
  }, {
      'type': 'STRING',
      'name': 'Site_Type',
      'mode': 'NULLABLE'
  }]

  rows_to_table(
      auth='service',
      project_id=project.id,
      dataset_id=project.task['dataset'],
      table_id=CM_SITE_SEGMENTATION_SHEET_TABLE,
      rows=sheet_rows,
      schema=schema,
      skip_rows=1,
      disposition='WRITE_TRUNCATE')

  # Get Site_Type from the sheet
  run_query_from_file(Queries.cm_site_segmentation, CM_SITE_SEGMENTATION_TABLE)

  # Move Table back to sheets
  query = 'SELECT * from `' + project.id + '.' + project.task[
      'dataset'] + '.' + CM_SITE_SEGMENTATION_TABLE + '`'
  rows = query_to_rows(
      'service', project.id, project.task['dataset'], query, legacy=False)

  # makes sure types are correct in sheet
  rows = rows_to_type(rows)
  sheets_clear('user', project.task['sheet'], 'CM_Site_Segments', 'A2:C')
  sheets_write('user', project.task['sheet'], 'CM_Site_Segments', 'A2:C', rows)


def run_query_from_file(query, table_name):
  query_to_table(
    'service',
    project.id,
    project.task['dataset'],
    table_name,
    query.format(**project.task),
    legacy=False
  )


if __name__ == '__main__':
  itp_audit()
