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

import re
import pytz
from datetime import date, datetime


RE_LOOKUP = re.compile(r' - (\d+)$')
def lookup_id(lookup):
  result = RE_LOOKUP.search(lookup)
  return result.group(1) if result else None


def date_to_str(value):
  if value is None:
    return None
  else:
    return value.strftime('%Y-%m-%d')


def str_to_date(value):
  if value is None:
    return None
  else:
    return datetime.strptime(value, '%Y-%m-%d').date()


# multiplier is used for milliseconds ( 1000 ) etc...
def datetime_to_epoch(datetime_utc, multiplier=1):
  if datetime_utc is None:
    return None
  else:
    return (datetime_utc - datetime(1970, 1, 1)).total_seconds() * multiplier


# multiplier is used for milliseconds ( 1000 ) etc...
def epoch_to_datetime(epoch_seconds, multiplier=1):
  if epoch_seconds is None:
    return None
  else:
    return datetime.fromtimestamp(int(epoch_seconds) / multiplier, pytz.utc)


RE_YYYYMMDD = re.compile(r'\d{4}[-/_]\d{2}[-/_]\d{2}')


def parse_yyyymmdd(text):
  value = (RE_YYYYMMDD.findall(text) or [None])[0]
  return value


RE__YYYYMMDD = re.compile(r'_?\d{4}[-/]\d{2}[-/]\d{2}')


def strip_yyymmdd(text):
  return RE__YYYYMMDD.sub('', text)


RE_URL = re.compile(r'https?://[^\s\'">]+')


def parse_url(text):
  return RE_URL.findall(text)


RE_DBM_REPORT = re.compile(r'\d{13}_report/')


def parse_dbm_report_id(download_url):
  return (RE_DBM_REPORT.findall(download_url) or
          [''])[0].replace('_report/', '')


RE_ALPHA_NUMERIC = re.compile('([^\s\w]|_)+')


def parse_filename(text):
  return RE_ALPHA_NUMERIC.sub('', text).lower().replace(' ', '_')


#RE_TABLE = re.compile(r'[\[`]([-\w]+)[:\.]([-\w]+)\.([-\w]+)[\]`]')
