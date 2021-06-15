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
"""Reads weather information from the National Weather Service API

   (api.weather.gov) and outputs to a datastore such as BigQuery or sheets

"""

import json, datetime
from urllib.request import urlopen
from starthinker.util.data import put_rows

# Used to turn wind direction in degrees to compass directions
WIND_DIRECTION_MAP = {
    'NNE': {
        'f': 11.25,
        't': 33.75
    },
    'NE': {
        'f': 33.75,
        't': 56.25
    },
    'ENE': {
        'f': 56.25,
        't': 78.75
    },
    'E': {
        'f': 78.75,
        't': 101.25
    },
    'ESE': {
        'f': 101.25,
        't': 123.75
    },
    'SE': {
        'f': 123.75,
        't': 146.25
    },
    'SSE': {
        'f': 146.25,
        't': 168.75
    },
    'S': {
        'f': 168.75,
        't': 191.25
    },
    'SSW': {
        'f': 191.25,
        't': 213.75
    },
    'SW': {
        'f': 213.75,
        't': 236.25
    },
    'WSW': {
        'f': 236.25,
        't': 258.75
    },
    'W': {
        'f': 258.75,
        't': 281.25
    },
    'WNW': {
        'f': 281.25,
        't': 303.75
    },
    'NW': {
        'f': 303.75,
        't': 326.25
    },
    'NNW': {
        'f': 326.25,
        't': 348.75
    }
}

# Endpoint for last observation url of a given station
LATEST_OBSERVATION_URL = 'https://api.weather.gov/stations/%s/observations/latest'


def degrees_to_compass(value):
  """Turns direction from degrees value to compass direction

  Args:
    value: floating point representing the degrees from 0 to 360
  Returns: String representing the compass direction.
  """
  if value is None:
    return None

  if (value >= 348.75 and value <= 360) or (value >= 0 and value <= 11.25):
    return 'N'
  else:
    for direction in WIND_DIRECTION_MAP.keys():
      if value >= WIND_DIRECTION_MAP[direction][
          'f'] and value <= WIND_DIRECTION_MAP[direction]['t']:
        return direction

  return None


def c_to_f(temperature):
  """Converts temperature from celcius to fahrenheit

  Args:
    temperature: floating point representing the temperature in celcius
  Returns: temperature in fahrenheit
  """
  if temperature is None:
    return None

  return (temperature * 9 / 5) + 32


def ms_to_mph(value):
  """Converts speed from meters per second to miles per hour

  Args:
    value: floating point representing the speed in meters per second
  Returns: speed in miles per hour
  """
  if value is None:
    return None

  return value * 2.237


def m_to_mile(value):
  """Converts distance in meters to miles

  Args:
    value: floating point representing the distance in meters
  Returns: distance in miles
  """
  if value is None:
    return None

  return value / 1609


def m_to_inches(value):
  """Converts distance in meters to inches

  Args:
    value: floating point representing the distance in meters
  Returns: distance in inches
  """
  if value is None:
    return None

  return value / 39.37


def weather_gov(config, task):
  """Main StarThinker entrypoint for weather_gov task.

  "weather_gov": {
    "auth": "user",
    "stations": ["station1", "station2"],
    "out":{
      "sheets":{
        "sheet": "sheet URL",
        "tab": "Weather",
        "range": "A2:K",
        "delete": true
      }
    }
  }

  stations: list of strings representing the station ID. This is the NOAA
  station ID, the list can be found in the weather.gov API. For example, all
  major airports are NOAA observation stations, and their station ID typically
  is K followed by the unique airport ID. E.g. The Chicago O'Hare international
  airport observation stations ID is KORD, for San Francisco international
  airport it is KSFO, Miami KMIA, etc.

  out can be any output configuration supported by StarThinker, here we have a
  sheets output as an example.

  """
  if config.verbose:
    print('weather_gov')

  rows = []

  stations = task.get('stations', [])

  for station_id in stations:
    result = json.loads(urlopen(LATEST_OBSERVATION_URL % station_id).read())

    rows += [[
        datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), station_id,
        c_to_f(result['properties']['temperature']['value']),
        c_to_f(result['properties']['windChill']['value']),
        c_to_f(result['properties']['heatIndex']['value']),
        degrees_to_compass(result['properties']['windDirection']['value']),
        ms_to_mph(result['properties']['windSpeed']['value']),
        m_to_mile(result['properties']['visibility']['value']),
        result['properties']['relativeHumidity']['value'],
        m_to_inches(result['properties']['precipitationLast3Hours']['value']),
        'NOAA'
    ]]

  put_rows(config, task['auth'], task['out'], rows)
