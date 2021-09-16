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

from datetime import timedelta
from time import sleep
import typing

from starthinker.util.csv import column_header_sanitize, csv_to_rows
from starthinker.util.google_api import API_SearchAds
from starthinker.util.sa_fields import SA_FIELDS


SA_TYPES = {
  'String':'STRING',
  'Integer':'INTEGER',
  'Boolean':'BOOLEAN',
  'Date':'DATE',
  'ID':'STRING',
  'Money':'FLOAT',
  'Number':'INTEGER',
  'Timestamp':'TIMESTAMP'
}


class SA_Report():
  '''Implement report donwload functionality for Search Ads.

  SA360 cannot list reports, so ID is tied to report creation.
  Class supports providing a reportID but is intended to be used as:
  Report is downloaded asynchrnously to allow wider felxibility.

   ```
   report = SA_Report(config, task['auth'])
   report.request(**task['kwargs'])
   rows = report.get_rows()
   ```

  Handles all serialization, and pagination, and schema convesion.

  '''

  def __init__(self, config, auth:str) -> None:
    '''Construct a report factory, providing project and authentication data.

    This class will track the reportID internally if the request call is used.

    Args:
     config, required - see: starthinker/util/configuration.py
     auth, required - either "user" or "service" used to create and/or read the report.

    Returns: None

  '''
    self.config = config
    self.auth = auth
    self.columns = SA_FIELDS
    self.reportId = None


  def column_type(self, agencyId:int, advertiserId:int, column:str) -> str:
    '''Return the column type for the given column name.

    Intended mostly as an internl helper function but left open for convenience.
    Leverages both saved columns and standard columns.
    Does not distinguish saved from standard, will this be a problem?

    Args:
     agencyId - required only for saved columns, usually derived from report
     advertiserid - required only for saved columns, usually derived from report

    Returns:
     Column type as defnined by BigQuery. Defaults to STRING if not found.

    '''

    if column not in self.columns:
      for saved_column in API_SearchAds(self.config, self.auth, iterate=True).savedcolumns().list(agencyId=agencyId, advertiserId=advertiserId).execute():
        self.columns[saved_column['savedColumnName']] = SA_TYPES.get(saved_column['type'], 'STRING')
    return self.columns.get(column, 'STRING')


  def request(self, body:dict) -> dict:
    '''Create a new SA360 report and return its JSON definition.

    If report is missing, date it will be added.
    Also added relativeTimeRange pattern from CM/DV reporting. If present, timeRange will be created.

    Args:
      body - required, the JSON definition of a report: https://developers.google.com/search-ads/v2/reference/reports

    Returns:
      A dictionary defining the newly created report and status.

    '''

    if 'relativeTimeRange' in body:
      # Not implemented:
      # WEEK_TO_DATE
      # MONTH_TO_DATE
      # QUARTER_TO_DATE
      # YEAR_TO_DATE
      # PREVIOUS_WEEK
      # PREVIOUS_MONTH
      # PREVIOUS_QUARTER
      # PREVIOUS_YEAR

      if body['relativeTimeRange'] == 'TODAY':
        body['timeRange'] = { 'startDate':self.config.date, 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'YESTERDAY':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=1), 'endDate':self.config.date  - timedelta(days=1) }
      elif body['relativeTimeRange'] == 'LAST_7_DAYS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=6), 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'LAST_14_DAYS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=13), 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'LAST_30_DAYS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=29), 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'LAST_60_DAYS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=59), 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'LAST_90_DAYS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=89), 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'LAST_365_DAYS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=364), 'endDate':self.config.date }
      elif body['relativeTimeRange'] == 'LAST_24_MONTHS':
        body['timeRange'] = { 'startDate':self.config.date - timedelta(days=729), 'endDate':self.config.date }

      del body['relativeTimeRange']


    self.reportId = API_SearchAds(self.config, self.auth).reports().request(body=body).execute()['id']
    return self.reportId


  def get_rows(self, reportId:int=None, timeout:int=60*3) -> typing.Iterator[dict]:
    '''Return each row of data from a report as a generator.

    Wait up to 3 hours with 1 minute poll intervals for report to finish.
    Handle fragmented downloads.

    Args:
     reportId - optional,  if not given uses prior value from request(...) call.
     timeout - optional, number of minutes to wait for report to complete.

    Returns:
     Generator with lists of column values.

    '''

    if reportId is None: reportId = self.reportId

    while (timeout > 0):
      report = API_SearchAds(self.config, self.auth).reports().get(reportId=reportId).execute()
      if report['isReportReady']:
        for fragment in range(len(report['files'])):
          rows = csv_to_rows(API_SearchAds(self.config, self.auth).reports().getFile(reportId=reportId, reportFragment=fragment).execute())
          if fragment > 0: next(rows) # skip header in all subsequent fragments
          yield from rows
        break
      else:
        if self.config.verbose:
          print('.', end='')
        sleep(60)
        timeout -= 1


  def get_schema(self, reportId:int=None) -> list:
    '''Read columns from report and produce BigQuery compatible schema.

    Columns with an unknown type default to STRING.

    Args:
     reportId - optional,  if not given uses prior value from request(...) call.

    Returns:
     List of BigQuery schema fields derived from report columns.

    '''

    if reportId is None: reportId = self.reportId

    schema = []
    report = API_SearchAds(self.config, self.auth).reports().get(reportId=reportId).execute()

    for column in report['request']['columns']:
      name = column.get('columnName', column.get('savedColumnName'))
      schema.append({
        'name': column_header_sanitize(name),
        'type':self.column_type(report['request']['reportScope']['agencyId'],report['request']['reportScope']['advertiserId'], name),
        'mode': 'NULLABLE'
      })

    return schema
