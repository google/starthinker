###########################################################################
#
#  Copyright 2017 Google Inc.
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
from starthinker.util.dbm import report_create, report_file, report_to_rows, report_clean, accounts_split, DBM_CHUNKSIZE
from starthinker.util.bigquery import rows_to_table
from starthinker.util.csv import rows_to_csv, rows_header_trim
from starthinker.util.sheets import sheets_tab_copy, sheets_read

RE_STATE = re.compile(r'\s+\(.*?\)') # remove things like (state) or (province) from end of state names

SCHEMA = [
  { "name":"Report_Day", "type":"INTEGER" },
  { "name":"Year_Month", "type":"STRING" },
  { "name":"Advertiser_Type", "type":"STRING" },
  { "name":"Platform_Type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Creative_Type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"State_Region", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Designated_Market_Area", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Client_Impressions", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Peer_Impressions", "type":"INTEGER", "mode":"NULLABLE" },
]


def sov_report(dbm_accounts, label):

  # make sure name does not collide
  name = "SOV DBM %s %s ( StarThinker )" % (project.task['dataset'], label)
  if project.verbose: print('SOV REPORT:', name)

  # legacy fix: split accounts into partners and advertisers
  partners, advertisers = accounts_split(dbm_accounts)

  # create a report on a regular schedule to provide SOV data
  report_create(
    project.task['auth'],
    name,
    'TYPE_CROSS_PARTNER',
    partners,
    advertisers,
    [],
    ['FILTER_ADVERTISER', 'FILTER_DATE', 'FILTER_MONTH', 'FILTER_MOBILE_DEVICE_TYPE', 'FILTER_CREATIVE_TYPE', 'FILTER_REGION', 'FILTER_CITY'],
    ['METRIC_IMPRESSIONS'],
    'LAST_365_DAYS',
    project.recipe['setup']['timezone']
  )

  # name is used later to look up this report
  return name


def sov_create_reports():
  if project.verbose: print("CLIENT:", project.task['dataset'])

  # make sure tab exists in sheet
  sheets_tab_copy(project.task['auth'], project.task['sheet']['template']['url'], project.task['sheet']['template']['tab'], project.task['sheet']['url'], project.task['sheet']['template']['tab'])

  # read peers from sheet
  rows = sheets_read(project.task['auth'], project.task['sheet']['url'], project.task['sheet']['template']['tab'], project.task['sheet']['range'])

  # CHECK: If minimum number of peers met ( prevents creation of reports )
  if len(rows) < 5:
    raise Exception('Peer sheet needs 5+ DBM entries to ensure anonymity, there are %d!' % len(rows))
  
  # create a report for the peers ( given in sheet ), make partner_id:advertiser_id
  peer_name = sov_report([('%s:%s' % (r[0], r[1])) if len(r) == 2 else r[0] for r in rows], 'Peer')

  # create a report for the client ( given in JSON )
  client_name = sov_report(project.task['dbm_accounts'], 'Client')

  # names are used to fetch the report
  return client_name, peer_name


def sov_process_client(report_name):
  sov_rows = {}

  # Download DBM report: ['Advertiser', 'Advertiser ID', 'Advertiser Status', 'Advertiser Integration Code', 'Date', 'Month', 'Device Type', 'Creative Type', 'Region', 'Region ID', 'City', 'City ID', 'Impressions']
  #                        0             1                2                    3                              4       5        6              7                8         9            10      11         12
  filename, report = report_file(
    project.task['auth'],
    None,
    report_name,
    60,
    DBM_CHUNKSIZE
  )

  # if a report exists
  if report:
    if project.verbose: print('CLIENT FILE', filename)

    # convert report to array
    rows = report_to_rows(report)
    rows = report_clean(rows, datastudio=True, nulls=True)
    rows = rows_header_trim(rows)
 
    # pull only needed fields ( see: SCHEMA )
    for row in rows:
      key = ''.join(row[4:-1]) # Everything except impressions

      # if peer is in sov, then just add the impressions
      if key in sov_rows:
        sov_rows[key][7] += int(row[12])

      # otherwise, create a new anonymous peer row
      else:
        sov_rows[key] = [
          row[4],                  # 0 Report_Day
          row[5],                  # 1 Year_Month
          'Client',                # 2 Advertiser_Type
          row[6],                  # 3 Platform_Type
          row[7],                  # 4 Creative_Type
          RE_STATE.sub('', row[8]),# 5 State_Region
          row[10],                 # 6 Designated_Market_Area
          int(row[12]),           # 7 Client_Impressions
          0                        # 8 Peer_Impressions
        ]

  else:
    if project.verbose: print('SOV REPORT NOT READY YET')

  # return only row values, hash key no longer necessary
  return sov_rows.values()


