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

# https://developers.google.com/bid-manager/v1/queries
# https://github.com/googleads/googleads-bidmanager-examples/blob/master/python/get_latest_report.py

import pprint
import urllib2
import csv
import json
import time
from apiclient import http
from StringIO import StringIO
from io import BytesIO

#from datetime import datetime, time as localtime, date
from googleapiclient.errors import HttpError

from setup import TIMEZONE_OFFSET
from util.project import project
from util.auth import get_service
from util.bigquery import bigquery_date, query
from util.regexp import parse_yyyymmdd

#DAY_OFFSET = 24 * 60 * 60 * 1000


def _retry(job, key=None, retries=10, wait=30):
  try:
    data = job.execute()
    #pprint.PrettyPrinter().pprint(data)
    return data[key] if key else data
  except http.HttpError, e:
    if project.verbose: print str(e) 
    if e.resp.status in [403, 429, 500, 503]:
      if retries > 0:
        time.sleep(wait)
        return _retry(job, key, retries - 1, wait * 2)
      elif json.loads(e.content)['error']['code'] == 409:
        pass  # already exists ( ignore )
      else:
        raise


def _process_filters(partners, advertisers, filters):
  structures = []

  for p in (partners or []):
    structures.append({
      'type':'FILTER_PARTNER',
      'value':p
    })

  for a in (advertisers or []):
    structures.append({
      'type':'FILTER_ADVERTISER',
      'value':a
    })

  for f in (filters or []):
    if isinstance(f['value'], basestring) and f['value'].startswith('SELECT '):
      # TODO: THIS VIOLATES THE RULE OF NO PROJECT REFERENCES HERE
      # this is a complex job and it should really be a job ( audiencepro/run.py )
      # inside that job consttruct the filters form the query, pass them into report_get already built
      # then get the resulting report data
      # thats how we avoid turning everything into spaghetti code ( its a way to keep things clean )
      for item in query(f['value']):
        structures.append({
          'type':f['type'],
          'value':item[0]
        })
    else:
      structures.append({
        'type':f['type'],
        'value':f['value']
      })

  return structures

#def report_time(day):
#  return long((datetime.combine(day, localtime(0, 0, 0)) +
#               TIMEZONE_OFFSET).strftime('%s000'))

def report_get(auth, title):
  service = get_service('doubleclickbidmanager', 'v1', auth)
  job = service.queries().listqueries()
  result = _retry(job)
  return ([query for query in result.get('queries', []) if query['metadata']['title'] == title ] or [None])[0]


def report_create(auth, title, report_type, partners, advertisers, filters, dimensions, metrics, data_range):
  service = get_service('doubleclickbidmanager', 'v1', auth)
  report = report_get(auth, title)
  #pprint.PrettyPrinter().pprint(report)

  if report is None:
    if project.verbose: print 'DBM Report Create:', title

    body = {
      'kind': 'doubleclickbidmanager#query',
      'timezoneCode': 'America/Los_Angeles',
      'metadata': {
        'title': title,
        'dataRange': data_range,
        'format': 'CSV',
        'sendNotification': False,
      },
      'params': {
        'filters': _process_filters(partners, advertisers, filters),
        'groupBys': dimensions or [
            'FILTER_DATE', 
            'FILTER_ADVERTISER', 
            'FILTER_LINE_ITEM',
            'FILTER_INSERTION_ORDER', 
            'FILTER_CREATIVE_ID',
            'FILTER_ADVERTISER_CURRENCY', 
            'FILTER_MOBILE_DEVICE_TYPE'
          ],
        'includeInviteData': False,
        'metrics': metrics or ['METRIC_REVENUE_ADVERTISER'],
        'type': report_type
      },
      'schedule': {
        'endTimeMs': long((time.time() + (365 * 24 * 60 * 60)) * 1000), # 1 year in future
        'frequency': 'DAILY',
        'nextRunMinuteOfDay':15,
        'nextRunTimezoneCode': 'America/Los_Angeles'
      },
    }

    #pprint.PrettyPrinter().pprint(body)
    job = service.queries().createquery(body=body)
    _retry(job)

    report = report_get(auth, title)

  return report


def report_run(auth, report):
  if project.verbose: print 'DBM Report Run:', report['metadata']['title']

  service = get_service('doubleclickbidmanager', 'v1', auth)
  body = {
    "dataRange":report['metadata']['dataRange'],
    "timezoneCode":report['schedule']['nextRunTimezoneCode']
  }
  job = service.queries().runquery(queryId=report['queryId'], body=body)
  _retry(job)
  return report_get(auth, report['metadata']['title'])


