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

import pprint
import csv
import re
import json
from time import sleep
from StringIO import StringIO
from types import GeneratorType
from datetime import date, timedelta

from googleapiclient.errors import HttpError

from starthinker.config import INTERNAL_MODE, EXECUTE_PATH, BUFFER_SCALE
from starthinker.util import flag_last
from starthinker.util.project import project
from starthinker.util.auth import get_service
from starthinker.util.google_api import API_Retry
from starthinker.util.storage import media_download
from starthinker.util.csv import column_header_sanitize
from starthinker.util.dcm.schema.Lookup import DCM_Field_Lookup


if INTERNAL_MODE:
  # fetch discovery uri using: wget https://www.googleapis.com/discovery/v1/apis/dfareporting/internalv3.2/rest > util/dcm/internalv32_uri.json
  API_VERSION = 'internalv3.2'
  API_URI = '%sutil/dcm/internalv32_uri.json' % EXECUTE_PATH
else:
  API_VERSION = 'v3.2'
  API_URI = None

DCM_CHUNK_SIZE = int(200 * 1024000 * BUFFER_SCALE) # 200MB minimum recommended by docs * scale in config.py
DCM_CONVERSION_SIZE = 1000


def get_profile_for_api(auth, account_id):
  """Return a DCM profile ID for the currently supplied credentials.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/userProfiles/get

  Handles cases of superuser, otherwise chooses the first matched profile.
  Allows DCM jobs to only specify account ID, which makes jobs more portable
  between accounts.

  Args:
    * auth: (string) Either user or service.
    * account_id: (int) Account number for which report is retrieved.

  Returns:
    * Is Superuser ( bool ): True if superuser account
    * Profile ID ( int ): profile id to be used to make API call
       
  Raises:
    * If current credentials do not have a profile for this account.

  """

  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)

  profile_admin = None
  profile_network = None

  for p in API_Retry(service.userProfiles().list())['items']:
    p_id = int(p['profileId'])
    a_id = int(p['accountId'])

    # take the first profile for admin
    if '@dcm' in p['userName']: profile_admin = p_id
    #elif '@dfa' in p['userName']: profile_admin = p_id
    elif a_id == 2515: profile_admin = p_id

    # try to find a network profile if exists
    if a_id == account_id: 
      profile_network = p_id
      break

  if profile_admin: return True, profile_admin
  elif profile_network: return False, profile_network
  else: raise Exception('Add your user profile to DCM account %s.' % account_id)
    

def get_profile_id(auth, account_id):
  """Legacy function replaced by get_profile_for_api(...).
  """
  return get_profile_for_api(auth, account_id)[1]


def account_profile_kwargs(auth, account, **kwargs):
  account_id, ignore, profile_id = parse_account(auth, account)
  if INTERNAL_MODE: kwargs['accountId']= account_id
  kwargs['profileId']= profile_id
  return kwargs


def get_account_name(auth, account):
  """ Return the name of a DCM account given the account ID.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.

  Returns:
    * Profile ID.
       
  Raises:
    * If current credentials do not have a profile for this account.

  """

  account_id, advertiser_ids, profile_id = parse_account(auth, account)
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  response = API_Retry(service.accounts().get(id=account_id, profileId=profile_id))
  return response["name"]


def parse_account(auth, account):
  """ Breaks a [account:advertiser@profile] string into parts if supplied.

  This function was created to accomodate supplying advertiser and profile information
  as a single token.  It needs to be refactored as this approach is messy.

  Possible variants include:
    * [account:advertiser@profile]
    * [account:advertiser]
    * [account@profile]

  Args:
    * auth: (string) Either user or service.
    * account: (string) A string represeting [account:advertiser@profile]

  Returns:
    * ( network_id, advertiser_ids, profile_id) after parsing the account token.

  """

  network_id = account
  advertiser_ids = None
  profile_id = None

  # if exists, get profile from end
  try: network_id, profile_id = network_id.split('@', 1)
  except: profile_id = None

  # if exists, get avertiser from end
  try: network_id, advertiser_ids = network_id.split(':', 1)
  except: pass

  # if network or advertiser, convert to integer
  if network_id is not None: network_id = int(network_id)
  if advertiser_ids is not None: advertiser_ids = [int(advertiser_id.strip()) for advertiser_id in advertiser_ids.split(',')]

  # if no profile, fetch a default one ( returns as int )
  if profile_id is None: profile_id = get_profile_id(auth, network_id)

  return network_id, advertiser_ids, profile_id


