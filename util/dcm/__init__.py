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

#https://developers.google.com/doubleclick-advertisers/v3.0/reports/get

import pprint
import csv
import re
import json
from StringIO import StringIO
from types import GeneratorType
from time import sleep
from datetime import date, timedelta

from googleapiclient.errors import HttpError

from util.project import project
from util.auth import get_service
from util.storage import media_download


API_VERSION = 'internalv3.0'
RE_HUMAN = re.compile('[^0-9a-zA-Z]+')

# if id has a sub account in the form of [account_id:subaccount_id] then split them
def parse_account(account_id):
  a_id = account_id
  s_id = None
  try: a_id, s_id = account_id.split(':', 1)
  except: pass
  return a_id, s_id


def _retry(job, retries=10, wait=5):
  try:
    data = job.execute()
    #pprint.PrettyPrinter().pprint(data)
    return data 
  except HttpError, e:
    if project.verbose: print str(e)
    if e.resp.status in [403, 429, 500, 503]:
      if retries > 0:
        sleep(wait)
        if project.verbose: print 'DCM RETRY', retries
        return _retry(job, retries - 1, wait * 2)
      elif json.loads(e.content)['error']['code'] == 409:
        pass # already exists ( ignore )
      else:
        raise


def get_body_floodlight(report, advertiser=None):
  return {
    "floodlightCriteria": {
      "dateRange": {
        "kind": "dfareporting#dateRange",
        "relativeDateRange": report.get('relativeDateRange', 'LAST_7_DAYS'),
      },
      "dimensions": [
        {
          "kind": "dfareporting#sortedDimension",
          "name": "dfa:" + d
        }
        for d in report.get('dimensions', [''])
      ],
      "metricNames": [
        "dfa:" + m
        for m in report.get('metrics', ['impressions', 'clicks'])
      ],
      "floodlightConfigId": {
        "kind": "dfareporting#dimensionValue",
        "dimensionName": "dfa:floodlightConfigId",
        "matchType": "EXACT",
        "value": report['floodlightConfigId']
      },
      "reportProperties": {
        "includeUnattributedCookieConversions": report.get('UnattributedCookieConversions', False),
        "includeUnattributedIPConversions": report.get('UnattributedIPConversions', False)
      }
    }
  }

def get_body_standard(report, advertiser=None):
  return {
    "criteria": {
      "dateRange": {
        "kind": "dfareporting#dateRange",
        "relativeDateRange": report.get('relativeDateRange', 'LAST_7_DAYS'),
      },
      "dimensions": [
        {
          "kind": "dfareporting#sortedDimension",
          "name": "dfa:" + d
        }
        for d in report.get('dimensions', [''])
      ],
      "metricNames": [
        "dfa:" + m
        for m in report.get('metrics', ['impressions', 'clicks'])
      ]
    }
  }


def get_profile_id(auth):
  service = get_service('dfareporting', API_VERSION, auth)
  return ([profile['profileId'] for profile in _retry(service.userProfiles().list())['items']] or [None])[0]


def report_get(auth, account_id, report_id = None, name=None):
  account_id, subaccount_id = parse_account(account_id)
  service = get_service('dfareporting', API_VERSION, auth)
  profile_id = get_profile_id(auth)
  report = None

  if name:
    next_page = None
    while next_page != '' and report is None:
      response = _retry(service.reports().list(accountId=account_id, profileId=profile_id, pageToken=next_page))
      next_page = response['nextPageToken']
      for r in response['items']:
        if r['name'] == name: 
          report = r
          break
  elif report_id:
    response = _retry(service.reports().get(accountId=account_id, profileId=profile_id, reportId=report_id))
    pprint.PrettyPrinter().pprint(response)
    
  return report


def report_delete(auth, account_id, report_id = None, name=None):
  account_id, subaccount_id = parse_account(account_id)
  report = report_get(auth, account_id, report_id, name)
  if report:
    service = get_service('dfareporting', API_VERSION, auth)
    profile_id = get_profile_id(auth)
    _retry(service.reports().delete(accountId=account_id, profileId=profile_id, reportId=report['id']))
  else:
    if project.verbose: print 'DCM DELETE: No Report'


