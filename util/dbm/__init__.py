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
# https://developers.google.com/drive/v3/web/manage-downloads

import re
import pprint
import urllib2
import csv
import json
import time
from StringIO import StringIO
from types import GeneratorType

from googleapiclient.errors import HttpError

from util.project import project
from util.auth import get_service
from util.bigquery import query_to_rows, storage_to_table
from util.storage import object_get_chunks


DBM_CHUNKSIZE = 200 * 1024 * 1024 # 200MB recommended by docs
RE_FILENAME = re.compile(r'.*/(.*)\?GoogleAccess')
RE_HUMAN = re.compile('[^0-9a-zA-Z]+')


def _retry(job, key=None, retries=10, wait=30):
  try:
    data = job.execute()
    #pprint.PrettyPrinter().pprint(data)
    return data if not key else data[key] if key in data else []
  except HttpError, e:
    if project.verbose: print str(e)
    if e.resp.status in [403, 429, 500, 503]:
      if retries > 0:
        time.sleep(wait)
        return _retry(job, key, retries - 1, wait * 2)
      elif json.loads(e.content)['error']['code'] == 409:
        pass  # already exists ( ignore )
      else:
        raise


def _process_filters(partners, advertisers, filters, project_id, dataset_id, auth='user'):
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

      items = query_to_rows(auth, project_id, dataset_id, f['value'])

      filtered = False
      for item in items:
        if item and len(item) != 0:
          filtered = True
          structures.append({
            'type':f['type'],
            'value':item[0]
          })
        else: break

      if not filtered:
        raise Exception('Select filter did not return any values: %s' % f['value'])
    else:
      structures.append({
        'type':f['type'],
        'value':f['value']
      })

  return structures


def accounts_split(accounts):
  partners = []
  advertisers = []
  for account in accounts:
    if isinstance(account, (int, long)):
      partners.append(account)
    else:
      partner_advertiser = account.split(':', 1)
      partners.append(int(partner_advertiser[0]))
      if len (partner_advertiser) == 2:
        advertisers.append(int(partner_advertiser[1]))
  return partners, advertisers


def report_get(auth, report_id=None, name=None):
  service = get_service('doubleclickbidmanager', 'v1', auth)
  if name:
    job = service.queries().listqueries()
    result = _retry(job)
    return ([query for query in result.get('queries', []) if query['metadata']['title'] == name ] or [None])[0]
  else:
    job = service.queries().getquery(queryId=report_id)
    return _retry(job)


def report_create(auth, name, typed, partners, advertisers, filters, dimensions, metrics, data_range, timezone, project_id=None, dataset_id=None):
  report = report_get(auth, name=name)
  #pprint.PrettyPrinter().pprint(report)

  # transform filters into DBM structures
  filters = _process_filters(partners, advertisers, filters, project_id, dataset_id, auth=auth)

  if report is None:
    if project.verbose: print 'DBM Report Create:', name

    service = get_service('doubleclickbidmanager', 'v1', auth)

    body = {
      'kind': 'doubleclickbidmanager#query',
      'timezoneCode': timezone,
      'metadata': {
        'title': name,
        'dataRange': data_range,
        'format': 'CSV',
        'sendNotification': False,
      },
      'params': {
        'filters': filters,
        'groupBys': dimensions or [
            'FILTER_DATE',
            'FILTER_ADVERTISER',
            'FILTER_LINE_ITEM',
            'FILTER_INSERTION_ORDER',
            'FILTER_CREATIVE_ID',
            'FILTER_ADVERTISER_CURRENCY'
            'FILTER_MOBILE_DEVICE_TYPE'
          ],
        'includeInviteData': False,
        'metrics': metrics or ['METRIC_REVENUE_ADVERTISER'],
        'type': typed
      },
      'schedule': {
        'endTimeMs': long((time.time() + (365 * 24 * 60 * 60)) * 1000), # 1 year in future
        'frequency': 'DAILY',
        'nextRunMinuteOfDay': 4 * 60,
        'nextRunTimezoneCode': timezone
      }
    }

    #pprint.PrettyPrinter().pprint(body)

    # create the job
    job = service.queries().createquery(body=body)
    report = _retry(job)

    #pprint.PrettyPrinter().pprint(report)

    # run job ( first time )
    body = {
     "dataRange":report['metadata']['dataRange'],
     "timezoneCode":report['schedule']['nextRunTimezoneCode']
    }
    run = service.queries().runquery(queryId=report['queryId'], body=body)
    _retry(run)
  else:
    if project.verbose: print 'DBM Report Exists:', name

  return report