#def report_file(auth, query_id, day):
#  if project.verbose:
#    print 'DBM Report Get', query_id
#
#  service = get_service('doubleclickbidmanager', 'v1', auth)
#
#  #pprint.PrettyPrinter(depth=20).pprint(service.queries().getquery(queryId=query_id).execute())
#  #exit()
#
#  # attempt to get already run report
#  job = service.reports().listreports(queryId=query_id)
#  for report in _retry(job, 'reports'):
#    #print 'ON', day
#    #print report['metadata']['reportDataStartTimeMs'], report['metadata']['reportDataEndTimeMs']
#    #print day
#    #print 'START', report_time(day),  report['metadata']['reportDataStartTimeMs'], (report_time(day) - long(report['metadata']['reportDataStartTimeMs'])) / 1000 / 60 / 60
#    if report_time(day) == long(report['metadata']['reportDataEndTimeMs']):
#      filename = 'DBM_Report_%s.csv' % str(day)
#      if report['metadata']['status']['state'] == 'DONE':
#        # report is done and downloaded
#        if project.verbose:
#          print 'Report Done'
#        return filename, BytesIO( urllib2.urlopen(report['metadata']['googleCloudStoragePath']).read())
#      else:
#        # report is scheduled but not done
#        if project.verbose:
#          print 'Report Running'
#        return filename, True
#
#  # no report matching this day
#  if project.verbose: print 'No Report'
#
#  return None, None


#def report_run(auth, query_id, day, data_range='CUSTOM_DATES'):
#  filename, report = report_file(auth, query_id, day)
#
#  # if no report scheduled, set one
#  if report is None:
#    service = get_service('doubleclickbidmanager', 'v1', auth)
#    body = {
#     'dataRange': data_range,
#     'timezoneCode': 'America/Los_Angeles',
#    }
#
#    if data_range == 'CUSTOM_DATES':
#      body['reportDataStartTimeMs'] = report_time(day) + DAY_OFFSET
#      body['reportDataEndTimeMs'] = report_time(day) + DAY_OFFSET
# 
#    job = service.queries().runquery(queryId=query_id, body=body)
#    _retry(job)
#    report = True
#
#  # wait for report to finish
#  wait_interval = 32
#  while report == True:
#    if project.verbose: print 'Wait For DBM Report'
#    time.sleep(wait_interval)
#    filename, report = report_file(auth, query_id, day)
#    wait_interval = wait_interval * 2
#
#  # report is a binary
#  return filename, report


def report_download(auth, title, report_type, partners, advertisers, filters, dimensions, metrics, data_range):
  if project.verbose: print 'DBM Report Download:', title

  if report_type is None: report = report_get(auth, title)
  else: report = report_create(auth, title, report_type, partners, advertisers, filters, dimensions, metrics, data_range)

  # no report found
  if report is None:
    if project.verbose: print 'DBM Report Not Found:', title
    return None, None

  # report exists
  else:
    # ensure report has at least one file created
    if report['metadata']['googleCloudStoragePathForLatestReport'] == '':
      report = report_run(auth, report)
      # if report is in progress wait for it to finish
      while report['metadata']['googleCloudStoragePathForLatestReport'] == '':
        if project.verbose: print 'DBM Report Running:', title
        time.sleep(30)
        report = report_get(auth, title)

    # download the latest report file
    filename = '%s_%s.%s' % (title, parse_yyyymmdd(report['metadata']['googleCloudStoragePathForLatestReport']), report['metadata']['format'].lower())
    return filename, BytesIO(urllib2.urlopen(report['metadata']['googleCloudStoragePathForLatestReport']).read())


#def report_get(auth,
#               title,
#               report_type='TYPE_CROSS_PARTNER',
#               partners=[],
#               advertisers=[],
#               filters=[],
#               dimensions=[],
#               metrics=[],
#               delete_report=False,
#               data_range='CUSTOM_DATES',
#               day=date.today()):
#
#  if project.verbose:
#    print 'Getting report %s' % title
#
#  query = report_create(auth, title, report_type, partners, advertisers, filters, dimensions, metrics, data_range, day)
#  result = report_run(auth, query['queryId'], day, data_range)
#
#  if delete_report:
#    service = get_service('doubleclickbidmanager', 'v1', auth)
#    job = service.queries().deletequery(queryId=query_id)
#    _retry(job)
#
#  return result

def report_to_rows(report):
  return list(csv.reader(report)) if report else []


def report_clean(rows, day=None, datastudio=False, nulls=False):
  if project.verbose: print 'DBM Report Clean'

  # remove summary data at end of dbm report
  delete_summary = True
  while (delete_summary and rows):
    line = rows.pop()
    delete_summary = not (line[0:3] == ['', '', ''] or line[0:3] == [])

  # remove last row of DBM report ( sum row )
  rows.pop()

  # change date to datastudio format
  if datastudio:
    rows[0][0] = 'Report_Day'
    for i in range(1, len(rows)):
      rows[i][0] = rows[i][0].replace('/', '')

  # remove unknown columns ( which throw off schema on import types )
  if nulls:
    for i in range(len(rows)):
      rows[i] = ['' if cell.strip() == 'Unknown' else cell for cell in rows[i]]

  # add a date column to the csv
  if rows and day:
    rows[0].insert(0, 'Report_Day')
    for line in rows[1:]:
      line.insert(0, bigquery_date(day))

  return rows


def report_to_csv(rows):
  csv_string = StringIO()
  writer = csv.writer(csv_string, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for row_number, row in enumerate(rows):
    try:
      writer.writerow(row)
    except Exception, e:
      print 'Error:', row_number, str(e), row
  csv_string.seek(0)  # important otherwise contents is zero
  return csv_string


def report_list(auth, title=None):
  service = get_service('doubleclickbidmanager', 'v1', auth)
  job = service.queries().listqueries()
  for query in _retry(job, 'queries'):
    if not title or query['metadata']['title'] == title:
      print(json.dumps(query, indent=2))
