###########################################################################
#
#  Copyright 2020 Google LLC
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
from time import sleep
from io import StringIO
from types import GeneratorType
from datetime import date, timedelta

from starthinker.config import BUFFER_SCALE
from starthinker.util import flag_last
from starthinker.util.data import get_rows
from starthinker.util.google_api import API_DCM
from starthinker.util.storage import media_download
from starthinker.util.csv import column_header_sanitize, csv_to_rows
from starthinker.util.cm_schema import DCM_Field_Lookup

DCM_CHUNK_SIZE = int(
    200 * 1024000 *
    BUFFER_SCALE)  # 200MB minimum recommended by docs * scale in config.py
DCM_CONVERSION_SIZE = 1000


def get_profile_for_api(config, auth, account_id=None):
  """Return a DCM profile ID for the currently supplied credentials.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/userProfiles/get

  Handles cases of superuser, otherwise chooses the first matched profile.
  Allows DCM jobs to only specify account ID, which makes jobs more portable
  between accounts.

  Args:
    * auth: (string) Either user or service.
    * account_id: (int) Account number for which report is retrieved, optional if superuser.

  Returns:
    * Is Superuser ( bool ): True if superuser account
    * Profile ID ( int ): profile id to be used to make API call

  Raises:
    * If current credentials do not have a profile for this account.

  """

  profile_admin = None
  profile_network = None

  if account_id is not None:
    account_id=int(account_id)

  for p in API_DCM(config, auth, iterate=True).userProfiles().list().execute():
    p_id = int(p['profileId'])
    a_id = int(p['accountId'])

    # take the first profile for admin
    if a_id == 2515 and 'subAccountId' not in p:
      profile_admin = p_id
      break

    # try to find first network profile if exists
    if profile_network is None and a_id == account_id:
      profile_network = p_id

  if profile_admin:
    return True, profile_admin
  elif profile_network:
    return False, profile_network
  else:
    raise Exception('Add your user profile to DCM account %s.' % account_id)


def get_account_name(config, auth, account):
  """ Return the name of a DCM account given the account ID.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.

  Returns:
    * Profile ID.

  Raises:
    * If current credentials do not have a profile for this account.

  """

  account_id, advertiser_ids = parse_account(config, auth, account)
  is_superuser, profile_id = get_profile_for_api(config, auth, account_id)
  response = API_DCM(
      config, auth, internal=is_superuser).accounts().get(
          id=account_id, profileId=profile_id).execute()
  return response['name']


