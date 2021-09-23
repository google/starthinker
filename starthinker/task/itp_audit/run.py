############################################################################
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
############################################################################
import os
from datetime import date

from starthinker.util.bigquery import datasets_create,query_to_table, query_to_rows, run_query, table_to_rows, get_schema, rows_to_table, table_create
from starthinker.util.csv import rows_to_type
from starthinker.util.data import get_rows, put_rows
from starthinker.util.cm import get_profile_for_api, report_delete, report_build, report_file, report_to_rows, report_clean, report_schema, report_run
from starthinker.util.sheets import sheets_read, sheets_clear, sheets_write
from starthinker.task.sdf.run import sdf
from starthinker.util.google_api import API_DCM
from starthinker.task.itp_audit.queries import Queries

# Output Tables
BROWSER_PERFORMANCE_2YEARS_TABLE = 'DV3_Browser'
SAFARI_DISTRIBUTION_90DAYS_TABLE = 'DV3_Safari'
DV360_BROWSER_SHARES_MULTICHART_TABLE = 'DV3_MultiChart'
CM_BROWSER_REPORT_CLEAN_TABLE = 'CM_Browser'
CM_FLOODLIGHT_MULTICHART_TABLE = 'CM_Floodlight_Multichart'
SDF_LI_SCORES_TABLE = 'DV3_Li_Scores'
CM_PLACEMENT_AUDIT_TABLE = 'CM_Placement_Audit'

# Tables
CLEAN_BROWSER_REPORT_TABLE = 'z_DV360_Browser_Report_Clean'
DV360_CUSTOM_SEGMENTS_TABLE = 'z_Custom_Segments'
DV360_CUSTOM_SEGMENTS_SHEET_TABLE = 'z_Custom_Segments_Sheet'
CM_SITE_SEGMENTATION_SHEET_TABLE = 'z_CM_Site_Segmentation_Sheet'
CM_SITE_SEGMENTATION_TABLE = 'z_CM_Site_Segmentation'
CM_BROWSER_REPORT_DIRTY_TABLE = 'z_CM_Browser_Report_Dirty'
CM_FLOODLIGHT_TABLE = 'z_CM_Floodlight'
SDF_FEATURE_FLAGS_TABLE = 'z_sdf_feature_flags'
SDF_SCORING_TABLE = 'z_sdf_scoring'
CM_FLOODLIGHT_OUTPUT_TABLE = 'z_Floodlight_CM_Report'

PLACEMENTS_SCHEMA = [
  {'name':'placement', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'placementId', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'placementName', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'advertiser', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'advertiserId', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'advertiserName', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'campaign', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'campaignId', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'campaignName', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'siteId', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'siteName', 'type':'STRING', 'mode':'REQUIRED'},
  {'name':'totalStandardAds', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'nonImpactedAds', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'frequencyCapAds', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'audienceListAds', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'audienceSegmentAds', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'browserPlatformTargetingAds', 'type':'INT64', 'mode':'REQUIRED'},
  {'name':'dynamicCreativeAds', 'type':'INT64', 'mode':'REQUIRED'}
]

def itp_audit(config, task):
  if config.verbose:
    print('ITP Audit Run Queries')

  # Run floodlight config reports
  run_floodlight_reports(config, task)

  # Run DV360 related queries
  run_dv_360_queries(config, task)

  # Create CM Site Segmentation Table and Sheet
  create_cm_site_segmentation(config, task)

  # CM Segmentation Query
  if config.verbose:
    print('RUN CM Segmentation Query')
  run_query_from_file(config, task, Queries.cm_segmentation.replace('{{dataset}}', task['dataset']), CM_BROWSER_REPORT_CLEAN_TABLE)

  run_cm_queries(config, task)

  # Run SDF queries
  run_sdf_queries(config, task)

  # CM Account Audit
  itp_audit_cm(config, task)

def run_sdf_queries(config, task):
  if config.verbose:
    print('RUN SDF Query')
  run_query_from_file(config, task, Queries.sdf_feature_flags.replace('{{dataset}}', task['dataset']), SDF_FEATURE_FLAGS_TABLE)
  run_query_from_file(config, task, Queries.sdf_scoring.replace('{{dataset}}', task['dataset']), SDF_SCORING_TABLE)
  run_query_from_file(config, task, Queries.sdf_li_scores.replace('{{dataset}}', task['dataset']), SDF_LI_SCORES_TABLE)

def run_cm_queries(config, task):
  # CM Floodlight Lookup Table
  run_query_from_file(config, task, Queries.cm_floodlight_join.replace('{{dataset}}', task['dataset']), CM_FLOODLIGHT_TABLE)

  # Floodlight Multichart
  if config.verbose:
    print('RUN CM Floodlight Multichart')
  run_query_from_file(config, task, Queries.cm_floodlight_multichart.replace('{{dataset}}', task['dataset']), CM_FLOODLIGHT_MULTICHART_TABLE)


