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
from util.dcm import report_get, report_to_rows, report_clean, report_to_csv
from util.storage import object_put, bucket_create
from util.regexp import strip_yyymmdd, str_to_date
from util.bigquery import storage_to_table, query_to_view


def run_report(dcm_account, dataset, label):

  # create the report and fetch latest download
  filename, report = report_get(
    project.task['auth'], 
    {
      "collate":"LATEST",
      "template":"standard",
      "name":"SOV %s %s %s ( StarThinker )" % (dataset, label, dcm_account),
      "fileName":"SOV_%s_report" % dcm_account, # ensure each file is unique as they go in same bucket
      "format":"CSV",
      "active":True,
      "accountId":dcm_account,
      "relativeDateRange":"QUARTER_TO_DATE",
      "dimensions":["date", "month", "platformType", "creativeType", "state", "dmaRegion"],
      "metrics":["impressions"]
    }
  )

  # if a report exists
  if report:

    # collate by removig date
    filename = strip_yyymmdd(filename)

    if project.verbose: print 'SOV FILE', filename

    # clean up the report
    rows = report_to_rows(report)
    rows = report_clean(rows, project.date, True)

    if rows:

      # add label and quarter to the report ( remember, this needs to be anyonymous so no ids )
      rows[0].append('Advertiser Type')
      for i in range(1, len(rows)): 
        rows[i].append(label)

      # upload to cloud if data
      if rows: object_put(project.task['auth'], project.task['storage']['bucket'] + ':' + project.task['storage']['path'] + filename, report_to_csv(rows))


def sov():
  if project.verbose: print "CLIENT", project.task['dataset']['dataset']

  # ensure we have minimum number of peer accounts to ensure obfuscation
  if len(project.task['dcm_accounts']) < 6:
    raise Exception('Need at least 6 DCM accounts to ensure anonymity!')

  # create a bucket
  bucket_create(project.task['auth'], project.id, project.task['storage']['bucket'])

  # loop all dcm ids ( first one is client )
  label = project.task['dataset']['dataset']
  for dcm_account in project.task['dcm_accounts']:
    run_report(dcm_account, project.task['dataset']['dataset'], label)
    label = 'Peer'
    
  # move data over to bigquery
  storage_to_table(
    project.task['auth'],
    project.id,
    project.task['dataset']['dataset'],
    project.task['dataset']['table'],
    project.task['storage']['bucket'] + ':' + project.task['storage']['path'] + '*',
  )

if __name__ == "__main__":
  project.load('sov')
  sov()