def parse_account(config, auth, account):
  """ Breaks a [account:advertiser@profile] string into parts if supplied.

  This function was created to accomodate supplying advertiser and profile
  information
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
  try:
    network_id, profile_id = network_id.split('@', 1)
  except:
    profile_id = None

  # if exists, get avertiser from end
  try:
    network_id, advertiser_ids = network_id.split(':', 1)
  except:
    pass

  # if network or advertiser, convert to integer
  if network_id is not None:
    network_id = int(network_id)
  if advertiser_ids is not None:
    advertiser_ids = [
        int(advertiser_id.strip())
        for advertiser_id in advertiser_ids.split(',')
    ]

  return network_id, advertiser_ids


def report_get(config, auth, account, report_id=None, name=None):
  """ Returns the DCM JSON definition of a report based on name or ID.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/reports/get

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * JSON definition of report.

  """

  report = None

  account_id, advertiser_ids = parse_account(config, auth, account)
  is_superuser, profile_id = get_profile_for_api(config, auth, account_id)
  kwargs = {
    'profileId': profile_id,
    'accountId': account_id
  } if is_superuser else {
    'profileId': profile_id
  }

  if name:
    for r in API_DCM(
      config,
      auth,
      iterate=True,
      internal=is_superuser
    ).reports().list(**kwargs).execute():
      if r['name'] == name:
        report = r
        break

  elif report_id:
    kwargs['reportId'] = report_id
    report = API_DCM(
      config,
      auth,
      internal=is_superuser
    ).reports().get(**kwargs).execute()

  return report


def report_delete(config, auth, account, report_id=None, name=None):
  """ Deletes a DCM report based on name or ID.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/reports/delete

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * None

  """

  report = report_get(config, auth, account, report_id, name)
  if report:
    account_id, advertiser_ids = parse_account(config, auth, account)
    is_superuser, profile_id = get_profile_for_api(config, auth, account_id)
    kwargs = {
        'profileId': profile_id,
        'accountId': account_id
    } if is_superuser else {
        'profileId': profile_id
    }
    kwargs['reportId'] = report['id']
    API_DCM(config, auth, internal=is_superuser).reports().delete(**kwargs).execute()
  else:
    if config.verbose:
      print('DCM DELETE: No Report')


def report_filter(config, auth, body, filters):
  """ Adds filters to a report body

  Filters cannot be easily added to the reports without templateing, this allows
  filters to be passed as lists.
  Values are specified using get_rows(...) helper, see
  starthinker/util/data/__init__.py.
  To specify a filter, use the official filter name and a list of values.

  For exmaple:

  ```
  filters = {
    "accountId": {
      "values": 789
    },
    "advertiser": {
      "values":[1234, 5678, 91011]
    }
  }
  ```

  Args:
    * auth: (string) Either user or service.
    * body: (json) the report body ( with or without filters )
    * filters: (json) a dictionary of filters to apply ( see above examples )

  Returns:
    * body: ( json ) modified report body
  """

  new_body = body.copy()

  for f, d in filters.items():
    for v in get_rows(config, auth, d):

      # accounts are specified in a unique part of the report json
      if f == 'accountId':
        new_body['accountId'] = v

      # activities are specified in a unique part of the report json
      elif f == 'activity':
        new_body['reachCriteria']['activities'].setdefault(
            'filters', []).append({
                'kind': 'dfareporting#dimensionValue',
                'dimensionName': f,
                'id': v
            })

      # all other filters go in the same place
      else:
        new_body.setdefault('criteria',
                            {}).setdefault('dimensionFilters', []).append({
                                'kind': 'dfareporting#dimensionValue',
                                'dimensionName': f,
                                'id': v,
                                'matchType': 'EXACT'
                            })

  return new_body


def report_build(config, auth, account, body):
  """ Creates a DCM report given a JSON definition.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/reports/insert

  The body JSON provided will have the following fields overriden:
    * accountId - supplied as a parameter in account token.
    * ownerProfileId - determined from the current credentials.
    * advertiser_ids - supplied as a parameter in account token.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * body: (json) As defined in:
      https://developers.google.com/doubleclick-advertisers/v3.2/reports#resource

  Returns:
    * JSON definition of report created or existing.

  """

  report = report_get(config, auth, account, name=body['name'])

  if report is None:
    account_id, advertiser_ids = parse_account(config, auth, account)
    is_superuser, profile_id = get_profile_for_api(config, auth, account_id)

    # add the account id to the body
    body['accountId'] = account_id
    body['ownerProfileId'] = profile_id

    # add advertisers to the body, ignore for floodlight reports
    if advertiser_ids and 'criteria' in body:
      body['criteria']['dimensionFilters'] = body.get('criteria', {}).get(
          'dimensionFilters', []) + [{
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'advertiser',
              'id': advertiser_id,
              'matchType': 'EXACT'
          } for advertiser_id in advertiser_ids]

    # add default daily schedule if it does not exist ( convenience )
    if 'schedule' not in body:
      body['schedule'] = {'active': True, 'repeats': 'DAILY', 'every': 1}

    # add default start and end if it does not exist ( convenience )
    if 'startDate' not in body['schedule']:
      body['schedule']['startDate'] = str(date.today())

    # add default start and end if it does not exist ( convenience )
    if 'expirationDate' not in body['schedule']:
      body['schedule']['expirationDate'] = str(
          (date.today() + timedelta(days=365)))

    #pprint.PrettyPrinter().pprint(body)

    # create the report
    kwargs = {
        'profileId': profile_id,
        'accountId': account_id
    } if is_superuser else {
        'profileId': profile_id
    }
    kwargs['body'] = body
    report = API_DCM(
        config, auth, internal=is_superuser).reports().insert(**kwargs).execute()

    # run the report
    kwargs = {
        'profileId': profile_id,
        'accountId': account_id
    } if is_superuser else {
        'profileId': profile_id
    }
    kwargs['reportId'] = report['id']
    API_DCM(config, auth, internal=is_superuser).reports().run(**kwargs).execute()

  else:
    if config.verbose:
      print('DCM Report Exists:', body['name'])

  return report


def report_fetch(config, auth, account, report_id=None, name=None, timeout=60):
  """ Retrieves most recent DCM file JSON by name or ID, if in progress, waits for it to complete.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/files/get

  Timeout is in minutes ( retries will happen at 1 minute interval, default
  total time is 60 minutes )

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

  if config.verbose:
    print('DCM REPORT FILE', report_id or name)

  if report_id is None:
    report = report_get(config, auth, account, name=name)
    if report is None:
      raise Exception('Report does not exist:', name)
    else:
      report_id = report['id']

  running = False

  # zero means run once
  while timeout >= 0:

    # loop all files recent to oldest looking for valid one
    for file_json in report_files(config, auth, account, report_id):
      #pprint.PrettyPrinter().pprint(file)

      # still running ( wait for timeout )
      if file_json['status'] == 'PROCESSING':
        if config.verbose:
          print('REPORT PROCESSING WILL WAIT')
        running = True
        if timeout > 0:
          break  # go to outer loop wait

      # ready for download ( return file )
      elif file_json['status'] == 'REPORT_AVAILABLE':
        if config.verbose:
          print('REPORT DONE')
        return file_json

      # cancelled or failed ( go to next file in loop )

    # if no report running ( skip wait )
    if not running:
      break

    # sleep a minute
    if timeout > 0:
      if config.verbose:
        print('WAITING MINUTES', timeout)
      sleep(60)

    # advance timeout
    timeout -= 1

  # if here, no file is ready, return status
  if config.verbose:
    print('NO REPORT FILES')
  return running


