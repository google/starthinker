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
#
#  This code generated (see scripts folder for possible source):
#    - Command: "python starthinker_ui/manage.py example"
#
###########################################################################

import argparse
import textwrap

from starthinker.util.configuration import Configuration
from starthinker.task.weather_gov.run import weather_gov
from starthinker.task.lineitem_beta.run import lineitem_beta


def recipe_dv3po_custom_signals(config, station_ids, auth_read, sheet_url):
  """DV-3PO Custom Signals allows automated changes to be made to DV360 campaigns
     based on external signals from weather and social media trends. In the
     future it will also support news, disaster alerts, stocks, sports, custom
     APIs, etc.

     Args:
       station_ids (string_list) - NOAA Weather Station ID
       auth_read (authentication) - Credentials used for reading data.
       sheet_url (string) - Feed Sheet URL
  """

  weather_gov(config, {
    'auth':'user',
    'stations':station_ids,
    'out':{
      'sheets':{
        'sheet':sheet_url,
        'tab':'Weather',
        'range':'A2:K',
        'delete':True
      }
    }
  })

  lineitem_beta(config, {
    'auth':auth_read,
    'read':{
      'sheet':{
        'sheet':sheet_url,
        'tab':'Rules',
        'range':'A1:D'
      }
    },
    'patch':{
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      DV-3PO Custom Signals allows automated changes to be made to DV360 campaigns based on external signals from weather and social media trends. In the future it will also support news, disaster alerts, stocks, sports, custom APIs, etc.

        1. Open the template sheet: <a target='_blank' href='https://docs.google.com/spreadsheets/d/1JYtVL3teV_4Jr2Bi_tS8v0Uq-I44r78hFbmveloxd2I'>[DV-3PO] Custom Signals Configs</a>.
        2. Make a copy of the sheet through the menu File -> Make a copy, for clarity we suggest you rename the copy to a meaningful name describing the usage of this copy.
        3. In the Station IDs field below enter a comma separated list of NOAA weather station IDs. Most major airports are stations and their ID typically is K followed by the 3 letter airport code, e.g. KORD for Chicago O'Hare International Airport, KSFO for San Francisco international airport, etc. You can get a full list of stations <a target='_blank' href='https://www1.ncdc.noaa.gov/pub/data/noaa/isd-history.txt'>here</a>, the station ID to use is the 'CALL' column of this list.
        4. In the Sheet URL field below, enter the URL of the copy of the config sheet you've created.
        5. Go to the sheet and configure the rules you'd like to be applied in the Rules tab.
        6. In the Advertiser ID column, enter the advertiser ID of the line items you'd like to automatically update.
        7. In the Line Item ID colunn, enter the line item ID of the line item you'd like to automatically update.
        8. The 'Active' column of the Rules tab allows you to control if the line item should be active or paused. If this field is TRUE the line item will be set to active, if this field is FALSE the line item will be set to inactive. You can use a formula to take weather data into consideration to update this field, e.g. =IF(Weather!C2>30, TRUE, FALSE) will cause the line item to be activated if the temperature of the first station in the Weather tab is above 30 degrees. Leave this field empty if you don't want it to be modified by the tool.
        9. The 'Fixed Bid' column of the Rules tab allows you to control the fixed bid amount of the line item. The value set to this field will be applied to the specified line item. You can use a formula to take weather data into consideration to update this field, e.g. =IF(Weather!G2>3, 0.7, 0.4) will cause bid to be set to $0.7 if the wind speed of the first line in the Weather tab is greater than 3 mph, or $0.4 otherwise. Leave this field empty if you don't want it to be modified by the tool.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-station_ids", help="NOAA Weather Station ID", default='')
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-sheet_url", help="Feed Sheet URL", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dv3po_custom_signals(config, args.station_ids, args.auth_read, args.sheet_url)