# DEPRECATED DO NOT USE
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

# DEPRECATED DO NOT USE
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


def report_get(auth, account, report_id = None, name=None):
  """ Returns the DCM JSON definition of a report based on name or ID.
 
  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/get

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * JSON definition of report.

  """

  account_id, advertiser_ids, profile_id = parse_account(auth, account)
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  report = None

  if name:
    next_page = None
    while next_page != '' and report is None:
      if INTERNAL_MODE: response = API_Retry(service.reports().list(accountId=account_id, profileId=profile_id, pageToken=next_page))
      else: response = API_Retry(service.reports().list(profileId=profile_id, pageToken=next_page))
      next_page = response['nextPageToken']
      for r in response['items']:
        if r['name'] == name: 
          report = r
          break
  elif report_id:
    if INTERNAL_MODE: response = API_Retry(service.reports().get(accountId=account_id, profileId=profile_id, reportId=report_id))
    else: response = API_Retry(service.reports().get(profileId=profile_id, reportId=report_id))
    #pprint.PrettyPrinter().pprint(response)
    
  return report


def report_delete(auth, account, report_id = None, name=None):
  """ Deletes a DCM report based on name or ID.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/delete

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * None

  """

  account_id, advertiser_ids, profile_id = parse_account(auth, account)
  report = report_get(auth, account, report_id, name)
  if report:
    service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
    if INTERNAL_MODE: API_Retry(service.reports().delete(accountId=account_id, profileId=profile_id, reportId=report['id']))
    else: API_Retry(service.reports().delete(profileId=profile_id, reportId=report['id']))
  else:
    if project.verbose: print 'DCM DELETE: No Report'


def report_build(auth, account, body):
  """ Creates a DCM report given a JSON definition.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/insert

  The body JSON provided will have the following fields overriden:
    * accountId - supplied as a parameter in account token.
    * ownerProfileId - determined from the current credentials.
    * advertiser_ids - supplied as a parameter in account token.
  
  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * body: (json) As defined in: https://developers.google.com/doubleclick-advertisers/v3.2/reports#resource

  Returns:
    * JSON definition of report created or existing.

  """

  report = report_get(auth, account, name=body['name'])

  if report is None:
    account_id, advertiser_ids, profile_id = parse_account(auth, account)
    service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)

    # add the account id to the body
    body['accountId'] = account_id
    body['ownerProfileId'] = profile_id

    # add advertisers to the body
    if advertiser_ids:
       body['criteria']['dimensionFilters'] = body['criteria'].get('dimensionFilters', []) + [{
         'kind':'dfareporting#dimensionValue',
         'dimensionName':'dfa:advertiser',
         'id':advertiser_id,
         'matchType':'EXACT'
       } for advertiser_id in advertiser_ids]

    #pprint.PrettyPrinter().pprint(body)

    # create the report
    if INTERNAL_MODE: report = API_Retry(service.reports().insert(accountId=account_id, profileId=profile_id, body=body))
    else: report = API_Retry(service.reports().insert(profileId=profile_id, body=body))

    # run the report
    if INTERNAL_MODE: API_Retry(service.reports().run(accountId=account_id, profileId=profile_id, reportId=report['id']))
    else: API_Retry(service.reports().run(profileId=profile_id, reportId=report['id']))

  else:
    if project.verbose: print 'DCM Report Exists:', body['name']

  return report


