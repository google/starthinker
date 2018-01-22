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
from util.dcm import report_create, report_file, report_to_rows, report_clean
from util.bigquery import csv_to_table
from util.csv import rows_column_add, rows_to_csv, rows_to_type, rows_header_trim, rows_print

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

def sov():
  if project.verbose: print "CLIENT", project.task['dataset']

  # ensure we have minimum number of peer accounts to ensure obfuscation
  if len(project.task['dcm_accounts']) < 6:
    raise Exception('Need at least 6 DCM accounts to ensure anonymity!')
  
  # first pass create reports
  label = project.task['dataset']
  for dcm_account in project.task['dcm_accounts']:
    name = "SOV %s %s %s ( StarThinker )" % (project.task['dataset'], label, dcm_account)
    if project.verbose: print 'SOV REPORT', name

    report_create(
      project.task['auth'], 
      dcm_account,  
      name,
      {
        "type":"STANDARD",
        "relativeDateRange":"LAST_90_DAYS",
        "dimensions":["date", "month", "platformType", "creativeType", "state", "dmaRegion"],
        "metrics":["impressions"]
      }
    )

    # after first id, change it to peer
    label = 'Peer'

  # second pass download data
  row_sum = {}
  row_mix = {}
  label = project.task['dataset']
  for dcm_account in project.task['dcm_accounts']:
    name = "SOV %s %s %s ( StarThinker )" % (project.task['dataset'], label, dcm_account)
    if project.verbose: print 'SOV DOWNLOAD', name

    filename, report = report_file(project.task['auth'], dcm_account, name=name)

    # if a report exists
    if report:
      # clean up the report
      rows = report_to_rows(report)
      rows = report_clean(rows, True)

      # add columns
      rows = rows_column_add(rows, 'Advertiser Type', label, 2)
  
      # trim headers and cast impressions
      rows = rows_header_trim(rows)
      rows = rows_to_type(rows, 7)

      for row in rows:
        key = ''.join(row[:7])
        new_row = [
          row[0], # Report_Day
          row[1], # Year_Month
          row[2], # Advertiser_Type
          row[3], # Platform_Type
          row[4], # Creative_Type
          row[5], # State_Region
          row[6], # Designated_Market_Area
          row[7] if label != 'Peer' else 0, # Client_Impressions
          row[7] if label == 'Peer' else 0, # Peer_Impressions
        ]

        # combine the rows for obfuscation
        if key in row_sum: 
          row_sum[key][7] += new_row[7]
          row_sum[key][8] += new_row[8]
        else: 
          row_sum[key] = new_row

        # check the mix ( needs to be relatively balanced )
        if label == 'Peer':
          row_mix[dcm_account] = row_mix.get(dcm_account, 0) + row[7]

    else:
      if project.verbose: print 'SOV REPORT NOT READY YET'

    # after first read pass
    label = 'Peer'
    
  if row_sum and row_mix:
  
    print row_mix
    # safety checks to make sure we've got obfuscated data ( trigger if no impressions or if percent mix is too low )
    mix_total = sum(row_mix.values())
    mix_ratio_low = (100 / (len(row_mix))) / 3  
    mix_ratio_high = 50 # 1/5 = 20%, so 50% covers that, no single peer can have more than 50% of the weight
    for account, impressions in row_mix.items():
      percent = (100 * impressions) / mix_total
      if project.verbose: print 'EXPECTED MIX %d%%-%d%%  ACTUAL MIX: %s %d%%' % (mix_ratio_low, mix_ratio_high, account, percent)
      if impressions == 0: 
        raise Exception('Account %s has no impressions, change it out!' % account)
      #elif percent < mix_ratio_low:
      #  raise Exception('Account %s has too little weight %d%%, expected above %d%%, change for bigger peer!' % (account, percent, mix_ratio_low))
      elif percent > mix_ratio_high:
        raise Exception('Account %s has too much weight %d%%, expected under %d%%, add other big peers!' % (account, percent, mix_ratio_high))

    csv_to_table(
      project.task['auth'],
      project.id,
      project.task['dataset'],
      project.task['table'],
      rows_to_csv(row_sum.values()),
      SCHEMA,
      0
    )
  else:
    raise Exception('NOT ENOUGH DATA: %d Rows AND %d Peers' % (len(row_sum), len(row_mix)))

if __name__ == "__main__":
  project.load('sov')
  sov()
