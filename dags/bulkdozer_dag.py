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

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu	
    l) Install All

--------------------------------------------------------------

Bulkdozer

Bulkdozer is a tool that can reduce trafficking time in Campaign Manager by up to 80%% by providing automated bulk editing capabilities.

Open the <a href='https://docs.google.com/spreadsheets/d/10YewffRUP1gCxTY0ZLTkVEfzmOQ1gPXPxp7qev3w8xk/edit?usp=sharing' target='_blank'>Bulkdozer 0.27</a> feed.
Make your own copy of the feed by clicking the File -> Make a copy... menu in the feed.
Give it a meaninful name including the version, your name, and team to help you identify it and ensure you are using the correct version.
Under the Account ID field below, enter the your Campaign Manager Network ID.
Under Sheet URL, enter the URL of your copy of the feed that you just created in the steps above.
Go to the Store tab of your new feed, and enter your profile ID in the profileId field (cell B2). Your profile ID is visible in Campaign Manager by clicking your avatar on the top right corner.
Click the 'Save' button below.
After clicking 'Save', copy this page's URL from your browser address bar, and paste it in the Store tab for the recipe_url field (cell B5) your sheet.
Bulkdozer is ready for use
Stay up to date on new releases and other general anouncements by joining <a href='https://groups.google.com/forum/#!forum/bulkdozer-announcements' target='_blank'>Bulkdozer announcements</a>.
Review the <a href='https://github.com/google/starthinker/blob/master/tutorials/Bulkdozer/Installation_and_User_guides.md' target='_blank'>Bulkdozer documentation</a>.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_timezone': 'America/Chicago',  # Timezone for report dates.
  'account_id': '',  # Campaign Manager Network ID (optional if profile id provided)
  'dcm_profile_id': '',  # Campaign Manager Profile ID (optional if account id provided)
  'sheet_url': '',  # Feed Sheet URL
}

TASKS = [
  {
    'traffic': {
      'hour': [
      ],
      'account_id': {
        'field': {
          'name': 'account_id',
          'kind': 'string',
          'order': 1,
          'description': 'Campaign Manager Network ID (optional if profile id provided)',
          'default': ''
        }
      },
      'dcm_profile_id': {
        'field': {
          'name': 'dcm_profile_id',
          'kind': 'string',
          'order': 1,
          'description': 'Campaign Manager Profile ID (optional if account id provided)',
          'default': ''
        }
      },
      'auth': 'user',
      'sheet_url': {
        'field': {
          'name': 'sheet_url',
          'kind': 'string',
          'order': 2,
          'description': 'Feed Sheet URL',
          'default': ''
        }
      },
      'timezone': {
        'field': {
          'name': 'recipe_timezone',
          'kind': 'timezone',
          'description': 'Timezone for report dates.',
          'default': 'America/Chicago'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bulkdozer', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