def sov_process_peer(report_name):
  sov_rows = {}
  sov_mix = {}
  mix_ratio_high = 50
  warnings = []
  errors = []

  # Download DBM report: ['Advertiser', 'Advertiser ID', 'Advertiser Status', 'Advertiser Integration Code', 'Date', 'Month', 'Device Type', 'Creative Type', 'Region', 'Region ID', 'City', 'City ID', 'Impressions']
  #                        0             1                2                    3                              4       5        6              7                8         9            10      11         12
  filename, report = report_file(
    project.task['auth'],
    None,
    report_name,
    60,
    DBM_CHUNKSIZE
  )

  # if a report exists
  if report:
    if project.verbose: print('CLIENT FILE', filename)

    # convert report to array
    rows = report_to_rows(report)
    rows = report_clean(rows, datastudio=True, nulls=True)
    rows = rows_header_trim(rows)
 
    for row in rows:
      key = ''.join(row[4:-1]) # Everything except impressions

      # track advertiser level mix
      sov_mix[row[1]] = sov_mix.get(row[1], 0) + int(row[12])

      # if peer is in sov, then just add the impressions
      if key in sov_rows:
        sov_rows[key][8] += int(row[12])

      # otherwise, create a new anonymous peer row
      else:
        sov_rows[key] = [
          row[4],                  # 0 Report_Day
          row[5],                  # 1 Year_Month
          'Peer',                  # 2 Advertiser_Type
          row[6],                  # 3 Platform_Type
          row[7],                  # 4 Creative_Type
          RE_STATE.sub('', row[8]),# 5 State_Region
          row[10],                 # 6 Designated_Market_Area
          0,                       # 7 Client_Impressions
          int(row[12])            # 8 Peer_Impressions
        ]

    # CHECK: Mix must be right, make sure we've got obfuscated data, no peer has more than 50% 
    mix_total = sum(sov_mix.values())

    for account, impressions in sov_mix.items():
      percent = (100 * impressions) / mix_total
      if project.verbose: print('EXPECTED MIX %d%% ACTUAL MIX: %s %d%%' % (mix_ratio_high, account, percent))

      if impressions == 0: 
        warnings.append('Warning advertiser %s has no impressions.' % account)
      elif percent > mix_ratio_high:
        errors.append('Advertiser %s has too much weight %d%%, expected under %d%%, add other big peers!' % (account, percent, mix_ratio_high))

    if len(sov_mix.keys()) < 5:
      errors.extend(warnings)
      errors.append('Need at least 5 DBM advertisers with impressions to ensure anonymity!')
  
    # raise all errors at once so user can clean up multiple errors at once
    if errors: raise Exception('\n'.join(errors))
  
  else:
    if project.verbose: print('SOV REPORT NOT READY YET')

  # return only row values, hash key no longer necessary
  return sov_rows.values()


@project.from_parameters
def sov_dbm():
  # 1 - creat one report for client and oen report for peers
  client_name, peer_name = sov_create_reports()

  # 2 - Download the reports and aggregate into one table
  sov_rows = sov_process_client(client_name)
  sov_rows.extend(sov_process_peer(peer_name))

  # 3 - Save the report to the specified table
  rows_to_table(
    project.task['auth'],
    project.id,
    project.task['dataset'],
    project.task['table'],
    sov_rows,
    SCHEMA,
    0
  )

if __name__ == "__main__":
  sov_dbm()
