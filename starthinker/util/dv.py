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

# https://developers.google.com/bid-manager/v1/queries
# https://developers.google.com/drive/v3/web/manage-downloads
# https://developers.google.com/bid-manager/guides/entity-write/format

import re
import pprint
import json
import time
from types import GeneratorType
from urllib.request import urlopen

from starthinker.config import BUFFER_SCALE
from starthinker.util.data import get_rows
from starthinker.util.storage import object_get_chunks
from starthinker.util.csv import column_header_sanitize, csv_to_rows, rows_to_csv, response_utf8_stream
from starthinker.util.google_api import API_DV360
from starthinker.util.google_api import API_DBM

DBM_CHUNKSIZE = int(
    200 * 1024000 *
    BUFFER_SCALE)  # 200MB recommended by docs * scale in config.py
RE_FILENAME = re.compile(r'.*/(.*)\?GoogleAccess')


def report_get(config, auth, report_id=None, name=None):
  """ Returns the DBM JSON definition of a report based on name or ID.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/getquery

  Args:
    * auth: (string) Either user or service.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * JSON definition of report.

  """

  if name:
    for query in API_DBM(config, auth, iterate=True).queries().listqueries().execute():
      if query['metadata']['title'] == name:
        return query
  else:
    return API_DBM(config, auth).queries().getquery(queryId=report_id).execute()


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
    "FILTER_PARTNER": {
      "values":789
    },
    "FILTER_ADVERTISER": {
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
      new_body['params'].setdefault('filters', []).append({
          'type': f,
          'value': v
      })

  return new_body


def report_build(config, auth, body):
  """ Creates a DBM report given a JSON definition.

  Bulletproofing:
  https://developers.google.com/bid-manager/v1/queries/createquery

  The report will be automatically run the first time.

  The body JSON provided will have the following fields added if not present:
    * schedule - set to run daily and expire in one year.

  Args:
    * auth: (string) Either user or service.
    * body: (json) As defined in:
      https://developers.google.com/doubleclick-advertisers/v3.2/reports#resource

  Returns:
    * JSON definition of report created or existing.

  """

  report = report_get(config, auth, name=body['metadata']['title'])

  if not report:

    # add default daily schedule if it does not exist ( convenience )
    body.setdefault('schedule', {})
    body['schedule'].setdefault('nextRunTimezoneCode', body['timezoneCode'])
    body['schedule'].setdefault('frequency', 'DAILY')
    if body['schedule']['frequency'] != 'ONE_TIME':
      body['schedule'].setdefault('nextRunMinuteOfDay', 4 * 60)
      body['schedule'].setdefault('endTimeMs',
                                  int((time.time() + (365 * 24 * 60 * 60)) *
                                      1000))  # 1 year in future

    # build report
    #pprint.PrettyPrinter().pprint(body)
    report = API_DBM(config, auth).queries().createquery(body=body, asynchronous=True).execute()

    # run report first time
    body = {
        'dataRange': report['metadata']['dataRange'],
        'timezoneCode': body['timezoneCode']
    }
    API_DBM(config, auth).queries().runquery(
        queryId=report['queryId'], body=body).execute()

  else:
    if config.verbose:
      print('DBM Report Exists:', body['metadata']['title'])

  return report


def report_fetch(config, auth, report_id=None, name=None, timeout=60):
  """ Retrieves most recent DBM file JSON by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/getquery

  Timeout is in minutes ( retries will happen at 5 minute interval, default
  total time is 20 minutes )

  Args:
    * auth: (string) Either user or service.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.

  Returns:
    * Report JSON if report exists and is ready.
    * True if report is in progress but not ready.
    * False if report does not exist.

  """

  if config.verbose:
    print('DBM Report Download ( timeout ):', report_id or name, timeout)

  while timeout >= 0:  # allow zero to execute at least once
    # advance timeout first ( if = 0 then exit condition met but already in loop, if > 0 then will run into sleep )
    timeout -= 1

    report = report_get(config, auth, report_id, name)
    #pprint.PrettyPrinter().pprint(report)
    if report:
      # report is running ( return only if timeout is exhausted )
      if report['metadata'].get('googleCloudStoragePathForLatestReport',
                                '') == '':
        if config.verbose:
          print('DBM Still Running')
        if timeout < 0:
          return True
      # file exists ( return it success )
      else:
        return report['metadata']['googleCloudStoragePathForLatestReport']

    # no report ( break out of loop it will never finish )
    else:
      if config.verbose:
        print('DBM No Report')
      return False

    # sleep a minute
    if timeout > 0:
      if config.verbose:
        print('WAITING MINUTES', timeout)
      time.sleep(60)


def report_file(config, auth,
                report_id=None,
                name=None,
                timeout=60,
                chunksize=DBM_CHUNKSIZE):
  """ Retrieves most recent DBM file by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/getquery

  Timeout is in minutes ( retries will happen at 1 minute interval, default
  total time is 60 minutes )
  If chunksize is set to None then the whole file is downloaded at once.

  Args:
    * auth: (string) Either user or service.
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

  storage_path = report_fetch(config, auth, report_id, name, timeout)

  if storage_path == False:
    return None, None
  elif storage_path == True:
    return 'report_running.csv', None
  else:
    filename = RE_FILENAME.search(storage_path).groups(0)[0]

    # streaming
    if chunksize:
      if config.verbose:
        print('REPORT FILE STREAM:', storage_path)
      return filename, response_utf8_stream(urlopen(storage_path), chunksize)

    # single object
    else:
      if config.verbose:
        print('REPORT FILE SINGLE:', storage_path)
      return filename, urlopen(storage_path).read().decode('UTF-8')


def report_delete(config, auth, report_id=None, name=None):
  """ Deletes a DBM report based on name or ID.

  Bulletproofing:
  https://developers.google.com/bid-manager/v1/queries/deletequery

  Args:
    * auth: (string) Either user or service.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * None

  """

  if config.verbose:
    print('DBM DELETE:', report_id or name)
  report = report_get(config, auth, report_id, name)
  if report:
    API_DBM(config, auth).queries().deletequery(queryId=report['queryId']).execute()
  else:
    if config.verbose:
      print('DBM DELETE: No Report')


def report_list(config, auth):
  """ Lists all the DBM report configurations for the current credentials.

  Bulletproofing:
  https://developers.google.com/bid-manager/v1/queries/listqueries

  Args:
    * auth: (string) Either user or service.

  Returns:
    * Iterator of JSONs.

  """

  for query in API_DBM(config, auth, iterate=True).queries().listqueries().execute():
    yield query


""" Get a DV360 report as a list

Args: * auth => auth from the job * report_id => the report id that wants to be
pulled

Returns:
  * a DV360 report represented as a list
"""


def report_to_list(config, auth, report_id):
  filename, report = report_file(
      auth,
      report_id,
      None,  #name
      10,  #timeout
      DBM_CHUNKSIZE)

  if report:
    rows = report_to_rows(report)
    rows = report_clean(rows)

  return list(rows)


def report_to_rows(report):
  """ Helper to convert DBM files into iterator of rows, memory efficient.

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


def report_clean(rows):
  """ Helper to fix DBM report issues for BigQuery and ensure schema compliance.

  Memory efficiently cleans each row by fixing:
  * Strips header and footer to preserve only data rows.
  * Changes 'Date' to 'Report_Day' to avoid using reserved name in BigQuery.
  * Changes date values to use '-' instead of '/' for BigQuery compatibility.
  * Changes columns '-' and 'Unknown' to NULL
  * Changes '< 1000' to 1000

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

  print('DBM Report Clean')

  first = True
  last = False
  date = None
  for row in rows:
    # stop if no data returned
    if row == ['No data returned by the reporting service.']:
      break

    # stop at blank row ( including sum row )
    if not row or row[0] is None or row[0] == '':
      break

    # sanitizie header row
    if first:
      try:
        date_column = row.index('Date')
        row[date_column] = 'Report_Day'
      except ValueError:
        pass
      row = [column_header_sanitize(cell) for cell in row]

    # for all data rows clean up cells
    else:
      # check if data studio formatting is applied reformat the dates
      row = [
          cell.replace('/', '-') if isinstance(cell, str) and len(cell) == 4 +
          1 + 2 + 1 + 2 and cell[4] == '/' and cell[7] == '/' else cell
          for cell in row
      ]  # 5x faster than regexp

    # remove unknown columns ( which throw off schema on import types )
    row = [
        '' if cell.strip() in (
            'Unknown',
            '-',
        ) else ('1000' if cell == '< 1000' else cell) for cell in row
    ]

    # return the row
    yield row

    # not first row anymore
    first = False


def lineitem_patch_v1(config, auth, patch, li):
  """Patches a DV360 Line Item

  Args:
    auth: StarThinker authentication scheme
    patch: List of field names to patch
    li: Line item with updates to push
  Returns: Updated Line Item
  """
  return API_DV360(config, auth).advertisers().lineItems().patch(
      advertiserId=li['advertiserId'],
      lineItemId=li['lineItemId'],
      updateMask=patch,
      body=li).execute()


def lineitem_get_v1(config, auth, advertiser_id, lineitem_id):
  """Gets a DV360 Line Item

  Args:
    auth: StarThinker authentication scheme
    advertiser_id: ID of the advertiser of the line item
    lineitem_id: ID of the line item
  Returns: Line Item from the DV360 API
  """
  return API_DV360(config, auth).advertisers().lineItems().get(
      advertiserId=advertiser_id, lineItemId=lineitem_id).execute()
