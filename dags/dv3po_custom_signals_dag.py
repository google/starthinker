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
#
#  This code generated (see starthinker/scripts for possible source):
#    - Command: "python starthinker_ui/manage.py airflow"
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

DV-3PO Custom Signals

DV-3PO Custom Signals allows automated changes to be made to DV360 campaigns based on external signals from weather and social media trends. In the future it will also support news, disaster alerts, stocks, sports, custom APIs, etc.

  - Open the template sheet: <a target='_blank' href='https://docs.google.com/spreadsheets/d/1JYtVL3teV_4Jr2Bi_tS8v0Uq-I44r78hFbmveloxd2I'>[DV-3PO] Custom Signals Configs</a>.
  - Make a copy of the sheet through the menu File -> Make a copy, for clarity we suggest you rename the copy to a meaningful name describing the usage of this copy.
  - In the Station IDs field below enter a comma separated list of NOAA weather station IDs. Most major airports are stations and their ID typically is K followed by the 3 letter airport code, e.g. KORD for Chicago O'Hare International Airport, KSFO for San Francisco international airport, etc. You can get a full list of stations <a target='_blank' href='https://www1.ncdc.noaa.gov/pub/data/noaa/isd-history.txt'>here</a>, the station ID to use is the 'CALL' column of this list.
  - In the Sheet URL field below, enter the URL of the copy of the config sheet you've created.
  - Go to the sheet and configure the rules you'd like to be applied in the Rules tab.
  - In the Advertiser ID column, enter the advertiser ID of the line items you'd like to automatically update.
  - In the Line Item ID colunn, enter the line item ID of the line item you'd like to automatically update.
  - The 'Active' column of the Rules tab allows you to control if the line item should be active or paused. If this field is TRUE the line item will be set to active, if this field is FALSE the line item will be set to inactive. You can use a formula to take weather data into consideration to update this field, e.g. =IF(Weather!C2>30, TRUE, FALSE) will cause the line item to be activated if the temperature of the first station in the Weather tab is above 30 degrees. Leave this field empty if you don't want it to be modified by the tool.
  - The 'Fixed Bid' column of the Rules tab allows you to control the fixed bid amount of the line item. The value set to this field will be applied to the specified line item. You can use a formula to take weather data into consideration to update this field, e.g. =IF(Weather!G2>3, 0.7, 0.4) will cause bid to be set to $0.7 if the wind speed of the first line in the Weather tab is greater than 3 mph, or $0.4 otherwise. Leave this field empty if you don't want it to be modified by the tool.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'station_ids':'',  # NOAA Weather Station ID
  'auth_read':'user',  # Credentials used for reading data.
  'sheet_url':'',  # Feed Sheet URL
}

RECIPE = {
  'setup':{
    'day':[
      'Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'
    ],
    'hour':[
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23
    ]
  },
  'tasks':[
    {
      'weather_gov':{
        'auth':'user',
        'stations':{'field':{'name':'station_ids','kind':'string_list','order':1,'description':'NOAA Weather Station ID','default':''}},
        'out':{
          'sheets':{
            'sheet':{'field':{'name':'sheet_url','kind':'string','order':2,'description':'Feed Sheet URL','default':''}},
            'tab':'Weather',
            'range':'A2:K',
            'delete':True
          }
        }
      }
    },
    {
      'lineitem_beta':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':1,'default':'user','description':'Credentials used for reading data.'}},
        'read':{
          'sheet':{
            'sheet':{'field':{'name':'sheet_url','kind':'string','order':2,'description':'Feed Sheet URL','default':''}},
            'tab':'Rules',
            'range':'A1:D'
          }
        },
        'patch':{
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dv3po_custom_signals', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
