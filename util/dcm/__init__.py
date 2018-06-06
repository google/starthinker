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

from setup import INTERNAL_MODE, EXECUTE_PATH, BUFFER_SCALE
from util import flag_last
from util.project import project
from util.auth import get_service
from util.storage import media_download
from util.csv import column_header_sanitize
from util.dcm.schema.Lookup import DCM_Field_Lookup


if INTERNAL_MODE:
  # fetch discovery uri using: wget https://www.googleapis.com/discovery/v1/apis/dfareporting/internalv3.0/rest > util/dcm/internalv30_uri.json
  API_VERSION = 'internalv3.0'
  API_URI = '%sutil/dcm/internalv30_uri.json' % EXECUTE_PATH
else:
  API_VERSION = 'v3.0'
  API_URI = None

DCM_CHUNK_SIZE = int(200 * 1024000 * BUFFER_SCALE) # 200MB minimum recommended by docs * scale in setup.py
DCM_CONVERSION_SIZE = 1000


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


def get_profile_id(auth, account_id):
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  for p in _retry(service.userProfiles().list())['items']:
    if INTERNAL_MODE: return int(p['profileId'])
    elif int(p['accountId']) == account_id: return int(p['profileId'])
  raise Exception('Add your user profile to DCM account %s.' % account_id)


def get_account_name(auth, account_id):
  account_id, subaccount_id, profile_id = parse_account(auth, account_id)
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  response = _retry(service.accounts().get(id=account_id, profileId=profile_id))
  return response["name"]


# if id has a sub account in the form of [account_id:subaccount_id@profile_id] then split them
def parse_account(auth, account_id):
  network_id = account_id
  advertiser_id = None
  profile_id = None

  # if exists, get profile from end
  try: network_id, profile_id = network_id.split('@', 1)
  except: profile_id = None

  # if exists, get avertiser from end
  try: network_id, advertiser_id = network_id.split(':', 1)
  except: pass

  # if network or advertiser, convert to integer
  if network_id is not None: network_id = int(network_id)
  if advertiser_id is not None: advertiser_id = int(advertiser_id)

  # if no profile, fetch a default one ( returns as int )
  if profile_id is None: profile_id = get_profile_id(auth, network_id)

  return network_id, advertiser_id, profile_id


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


def report_get(auth, account_id, report_id = None, name=None):
  account_id, subaccount_id, profile_id = parse_account(auth, account_id)
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  report = None

  if name:
    next_page = None
    while next_page != '' and report is None:
      if INTERNAL_MODE: response = _retry(service.reports().list(accountId=account_id, profileId=profile_id, pageToken=next_page))
      else: response = _retry(service.reports().list(profileId=profile_id, pageToken=next_page))
      next_page = response['nextPageToken']
      for r in response['items']:
        if r['name'] == name: 
          report = r
          break
  elif report_id:
    if INTERNAL_MODE: response = _retry(service.reports().get(accountId=account_id, profileId=profile_id, reportId=report_id))
    else: response = _retry(service.reports().get(profileId=profile_id, reportId=report_id))
    pprint.PrettyPrinter().pprint(response)
    
  return report


def report_delete(auth, account_id, report_id = None, name=None):
  account_id, subaccount_id, profile_id = parse_account(auth, account_id)
  report = report_get(auth, account_id, report_id, name)
  if report:
    service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
    if INTERNAL_MODE: _retry(service.reports().delete(accountId=account_id, profileId=profile_id, reportId=report['id']))
    else: _retry(service.reports().delete(profileId=profile_id, reportId=report['id']))
  else:
    if project.verbose: print 'DCM DELETE: No Report'


def report_create(auth, account_id, name, config):
  account_id, subaccount_id, profile_id = parse_account(auth, account_id)
  report = report_get(auth, account_id, name=name)

  if report is None:
    service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)

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
    if INTERNAL_MODE: report = _retry(service.reports().insert(accountId=account_id, profileId=profile_id, body=body))
    else: report = _retry(service.reports().insert(profileId=profile_id, body=body))

    # run the report
    if INTERNAL_MODE: _retry(service.reports().run(accountId=account_id, profileId=profile_id, reportId=report['id']))
    else: _retry(service.reports().run(profileId=profile_id, reportId=report['id']))

  return report


# timeout is in minutes ( retries will happen at 1 minute interval, default total time is 60 minutes )
def report_fetch(auth, account_id, report_id=None, name=None, timeout = 60):
  if project.verbose: print 'DCM REPORT FILE', report_id or name

  if report_id is None:
    report = report_get(auth, account_id, name=name)
    report_id = report['id']

  running = False

  # zero means run once
  while timeout >= 0: 

    # loop all files recent to oldest looking for valid one
    for file_json in report_files(auth, account_id, report_id):
      #pprint.PrettyPrinter().pprint(file)

      # still running ( wait for timeout )
      if file_json['status'] == 'PROCESSING':
        running = True
        if timeout > 0: break # go to outer loop wait

      # ready for download ( return file )
      elif file_json['status'] == 'REPORT_AVAILABLE':
        if project.verbose: print 'REPORT DONE'
        return file_json
       
      # cancelled or failed ( go to next file in loop )

    # if no report running ( skip wait )
    if not running: break

    # sleep a minute
    if timeout > 0:
      if project.verbose: print 'WAITING MINUTES', timeout
      sleep(60)

    # advance timeout 
    timeout -= 1

  # if here, no file is ready, return status
  if project.verbose: print 'NO REPORT FILES'
  return running


