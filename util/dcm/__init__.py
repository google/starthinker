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

import pprint
import urllib2
import csv
import re
import json
from StringIO import StringIO
from io import BytesIO
from copy import deepcopy

from time import sleep, mktime
from datetime import datetime, time, date, timedelta
from googleapiclient.errors import HttpError
from jinja2 import Environment, FileSystemLoader

from setup import EXECUTE_PATH, TIMEZONE_OFFSET
from util.project import project
from util.auth import get_service
from util.regexp import parse_yyyymmdd
from util.bigquery import bigquery_date
from util.dcm.metrics import dcm_report_to_api, dcm_dimensions_to_api, dcm_metrics_to_api, dcm_label_report_type

API_VERSION = 'internalv2.7'

def get_profile_id(auth):
  service = get_service('dfareporting', API_VERSION, auth)
  return ([profile['profileId'] for profile in service.userProfiles().list().execute()['items']] or [None])[0]


def get_template(auth, config):

  def as_json(data):
    return json.dumps(data)

  def as_boolean(data):
    return 'true' if data else 'false'

  env = Environment(loader=FileSystemLoader(EXECUTE_PATH + 'dcm/templates'))
  env.filters['as_json'] = as_json
  env.filters['as_boolean'] = as_boolean

  template = env.get_template(config['template'] + '.tmplt')

  variables = deepcopy(config)
  variables['profileId'] = get_profile_id(auth)
  variables['scheduleStart'] = str(date.today())
  variables['scheduleExpiration'] = str(date.today() + timedelta(days=365))

  #print template.render({'report':variables})
  return json.loads(template.render({'report':variables}))


def report_delete(auth, name, account_id):
  service = get_service('dfareporting', API_VERSION, auth)
  profile_id = get_profile_id(auth)
  report = None

  # find existing report
  next_page = None
  while next_page != '' and report is None:
    response = service.reports().list(accountId=account_id, profileId=profile_id, pageToken=next_page).execute()
    next_page = response['nextPageToken']
    #pprint.PrettyPrinter(depth=20).pprint(response['items'])
    report = ([report for report in response['items'] if report['name'] == name] or [None])[0]
  
  if report is None:
    print 'No report found'
  else:
    try:
      report = service.reports().delete(accountId=account_id, profileId=profile_id, reportId=report['id']).execute()
    except HttpError, e:
      if e.resp.status in [403, 500, 503]: sleep(5)
      elif json.loads(e.content)['error']['code'] == 409: pass # already exists ( ignore )
      else: raise


def report_create(auth, config):
  service = get_service('dfareporting', API_VERSION, auth)
  profile_id = get_profile_id(auth)
  report = None

  # find existing report
  next_page = None
  while next_page != '' and report is None:
    response = service.reports().list(accountId=config['accountId'], profileId=profile_id, pageToken=next_page).execute()
    next_page = response['nextPageToken']
    #pprint.PrettyPrinter(depth=20).pprint(response['items'])
    report = ([report for report in response['items'] if report['name'] == config['name']] or [None])[0]

  if report is None:
    body = get_template(auth, config)

    print body
    try:
      report = service.reports().insert(accountId=config['accountId'], profileId=profile_id, body=body).execute()
    except HttpError, e:
      print 'Report Error:', e.content
      if e.resp.status in [403, 500, 503]: sleep(5)
      elif json.loads(e.content)['error']['code'] == 409: pass # already exists ( ignore )
      else: raise

  return report


def report_file(auth, account_id, report_id, collate, file_regexp = None, day = date.today()):
  if project.verbose: print 'DCM Report File', report_id

  service = get_service('dfareporting', API_VERSION, auth)
  profile_id =  get_profile_id(auth)

  file_filter = re.compile(r'%s' % file_regexp) if file_regexp else None
  day = str(day + timedelta(days=(-1 if collate == 'YESTERDAY' else 0)) + TIMEZONE_OFFSET)

  # find existing file
  next_page = None
  while next_page != '':
    response = service.reports().files().list(accountId=account_id, profileId=profile_id, reportId=report_id, pageToken=next_page).execute()
    next_page = response['nextPageToken']
    #pprint.PrettyPrinter(depth=20).pprint(response['items'])
    for report in response['items']:
      #pprint.PrettyPrinter(depth=20).pprint(report)
      if file_filter is None or file_filter.match(report['fileName']):
        #print 'DA', report['dateRange']['endDate'], day
        if collate == 'LATEST' or report['dateRange']['endDate'] == day:
          filename = '%s.csv' % report['fileName'] if collate == 'LATEST' else '%s_%s.csv' % (report['fileName'], day)
          if report['status'] == 'REPORT_AVAILABLE':
            # report is done and downloaded
            if project.verbose: print 'Report Done'
            return filename, BytesIO(service.files().get_media(reportId=report_id, fileId=report['id']).execute())
            #return BytesIO(urllib2.urlopen(report['urls']['browserUrl']).read())
          else: 
            # report is scheduled but not done
            if project.verbose: print 'Report Running'
            return filename, True
       
  # no report matching this day
  if project.verbose: print 'No Report'
  return None, None


def report_run(auth, account_id, report_id, collate):
  filename, report = report_file(auth, account_id, report_id, collate)

  # if no report scheduled, set one
  if report is None:
    service = get_service('dfareporting', API_VERSION, auth)
    profile_id =  get_profile_id(auth)

    #body = get_template(auth, config)
    #service.reports().patch(accountId=account_id, profileId=profile_id, reportId=report_id, body=body).execute()

    # then run it to get a file
    #sleep(1)
    service.reports().run(accountId=account_id, profileId=profile_id, reportId=report_id).execute()
    report = True

  # wait for report to finish
  while report == True:
    if project.verbose: print 'Wait For DCM Report'
    sleep(30)
    filename, report = report_file(auth, account_id, report_id, collate)

  # report is a binary
  return filename, report


def report_get(auth, config):
  report = report_create(auth, config)
  return report_run(auth, config['accountId'], report['id'], config['collate'])


def report_to_rows(report):
  return list(csv.reader(report)) if report else []


def report_clean(rows, date, datastudio=False, human_column_name=True):
  if project.verbose: print 'DCM Report Clean'

  # remove summary data at end of dbm report
  delete_summary = True
  while rows[0] == [] or rows[0][0] != 'Report Fields': rows.pop(0)
  rows.pop(0)
  rows.pop()

  # change date to datastudio format
  if datastudio:
    rows[0][0] = 'Report_Day'
    for i in range(1, len(rows)): rows[i][0] = rows[i][0].replace('-', '')

  if not human_column_name:
    for i in range(0, len(rows[0])): rows[0][i] = re.sub('[^0-9a-zA-Z]+', '_', rows[0][i])

  return rows


def report_to_csv(rows):
  csv_string = StringIO()
  writer = csv.writer(csv_string, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for row_number, row in enumerate(rows):
    try: writer.writerow(row)
    except Exception, e: print 'Error:', row_number, str(e), row
  csv_string.seek(0) # important otherwise contents is zero
  return csv_string