def report_run(config, auth, account, report_id=None, name=None):
  """ Trigger a DCM report to run by name or ID.

  Will do nothing if report is currently in progress.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.3/reports/run

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * True if report run is executed
    * False otherwise

  """

  account_id, advertiser_id = parse_account(config, auth, account)
  is_superuser, profile_id = get_profile_for_api(config, auth, account_id)
  kwargs = {
      'profileId': profile_id,
      'accountId': account_id
  } if is_superuser else {
      'profileId': profile_id
  }

  if config.verbose:
    print('DCM REPORT RUN INIT', report_id or name)
  if report_id is None:
    report = report_get(config, auth, account, name=name)
    if report is None:
      raise Exception('Report does not exist:', name)
    else:
      report_id = report['id']

  kwargs = {
      'profileId': profile_id,
      'accountId': account_id
  } if is_superuser else {
      'profileId': profile_id
  }
  kwargs['reportId'] = report_id

  files = report_files(config, auth, account, report_id)
  latest_file_json = next(files, None)
  if latest_file_json == None or latest_file_json['status'] != 'PROCESSING':
    # run report if previously never run or currently not running
    if config.verbose:
      print('RUNNING REPORT', report_id or name)
    API_DCM(config, auth, internal=is_superuser).reports().run(**kwargs).execute()
    return True
  if config.verbose:
    print('REPORT RUN SKIPPED', report_id or name)
  return False