# DEPRECATED DO NOT USE
def report_create(auth, account, name, config):
  account_id, advertiser_ids, profile_id = parse_account(auth, account)
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

    if advertiser_ids:
       body['criteria']['dimensionFilters'] = body['criteria'].get('dimensionFilters', []) + [{
         'kind':'dfareporting#dimensionValue',
         'dimensionName':'dfa:advertiser',
         'id':advertiser_id,
         'matchType':'EXACT'
       } for advertiser_id in advertiser_ids]

    #pprint.PrettyPrinter().pprint(body)

    # create the report
    if INTERNAL_MODE: report = API_Retry(service.reports().insert(accountId=account_id, profileId=profile_id, body=body))
    else: report = API_Retry(service.reports().insert(profileId=profile_id, body=body))

    # run the report
    if INTERNAL_MODE: API_Retry(service.reports().run(accountId=account_id, profileId=profile_id, reportId=report['id']))
    else: API_Retry(service.reports().run(profileId=profile_id, reportId=report['id']))

  return report


def report_fetch(auth, account, report_id=None, name=None, timeout = 60):
  """ Retrieves most recent DCM file JSON by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/files/get

  Timeout is in minutes ( retries will happen at 1 minute interval, default total time is 60 minutes )

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.

  Returns:
    * Report JSON if report exists and is ready. 
    * True if report is in progress but not ready.
    * False if report does not exist.

  """

  if project.verbose: print 'DCM REPORT FILE', report_id or name

  if report_id is None:
    report = report_get(auth, account, name=name)
    report_id = report['id']

  running = False

  # zero means run once
  while timeout >= 0: 

    # loop all files recent to oldest looking for valid one
    for file_json in report_files(auth, account, report_id):
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


def report_file(auth, account, report_id=None, name=None, timeout=60, chunksize=DCM_CHUNK_SIZE):
  """ Retrieves most recent DCM file by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/files/get

  Timeout is in minutes ( retries will happen at 1 minute interval, default total time is 60 minutes )
  If chunksize is set to 0 then the whole file is downloaded at once.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.
    * chunksize: (int) number of bytes to download at a time, for memory constrained systems.

  Returns:
    * (filename, iterator) if file exists and is ready to download in chunks.
    * (filename, file) if file exists and chunking is off.
    * ('report_running.csv', None) if report is in progress.
    * (None, None) if file does not exist.

  """

  account_id, advertiser_id, profile_id = parse_account(auth, account)
  file_json = report_fetch(auth, account, report_id, name, timeout)

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
      return filename, StringIO(API_Retry(service.files().get_media(reportId=file_json['reportId'], fileId=file_json['id'])))

       
def report_list(auth, account):
  """ Lists all the DCM report configurations for an account given the current credentials.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/list

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.

  Returns:
    * Iterator of JSONs.

  """

  account_id, advertiser_id, profile_id = parse_account(auth, account)
  service = get_service('dfareporting', API_VERSION, auth, uri_file=API_URI)
  next_page = None
  while next_page != '':
    if INTERNAL_MODE: response = API_Retry(service.reports().list(accountId=account_id, profileId=profile_id, pageToken=next_page))
    else: API_Retry(service.reports().list(profileId=profile_id, pageToken=next_page))
    next_page = response['nextPageToken']
    for report in response['items']:
      yield report


def report_files(auth, account, report_id):
  """ Lists all the files available for a given DCM report configuration.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/files/list

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) DCM report identifier.

  Returns:
    * Iterator of JSONs.

  """

  account_id, advertiser_id, profile_id = parse_account(auth, account)
  service = get_service('dfareporting', API_VERSION, auth)
  next_page = None
  while next_page != '':
    if INTERNAL_MODE: response = API_Retry(service.reports().files().list(accountId=account_id, profileId=profile_id, reportId=report_id, pageToken=next_page))
    else: response = API_Retry(service.reports().files().list(profileId=profile_id, reportId=report_id, pageToken=next_page))
    next_page = response['nextPageToken']
    for report in response['items']:
      yield report


