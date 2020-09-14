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

import json
from urllib.request import urlopen
from urllib.parse import urlencode

from starthinker.util.project import project
from starthinker.util.data import put_rows


def fred_series(api_key, frequency, **kwargs):
  kwargs['api_key'] = api_key
  kwargs['frequency'] = frequency
  kwargs['file_type'] = 'json'

  url = 'https://api.stlouisfed.org/fred/series/observations?' + urlencode(
      kwargs)
  for observation in json.loads(
      urlopen(url).read().decode('UTF-8'))['observations']:
    yield [
        observation['realtime_start'], observation['realtime_end'],
        observation['date'], observation['value']
    ]


def fred_regional(api_key, frequency, region, **kwargs):
  kwargs['api_key'] = api_key
  kwargs['frequency'] = frequency
  kwargs['region_type'] = region_type
  kwargs['file_type'] = 'json'
  kwargs['start_date'] = str(project.date)

  url = 'https://api.stlouisfed.org/geofred/regional/data?' + urlencode(kwargs)
  for observation in json.loads(
      urlopen(url).read().decode('UTF-8'))['observations']:
    yield [
        observation['region'], observation['code'], observation['date'],
        observation['series_id']
    ]


@project.from_parameters
def fred():

  if 'series' in project.task:

    for parameters in project.task['series']:

      name = 'FRED_SERIES_%s' % parameters['series_id']
      rows = fred_series(project.task['api_key'], project.task['frequency'],
                         **parameters)

      if 'bigquery' in project.task['out']:
        project.task['out']['bigquery']['schema'] = [{
            'name': 'realtime_start',
            'type': 'DATE',
            'mode': 'REQUIRED'
        }, {
            'name': 'realtime_end',
            'type': 'DATE',
            'mode': 'REQUIRED'
        }, {
            'name': 'day',
            'type': 'DATE',
            'mode': 'REQUIRED'
        }, {
            'name': 'value',
            'type': 'FLOAT',
            'mode': 'REQUIRED'
        }]

  elif 'regions' in project.task:
    for parameters in project.task['regions']:

      name = 'FRED_SERIES_%s' % parameters['series_group']
      rows = fred_regional(project.task['api_key'], project.task['frequency'],
                           project.task['region_type'], **parameters)

      if 'bigquery' in project.task['out']:
        project.task['out']['bigquery']['schema'] = [{
            'name': 'region',
            'type': 'STRING',
            'mode': 'REQUIRED'
        }, {
            'name': 'code',
            'type': 'INTEGER',
            'mode': 'REQUIRED'
        }, {
            'name': 'series_id',
            'type': 'STRING',
            'mode': 'REQUIRED'
        }, {
            'name': 'value',
            'type': 'FLOAT',
            'mode': 'REQUIRED'
        }]

  else:
    raise Excpetion(
        'MISSING CONFIGURATION: Specify either series_id or series_group.')

  put_rows(project.task['auth'], name, rows)


if __name__ == '__main__':
  fred()