def report_file(config, auth,
                account,
                report_id=None,
                name=None,
                timeout=60,
                chunksize=DCM_CHUNK_SIZE):
  """ Retrieves most recent DCM file by name or ID, if in progress, waits for it to complete.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/files/get

  Timeout is in minutes ( retries will happen at 1 minute interval, default
  total time is 60 minutes )
  If chunksize is set to 0 then the whole file is downloaded at once.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.
    * chunksize: (int) number of bytes to download at a time, for memory
      constrained systems.

  Returns:
    * (filename, iterator) if file exists and is ready to download in chunks.
    * (filename, file) if file exists and chunking is off.
    * ('report_running.csv', None) if report is in progress.
    * (None, None) if file does not exist.

  """

  account_id, advertiser_id = parse_account(config, auth, account)
  file_json = report_fetch(config, auth, account, report_id, name, timeout)

  if file_json == False:
    return None, None
  elif file_json == True:
    return 'report_running.csv', None
  else:
    filename = '%s_%s.csv' % (file_json['fileName'],
                              file_json['dateRange']['endDate'].replace(
                                  '-', ''))

    # streaming
    if chunksize:
      return filename, media_download(
          API_DCM(config, auth).files().get_media(
              reportId=file_json['reportId'],
              fileId=file_json['id']).execute(False), chunksize, 'utf-8')

    # single object
    else:
      return filename, StringIO(
          API_DCM(config, auth).files().get_media(
              reportId=file_json['reportId'],
              fileId=file_json['id']).execute().decode('utf-8'))


def report_list(config, auth, account):
  """ Lists all the DCM report configurations for an account given the current credentials.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/reports/list

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.

  Returns:
    * Iterator of JSONs.

  """

  account_id, advertiser_id = parse_account(config, auth, account)
  is_superuser, profile_id = get_profile_for_api(config, auth, account_id)
  kwargs = {
    'profileId': profile_id,
    'accountId': account_id
  } if is_superuser else {
    'profileId': profile_id
  }
  for report in API_DCM(
    auth,
    iterate=True,
    internal=is_superuser
  ).reports().list(**kwargs).execute():
    yield report


def report_files(config, auth, account, report_id):
  """ Lists all the files available for a given DCM report configuration.

  Bulletproofing:
  https://developers.google.com/doubleclick-advertisers/v3.2/files/list

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) DCM report identifier.

  Returns:
    * Iterator of JSONs.

  """

  account_id, advertiser_id = parse_account(config, auth, account)
  is_superuser, profile_id = get_profile_for_api(config, auth, account_id)
  kwargs = {
    'profileId': profile_id,
    'accountId': account_id
  } if is_superuser else {
    'profileId': profile_id
  }
  kwargs['reportId'] = report_id
  for report_file in API_DCM(
    config,
    auth,
    iterate=True,
    internal=is_superuser
  ).reports().files().list(**kwargs).execute():
    yield report_file


def report_to_rows(report):
  """ Helper to convert DCM files into iterator of rows, memory efficient.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  ```

  Args:
    * report: (iterator or file) Either an iterator or file that will be
      converted to rows.

  Returns:
    * Iterator of lists representing each row.

  """

  # if reading from stream
  if type(report) is GeneratorType:
    leftovers = ''
    for chunk in report:
      data, extra = chunk.rsplit('\n', 1)
      for row in csv_to_rows(leftovers + data):
        yield row
      leftovers = extra

  # if reading from buffer
  else:
    for row in csv_to_rows(report):
      yield row


def report_schema(headers):
  """ Helper to determine the schema of a given set of report headers.

  Using a match table generated from the DCM proto, each report header is
  matched
  to its type and a schema is assembled. If not found defaults to STRING.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  rows = report_clean(rows)
  schema = report_schema(next(rows))
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
    if header_type is None:
      header_type = 'STRING'

    schema.append({
        'name': header_sanitized,
        'type': header_type,
        'mode': 'NULLABLE'
    })

  return schema


def report_clean(rows):
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
  rows = report_clean(rows)
  ```

  Args:
    * rows: (iterator) Rows to clean.

  Returns:
    * Iterator of cleaned rows.

  """

  print('DCM REPORT CLEAN')

  first = True
  last = False

  # find start of report
  for row in rows:
    if row and row[0] == 'Report Fields':
      break

  # process the report
  for row in rows:
    # quit if empty report
    if 'No data returned by the reporting service.' in row:
      break

    # stop parsing if end of data
    if not row or row[0] == 'Grand Total:':
      break

    # find 'Date' column if it exists
    if first:
      try:
        date_column = row.index('Date')
        row[date_column] = 'Report_Day'
      except ValueError:
        pass
      row = [column_header_sanitize(cell) for cell in row]

    # remove not set columns ( which throw off schema on import types )
    row = ['' if cell.strip() in ('(not set)', '-') else cell for cell in row]

    # return the row
    yield row

    # not first row anymore
    first = False