def run_dv_360_queries(config, task):
  # Create empty DV360 Custom Segments table for join until sheet is created
  table_create(config, task['auth_bq'], config.project, task['dataset'], DV360_CUSTOM_SEGMENTS_TABLE)

  # Create DV360 Segments Table
  create_dv360_segments(config, task)

  # Clean DV360 Browser Report
  run_query_from_file(config, task, Queries.clean_browser_report.replace('{{dataset}}', task['dataset']), CLEAN_BROWSER_REPORT_TABLE)

  # Browser Performance 2 years
  if config.verbose:
    print('RUN Browser Performance 2 years Query')
  run_query_from_file(config, task, Queries.browser_2_year.replace('{{dataset}}', task['dataset']), BROWSER_PERFORMANCE_2YEARS_TABLE)

  #Safari Distribution 90 days
  if config.verbose:
    print('RUN Safari Distribution 90 days Query')
  run_query_from_file(config, task, Queries.safari_distribution_90days.replace('{{dataset}}', task['dataset']), SAFARI_DISTRIBUTION_90DAYS_TABLE)

  # Browser Shares Multichart
  if config.verbose:
    print('RUN Dv360 Browser Share Multichart')
  run_query_from_file(config, task, Queries.browser_share_multichart.replace('{{dataset}}', task['dataset']), DV360_BROWSER_SHARES_MULTICHART_TABLE)


def create_dv360_segments(config, task):
  a1_notation = 'A:N'
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
      { "type": "STRING", "name": "SegmentAutoGen", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Segment1", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Segment2", "mode": "NULLABLE" },
      { "type": "STRING", "name": "Segment3", "mode": "NULLABLE" }
    ]

  sheet_rows = sheets_read(config, task['auth_sheets'], task['sheet'], 'DV3 Segments', a1_notation)

  if not sheet_rows:
    sheet_rows = []

  print('DV360 SEGMENT SHEET TABLE WRITE')

  rows_to_table(
    config,
    auth=task['auth_bq'],
    project_id=config.project,
    dataset_id=task['dataset'],
    table_id=DV360_CUSTOM_SEGMENTS_SHEET_TABLE,
    rows=sheet_rows,
    schema=schema,
    skip_rows=1,
    disposition='WRITE_TRUNCATE'
    )

  # Run Query
  if config.verbose:
    print('RUN DV360 Custom Segments Query')
  run_query_from_file(config, task, Queries.dv360_custom_segments.replace('{{dataset}}', task['dataset']), DV360_CUSTOM_SEGMENTS_TABLE)

  # Move Table back to sheets
  query = 'SELECT * from `' + config.project + '.' + task['dataset'] + '.' + DV360_CUSTOM_SEGMENTS_TABLE + '`'
  rows = query_to_rows(config, task['auth_bq'], config.project, task['dataset'], query, legacy=False)

  # makes sure types are correct in sheet
  a1_notation = a1_notation[:1] + '2' + a1_notation[1:]
  rows = rows_to_type(rows)
  sheets_clear(config, task['auth_sheets'], task['sheet'], 'DV3 Segments', a1_notation)
  sheets_write(config, task['auth_sheets'], task['sheet'], 'DV3 Segments', a1_notation, rows)


'''
This method will update the BQ table and update the Google sheet
'''
def create_cm_site_segmentation(config, task):
  # Read sheet to bq table
  sheet_rows = sheets_read(config, task['auth_sheets'], task['sheet'], 'CM_Site_Segments', 'A:C')
  if not sheet_rows:
    sheet_rows = []

  schema = [
    { "type": "STRING", "name": "Site_Dcm", "mode": "NULLABLE" },
    { "type": "INTEGER", "name": "Impressions", "mode": "NULLABLE" },
    { "type": "STRING", "name": "Site_Type", "mode": "NULLABLE" }
  ]

  rows_to_table(
    config,
    auth=task['auth_bq'],
    project_id=config.project,
    dataset_id=task['dataset'],
    table_id=CM_SITE_SEGMENTATION_SHEET_TABLE,
    rows=sheet_rows,
    schema=schema,
    skip_rows=1,
    disposition='WRITE_TRUNCATE'
  )

  # Get Site_Type from the sheet
  run_query_from_file(config, task, Queries.cm_site_segmentation.replace('{{dataset}}', task['dataset']), CM_SITE_SEGMENTATION_TABLE)

  # Move Table back to sheets
  query = 'SELECT * from `' + config.project + '.' + task['dataset'] + '.' + CM_SITE_SEGMENTATION_TABLE + '`'
  rows = query_to_rows(config, task['auth_bq'], config.project, task['dataset'], query, legacy=False)

  # makes sure types are correct in sheet
  rows = rows_to_type(rows)
  sheets_clear(config, task['auth_sheets'], task['sheet'], 'CM_Site_Segments', 'A2:C')
  sheets_write(config, task['auth_sheets'], task['sheet'], 'CM_Site_Segments', 'A2:C', rows)