def report_to_rows(report):
  """ Helper to convert DCM files into iterator of rows, memory efficient.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  ```

  Args:
    * report: (iterator or file) Either an iterator or file that will be converted to rows.

  Returns:
    * Iterator of lists representing each row.

  """

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
  """ Helper to determine the schema of a given set of report headers.

  Using a match table generated from the DCM proto, each report header is matched
  to its type and a schema is assembled. If not found defaults to STRING.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  rows = report_clean(rows,  project.task.get('datastudio', False))
  schema = report_schema(rows.next())
  ```

  Args:
    * headers: (list) First row of a report.
   
  Returns:
    * JSON schema definition.

  """
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
  """ Helper to fix DCM report issues for BigQuery and ensure schema compliance.

  Memory efficiently cleans each row by fixing:
  * Strips header and footer to preserve only data rows.
  * Changes 'Date' to 'Report_Day' to avoid using reserved name in BigQuery.
  * removes '-' as columns
  * Changes data format to match data studio if datastusio=True.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  rows = report_clean(rows,  project.task.get('datastudio', False))
  ```

  Args:
    * rows: (iterator) Rows to clean.
   
  Returns:
    * Iterator of cleaned rows.

  """

  if project.verbose: print 'DCM REPORT CLEAN'

  first = True
  last = False

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
      try: 
        date_column = row.index('Date')
        row[date_column] = 'Report_Day'
      except ValueError: pass
      if datastudio: row = [column_header_sanitize(cell) for cell in row]
      
    # remove not set columns ( which throw off schema on import types )
    row = ['' if cell.strip() in ('(not set)', '-') else cell for cell in row]

    # return the row
    yield row

    # not first row anymore
    first = False


def conversions_upload(auth, account, floodlight_activity_id, conversion_type, conversion_rows, encryption_entity=None, update=False):
  """ Uploads an offline conversion list to DCM.

  BulletProofing: https://developers.google.com/doubleclick-advertisers/guides/conversions_upload

  Handles errors and segmentation of conversion so list can be any size.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * floodlight_activity_id: (int) ID of DCM floodlight to upload conversions to.
    * converstion_type: (string) One of the following: encryptedUserId, encryptedUserIdCandidates, gclid, mobileDeviceId.
    * conversion_rows: (iterator) List of the following rows: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId.
    * encryption_entity: (object) See EncryptionInfo docs: https://developers.google.com/doubleclick-advertisers/v3.2/conversions/batchinsert#encryptionInfo

  """

  account_id, advertiser_id, profile_id = parse_account(auth, account)

  service = get_service('dfareporting', API_VERSION, auth)
  if INTERNAL_MODE: response = API_Retry(service.floodlightActivities().get(accountId=account_id, profileId=profile_id, id=floodlight_activity_id))
  else: response = API_Retry(service.floodlightActivities().get(profileId=profile_id, id=floodlight_activity_id))
  
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
        if INTERNAL_MODE: results = API_Retry(service.conversions().batchupdate(accountId=account_id, profileId=profile_id, body=body))
        else: results = API_Retry(service.conversions().batchupdate(profileId=profile_id, body=body))
      else:
        if INTERNAL_MODE: results = API_Retry(service.conversions().batchinsert(accountId=account_id, profileId=profile_id, body=body))
        else: results = API_Retry(service.conversions().batchinsert(profileId=profile_id, body=body))

      # stream back satus
      for status in results['status']: yield status 

      # clear the buffer
      row_count += len(row_buffer)
      row_buffer = []


def id_to_timezone(reportGenerationTimeZoneId):
  return {
    1:"America/New_York",
    2:"Europe/London",
    3:"Europe/Paris",
    4:"Africa/Johannesburg",
    5:"Asia/Jerusalem",
    6:"Asia/Shanghai",
    7:"Asia/Hong_Kong",
    8:"Asia/Tokyo",
    9:"Australia/Sydney",
    10:"Asia/Dubai",
    11:"America/Los_Angeles",
    12:"Pacific/Auckland",
    13:"America/Sao_Paulo",
  }.get(reportGenerationTimeZoneId)
