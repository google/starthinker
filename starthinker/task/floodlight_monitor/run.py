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

"""Pulls floodlights from a sheet, checks if impressions have changed significantly and sends an alert email.

For example ( modify floodlight_monitor/test.json to include your account and sheet ):

python floodlight_monitor/run.py floodlight_monitor/test.json -u [user credentials path]

"""

from statistics import quantiles
from datetime import date, timedelta
from typing import Generator

from starthinker.util.cm import report_build, report_file, report_to_rows, report_clean, parse_account
from starthinker.util.sheets import sheets_tab_copy, sheets_read, sheets_url
from starthinker.util.csv import rows_to_type, rows_header_trim
from starthinker.util.email import send_email
from starthinker.util.email_template import EmailTemplate


FLOODLIGHT_DATE = 0
FLOODLIGHT_CONFIG_ID = 1
FLOODLIGHT_GROUP_ID = 2
FLOODLIGHT_ACTIVITY_GROUP = 3
FLOODLIGHT_ACTIVITY_ID = 4
FLOODLIGHT_ACTIVITY = 5
FLOODLIGHT_IMPRESSIONS = 6
FLOODLIGHT_STATUS = 7  # added by the script ( LOW, NORMAL, HIGH )

TRIGGER_ID = 0  # from source
TRIGGER_EMAIL = 1  # from source
TRIGGER_REPORT = 2  # added by this script


def floodlight_report(config, task:dict, floodlight_id: int) -> int:
  """ Create a report for a specific floodlight if it does not exist.

  Args:
    floodlight_id - the floodlight being monitored

  Returns:
    The id of the created report.
  """

  account_id, subaccount_id = parse_account(
    config,
    task['auth'],
    task['account']
  )

  name = 'Floodlight Monitor %s %s ( StarThinker )' % (
    account_id,
    floodlight_id
  )

  if config.verbose:
    print('FLOODLIGHT MONITOR REPORT: ', name)

  # create report if it does not exists
  report = report_build(
    config,
    task['auth'],
    task['account'],
    { 'kind': 'dfareporting#report',
      'type': 'FLOODLIGHT',
      'accountId': account_id,
      'name': name,
      'fileName': name.replace('( ', '').replace(' )', '').replace(' ', '_'),
      'format': 'CSV',
      'delivery': { 'emailOwner': False },
      'floodlightCriteria': {
        'dateRange': {
          'kind': 'dfareporting#dateRange',
          'relativeDateRange': 'LAST_7_DAYS'
        },
        'dimensions': [
          {'kind': 'dfareporting#sortedDimension','name': 'date' },
          { 'kind': 'dfareporting#sortedDimension', 'name': 'floodlightConfigId' },
          { 'kind': 'dfareporting#sortedDimension', 'name': 'activityGroupId' },
          { 'kind': 'dfareporting#sortedDimension', 'name': 'activityGroup' },
          { 'kind': 'dfareporting#sortedDimension', 'name': 'activityId' },
          { 'kind': 'dfareporting#sortedDimension', 'name': 'activity' }
        ],
        'floodlightConfigId': {
          'dimensionName': 'floodlightConfigId',
          'kind': 'dfareporting#dimensionValue',
          'matchType': 'EXACT',
          'value': floodlight_id
        },
        'metricNames': ['floodlightImpressions'],
        'reportProperties': {
          'includeUnattributedCookieConversions': False,
          'includeUnattributedIPConversions': False
        }
    },
    'schedule': {
        'active': True,
        'every': 1,
        'repeats': 'DAILY',
        'startDate': str(date.today()),
        'expirationDate': str((date.today() + timedelta(days=365))),
    },
  })

  return report['id']


def floodlight_rows(config, task:dict, report_id:int) -> Generator[list[str, str, str, str, str, str, int], None, None]:
  """ Monitor a report for completion and return rows

  Args:
    report_id - the report created earlier for a specific floodlight id.

  Returns:
    A stream of rows, see FLOODLIGHT_* constants for definitions.
  """

  # fetch report file if it exists
  filename, report = report_file(
    config,
    task['auth'],
    task['account'],
    report_id,
    None, # no name
    10 # wait up to 10 minutes for report to complete
  )

  # clean up rows
  rows = report_to_rows(report)
  rows = report_clean(rows)
  rows = rows_header_trim(rows)
  rows = rows_to_type(rows, column=6)

  return rows


