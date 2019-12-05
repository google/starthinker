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
import os

from starthinker.util.project import project
from starthinker.util.bigquery import query_to_table, query_to_rows, run_query, table_to_rows, get_schema, rows_to_table, table_create
from starthinker.util.csv import rows_to_type
from starthinker.util.data import get_rows, put_rows
from starthinker.util.dcm import report_delete, report_build, report_create, report_file, report_to_rows, report_clean, report_schema, report_run
from starthinker.util.sheets import sheets_read, sheets_clear, sheets_write
from starthinker.task.sdf.run import sdf

SQL_DIRECTORY = 'sql/'

# Queries
CLEAN_BROWSER_REPORT_FILENAME = 'clean_browser_report.sql'
BROWSER_ENV_90DAYS_FILENAME = 'browser_env_90days.sql'
BROWSER_PERFORMANCE_2YEARS_FILENAME = 'browser_performance_2years.sql'
SAFARI_DISTRIBUTION_90DAYS_FILENAME = 'safari_distribution_90days.sql'
DV360_BROWSER_SHARES_MULTICHART_FILENAME = 'browser_share_multichart.sql'
CM_SEGMENTATION_FILENAME ='CM_Segmentation.sql'
CM_SITE_SEGMENTATION_FILENAME = 'CM_Site_Segmentation.sql'
CM_FLOODLIGHT_JOIN_FILENAME = 'CM_Floodlight_Join.sql' 
CM_FLOODLIGHT_MULTICHART_FILENAME = 'CM_Floodlight_Multichart.sql' 
SDF_JOIN_FILENAME = 'sdf_join.sql'
DV360_CUSTOM_SEGMENTS_FILENAME = 'DV360_Custom_Segments.sql'

# Tables
CLEAN_BROWSER_REPORT_TABLE = 'Dv360_Browser_Report_Clean'
BROWSER_ENV_90DAYS_TABLE = 'Dv360_Browser_Environment_90_Days'
BROWSER_PERFORMANCE_2YEARS_TABLE = 'Dv360_Browser_Performance_2_Years'
SAFARI_DISTRIBUTION_90DAYS_TABLE = 'Dv360_Safari_Distribution_90_Days'
DV360_BROWSER_SHARES_MULTICHART_TABLE = 'Dv360_Browser_Shares_MultiChart'
DV360_CUSTOM_SEGMENTS_TABLE = 'Custom_Segments'
DV360_CUSTOM_SEGMENTS_SHEET_TABLE = 'Custom_Segments_Sheet'

CM_BROWSER_REPORT_CLEAN_TABLE = 'CM_Browser_Report_Clean'
CM_SITE_SEGMENTATION_SHEET_TABLE = 'CM_Site_Segmentation_Sheet'
CM_SITE_SEGMENTATION_TABLE = 'CM_Site_Segmentation'
CM_BROWSER_REPORT_DIRTY_TABLE = 'CM_Browser_Report'
CM_FLOODLIGHT_TABLE = 'CM_Floodlight'
CM_FLOODLIGHT_MULTICHART_TABLE = 'CM_Floodlight_Multichart'
SDF_JOIN_TABLE = 'SDF'

@project.from_parameters
def itp_audit():
  if project.verbose: print('ITP Audit Run Queries')
  # Run DV360 related queries
  run_dv_360_queries(project)

  # CM Browser Report, create and move to bigquery
  create_and_move_cm_browser_report(project)



  # Create CM Site Segmentation Table and Sheet
  create_cm_site_segmentation(project)

  # CM Segmentation Query
  if project.verbose: print('RUN CM Segmentation Query')
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + CM_SEGMENTATION_FILENAME), project.id, project.task['dataset'], CM_BROWSER_REPORT_CLEAN_TABLE)

  run_cm_queries(project)

  #TODO Terwilleger: SDF is part of phase two
  # Join SDF files
  #run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + SDF_JOIN_FILENAME), project.id, project.task['dataset'], SDF_JOIN_TABLE)


def run_cm_queries(project):
  # CM Floodlight Lookup Table
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + CM_FLOODLIGHT_JOIN_FILENAME), project.id, project.task['dataset'], CM_FLOODLIGHT_TABLE)

  # Floodlight Multichart
  if project.verbose: print('RUN CM Floodlight Multichart')
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + CM_FLOODLIGHT_MULTICHART_FILENAME), 
    project.id, project.task['dataset'], CM_FLOODLIGHT_MULTICHART_TABLE)