def run_floodlight_reports(config, task):
  if config.verbose:
    print('Creating Floodlight reports')

  body = {
    "kind": "dfareporting#report",
    "name": '', # this is updated below based on Floodlight Config ID
    "format": "CSV",
    "type": "FLOODLIGHT",
    "floodlightCriteria": {
      "dateRange": {
        "kind": "dfareporting#dateRange",
        "relativeDateRange": "LAST_60_DAYS"
      },
      "floodlightConfigId": {
        "kind": "dfareporting#dimensionValue",
        "dimensionName": "floodlightConfigId",
        "value": 0, # updated below and replaced with Floodlight Config ID
        "matchType": "EXACT"
      },
      "reportProperties": {
        "includeUnattributedIPConversions": False,
        "includeUnattributedCookieConversions": True
      },
      "dimensions": [
      {
        "kind": "dfareporting#sortedDimension",
        "name": "site"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "floodlightAttributionType"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "interactionType"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "pathType"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "browserPlatform"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "platformType"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "week"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "placementId"
      },
      {
        "kind": "dfareporting#sortedDimension",
        "name": "floodlightConfigId"
      }],
      "metricNames": [
        "activityClickThroughConversions",
        "activityViewThroughConversions",
        "totalConversions",
        "totalConversionsRevenue"
      ]
    },
    "schedule": {
      "active": True,
      "repeats": "WEEKLY",
      "every": 1,
      "repeatsOnWeekDays":["Sunday"]
    },
    "delivery": {
      "emailOwner": False
    }
  }

  reports = []
  floodlightConfigs = task.get('floodlightConfigIds', None)

  for configId in floodlightConfigs:
    body['name'] = task.get('reportPrefix', '') + "_" + str(configId)
    body['floodlightCriteria']['floodlightConfigId']['value'] = configId
    report = report_build(
      config, task['auth_cm'],
      task['account'],
      body
    )
    reports.append(report['id'])

  if config.verbose:
    print('Finished creating Floodlight reports - moving to BQ')

  queries = []

  for createdReportId in reports:
    filename, report = report_file(
      config, task['auth_cm'],
      task['account'],
      createdReportId,
      None,
      task.get('timeout', 10),
    )

    if report:
      if config.verbose:
        print('Floodlight config report ', filename)

      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows)

      # determine schema
      schema = report_schema(next(rows))

      out_block = {}
      out_block['bigquery'] = {}


      out_block['bigquery']['dataset'] = task['dataset']
      out_block['bigquery']['schema'] = schema
      out_block['bigquery']['skip_rows'] = 0
      out_block['bigquery']['table'] = 'z_Floodlight_CM_Report_' + str(createdReportId)

      # write rows using standard out block in json ( allows customization across all scripts )
      if rows: put_rows(config, task['auth_bq'], out_block, rows)
      queries.append('SELECT * FROM `{0}.{1}.{2}`'.format(config.project, out_block['bigquery']['dataset'], out_block['bigquery']['table']))

  if config.verbose:
    print('Moved reports to BQ tables - starting join')
  finalQuery = ' UNION ALL '.join(queries)

  query_to_table(
    config, task['auth_bq'],
    config.project,
    task['dataset'],
    CM_FLOODLIGHT_OUTPUT_TABLE,
    finalQuery,
    legacy=False
  )

  if config.verbose:
    print('Finished with Floodlight Config reports')

def run_query_from_file(config, task, query, table_name):
  query_to_table(
    config, task['auth_bq'],
    config.project,
    task['dataset'],
    table_name,
    query.format(**task),
    legacy=False
  )


