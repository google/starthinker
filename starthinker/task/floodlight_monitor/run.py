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

import pandas
from datetime import date, timedelta

from starthinker.util.project import project
from starthinker.util.dcm import report_build, report_file, report_to_rows, report_clean, parse_account
from starthinker.util.sheets import sheets_tab_copy, sheets_read, sheets_url
from starthinker.util.csv import rows_to_type, rows_header_trim
from starthinker.util.email.template import EmailTemplate
from starthinker.util.email import send_email
"""Pulls floodlights from a sheet, checks if impressions have changed significantly and sends an alert email.

For example ( modify floodlight_monitor/test.json to include your account and
sheet ):

python floodlight_monitor/run.py floodlight_monitor/test.json -u [user
credentials path]

"""


def floodlight_report(floodlight_id):

  account_id, subaccount_id = parse_account(project.task['auth'],
                                            project.task['account'])

  name = 'Floodlight Monitor %s %s ( StarThinker )' % (account_id,
                                                       floodlight_id)

  if project.verbose:
    print('FLOODLIGHT MONITOR REPORT: ', name)

  # create report if it does not exists
  report = report_build(
      project.task['auth'], project.task['account'], {
          'kind':
              'dfareporting#report',
          'type':
              'FLOODLIGHT',
          'accountId':
              account_id,
          'name':
              name,
          'fileName':
              name.replace('( ', '').replace(' )', '').replace(' ', '_'),
          'format':
              'CSV',
          'delivery': {
              'emailOwner': False
          },
          'floodlightCriteria': {
              'dateRange': {
                  'kind': 'dfareporting#dateRange',
                  'relativeDateRange': 'LAST_7_DAYS'
              },
              'dimensions': [{
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:date'
              }, {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:floodlightConfigId'
              }, {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:activityGroupId'
              }, {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:activityGroup'
              }, {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:activityId'
              }, {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:activity'
              }],
              'floodlightConfigId': {
                  'dimensionName': 'dfa:floodlightConfigId',
                  'kind': 'dfareporting#dimensionValue',
                  'matchType': 'EXACT',
                  'value': floodlight_id
              },
              'metricNames': ['dfa:floodlightImpressions'],
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


def floodlight_rows(report_id):

  # fetch report file if it exists
  filename, report = report_file(project.task['auth'], project.task['account'],
                                 report_id, None, 10)

  # clean up rows
  rows = report_to_rows(report)
  rows = report_clean(rows)
  rows = rows_header_trim(rows)
  rows = rows_to_type(rows, column=6)

  return rows


def floodlight_outliers(df_in, col_name):
  q1 = df_in[col_name].quantile(0.25)
  q3 = df_in[col_name].quantile(0.75)
  iqr = q3 - q1
  fence_low = q1 - 1.5 * iqr
  fence_high = q3 + 1.5 * iqr

  df_in['status'] = 'NORMAL'
  df_in.loc[df_in[col_name] < fence_low, 'status'] = 'LOW'
  df_in.loc[df_in[col_name] > fence_high, 'status'] = 'HIGH'

  return df_in


def floodlight_analysis(rows):

  df = pandas.DataFrame.from_records(
      rows,
      columns=[
          'date', 'floodlightConfigId', 'activityGroupId', 'activityGroup',
          'activityId', 'activity', 'impressions'
      ])

  try:
    # return only lowest quartile outliers for the last day ( don't flag outliers from past days )
    last_day = pandas.to_datetime(df['date']).max().strftime('%Y-%m-%d')
    outliers = floodlight_outliers(
        df[[
            'date', 'floodlightConfigId', 'activityId', 'activity',
            'impressions'
        ]], 'impressions').values.tolist()
    outliers_today = [o for o in outliers if o[0] == last_day]
  except ValueError:
    print('No data available.')
    return None, None

  return last_day, outliers_today


def floodlight_email(day, alerts):

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
    t.paragraph(
        'The following floodlights are being monitored.  A status of LOW or HIGH inidcates impressions have changed significantly for the day.  A status of NORMAL means impressions are close to the average for the past 7 days.'
    )
    t.table([
        {
            'name': 'Date',
            'type': 'STRING'
        },
        {
            'name': 'Floodlight',
            'type': 'STRING'
        },
        {
            'name': 'Activity Id',
            'type': 'STRING'
        },
        {
            'name': 'Activity',
            'type': 'STRING'
        },
        {
            'name': 'Impressions',
            'type': 'INTEGER'
        },
        {
            'name': 'Status',
            'type': 'STRING'
        },
    ], table)

    t.paragraph(
        'Your monitored floodlights and recipients are listed in the sheet below.'
    )

    # either way link to the configuration sheet
    t.button(
        'Floodlight Monitoring Sheet',
        sheets_url(project.task['auth'], project.task['sheet']['sheet']),
        big=True)
    t.section(False)

    if project.verbose:
      print('FLOODLIGHT MONITOR EMAIL ALERTS', email, len(table))

    # send email template
    send_email(project.task['auth'], email, None, None, subject, t.get_text(),
               t.get_html())


@project.from_parameters
def floodlight_monitor():
  if project.verbose:
    print('FLOODLIGHT MONITOR')

  # make sure tab exists in sheet ( deprecated, use sheet task instead )
  if 'template' in project.task['sheet']:
    sheets_tab_copy(project.task['auth'],
                    project.task['sheet']['template']['sheet'],
                    project.task['sheet']['template']['tab'],
                    project.task['sheet']['sheet'],
                    project.task['sheet']['tab'])

  # read peers from sheet
  triggers = sheets_read(project.task['auth'], project.task['sheet']['sheet'],
                         project.task['sheet']['tab'],
                         project.task['sheet']['range'])
  # 0 - Floodlight Id
  # 1 - email
  # 2 - dcm report id ( added by this script )
  # 3 - status, added by the script ( LOW, NORMAL, HIGH )

  if project.verbose and len(triggers) == 0:
    print('FLOODLIGHT MONITOR: No floodlight ids specified in sheet.')

  alerts = {}
  day = None

  # create reports first in parallel
  for trigger in triggers:
    trigger.append(floodlight_report(trigger[0]))

  # download data from all reports
  for trigger in triggers:

    # get report rows for each floodlight
    rows = floodlight_rows(trigger[2])

    # calculate outliers
    last_day, rows = floodlight_analysis(rows)

    if last_day:
      # find last day report ran
      day = last_day if day is None else max(day, last_day)

      # group alerts by email
      alerts.setdefault(trigger[1], [])
      alerts[trigger[1]].extend(rows)

  if alerts:
    floodlight_email(day, alerts)


if __name__ == '__main__':
  floodlight_monitor()
