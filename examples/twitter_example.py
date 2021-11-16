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
from starthinker.task.dataset.run import dataset
from starthinker.task.sheets.run import sheets
from starthinker.task.twitter.run import twitter
from starthinker.task.google_api.run import google_api


def recipe_twitter(config, auth_read, auth_write, recipe_name, twitter_secret, recipe_slug, twitter_key):
  """Adjusts line item settings based on Twitter hashtags and locations specified in
     a sheet.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Credentials used for writing data.
       recipe_name (string) - Name of sheet where Line Item settings will be read from.
       twitter_secret (string) - Twitter API secret token.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
       twitter_key (string) - Twitter API key token.
  """

  dataset(config, {
    'description':'Create a dataset where data will be combined and transfored for upload.',
    'auth':auth_write,
    'dataset':recipe_slug
  })

  sheets(config, {
    'description':'Read mapping of hash tags to line item toggles from sheets.',
    'auth':auth_read,
    'template':{
      'sheet':'https://docs.google.com/spreadsheets/d/1iYCGa2NKOZiL2mdT4yiDfV_SWV9C7SUosXdIr4NAEXE/edit?usp=sharing',
      'tab':'Twitter Triggers'
    },
    'sheet':recipe_name,
    'tab':'Twitter Triggers',
    'range':'A7:E',
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'Twitter_Triggers',
        'schema':[
          {
            'name':'Location',
            'type':'STRING',
            'mode':'REQUIRED'
          },
          {
            'name':'WOEID',
            'type':'INTEGER',
            'mode':'REQUIRED'
          },
          {
            'name':'Hashtag',
            'type':'STRING',
            'mode':'REQUIRED'
          },
          {
            'name':'Advertiser_Id',
            'type':'INTEGER',
            'mode':'REQUIRED'
          },
          {
            'name':'Line_Item_Id',
            'type':'INTEGER',
            'mode':'REQUIRED'
          }
        ]
      }
    }
  })

  twitter(config, {
    'description':'Read trends from Twitter and place into BigQuery.',
    'auth':auth_write,
    'secret':twitter_secret,
    'key':twitter_key,
    'trends':{
      'places':{
        'single_cell':True,
        'bigquery':{
          'dataset':recipe_slug,
          'query':'SELECT DISTINCT WOEID FROM {dataset}.Twitter_Triggers',
          'legacy':False,
          'parameters':{
            'dataset':recipe_slug
          }
        }
      }
    },
    'out':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'Twitter_Trends_Place'
      }
    }
  })

  google_api(config, {
    'description':'Combine sheet and twitter data into API operations for each line item.  Match all possibilities and PAUSE if no trigger match.',
    'auth':auth_write,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.lineItems.patch',
    'kwargs_remote':{
      'bigquery':{
        'dataset':recipe_slug,
        'query':'''
           SELECT
             CAST(S.Advertiser_Id AS STRING) advertiserId,
             CAST(S.Line_Item_Id AS STRING) AS lineItemId,
             STRUCT(
               IF(LOGICAL_OR(T.Name is NULL), 'ENTITY_STATUS_ACTIVE', 'ENTITY_STATUS_PAUSED') AS entityStatus
             ) AS body,
             'entityStatus' AS updateMask,
           FROM `{dataset}.Twitter_Triggers` AS S
           LEFT JOIN `{dataset}.Twitter_Trends_Place` As T
           ON S.WOEID=T.WOEID AND REPLACE(LOWER(S.Hashtag), '#', '')=REPLACE(LOWER(T.Name), '#', '')
           GROUP BY 1,2           ''',
        'parameters':{
          'dataset':recipe_slug
        }
      }
    },
    'results':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'Trigger_Results'
      }
    },
    'errors':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'Trigger_Errors'
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Adjusts line item settings based on Twitter hashtags and locations specified in a sheet.

      1. Click Run Now and a sheet called Twitter Targeting  will be generated with a tab called Twitter Triggers.
      2. Follow instructions on the sheets tab to provide triggers and lineitems.
      3. Click Run Now again, trends are downloaded and triggered.
      4. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-recipe_name", help="Name of sheet where Line Item settings will be read from.", default='')
  parser.add_argument("-twitter_secret", help="Twitter API secret token.", default='')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')
  parser.add_argument("-twitter_key", help="Twitter API key token.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_twitter(config, args.auth_read, args.auth_write, args.recipe_name, args.twitter_secret, args.recipe_slug, args.twitter_key)
