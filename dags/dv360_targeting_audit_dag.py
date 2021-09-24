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

DV360 Targeting Audit

Continously audit all targeting settings for a DV360 Partner in one dashboard. Use filters to locate errant targeting and quickly correct issues.

  - Wait for <b>BigQuery->->->Targeting Audit</b> to be created.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/reporting/2f140045-dd62-48ae-bc3b-8d01b79828b7' target='_blank'>Sample DV360 Targeting Audit</a>.
  - Edit the data source to point at <b>BigQuery->->->Targeting_Audit</b>.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug':'',  # Google BigQuery dataset to create tables in.
  'auth_dv':'user',  # Credentials to use for DV360 reads.
  'auth_bigquery':'service',  # Credentials to use for BigQuery reads and writes.
  'partner':'',  # DV360 Partner to load, user access determines returned data.
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
      4,
      10,
      8
    ]
  },
  'tasks':[
    {
      'dataset':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}}
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'partners.get',
        'kwargs':{
          'partnerId':{'field':{'name':'partner','kind':'string','order':4,'default':'','description':'DV360 Partner to load, user access determines returned data.'}}
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Partners'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.list',
        'kwargs':{
          'partnerId':{'field':{'name':'partner','kind':'string','order':4,'default':'','description':'DV360 Partner to load, user access determines returned data.'}},
          'fields':'advertisers.displayName,advertisers.advertiserId,advertisers.partnerId,nextPageToken'
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Advertisers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.lineItems.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId FROM `{dataset}.DV_Advertisers`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_LineItems'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'partners.targetingTypes.assignedTargetingOptions.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT CAST(partnerId AS STRING) AS partnerId, 'TARGETING_TYPE_CHANNEL' AS targetingType FROM `{dataset}.DV_Partners`;",
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Targeting'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.bulkListAdvertiserAssignedTargetingOptions',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId FROM `{dataset}.DV_Advertisers`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Targeting',
            'disposition':'WRITE_APPEND'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.lineItems.bulkListLineItemAssignedTargetingOptions',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId, CAST(lineItemId AS STRING) AS lineItemId FROM `{dataset}.DV_LineItems`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Targeting',
            'disposition':'WRITE_APPEND'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'targetingTypes.targetingOptions.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT SAFE_CAST(REGEXP_EXTRACT(name, r'advertisers/(\\d+)/') AS INT64) AS advertiserId, targetingType FROM `{dataset}.DV_Targeting` WHERE targetingType IN ('TARGETING_TYPE_EXCHANGE', 'TARGETING_TYPE_SUB_EXCHANGE') GROUP BY 1,2 HAVING advertiserId IS NOT NULL",
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_TargetingOptions'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'partners.channels.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(partnerId AS STRING) AS partnerId FROM `{dataset}.DV_Partners`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Channels'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.channels.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId FROM `{dataset}.DV_Advertisers`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_Channels',
            'disposition':'WRITE_APPEND'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.locationLists.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId FROM `{dataset}.DV_Advertisers`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_LocationLists'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.negativeKeywordLists.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId FROM `{dataset}.DV_Advertisers`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_NegativeKeywordLists'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'inventorySources.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(partnerId AS STRING) AS partnerId FROM `{dataset}.DV_Partners`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_InventorySources'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'inventorySourceGroups.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(partnerId AS STRING) AS partnerId FROM `{dataset}.DV_Partners`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_InventorySourceGroups'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'firstAndThirdPartyAudiences.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT CAST(partnerId AS STRING) AS partnerId, 'firstAndThirdPartyAudienceId desc' AS orderBy FROM `{dataset}.DV_Partners`;",
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'limit':10000,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_FirstAndThirdPartyAudiences'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'googleAudiences.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(partnerId AS STRING) AS partnerId FROM `{dataset}.DV_Partners`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_GoogleAudiences'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'combinedAudiences.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(partnerId AS STRING) AS partnerId FROM `{dataset}.DV_Partners`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_CombinedAudiences'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'user','description':'Credentials to use for DV360 reads.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'customLists.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT CAST(advertiserId AS STRING) AS advertiserId FROM `{dataset}.DV_Advertisers`;',
            'parameters':{
              'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
            },
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'table':'DV_CustomLists'
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
        'from':{
          'query':"WITH DV_Targeting_With_Ids AS (           SELECT             SAFE_CAST(REGEXP_EXTRACT(name, r'partners/(\\d+)/targetingTypes') AS INT64) AS partnerId,             SAFE_CAST(REGEXP_EXTRACT(name, r'advertisers/(\\d+)/targetingTypes') AS INT64) AS advertiserId,             SAFE_CAST(REGEXP_EXTRACT(name, r'lineItems/(\\d+)/targetingTypes') AS INT64) AS lineItemId,             *           FROM `{dataset}.DV_Targeting`         ),          DV_Targeting_With_Names AS (           SELECT             CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,             NULL AS Advertiser,             NULL AS LineItem,             NULL AS lineItemType,             NULL AS pacingType,             NULL AS performanceGoalType,             NULL AS targetingExpansionLevel,             NULL AS excludeFirstPartyAudience,             T.*           FROM DV_Targeting_With_Ids AS T           LEFT JOIN `{dataset}.DV_Partners` AS P           ON T.partnerId=P.partnerId           WHERE T.lineItemId IS NULL           AND T.advertiserId IS NULL           AND T.partnerId IS NOT NULL            UNION ALL            SELECT             CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,             CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,             NULL AS LineItem,             NULL AS lineItemType,             NULL AS pacingType,             NULL AS performanceGoalType,             NULL AS targetingExpansionLevel,             NULL AS excludeFirstPartyAudience,             T.*           FROM DV_Targeting_With_Ids AS T           LEFT JOIN `{dataset}.DV_Advertisers` AS A           ON T.advertiserId=A.advertiserId           LEFT JOIN `{dataset}.DV_Partners` AS P           ON A.partnerId=P.partnerId           WHERE T.lineItemId IS NULL           AND T.advertiserId IS NOT NULL           AND T.partnerId IS NULL            UNION ALL            SELECT             CONCAT(P.displayName, ' - ', P.partnerId) AS Partner,             CONCAT(A.displayName, ' - ', A.advertiserId) AS Advertiser,             CONCAT(L.displayName, ' - ', L.lineItemId) AS LineItem,             L.lineItemType AS lineItemType,             L.pacing.pacingType AS pacingType,             L.bidStrategy.performanceGoalAutoBid.performanceGoalType AS performanceGoalType,             L.targetingExpansion.targetingExpansionLevel AS targetingExpansionLevel,             L.targetingExpansion.excludeFirstPartyAudience AS excludeFirstPartyAudience,             T.*,           FROM DV_Targeting_With_Ids AS T           LEFT JOIN `{dataset}.DV_LineItems` AS L           ON T.lineItemId=L.lineItemId           LEFT JOIN `{dataset}.DV_Advertisers` AS A           ON L.advertiserId=A.advertiserId           LEFT JOIN `{dataset}.DV_Partners` AS P           ON A.partnerId=P.partnerId           WHERE T.lineItemId IS NOT NULL           AND T.advertiserId IS NULL           AND T.partnerId IS NULL         ),          DV_Included_Google_Audience_Group AS (         SELECT           assignedTargetingOptionId,           ARRAY_AGG(CONCAT(DV_AG.displayName, ' - ', DV_AG.googleAudienceId)) AS Included_Google_Audience,         FROM DV_Targeting_With_Names, UNNEST(audienceGroupDetails.includedGoogleAudienceGroup.settings) AS T_AG         LEFT JOIN `{dataset}.DV_GoogleAudiences` AS DV_AG         ON T_AG.googleAudienceId=DV_AG.googleAudienceId         GROUP BY 1         ),          DV_Excluded_Google_Audience_Group AS (         SELECT           assignedTargetingOptionId,           ARRAY_AGG(CONCAT(DV_AG.displayName, ' - ', DV_AG.googleAudienceId)) AS Excluded_Google_Audience,         FROM DV_Targeting_With_Names, UNNEST(audienceGroupDetails.excludedGoogleAudienceGroup.settings) AS T_AG         LEFT JOIN `{dataset}.DV_GoogleAudiences` AS DV_AG         ON T_AG.googleAudienceId=DV_AG.googleAudienceId         GROUP BY 1         ),          DV_Included_Custom_List AS (         SELECT           assignedTargetingOptionId,           ARRAY_AGG(CONCAT(DV_AG.displayName, ' - ', DV_AG.customListId)) AS Included_Custom_List,         FROM DV_Targeting_With_Names, UNNEST(audienceGroupDetails.includedCustomListGroup.settings) AS T_AG         LEFT JOIN `{dataset}.DV_CustomLists` AS DV_AG         ON T_AG.customListId=DV_AG.customListId         GROUP BY 1         ),          DV_Included_Combined_Audience AS (         SELECT           assignedTargetingOptionId,           ARRAY_AGG(CONCAT(DV_AG.displayName, ' - ', DV_AG.combinedAudienceId)) AS Included_Combined_Audience,         FROM DV_Targeting_With_Names, UNNEST(audienceGroupDetails.includedCombinedAudienceGroup.settings) AS T_AG         LEFT JOIN `{dataset}.DV_CombinedAudiences` AS DV_AG         ON T_AG.combinedAudienceId=DV_AG.combinedAudienceId         GROUP BY 1         ),          DV_Excluded_First_And_Third_Party_Audience AS (         SELECT           assignedTargetingOptionId,           ARRAY_AGG(CONCAT(DV_AG.displayName, ' - ', DV_AG.firstAndThirdPartyAudienceId)) AS Excluded_First_And_Third_Party_Audience,         FROM DV_Targeting_With_Ids, UNNEST(audienceGroupDetails.excludedFirstAndThirdPartyAudienceGroup.settings) AS T_AG         LEFT JOIN `{dataset}.DV_FirstAndThirdPartyAudiences` AS DV_AG         ON T_AG.firstAndThirdPartyAudienceId=DV_AG.firstAndThirdPartyAudienceId         GROUP BY 1         ),          DV_Included_First_And_Third_Party_Audience AS (         SELECT           T_AO.assignedTargetingOptionId,           ARRAY_AGG(CONCAT(DV_AG.displayName, ' - ', DV_AG.firstAndThirdPartyAudienceId)) AS Included_First_And_Third_Party_Audience,         FROM (           SELECT             assignedTargetingOptionId,             ARRAY_CONCAT(T_AG.settings) AS First_And_Third_Party_Audience           FROM DV_Targeting_With_Ids, UNNEST(audienceGroupDetails.includedFirstAndThirdPartyAudienceGroups) AS T_AG           ) AS T_AO, UNNEST(First_And_Third_Party_Audience) AS T_AG         LEFT JOIN `{dataset}.DV_FirstAndThirdPartyAudiences` AS DV_AG         ON T_AG.firstAndThirdPartyAudienceId=DV_AG.firstAndThirdPartyAudienceId         GROUP BY 1         )          SELECT           CONCAT(C.displayName, ' - ', C.channelId) AS Channel,           CONCAT(RL.displayName, ' - ', RL.LocationListId) AS Regional_Location_List,           CONCAT(PL.displayName, ' - ', PL.LocationListId) AS Proximity_Location_List,           CONCAT(I.displayName, ' - ', I.inventorySourceId) AS Inventory_Source,           CONCAT(IG.displayName, ' - ', IG.inventorySourceGroupId) AS Inventory_Source_Group,           CONCAT(NK.displayName, ' - ', NK.negativeKeywordListId) AS Negative_Keyword_List,           EO.exchangeDetails.exchange AS Exchange,           SEO.subExchangeDetails.displayName AS SubExchange,            DV_IGAG.Included_Google_Audience,           DV_EGAG.Excluded_Google_Audience,           DV_ICL.Included_Custom_List,           DV_ICA.Included_Combined_Audience,           DV_IFTPA.Included_First_And_Third_Party_Audience,           DV_EFTPA.Excluded_First_And_Third_Party_Audience,           T.*         FROM DV_Targeting_With_Names AS T         LEFT JOIN `{dataset}.DV_Channels` AS C         ON T.channelDetails.channelId=C.channelId         LEFT JOIN `{dataset}.DV_LocationLists` AS RL         ON T.regionalLocationListDetails.regionalLocationListId=RL.LocationListId         LEFT JOIN `{dataset}.DV_LocationLists` AS PL         ON T.proximityLocationListDetails.proximityLocationListId=PL.LocationListId         LEFT JOIN `{dataset}.DV_InventorySources` AS I         ON T.inventorySourceDetails.inventorySourceId=I.inventorySourceId         LEFT JOIN `{dataset}.DV_InventorySourceGroups` AS IG         ON T.inventorySourceGroupDetails.inventorySourceGroupId=IG.inventorySourceGroupId         LEFT JOIN `{dataset}.DV_NegativeKeywordLists` AS NK         ON T.negativeKeywordListDetails.negativeKeywordListId=NK.negativeKeywordListId         LEFT JOIN `{dataset}.DV_TargetingOptions` AS EO         ON T.exchangeDetails.targetingOptionId=EO.targetingOptionId         LEFT JOIN `{dataset}.DV_TargetingOptions` AS SEO         ON T.subExchangeDetails.targetingOptionId=SEO.targetingOptionId          LEFT JOIN DV_Included_Google_Audience_Group AS DV_IGAG         ON T.assignedTargetingOptionId=DV_IGAG.assignedTargetingOptionId         LEFT JOIN DV_Excluded_Google_Audience_Group AS DV_EGAG         ON T.assignedTargetingOptionId=DV_EGAG.assignedTargetingOptionId          LEFT JOIN DV_Included_Custom_List AS DV_ICL         ON T.assignedTargetingOptionId=DV_ICL.assignedTargetingOptionId         LEFT JOIN DV_Included_Combined_Audience AS DV_ICA         ON T.assignedTargetingOptionId=DV_ICA.assignedTargetingOptionId          LEFT JOIN DV_Included_First_And_Third_Party_Audience AS DV_IFTPA         ON T.assignedTargetingOptionId=DV_IFTPA.assignedTargetingOptionId         LEFT JOIN DV_Excluded_First_And_Third_Party_Audience AS DV_EFTPA         ON T.assignedTargetingOptionId=DV_EFTPA.assignedTargetingOptionId         ;         ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Name of Google BigQuery dataset to create.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
          'view':'Targeting_Audit'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dv360_targeting_audit', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