def run_dv_360_queries(project):
  # Create empty DV360 Custom Segments table for join until sheet is created
  table_create('service', project.id, project.task['dataset'], DV360_CUSTOM_SEGMENTS_TABLE)

  # Create DV360 Segments Table
  create_dv360_segments(project)

  # Clean DV360 Browser Report
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + CLEAN_BROWSER_REPORT_FILENAME), project.id, project.task['dataset'], CLEAN_BROWSER_REPORT_TABLE)
 
  # Browser Env 90 days
  if project.verbose: print('RUN Browser Env 90 Days Query')
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + BROWSER_ENV_90DAYS_FILENAME), 
    project.id, project.task['dataset'], BROWSER_ENV_90DAYS_TABLE)

  # Browser Performance 2 years
  if project.verbose: print('RUN Browser Performance 2 years Query')
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + BROWSER_PERFORMANCE_2YEARS_FILENAME), 
    project.id, project.task['dataset'], BROWSER_PERFORMANCE_2YEARS_TABLE)

  # Safari Distribution 90 days
  if project.verbose: print('RUN Safari Distribution 90 days Query')
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + SAFARI_DISTRIBUTION_90DAYS_FILENAME), 
    project.id, project.task['dataset'], SAFARI_DISTRIBUTION_90DAYS_TABLE)

  # Browser Shares Multichart
  if project.verbose: print('RUN Dv360 Browser Share Multichart')
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + DV360_BROWSER_SHARES_MULTICHART_FILENAME), 
    project.id, project.task['dataset'], DV360_BROWSER_SHARES_MULTICHART_TABLE)


