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

from starthinker.util.data import get_rows


def weather_gov_test(config, task):
  print('testing weather_gov connector')

  if 'verify' in task['weather_gov']:
    rows = get_rows(config, task['auth'],
                    task['weather_gov']['verify']['read'])
    station_ids = task['weather_gov']['verify']['station_ids']

    for idx, row in enumerate(rows):
      if row[1] != station_ids[idx]:
        raise 'Station weather data not loaded correctly'