def conversions_upload(config, auth,
                       account,
                       floodlight_activity_id,
                       conversion_type,
                       conversion_rows,
                       encryption_entity=None,
                       update=False):
  """ Uploads an offline conversion list to DCM.

  BulletProofing:
  https://developers.google.com/doubleclick-advertisers/guides/conversions_upload

  Handles errors and segmentation of conversion so list can be any size.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * floodlight_activity_id: (int) ID of DCM floodlight to upload conversions
      to.
    * converstion_type: (string) One of the following: encryptedUserId,
      encryptedUserIdCandidates, gclid, mobileDeviceId.
    * conversion_rows: (iterator) List of the following rows: Ordinal,
      timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid |
      mobileDeviceId.
    * encryption_entity: (object) See EncryptionInfo docs:
      https://developers.google.com/doubleclick-advertisers/v3.2/conversions/batchinsert#encryptionInfo
  """

  account_id, advertiser_id = parse_account(config, auth, account)
  is_superuser, profile_id = get_profile_for_api(config, auth, account_id)

  kwargs = {
      'profileId': profile_id,
      'accountId': account_id
  } if is_superuser else {
      'profileId': profile_id
  }
  kwargs['id'] = floodlight_activity_id
  response = API_DCM(
      config,
      auth,
      internal=is_superuser).floodlightActivities().get(**kwargs).execute()

  # upload in batch sizes of DCM_CONVERSION_SIZE
  row_count = 0
  row_buffer = []
  for is_last, row in flag_last(conversion_rows):
    row_buffer.append(row)

    if is_last or len(row_buffer) == DCM_CONVERSION_SIZE:

      if config.verbose:
        print('CONVERSION UPLOADING ROWS: %d - %d' %
              (row_count, row_count + len(row_buffer)))

      body = {
        'conversions': [{
          'floodlightActivityId': floodlight_activity_id,
          'floodlightConfigurationId': response['floodlightConfigurationId'],
          'ordinal': row[0],
          'timestampMicros': row[1],
          conversion_type: row[2],
          'quantity': row[3],
          'value': row[4],
        } for row in row_buffer]
      }

      if encryption_entity:
        body['encryptionInfo'] = encryption_entity

      kwargs = {
        'profileId': profile_id,
        'accountId': account_id
      } if is_superuser else {
        'profileId': profile_id
      }
      kwargs['body'] = body

      if update:
        results = API_DCM(
            config, auth, internal=is_superuser).conversions().batchupdate(
                **kwargs).execute()
      else:
        results = API_DCM(
            config, auth, internal=is_superuser).conversions().batchinsert(
                **kwargs).execute()

      # stream back satus
      for status in results['status']:
        yield status

      # clear the buffer
      row_count += len(row_buffer)
      row_buffer = []


def id_to_timezone(reportGenerationTimeZoneId):
  return {
      1: 'America/New_York',
      2: 'Europe/London',
      3: 'Europe/Paris',
      4: 'Africa/Johannesburg',
      5: 'Asia/Jerusalem',
      6: 'Asia/Shanghai',
      7: 'Asia/Hong_Kong',
      8: 'Asia/Tokyo',
      9: 'Australia/Sydney',
      10: 'Asia/Dubai',
      11: 'America/Los_Angeles',
      12: 'Pacific/Auckland',
      13: 'America/Sao_Paulo',
  }.get(reportGenerationTimeZoneId)
