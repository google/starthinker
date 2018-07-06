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


import pandas
from datetime import date, timedelta


from util.project import project 
from util.dcm import report_build, report_file, report_to_rows, report_clean, parse_account, DCM_CHUNK_SIZE
from util.sheets import sheets_tab_copy, sheets_read
from util.csv import rows_to_type, rows_header_trim
from util.email.template import EmailTemplate
from util.email import send_email


"""Pulls floodlights from a sheet, checks if impressions have changed significantly and sends an alert email.

For example ( modify floodlight_monitor/test.json to include your account and sheet ):

python floodlight_monitor/run.py floodlight_monitor/test.json -u [user credentials path]

"""


def floodlight_report(floodlight_id):

  account_id, subaccount_id, profile_id = parse_account(project.task['auth'], project.task['account'])

  name = 'Floodlight Monitor %s %s ( StarThinker )' % ( account_id, floodlight_id )

  if project.verbose: print "FLOODLIGHT MONITOR REPORT: ", name

  # create report if it does not exists
  report = report_build(
    project.task['auth'], 
    project.task['account'], 
    { 
      'kind': 'dfareporting#report',
      'type': 'FLOODLIGHT',
      'accountId': account_id,
      'ownerProfileId': profile_id,
      'name': name,
      'fileName': name.replace('( ', '').replace(' )', '').replace(' ', '_'),
      'format': 'CSV',
      'delivery': {
        'emailOwner': False
      },
      'floodlightCriteria': {
        'dateRange': {
          'kind': 'dfareporting#dateRange',
          'relativeDateRange': 'LAST_7_DAYS'
        },
        'dimensions': [
          {'kind': 'dfareporting#sortedDimension', 'name': 'dfa:date'},
          {'kind': 'dfareporting#sortedDimension', 'name': 'dfa:floodlightConfigId'},
          {'kind': 'dfareporting#sortedDimension', 'name': 'dfa:activityGroupId'},
          {'kind': 'dfareporting#sortedDimension', 'name': 'dfa:activityGroup'},
          {'kind': 'dfareporting#sortedDimension', 'name': 'dfa:activityId'},
          {'kind': 'dfareporting#sortedDimension', 'name': 'dfa:activity'}
        ],
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
        'startDate':str(date.today()),
        'expirationDate':str((date.today() + timedelta(days=365))),
      },
    }
  )

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, report = report_file(
    project.task['auth'],
    project.task['account'],
    report['id'],
    None,
    0,
    DCM_CHUNK_SIZE
  )

  return report


def floodlight_outliers(df_in, col_name):
  q1 = df_in[col_name].quantile(0.25)
  q3 = df_in[col_name].quantile(0.75)
  iqr = q3-q1 
  fence_low  = q1-1.5*iqr
  #fence_high = q3+1.5*iqr
  #df_out = df_in.loc[(df_in[col_name] < fence_low) | (df_in[col_name] > fence_high)]
  df_out = df_in.loc[(df_in[col_name] < fence_low)]
  #return df_in # for debug
  return df_out


def floodlight_analysis(rows):

  df = pandas.DataFrame.from_records(
    rows,
    columns=['date', 'floodlightConfigId', 'activityGroupId', 'activityGroup', 'activityId', 'activity', 'impressions']
  )

  # return only lowest quartile outliers for the last day ( don't flag outliers from past days )
  last_day = pandas.to_datetime(df['date']).max().strftime('%Y-%m-%d')
  outliers = floodlight_outliers(df[['date', 'floodlightConfigId', 'activityId', 'activity', 'impressions']], 'impressions').values.tolist()
  outliers_today = [o for o in outliers if o[0] == last_day]

  return last_day, outliers_today


def floodlight_email(day, alerts):

  for email, table in alerts.items():

    # build email template
    t = EmailTemplate();

    # when floodlight alerts exist
    if table:
      subject = '%d Floodlight Alerts For %s' % (len(table), day)
      t.header(subject)
      t.paragraph('For the following floodlights, there are suspiciously low impressions. Please check their configurations.')
      t.table(
        [
          { "name":"Date", "type":"STRING" },
          { "name":"Floodlight", "type":"STRING" },
          { "name":"Activity Id", "type":"STRING" },
          { "name":"Activity", "type":"STRING" },
          { "name":"Impressions", "type":"INTEGER" },
        ],
        table
      )

    # when everything is OK
    else:
      subject = 'All Floodlights Normal For %s' % day
      t.header(subject)
      t.paragraph('Impressions all look within statistically expected range.')

    # either way link to the configuration sheet
    t.button('Floodlight Monitoring Sheet', project.task['sheet']['url'], big=True)

    if project.verbose: print "FLOODLIGHT MONITOR EMAIL ALERTS", email, len(table)

    # send email template
    send_email(
      project.task['auth'], 
      email, 
      None, 
      None, 
      subject,
      t.get_text(), 
      t.get_html()
    )


def floodlight_monitor():
  if project.verbose: print "FLOODLIGHT MONITOR"

  # make sure tab exists in sheet
  sheets_tab_copy(
    project.task['auth'],
    project.task['sheet']['template']['url'],
    project.task['sheet']['template']['tab'],
    project.task['sheet']['url'],
    project.task['sheet']['tab'])

  # read peers from sheet
  triggers = sheets_read(
    project.task['auth'],
    project.task['sheet']['url'],
    project.task['sheet']['tab'],
    project.task['sheet']['range']
  )
  # 0 - Floodlight Id
  # 1 - email

  if project.verbose and len(triggers) == 0: print "FLOODLIGHT MONITOR: No floodlight ids specified in sheet."

  alerts = {}
  day = None

  for trigger in triggers:

    # get report data for each floodlight
    report = floodlight_report(trigger[0])
    rows = report_to_rows(report)
    rows = report_clean(rows)
    rows = rows_header_trim(rows)
    rows = rows_to_type(rows, column=6)
 
    # calculate outliers
    last_day, rows = floodlight_analysis(rows)

    # find last day report ran
    day = last_day if day is None else max(day, last_day)

    # group alerts by email
    alerts.setdefault(trigger[1], [])
    alerts[trigger[1]].extend(rows)

  floodlight_email(day, alerts)


if __name__ == "__main__":
  project.load('floodlight_monitor')
  floodlight_monitor()
