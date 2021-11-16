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


def recipe_cm360_data_warehouse(config, auth_bigquery, auth_cm, recipe_slug, accounts):
  """Deploy a BigQuery dataset mirroring CM360 account structure. Foundation for
     solutions on top.

     Args:
       auth_bigquery (authentication) - Credentials used for writing data.
       auth_cm (authentication) - Credentials used for reading data.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
       accounts (integer_list) - List of account ids to pull.
  """

  dataset(config, {
    'description':'Create a dataset for bigquery tables.',
    'hour':[
      4
    ],
    'auth':auth_bigquery,
    'dataset':recipe_slug
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'userProfiles.list',
    'kwargs':{
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_userProfiles'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'accounts.get',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'''SELECT DISTINCT accountId AS id
           FROM `CM360_userProfiles`
           WHERE NOT ENDS_WITH(userName, '@dcm')
           AND (ARRAY_LENGTH({accounts}) = 0 OR accountId IN UNNEST({accounts}))           ''',
        'parameters':{
          'accounts':accounts
        },
        'legacy':False
      }
    },
    'iterate':False,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_accounts'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'subaccounts.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_subaccounts'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'advertisers.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_advertisers'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'advertiserGroups.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_advertiserGroups'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'advertiserLandingPages.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_advertiserLandingPages'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'campaigns.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_campaigns'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'campaignCreativeAssociations.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT accountId, id AS campaignId FROM `CM360_campaigns` WHERE accountId=10394172;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_campaignCreativeAssociations'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'ads.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_ads'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'sites.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_sites'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'directorySites.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_directorySites'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'placements.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_placements'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'placementGroups.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_placementGroups'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'placementStrategies.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_placementStrategies'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'creatives.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_creatives'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'creativeGroups.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_creativeGroups'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'sizes.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_sizes'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'creativeFields.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_creativeFields'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'creativeFieldValues.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT accountId, id AS creativeFieldId FROM `CM360_creativeFields`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_creativeFieldValues'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'browsers.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_browsers'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'cities.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_cities'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'languages.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_languages'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'metros.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_metros'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'connectionTypes.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_connectionTypes'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'contentCategories.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_contentCategories'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'countries.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_countries'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'regions.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_regions'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'postalCodes.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_postalCodes'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'projects.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_projects'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'videoFormats.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_videoFormats'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'platformTypes.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_platformTypes'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'orders.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS projectId, accountId FROM `CM360_projects`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_orders'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'orderDocuments.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS projectId, accountId FROM `CM360_projects`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_orderDocuments'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'mobileApps.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_mobileApps'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'mobileCarriers.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_mobileCarriers'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'operatingSystems.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_operatingSystems'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'operatingSystemVersions.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_operatingSystemVersions'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'remarketingLists.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS advertiserId, id AS accountId FROM `CM360_accounts` where name='BROKEN API CALL SEE: b/183547271';',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_remarketingLists'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'targetingTemplates.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS advertiserId, id AS accountId FROM `CM360_accounts` where name='BROKEN API CALL SEE: b/183547271';',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_targetingTemplates'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'targetableRemarketingLists.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS advertiserId, id AS accountId FROM `CM360_accounts` where name='BROKEN API CALL SEE: b/183547271';',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_targetableRemarketingLists'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'inventoryItems.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS projectId, accountId FROM `CM360_projects`;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_inventoryItems'
      }
    }
  })

  google_api(config, {
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'dynamicTargetingKeys.list',
    'kwargs_remote':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
        'legacy':False
      }
    },
    'iterate':True,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM360_dynamicTargetingKeys'
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Deploy a BigQuery dataset mirroring CM360 account structure. Foundation for solutions on top.

      1. Wait for BigQuery->->->... to be created.
      2. Every table mimics the 1-CM360 API Endpoints.
         2.1 - CM360 API Endpoints: https://developers.google.com/doubleclick-advertisers/rel_notes
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_bigquery", help="Credentials used for writing data.", default='service')
  parser.add_argument("-auth_cm", help="Credentials used for reading data.", default='service')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')
  parser.add_argument("-accounts", help="List of account ids to pull.", default=[])


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm360_data_warehouse(config, args.auth_bigquery, args.auth_cm, args.recipe_slug, args.accounts)