def report_create(auth, account_id, name, config):
  account_id, subaccount_id = parse_account(account_id)
  report = report_get(auth, account_id, name=name)

  if report is None:
    service = get_service('dfareporting', API_VERSION, auth)
    profile_id = get_profile_id(auth)

    body = { 
      'kind':'dfareporting#report',
      'type':config.get('type', 'STANDARD').upper(),
      'name':name,
      'format':config.get('format', 'CSV'),
      'accountId':account_id,
      'delivery': {
        'emailOwner':False,
        'emailOwnerDeliveryType':'LINK'
      },
      'schedule': {
        'active':True,
        'repeats':'DAILY',
        'every': 1,
        'startDate':str(date.today()),
        'expirationDate':str((date.today() + timedelta(days=365))),
      }
    } 

    if body['type'] == 'STANDARD': body.update(get_body_standard(config))
    elif body['type'] == 'FLOODLIGHT': body.update(get_body_floodlight(config))

    if subaccount_id:
       body['criteria']['dimensionFilters'] = body['criteria'].get('dimensionFilters', []) + [{
         'kind':'dfareporting#dimensionValue',
         'dimensionName':'dfa:advertiser',
         'id':subaccount_id,
         'matchType':'EXACT'
       }]

    #pprint.PrettyPrinter().pprint(body)

    # create the report
    report = _retry(service.reports().insert(accountId=account_id, profileId=profile_id, body=body))

    # run the report
    _retry(service.reports().run(accountId=account_id, profileId=profile_id, reportId=report['id']))

  return report


# timeout is in minutes ( retries will happen at 5 minute interval, default total time is 60 minutes )
def report_fetch(auth, account_id, report_id=None, name=None, timeout = 60):
  account_id, subaccount_id = parse_account(account_id)
  if project.verbose: print 'DCM Report File', report_id or name
  profile_id = get_profile_id(auth)

  if report_id is None:
    report = report_get(auth, account_id, name=name)
    #pprint.PrettyPrinter().pprint(report)
    report_id = report['id']

  service = get_service('dfareporting', API_VERSION, auth)

  while timeout >= 0: # allow zero to execute at least once
    # advance timeout first ( if = 0 then exit condition met but already in loop, if > 0 then will run into sleep )
    timeout -= 1

    response = _retry(service.reports().files().list(accountId=account_id, profileId=profile_id, reportId=report_id, maxResults=1))
    file = response['items'][0] if len(response['items']) > 0 else None
    #pprint.PrettyPrinter().pprint(file)

    if file:
      # file exists ( return it success )
      if file['status'] == 'REPORT_AVAILABLE':
        if project.verbose: print 'Report Done'
        return file

      # report is running ( return only if timeout is exhausted )
      else: 
        if project.verbose: print 'Report Running'
        if timeout < 0: return True

    # no report ( break out of loop it will never finish )
    else:
      return False

    # sleep a minute
    sleep(60)

# NOT A THING IN DCM - FIX
#def report_bigquery(auth, account_id, report_id, name, dataset, table, schema=[], timeout=60):
#  storage_path = report_fetch(auth, account_id, report_id, name, timeout)
#  if storage_path not in (True, False):
#    #print project.id, dataset, table, storage_path
#    storage_to_table(auth, project.id, dataset, table, storage_path, schema, 1 if schema else 0)


def report_file(auth, account_id, report_id=None, name=None, timeout=60, chunksize=None):
  account_id, subaccount_id = parse_account(account_id)
  file = report_fetch(auth, account_id, report_id, name, timeout)

  if file == False:
    return None, None
  elif file == True:
    return 'report_running.csv', None
  else:
    service = get_service('dfareporting', API_VERSION, auth)
    filename = '%s_%s_%s.csv' % (file['reportId'] , file['id'], file['lastModifiedTime'])

    # streaming
    if chunksize:
      return filename, media_download(service.files().get_media(reportId=file['reportId'], fileId=file['id']), chunksize)

    # single object
    else:
      return filename, StringIO(_retry(service.files().get_media(reportId=file['reportId'], fileId=file['id'])))

       
def report_list(auth, account):
  service = get_service('dfareporting', API_VERSION, auth)
  profile = get_profile_id(auth)
  next_page = None
  while next_page != '':
    response = _retry(service.reports().list(accountId=args.account, profileId=profile, pageToken=next_page))
    next_page = response['nextPageToken']
    for report in response['items']:
      yield report


def report_to_rows(report):
  # if reading from stream
  if type(report) is GeneratorType:
    leftovers = ''
    for chunk in report:
      data, extra = chunk.read().rsplit('\n', 1)
      for row in csv.reader(StringIO(leftovers + data)):
        yield row
      leftovers = extra

  # if reading from buffer
  else:
    for row in csv.reader(report) if report else []:
      yield row


def report_clean(rows, datastudio=False):
  if project.verbose: print 'DCM Report Clean'

  first = True
  last = False
  date = None

  # find start of report
  for row in rows:
    if row and row[0] == 'Report Fields': break

  # process the report
  for row in rows:
    # quit if empty report
    if 'No data returned by the reporting service.' in row: break

    # stop parsing if end of data
    if not row or row[0] == 'Grand Total:': break

    # find 'Date' column if it exists
    if first: 
      try: date = row.index('Date')
      except ValueError: pass
      if datastudio: row = [RE_HUMAN.sub('_', column) for column in row]
      
    # check if data studio formatting is applied
    if datastudio and date is not None:
      row[date] = 'Report_Day' if first else row[date].replace('-', '')

    # return the row
    yield row

    # not first row anymore
    first = False