def create_dv360_segments(project):
  a1_notation = 'A:M'
  schema = [
      { "type": "STRING", "name": "Advertiser", "mode": "NULLABLE" }, 
      { "type": "INTEGER", "name": "Advertiser_Id", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Campaign", "mode": "NULLABLE" }, 
      { "type": "INTEGER", "name": "Campaign_Id", "mode": "NULLABLE" },      
      { "type": "STRING", "name": "Insertion_Order", "mode": "NULLABLE" }, 
      { "type": "INTEGER", "name": "Insertion_Order_Id", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Line_Item", "mode": "NULLABLE" }, 
      { "type": "INTEGER", "name": "Line_Item_Id", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Line_Item_Type", "mode": "NULLABLE" },
      { "type": "INTEGER", "name": "Impressions", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Segment1", "mode": "NULLABLE" }, 
      { "type": "STRING", "name": "Segment2", "mode": "NULLABLE" },      
      { "type": "STRING", "name": "Segment3", "mode": "NULLABLE" }
    ]

  sheet_rows = sheets_read('user', project.task['sheet'], 'DV3 Segments', a1_notation, retries=10)

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
    disposition='WRITE_TRUNCATE'
    )

  # Run Query
  path = os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + DV360_CUSTOM_SEGMENTS_FILENAME)
  query = ''
  with open(path, 'r') as file:
    data = file.read().replace('\n', ' ')
    query = data.replace("{{project_id}}", project.id).replace("{{dataset}}", project.task['dataset'])

  print('DV360 CUSTOM SEGMENT TABLE')

  query_to_table(
    'service',
    project.id,
    project.task['dataset'],
    DV360_CUSTOM_SEGMENTS_TABLE,
    query,
    legacy=False
  )  

  # Move Table back to sheets
  query = 'SELECT * from `' + project.id + '.' + project.task['dataset'] + '.' + DV360_CUSTOM_SEGMENTS_TABLE + '`'
  rows = query_to_rows('service', project.id, project.task['dataset'], query, legacy=False)

  # makes sure types are correct in sheet
  a1_notation = a1_notation[:1] + '2' +a1_notation[1:]
  rows = rows_to_type(rows)
  sheets_clear('user', project.task['sheet'], 'DV3 Segments', a1_notation)
  sheets_write('user', project.task['sheet'], 'DV3 Segments', a1_notation, rows)


'''
This method will update the BQ table and update the Google sheet
'''
def create_cm_site_segmentation(project):
  # Read sheet to bq table
  sheet_rows = sheets_read('user', project.task['sheet'], 'CM_Site_Segments', 'A:C', retries=10)
  if not sheet_rows:
    sheet_rows = []

  schema = [
    { "type": "STRING", "name": "Site_Dcm", "mode": "NULLABLE" }, 
    { "type": "INTEGER", "name": "Impressions", "mode": "NULLABLE" }, 
    { "type": "STRING", "name": "Site_Type", "mode": "NULLABLE" }
  ]

  rows_to_table(
    auth='service',
    project_id=project.id,
    dataset_id=project.task['dataset'],
    table_id=CM_SITE_SEGMENTATION_SHEET_TABLE,
    rows=sheet_rows,
    schema=schema,
    skip_rows=1,
    disposition='WRITE_TRUNCATE'
  )

  # Get Site_Type from the sheet
  run_query_from_file(os.path.join(os.path.dirname(__file__), SQL_DIRECTORY + CM_SITE_SEGMENTATION_FILENAME), project.id, project.task['dataset'], CM_SITE_SEGMENTATION_TABLE)  

  # Move Table back to sheets
  query = 'SELECT * from `' + project.id + '.' + project.task['dataset'] + '.' + CM_SITE_SEGMENTATION_TABLE + '`'
  rows = query_to_rows('service', project.id, project.task['dataset'], query, legacy=False)

  # makes sure types are correct in sheet
  rows = rows_to_type(rows)
  sheets_clear('user', project.task['sheet'], 'CM_Site_Segments', 'A2:C')
  sheets_write('user', project.task['sheet'], 'CM_Site_Segments', 'A2:C', rows)


def run_query_from_file(path, project_id, dataset, table_name):
  query = ''
  with open(path, 'r') as file:
    data = file.read().replace('\n', ' ')
    query = data.replace("{{project_id}}", project_id).replace("{{dataset}}", dataset)

  query_to_table(
    'service',
    project_id,
    dataset,
    table_name,
    query,
    legacy=False
  )  


def create_and_move_cm_browser_report(project):
  browser_report_body = {
    "kind": "dfareporting#report",
    "name": project.task['cm_browser_report_name'],
    "fileName": project.task['cm_browser_report_name'],
    "format": "CSV",
    "type": "STANDARD",
    "criteria": {
      "dateRange": {
       "kind": "dfareporting#dateRange",
       "relativeDateRange": "LAST_24_MONTHS"
      },
      "dimensions": [
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:campaign"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:campaignId"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:site"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:advertiser"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:advertiserId"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:browserPlatform"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:platformType"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:month"
       },
       {
        "kind": "dfareporting#sortedDimension",
        "name": "dfa:week"
       }
      ],
      "metricNames": [
       "dfa:impressions",
       "dfa:clicks",
       "dfa:totalConversions",
       "dfa:activityViewThroughConversions",
       "dfa:activityClickThroughConversions"
      ],
      "dimensionFilters": []
    },
    "schedule": {
      "active": False,
      "repeats": "DAILY",
      "every": 1,
      "startDate": "2019-09-10",
      "expirationDate": "2029-12-09"
    },
    "delivery": {
      "emailOwner": False
  }}

  # Remove any duplicate entries from the advertiser ids
  advertiser_ids = project.task['advertiser_ids'].split(',')

  # Update body with all the advertiser filters
  for advertiser in advertiser_ids:
    if advertiser:
      browser_report_body["criteria"]["dimensionFilters"].append({
        "kind": "dfareporting#dimensionValue",
        "dimensionName": "dfa:advertiser",
        "id": advertiser,
        "matchType": "EXACT"
        })

  # Create report
  report = report_build(
    'user',
    project.task['account'],
    browser_report_body
  )

  # moving a report
  filename, report = report_file(
    'user',
    project.task['account'],
    None,
    project.task['cm_browser_report_name'],
    project.task.get('timeout', 60),
  )

  if report:
    if project.verbose: print('DCM FILE: ' + filename)

    # clean up the report
    rows = report_to_rows(report)
    rows = report_clean(rows)

    # if bigquery, remove header and determine schema
    schema = report_schema(rows.__next__())
    bigquery_out = {}
    bigquery_out["bigquery"] = {
      "dataset": project.task["dataset"], #todo update to reac from project
      "table": CM_BROWSER_REPORT_DIRTY_TABLE, 
      "is_incremental_load": False,
      "datastudio": True,
      "schema": schema,
      "skip_rows": 0
    }

    # write rows using standard out block in json ( allows customization across all scripts )
    if rows: put_rows(project.task['auth'], bigquery_out, rows)  



if __name__ == "__main__":
  itp_audit()
