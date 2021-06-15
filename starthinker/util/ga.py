###########################################################################
#
#  Copyright 2021 Google LLC
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

#https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/

import datetime
import typing

from starthinker.util.csv import column_header_sanitize, csv_to_rows, rows_to_csv, response_utf8_stream
from starthinker.util.google_api import API_AnalyticsReporting


class GA_Report():
  """ Implement report donwload functionality for Google Analytics.

  Accepts a body definition per the API doc:
  https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#ReportRequest

  TODO: Add support for pivot and histogram.

  Handles all serialization, and pagination, providing both rows and schema.
  """

  def __init__(self, config, auth:str, reportRequests:list, useResourceQuotas:bool) -> None:
    self.config = config
    self.auth = auth
    self.body = {
      "reportRequests":reportRequests,
      "useResourceQuotas":useResourceQuotas
    }
    self.schema = None


  def get_reports(self) -> typing.Iterator[dict]:
    response = API_AnalyticsReporting(self.config, self.auth).reports().batchGet(body=self.body).execute()

    while response:
      next_body = {
        "reportRequests":[],
        "useResourceQuotas":self.body["useResourceQuotas"]
      }

      for index, report in enumerate(response.get('reports', [])):
        if self.schema is None:
          self.set_schema(report.get('columnHeader', {}))

        yield report

        if 'nextPageToken' in report:
          next_body["reportRequests"].append(body["reportRequests"][index])

      if next_body["reportRequests"]:
        self.body = next_body
        respone = API_AnalyticsReporting(self.config, self.auth).reports().batchGet(body=self.body).execute()
      else:
        response = None


  def get_date(self, date_string:str) -> datetime.date:
    if date_string == 'today':
      return datetime.date.today()
    elif date_string == 'yesterday':
      return datetime.date.today() - datetime.timedelta(days=1)
    elif date_string.endswith('daysAgo'):
      return datetime.date.today() - datetime.timedelta(days=int(date_string.replace('daysAgo', '')))
    else:
      return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()


  def get_dates(self) -> list:
    report_dates = []

    for report in self.body['reportRequests']:
      dates = []
      for date_range in report['dateRanges']:
        date_start = self.get_date(date_range['startDate'])
        date_end = self.get_date(date_range['endDate'])

        while date_start <= date_end:
          dates.append(date_start)
          date_start += datetime.timedelta(days=1)

      report_dates.append(dates)

    return report_dates


  def set_schema(self, columnHeader:dict) -> None:
    dimensions = [{
      'name':d.replace('ga:', ''),
      'type':'STRING',
      'mode':'REQUIRED',
    } for d in columnHeader.get("dimensions", [])]

    metrics = [{
      'name':m['name'].replace('ga:', ''),
      'type':m['type'],
      'mode':'NULLABLE',
    } for m in columnHeader.get("metricHeader", {}).get("metricHeaderEntries", [])]

    self.schema = []
    if dimensions:
      self.schema.append({
        "name": "Dimensions",
        "type": "RECORD",
        "mode": "REQUIRED",
        "fields": dimensions
      })
    if metrics:
      self.schema.append({
        "name": "Metrics",
        "type": "RECORD",
        "mode": "REQUIRED",
        "fields": metrics
      })


  def get_schema(self) -> list:
    return self.schema


  def get_rows(self) -> typing.Iterator[dict]:

    for index, report in enumerate(self.get_reports()):
      columnHeader = report.get("columnHeader", {})
      dimensionHeaders = [h.replace('ga:', '') for h in columnHeader.get("dimensions", [])]
      metricHeaders = [h['name'].replace('ga:', '') for h in columnHeader.get("metricHeader", {}).get("metricHeaderEntries", [])]
      rows = report.get("data", {}).get("rows", [])
      dates = self.get_dates()

      for row in rows:
        dimensions = row.get("dimensions", [])
        dateRangeValues = row.get("metrics", [])
        row_dimensions = dict(zip(dimensionHeaders, dimensions))

        for i, values in enumerate(dateRangeValues):
          yield {
            'Report_Day':str(dates[index][i]),
            'Dimensions':row_dimensions,
            'Metrics':dict(zip(metricHeaders, values.get("values")))
          }