def itp_audit_cm(config, task):
  account_id = task['account']
  # Read Advertiser Ids
  advertiser_ids = list(get_rows(config, task['auth_bq'], task['read']['advertiser_ids']))
  is_superuser, profile_id = get_profile_for_api(config, task['auth_cm'], account_id)

  datasets_create(config, task['auth_bq'], config.project, task['dataset'])

  placements = {}
  campaignNames = {}
  siteNames = {}
  advertiserNames = {}

  for c in API_DCM(config, task['auth_cm'], iterate=True, internal=is_superuser).campaigns().list(archived=False, profileId=profile_id, accountId=account_id, advertiserIds=advertiser_ids if advertiser_ids else None).execute():
    # only keep campaigns with end dates in the future or less than 90 days ago
    if ((date.fromisoformat(c['endDate']) - date.today()).days > -90):
      campaignNames[c['id']] = {
        'id': c['id'],
        'name': c['name'],
        'startDate': c['startDate'],
        'endDate': c['endDate']
      }

  validCampaignIds = [int(i) for i in campaignNames.keys()]

  for s in API_DCM(config, task['auth_cm'], iterate=True, internal=is_superuser).sites().list(profileId=profile_id, accountId=account_id, campaignIds=validCampaignIds).execute():
    siteNames[s['id']] = s['name']

  for a in API_DCM(config, task['auth_cm'], iterate=True, internal=is_superuser).advertisers().list(profileId=profile_id, accountId=account_id, ids=advertiser_ids[:500] if advertiser_ids else None).execute():
    advertiserNames[a['id']] = a['name']

  if len(advertiser_ids) > 500:
      for a in API_DCM(config, task['auth_cm'], iterate=True, internal=is_superuser).advertisers().list(profileId=profile_id, accountId=account_id, ids=advertiser_ids[500:] if advertiser_ids else None).execute():
        advertiserNames[a['id']] = a['name']

  for p in API_DCM(config, task['auth_cm'], iterate=True, internal=is_superuser).placements().list(archived=False, profileId=profile_id, accountId=account_id, advertiserIds=advertiser_ids if advertiser_ids else None, campaignIds=validCampaignIds).execute():
    # exclude 1x1 tracking placements
    if not (p['size']['height'] == 1 and p['size']['width'] == 1):
      placements[p['id']] = {
      'id': p['id'],
      'name': p['name'],
      'advertiserId': p['advertiserId'],
      'advertiserName': advertiserNames[p['advertiserId']],
      'campaignId': p['campaignId'],
      'campaignName': campaignNames[p['campaignId']]['name'],
      'siteId': p['siteId'],
      'siteName': siteNames[p['siteId']],
      'adsTotal': 0,
      'adsNotImpacted': 0,
      'adsFrequencyCapped': 0,
      'adsAudienceSegmentation': 0,
      'adsAudienceListTargeting': 0,
      'adsDynamicCreative': 0,
      'adsPlatformBrowserTargeting': 0
      }

  for ad in API_DCM(config, task['auth_cm'], iterate=True, internal=is_superuser).ads().list(type='AD_SERVING_STANDARD_AD', profileId=profile_id, accountId=account_id, campaignIds=validCampaignIds).execute():
    # only analyze standard, non-default priority ads that have been assigned 1+ placements and creatives
    if ad['deliverySchedule']['priority'] != "AD_PRIORITY_16" and 'placementAssignments' in ad and 'creativeAssignments' in ad['creativeRotation']:
      hasDynamicCreative = False
      for creative in ad['creativeRotation']['creativeAssignments']:
        if 'richMediaExitOverrides' in creative:
          hasDynamicCreative = True
          break

      for p in ad['placementAssignments']:
        if p['placementId'] in placements:
          knownPlacement = placements[p['placementId']]
          knownPlacement['adsTotal'] += 1

          if 'frequencyCap' in ad['deliverySchedule']:
            knownPlacement['adsFrequencyCapped'] += 1
          if 'audienceSegmentId' in ad:
            knownPlacement['adsAudienceSegmentation'] += 1
          if 'remarketingListExpression' in ad:
            knownPlacement['adsAudienceListTargeting'] += 1
          if 'technologyTargeting' in ad and ('browsers' in ad['technologyTargeting'] or 'platformTypes' in ad['technologyTargeting']):
            knownPlacement['adsPlatformBrowserTargeting'] += 1
          if hasDynamicCreative:
            knownPlacement['adsDynamicCreative'] += 1
          if not 'frequencyCap' in ad['deliverySchedule'] and not 'audienceSegmentId' in ad and not 'remarketingListExpression' in ad:
            knownPlacement['adsNotImpacted'] += 1

  write_data = []
  for p in placements.values():
    write_data.append([
      p['name'] + ' - ' + str(p['id']),
      p['id'],
      p['name'],
      p['advertiserName'] + ' - ' + str(p['advertiserId']),
      p['advertiserId'],
      p['advertiserName'],
      p['campaignName'] + ' - ' + str(p['campaignId']),
      p['campaignId'],
      p['campaignName'],
      p['siteId'],
      p['siteName'],
      p['adsTotal'],
      p['adsNotImpacted'],
      p['adsFrequencyCapped'],
      p['adsAudienceListTargeting'],
      p['adsAudienceSegmentation'],
      p['adsPlatformBrowserTargeting'],
      p['adsDynamicCreative']
    ])

  placements_out = {}
  placements_out["bigquery"] = {
    "dataset": task['dataset'],
    "table": CM_PLACEMENT_AUDIT_TABLE,
    "is_incremental_load": False,
    "datastudio": True,
    "schema": PLACEMENTS_SCHEMA,
    "skip_rows": 0
  }

  if placements: put_rows(config, task['auth_bq'], placements_out, write_data)
