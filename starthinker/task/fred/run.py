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


def fred_series(**kwargs):
  kwargs['file_type'] = 'json'

  url = 'https://api.stlouisfed.org/fred/series/observations?' + urlencode(kwargs)
  for observation in json.loads(urlopen(url).read().decode('UTF-8'))['observations']:
    yield [
      observation['realtime_start'],
      observation['realtime_end'],
      observation['date'],
      observation['value']
    ]


def fred_regional(**kwargs):
  kwargs['file_type'] = 'json'
  kwargs['start_date'] = str(project.date)

  url = 'https://api.stlouisfed.org/geofred/regional/data?' + urlencode(kwargs)
  for observation in json.loads(urlopen(url).read().decode('UTF-8'))['observations']:
    yield [
      observation['region'],
      observation['code'],
      observation['date'],
      observation['series_id']
    ]


@project.from_parameters
def fred():

  if 'series_id' in project.task['parameters']:
    rows = fred_series(**project.task['parameters'])
    if 'bigquery' in project.task['out']:
      project.task['out']['bigquery']['schema'] = [
        { "name":"realtime_start", "type":"DATE", "mode":"REQUIRED" },
        { "name":"realtime_end", "type":"DATE", "mode":"REQUIRED" },
        { "name":"day", "type":"DATE", "mode":"REQUIRED" },
        { "name":"value", "type":"FLOAT", "mode":"REQUIRED" }
      ]

  elif 'series_group' in project.task['parameters']:
    rows = fred_regional(**project.task['parameters'])
    if 'bigquery' in project.task['out']:
      project.task['out']['bigquery']['schema'] = [
        { "name":"region", "type":"STRING", "mode":"REQUIRED" },
        { "name":"code", "type":"INTEGER", "mode":"REQUIRED" },
        { "name":"series_id", "type":"STRING", "mode":"REQUIRED" },
        { "name":"value", "type":"FLOAT", "mode":"REQUIRED" }
      ]
  else:
    raise Excpetion("MISSING CONFIGURATION: Specify either series_id or series_group.")

  put_rows(project.task['auth'], project.task['out'], rows)


if __name__ == "__main__":
  fred()
