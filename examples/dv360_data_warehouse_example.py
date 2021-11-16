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
from starthinker.task.google_api.run import google_api


def recipe_dv360_data_warehouse(config, auth_bigquery, auth_dv, recipe_slug, partners):
  """Deploy a BigQuery dataset mirroring DV360 account structure. Foundation for
     solutions on top.

     Args:
       auth_bigquery (authentication) - Credentials used for writing data.
       auth_dv (authentication) - Credentials used for reading data.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
       partners (integer_list) - List of account ids to pull.
  """

  dataset(config, {
    'description':'Create a dataset for bigquery tables.',
    'auth':auth_bigquery,
    'dataset':recipe_slug
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'partners.get',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'legacy':False,
        'query':'SELECT CAST(partnerId AS STRING) partnerId FROM (SELECT DISTINCT * FROM UNNEST({partners}) AS partnerId)',
        'parameters':{
          'partners':partners
        }
      }
    },
    'iterate':False,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Partners'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'''SELECT DISTINCT CAST(partnerId
AS STRING) partnerId FROM `DV360_Partners`''',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Advertisers'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.insertionOrders.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_InsertionOrders'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.lineItems.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_LineItems'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.campaigns.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Campaigns'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.channels.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Channels'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.creatives.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Creatives'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'inventorySources.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Inventory_Sources'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'googleAudiences.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Google_Audiences'
      }
    }
  })

  google_api(config, {
    'auth':auth_dv,
    'api':'displayvideo',
    'version':'v1',
    'function':'combinedAudiences.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'DV360_Combined_Audiences'
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Deploy a BigQuery dataset mirroring DV360 account structure. Foundation for solutions on top.

      1. Wait for BigQuery->->->... to be created.
      2. Every table mimics the 1-DV360 API Endpoints.
         2.1 - DV360 API Endpoints: https://developers.google.com/display-video/api/reference/rest
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_bigquery", help="Credentials used for writing data.", default='service')
  parser.add_argument("-auth_dv", help="Credentials used for reading data.", default='service')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')
  parser.add_argument("-partners", help="List of account ids to pull.", default=[])


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_dv360_data_warehouse(config, args.auth_bigquery, args.auth_dv, args.recipe_slug, args.partners)
