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

from util.project import project 
from util.dcm import report_create, report_file, report_to_rows, report_clean, DCM_CHUNKSIZE
from util.bigquery import csv_to_table
from util.csv import rows_to_csv, rows_header_trim
from util.sheets import sheets_tab_copy, sheets_read


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


def sov_report(dcm_accounts, label):
  names = []

  for dcm_account in dcm_accounts:
    name = "SOV %s %s %s ( StarThinker )" % (project.task['dataset'], label, dcm_account.split('@', 1)[0])
    if project.verbose: print 'SOV REPORT', name

    report_create(
      project.task['auth'],
      dcm_account,
      name,
      {
        "type":"STANDARD",
        "relativeDateRange":"LAST_365_DAYS",
        "dimensions":["date", "month", "platformType", "creativeType", "state", "dmaRegion"],
        "metrics":["impressions"]
      }
    )

    names.append({ 'account':dcm_account, 'name':name})

  return names
    

def sov_create_reports():
  if project.verbose: print "CLIENT:", project.task['dataset']

  # make sure tab exists in sheet
  sheets_tab_copy(project.task['auth'], project.task['sheet']['template']['url'], project.task['sheet']['template']['tab'], project.task['sheet']['url'], project.task['sheet']['template']['tab'])

  # read peers from sheet
  rows = sheets_read(project.task['auth'], project.task['sheet']['url'], project.task['sheet']['template']['tab'], project.task['sheet']['range'])

  # CHECK: If minimum number of peers met
  if len(rows) < 5:
    raise Exception('Need at least 5 DBM accounts in the sheet to ensure anonymity!')

  # create reports for the peers ( given in sheet ), make account_id:advertiser_id@profile_id
  peer_names = sov_report([r[0] + ((':%s' % r[1]) if len(r) > 1 else '') + (('@%s' % r[2]) if len(r) > 2 else '')  for r in rows], 'Peer')

  # create reports for the client ( given in JSON )
  client_names = sov_report(project.task['dcm_accounts'], 'Client')

  # names are used to fetch the report
  return client_names, peer_names


def sov_process_client(names):
  sov_rows = {}

  # Download DCM report: ['Report_Day', 'Month', 'Platform_Type', 'Creative_Type', 'State_Region', 'Designated_Market_Area_DMA_', 'Impressions']
  #                        0             1        2                3                4               5                              6 
  for name in names:

    filename, report = report_file(
      project.task['auth'],
      name['account'],
      None,
      name['name'],
      60,
      DCM_CHUNKSIZE
    )

    # if a report exists
    if report:
      if project.verbose: print 'CLIENT FILE', filename

      # convert report to array
      rows = report_to_rows(report)
      rows = report_clean(rows, datastudio=True)
      rows = rows_header_trim(rows)

      # pull only needed fields ( see: SCHEMA )
      for row in rows:
        key = ''.join(row[:-1]) # Everything except impressions

        # if peer is in sov, then just add the impressions
        if key in sov_rows:
          sov_rows[key][7] += long(row[6])

        # otherwise, create a new anonymous peer row
        else:
          sov_rows[key] = [
            row[0],        # 0 Report_Day
            row[1],        # 1 Year_Month
            'Client',      # 2 Advertiser_Type
            row[2],        # 3 Platform_Type
            row[3],        # 4 Creative_Type
            row[4],        # 5 State_Region
            row[5],       # 6 Designated_Market_Area
            long(row[6]), # 7 Client_Impressions
            0              # 8 Peer_Impressions
          ]

    else:
      if project.verbose: print 'SOV REPORT NOT READY YET'

  # return only row values, hash key no longer necessary
  return sov_rows.values()


def sov_process_peer(names):
  sov_rows = {}
  sov_mix = {}

  # Download DCM report: ['Report_Day', 'Month', 'Platform_Type', 'Creative_Type', 'State_Region', 'Designated_Market_Area_DMA_', 'Impressions']
  #                        0             1        2                3                4               5                              6 
  for name in names:

    filename, report = report_file(
      project.task['auth'],
      name['account'],
      None,
      name['name'],
      60,
      DCM_CHUNKSIZE
    )

    # track impressions per report ( start with zero to trigger checks below )
    sov_mix[name['account']] = 0

    # if a report exists
    if report:
      if project.verbose: print 'CLIENT FILE', filename

      # convert report to array
      rows = report_to_rows(report)
      rows = report_clean(rows, datastudio=True)
      rows = rows_header_trim(rows)

      # pull only needed fields ( see: SCHEMA )
      for row in rows:
        key = ''.join(row[:-1]) # Everything except impressions

        # track peer level mix
        sov_mix[name['account']] += long(row[6])

        # if peer is in sov, then just add the impressions
        if key in sov_rows:
          sov_rows[key][8] += long(row[6])

        # otherwise, create a new anonymous peer row
        else:
          sov_rows[key] = [
            row[0],        # 0 Report_Day
            row[1],        # 1 Year_Month
            'Peer',        # 2 Advertiser_Type
            row[2],        # 3 Platform_Type
            row[3],        # 4 Creative_Type
            row[4],        # 5 State_Region
            row[5],        # 6 Designated_Market_Area
            0,             # 7 Client_Impressions
            long(row[6]),  # 8 Peer_Impressions
          ]

    else:
      if project.verbose: print 'SOV REPORT NOT READY YET'

  # CHECK: Mix must be right, make sure we've got obfuscated data ( trigger if no impressions or if percent mix is too high )
  mix_total = sum(sov_mix.values())
  mix_ratio_high = 50 
  mix_count = 0
  warnings = []
  errors = []

  for account, impressions in sov_mix.items():
    percent = (100 * impressions) / mix_total
    if project.verbose: print 'EXPECTED MIX %d%% ACTUAL MIX: %s %d%%' % (mix_ratio_high, account, percent)

    # check impression minimums ( track number of valid peers for 5 required ), empty peers are warnings until required
    if impressions > 0: 
      mix_count += 1
    else: 
      warnings.append('Advertiser %s has no impressions, change it out!' % account)

    # check for peer mix, any violation is immeditely an error
    if percent > mix_ratio_high:
      errors.append('Advertiser %s has too much weight %d%%, expected under %d%%, add other big peers!' % (account, percent, mix_ratio_high))

  # check if enough peers ( ignore peers without impressions until it affects the required minimum )
  if mix_count < 5:
    errors.extend(warnings)
    errors.append('Need at least 5 DCM accounts with impressions to ensure anonymity!')

  # raise all errors at once so user can clean up multiple errors at once
  if errors: raise Exception('\n'.join(errors))

  # return only row values, hash key no longer necessary
  return sov_rows.values()


def sov():
  # 1 - creat one report for client and oen report for peers
  client_names, peer_names = sov_create_reports()

  # 2 - Download the reports and aggregate into one table
  sov_rows = sov_process_client(client_names)
  sov_rows.extend(sov_process_peer(peer_names))

  # 3 - Save the report to the specified table
  csv_to_table(
    project.task['auth'],
    project.id,
    project.task['dataset'],
    project.task['table'],
    rows_to_csv(sov_rows),
    SCHEMA,
    0
  )

if __name__ == "__main__":
  project.load('sov_dcm')
  sov()