def floodlight_analysis(config, task:dict, rows:Generator[list[str, str, str, str, str, str, int], None, None]) -> list[str, list[str, str, str, str, str, str, int, str]]:
  """ Perform outlier analysis and return last row by date with satatus indicator.

  Groups all floodlight data by activity, checking for ourliers using.
  See: http://www.mathwords.com/o/outlier.htm

  Args:
    rows - A stream of rows, see FLOODLIGHT_* constants for definitions.

  Returns:
    A date string for the last date as well as the last row for each activity with status appended (LOW, HIGH, NORMAL).
    Possibly None, None if no rows.
  """

  outliers_today = []
  activities = {}

  for row in rows:
    activities.setdefault(row[FLOODLIGHT_ACTIVITY_ID], []).append(row)

  for activity in activities.values():
    data = sorted(activity, key=lambda k: k[FLOODLIGHT_IMPRESSIONS])

    quartile_1, quartile_median, quartile_3 = quantiles(map(lambda d:d[FLOODLIGHT_IMPRESSIONS], data), n=4)
    quartile_range = quartile_3 - quartile_1
    outlier_top = quartile_3 + (1.5 * quartile_range)
    outlier_bottom = quartile_1 - (1.5 * quartile_range)
    last_day = max(data, key=lambda k:k[FLOODLIGHT_DATE])

    if last_day[FLOODLIGHT_IMPRESSIONS] == 0 or last_day[FLOODLIGHT_IMPRESSIONS] < outlier_bottom:
      last_day.append('LOW')
    elif last_day[FLOODLIGHT_IMPRESSIONS] > outlier_top:
      last_day.append('HIGH')
    else:
      last_day.append('NORMAL')

    outliers_today.append((
      last_day[FLOODLIGHT_DATE],
      last_day[FLOODLIGHT_CONFIG_ID],
      last_day[FLOODLIGHT_ACTIVITY_ID],
      last_day[FLOODLIGHT_ACTIVITY],
      last_day[FLOODLIGHT_IMPRESSIONS],
      last_day[FLOODLIGHT_STATUS],
    ))

  if len(outliers_today) > 0:
    return outliers_today[0][FLOODLIGHT_DATE], outliers_today
  else:
    return None, None


def floodlight_email(config, task:dict, day:str, alerts:dict[str, list[str, str, str, str, int, str]]) -> None:
  """ Send an email to each alert group with status of all activities.

  The email template will contain all activities for each email address specified in the input sheet.

  Args:
    day - the latest day that was present in all combined reports, used for title of email.
    alerts - Each email in the sheet with a list of activities and statuses.

  Returns:
    Nothing.
  """

  for email, table in alerts.items():

    # build email template
    t = EmailTemplate()
    t.align('center')
    t.section(True)

    # when floodlight alerts exist
    issues = sum(1 for row in table if row[5] != 'NORMAL')

    if issues > 0:
      subject = '%d Floodlight Alerts For %s' % (issues, day)
    else:
      subject = 'All Floodlights Normal For %s' % day

    t.header(subject)
    t.paragraph('The following floodlights are being monitored.  A status of LOW or HIGH inidcates impressions have changed significantly for the day.  A status of NORMAL means impressions are close to the average for the past 7 days.')
    t.table([
      { 'name': 'Date', 'type': 'STRING' },
      { 'name': 'Floodlight', 'type': 'STRING' },
      { 'name': 'Activity Id', 'type': 'STRING' },
      { 'name': 'Activity', 'type': 'STRING' },
      { 'name': 'Impressions', 'type': 'INTEGER' },
      { 'name': 'Status', 'type': 'STRING' },
    ], table)

    t.paragraph('Your monitored floodlights and recipients are listed in the sheet below.')

    # either way link to the configuration sheet
    t.button(
      'Floodlight Monitoring Sheet',
      sheets_url(config, task['auth'], task['sheet']['sheet']),
      big=True
    )
    t.section(False)

    if config.verbose:
      print('FLOODLIGHT MONITOR EMAIL ALERTS', email, len(table))

    # send email template
    send_email(
      config,
      task['auth'],
      email,
      None,
      None,
      subject,
      t.get_text(),
      t.get_html()
    )


def floodlight_monitor(config, task:dict) -> None:
  """ The task handler.  See module description.

  Args:
    Everuthing is passed using task.

  Returns:
    Nothing.
  """

  if config.verbose:
    print('FLOODLIGHT MONITOR')

  # make sure tab exists in sheet ( deprecated, use sheet task instead )
  if 'template' in task['sheet']:
    sheets_tab_copy(
      config,
      task['auth'],
      task['sheet']['template']['sheet'],
      task['sheet']['template']['tab'],
      task['sheet']['sheet'],
      task['sheet']['tab']
  )

  # read peers from sheet
  triggers = sheets_read(
    config,
    task['auth'],
    task['sheet']['sheet'],
    task['sheet']['tab'],
    task['sheet']['range']
  )

  if config.verbose and len(triggers) == 0:
    print('FLOODLIGHT MONITOR: No floodlight ids specified in sheet.')

  alerts = {}
  day = None

  # create reports first in parallel
  for trigger in triggers:
    trigger.append(floodlight_report(config, task, trigger[TRIGGER_ID]))

  # download data from all reports
  for trigger in triggers:

    # get report rows for each floodlight
    rows = floodlight_rows(config, task, trigger[TRIGGER_REPORT])

    # calculate outliers
    last_day, rows = floodlight_analysis(config, task, rows)

    if last_day:
      # find last day report ran
      day = last_day if day is None else max(day, last_day)

      # group alerts by email
      alerts.setdefault(trigger[TRIGGER_EMAIL], [])
      alerts[trigger[TRIGGER_EMAIL]].extend(rows)

  if alerts:
    floodlight_email(config, task, day, alerts)
