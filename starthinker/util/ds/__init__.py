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
import csv
import re
import json
import sys

from io import StringIO
from io import BytesIO

from time import sleep, mktime
from datetime import datetime, time, date, timedelta
from googleapiclient.errors import HttpError
from jinja2 import Environment, FileSystemLoader

from starthinker.util.project import project
from starthinker.util.auth import get_service
from starthinker.util.regexp import parse_dbm_report_id
from starthinker.util.csv import bigquery_date


def report_request(auth, title, template_name, parameters, day=date.today()):
  service = get_service('doubleclicksearch', 'v2', auth)
  print('.', end='')
  sys.stdout.flush()
  
  env = Environment(loader=FileSystemLoader('ds/templates'))
  template = env.get_template(template_name)
  variables = {
            'title' : title,
            'fromDate' : str(day), 
            'toDate' : str(date.today() - timedelta(days=1)),
            'parameters' : parameters,
            }
  body = json.loads(template.render(variables))
  try:
    report = service.reports().request(body=body).execute()
    return report
  except HttpError as e:
    print(e)
    if e.resp.status in [403, 500, 503]: sleep(10)
    elif json.loads(e.content.decode())['error']['code'] == 409: pass # already exists ( ignore )
    else: raise


def report_ready(service, report_id):
  report_running = True

  files = []
  tries = 60 #try for 1 hour to check the report
  while report_running and tries > 0:
    report = service.reports().get(reportId=report_id).execute()

    if report['isReportReady']:
      if project.verbose: print('Report Ready')
      report_running = False
      files = report['files']
    else:
      tries -= 1
      if project.verbose: print('Wait For DS Report')
      sleep(60)
  
  return files 


def report_read_data(auth, report_id, report_fragment):
   service = get_service('doubleclicksearch', 'v2', auth)

   return BytesIO(service.reports().getFile(reportId=report_id, reportFragment=report_fragment).execute())


def report_fetch(auth, report_id):
  service = get_service('doubleclicksearch', 'v2', auth)
  
  if project.verbose: print('Fetching Report', report_id)
  files = report_ready(service, report_id)
  
  reports = []
  i = 0
  for file in files:
    reports.append({'name': '%s_%d_%s.csv' % (report_id, i, str(date.today())), 'report_id': report_id, 'report_fragment': i})
   
  return reports


def report_get(auth, title, template_name='standard.json', parameters={}, day=date.today()):
  reports = []
  if 'ids' in parameters:
    report_ids = []
    if isinstance(parameters['ids'], str):
      for line in parameters['ids'].splitlines():
        items = line.split(',')
        parameters['agencyId'] = items[0]
        if len(items) == 2:
          parameters['advertiserId'] = items[1]
        report_ids.append(report_request(auth, title, template_name, parameters, day))
    else:
      for ids in parameters['ids']:
        pair = ids.split(':')
        parameters['agencyId'] = pair[0]
        if len(pair) == 2:
          parameters['advertiserId'] = pair[1]
        report_ids.append(report_request(auth, title, template_name, parameters, day))
    for report_id in report_ids:
      reports.append(report_fetch(auth, report_id['id']))
  else: 
    report = report_request(auth, title, template_name, parameters, day)
    reports.append(report_fetch(auth, report['id']))
  return reports


def report_to_rows(report):
  return list(csv.reader(report)) if report else []


def report_to_csv(rows):
  csv_string = StringIO()
  writer = csv.writer(csv_string, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  share_columns = []
  for row_number, row in enumerate(rows):
    if row_number == 0:
      for i, col in enumerate(row):
        if col.endswith('Share'):
          share_columns.append(i)
    
    for col in share_columns:
      if row[col] == '< 10%':
        row[col] = '0.099999'
      elif row[col] == '> 90%':
        row[col] = '0.900001'
   
    try: writer.writerow(row)
    except Exception as e: print('Error:', row_number, str(e), row)
  csv_string.seek(0) # important otherwise contents is zero
  return csv_string

 
#if __name__ == "__main__":
#  pass