def report_file(auth, account_id, report_id=None, name=None, timeout=60, chunksize=None):
  account_id, subaccount_id, profile_id = parse_account(auth, account_id)
  file_json = report_fetch(auth, account_id, report_id, name, timeout)

  if file_json == False:
    return None, None
  elif file_json == True:
    return 'report_running.csv', None
  else:
    service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
    filename = '%s_%s.csv' % (file_json['fileName'], file_json['dateRange']['endDate'].replace('-', ''))

    # streaming
    if chunksize:
      return filename, media_download(service.files().get_media(reportId=file_json['reportId'], fileId=file_json['id']), chunksize)

    # single object
    else:
      return filename, StringIO(_retry(service.files().get_media(reportId=file_json['reportId'], fileId=file_json['id'])))

       
def report_list(auth, account):
  account_id, subaccount_id, profile_id = parse_account(auth, account)
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  next_page = None
  while next_page != '':
    if INTERNAL_MODE: response = _retry(service.reports().list(accountId=account_id, profileId=profile_id, pageToken=next_page))
    else: _retry(service.reports().list(profileId=profile_id, pageToken=next_page))
    next_page = response['nextPageToken']
    for report in response['items']:
      yield report


def report_files(auth, account, report_id):
  account_id, subaccount_id, profile_id = parse_account(auth, account)
  service = get_service('dfareporting', API_VERSION, auth)
  next_page = None
  while next_page != '':
    if INTERNAL_MODE: response = _retry(service.reports().files().list(accountId=account_id, profileId=profile_id, reportId=report_id, pageToken=next_page))
    else: response = _retry(service.reports().files().list(profileId=profile_id, reportId=report_id, pageToken=next_page))
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


def report_schema(headers):
  schema = []

  for header_name in headers:
    header_sanitized = column_header_sanitize(header_name)

    # first try exact match
    header_type = DCM_Field_Lookup.get(header_sanitized)

    # second try to match end for custom field names ( activity reports )
    if header_type is None:
      for field_name, field_type in DCM_Field_Lookup.items():
        if header_sanitized.endswith('_' + field_name):
          header_type = field_type
          break

    # finally default it to STRING   
    if header_type is None: header_type = 'STRING'

    schema.append({ 
      'name':header_sanitized,
      'type':header_type,
      'mode':'NULLABLE'
    })

  return schema


def report_clean(rows, datastudio=False):
  if project.verbose: print 'DCM REPORT CLEAN'

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
      if datastudio: row = [column_header_sanitize(cell) for cell in row]
      
    # check if data studio formatting is applied
    if datastudio and date is not None:
      row[date] = 'Report_Day' if first else row[date].replace('-', '')

    # remove not set columns ( which throw off schema on import types )
    row = ['' if cell.strip() == '(not set)' else cell for cell in row]

    # return the row
    yield row

    # not first row anymore
    first = False


#filed: encryptedUserId, encryptedUserIdCandidates[], gclid, mobileDeviceId

def conversions_upload(auth, account_id, floodlight_activity_id, conversion_type, conversion_rows, encryption_entity=None, update=False):
  account_id, subaccount_id, profile_id = parse_account(auth, account_id)

  service = get_service('dfareporting', API_VERSION, auth)
  if INTERNAL_MODE: response = _retry(service.floodlightActivities().get(accountId=account_id, profileId=profile_id, id=floodlight_activity_id))
  else: response = _retry(service.floodlightActivities().get(profileId=profile_id, id=floodlight_activity_id))
  
  # upload in batch sizes of DCM_CONVERSION_SIZE
  row_count = 0
  row_buffer = []
  for is_last, row in flag_last(conversion_rows):
    row_buffer.append(row)

    if is_last or len(row_buffer) == DCM_CONVERSION_SIZE:
          
      if project.verbose: print 'CONVERSION UPLOADING ROWS: %d - %d' % (row_count,  row_count + len(row_buffer))

      body = {
        'conversions': [{
          'floodlightActivityId': floodlight_activity_id,
          'floodlightConfigurationId': response['floodlightConfigurationId'],
          'ordinal': row[0],
          'timestampMicros': row[1],
          'quantity':1,
          'value':0.0,
          conversion_type: row[2],
        } for row in row_buffer]
      }

      if encryption_entity: body['encryptionInfo'] = encryption_entity

      if update:
        if INTERNAL_MODE: results = _retry(service.conversions().batchupdate(accountId=account_id, profileId=profile_id, body=body))
        else: results = _retry(service.conversions().batchupdate(profileId=profile_id, body=request_body))
      else:
        if INTERNAL_MODE: results = _retry(service.conversions().batchinsert(accountId=account_id, profileId=profile_id, body=body))
        else: results = _retry(service.conversions().batchinsert(profileId=profile_id, body=request_body))

      # stream back satus
      for status in results['status']: yield status 

      # clear the buffer
      row_count += len(row_buffer)
      row_buffer = []