# timeout is in minutes ( retries will happen at 5 minute interval, default total time is 60 minutes )
def report_fetch(auth, report_id=None, name=None, timeout = 4):
  if project.verbose: print 'DBM Report Download ( timeout ):', report_id or name, timeout

  wait = 256

  while timeout >= 0: # allow zero to execute at least once
    # advance timeout first ( if = 0 then exit condition met but already in loop, if > 0 then will run into sleep )
    timeout -= 1

    report = report_get(auth, report_id, name)
    #pprint.PrettyPrinter().pprint(report)
    if report:
      # report is running ( return only if timeout is exhausted )
      if report['metadata']['googleCloudStoragePathForLatestReport'] == '':
        if project.verbose: print 'DBM Still Running'
        if timeout < 0: return True
      # file exists ( return it success )
      else:
        return report['metadata']['googleCloudStoragePathForLatestReport']

    # no report ( break out of loop it will never finish )
    else:
      if project.verbose: print 'DBM No Report'
      return False

    wait = wait * 2
    time.sleep(wait)


def report_bigquery(auth, report_id, name, dataset, table, schema=[], timeout=60):
  storage_path = report_fetch(auth, report_id, name, timeout)
  if storage_path not in (True, False):
    print project.id, dataset, table, storage_path
    storage_to_table(auth, project.id, dataset, table, storage_path, schema, 1 if schema else 0)


def report_file(auth, report_id=None, name=None, timeout = 60, chunksize = None):
  storage_path = report_fetch(auth, report_id, name, timeout)

  if storage_path == False:
    return None, None
  elif storage_path == True:
    return 'report_running.csv', None
  else:
    filename = RE_FILENAME.search(storage_path).groups(0)[0]

    # streaming
    if 0: #if chunksize: BROKEN SO DEFAULTING TO STREAMING
      #print 'PATH PRE', storage_path
      path = storage_path.split('?', 1)[0].replace('https://storage.googleapis.com/', '').replace('/', ':', 1)
      #print 'PATH POST', path
      return filename, object_get_chunks(auth, path, chunksize)

    # single object
    else:
      return filename, StringIO(urllib2.urlopen(storage_path).read())


def report_delete(auth, report_id=None, name=None):
  if project.verbose: print "DBM DELETE:", report_id or name
  report = report_get(auth, report_id, name)
  if report:
    service = get_service('doubleclickbidmanager', 'v1', auth)
    job = service.queries().deletequery(queryId=report['queryId'])
    _retry(job)
  else:
    if project.verbose: print 'DBM DELETE: No Report'


def report_list(auth):
  service = get_service('doubleclickbidmanager', 'v1', auth)
  job = service.queries().listqueries()
  for query in _retry(job, 'queries'):
    yield query



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


def report_clean(rows, datastudio=False, nulls=False):
  if project.verbose: print 'DBM Report Clean'

  first = True
  last = False
  date = None
  for row in rows:
    # stop if no data returned
    if row == ['No data returned by the reporting service.']: break

    # stop at blank row ( including sum row )
    if not row or row[0] is None or row[0] == '': break

    # find 'Date' column if it exists
    if first:
      try: date = row.index('Date')
      except ValueError: pass
      if datastudio: row = [RE_HUMAN.sub('_', column) for column in row]

    # check if data studio formatting is applied
    if datastudio and date is not None:
      row[date] = 'Report_Day' if first else row[date].replace('/', '')

    # remove unknown columns ( which throw off schema on import types )
    if nulls: row = ['' if cell.strip() == 'Unknown' else cell for cell in row]

    # return the row
    yield row

    # not first row anymore
    first = False
