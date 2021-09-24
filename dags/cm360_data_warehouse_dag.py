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

CM360 Data Warehouse

Deploy a BigQuery dataset mirroring CM360 account structure. Foundation for solutions on top.

  - Wait for <b>BigQuery->->->*</b> to be created.
  - Every table mimics the <a href='https://developers.google.com/doubleclick-advertisers/rel_notes' target='_blank'>CM360 API Endpoints</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_bigquery':'service',  # Credentials used for writing data.
  'auth_cm':'service',  # Credentials used for reading data.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
  'accounts':[],  # List of account ids to pull.
}

RECIPE = {
  'tasks':[
    {
      'dataset':{
        'description':'Create a dataset for bigquery tables.',
        'hour':[
          4
        ],
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}}
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'userProfiles.list',
        'kwargs':{
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_userProfiles'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'accounts.get',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT DISTINCT accountId AS id             FROM `CM360_userProfiles`             WHERE NOT ENDS_WITH(userName, '@dcm')             AND (ARRAY_LENGTH({accounts}) = 0 OR accountId IN UNNEST({accounts}))           ",
            'parameters':{
              'accounts':{'field':{'name':'accounts','kind':'integer_list','order':4,'default':[],'description':'List of account ids to pull.'}}
            },
            'legacy':False
          }
        },
        'iterate':False,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_accounts'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'subaccounts.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_subaccounts'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'advertisers.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_advertisers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'advertiserGroups.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_advertiserGroups'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'advertiserLandingPages.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_advertiserLandingPages'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'campaigns.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_campaigns'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'campaignCreativeAssociations.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT accountId, id AS campaignId FROM `CM360_campaigns` WHERE accountId=10394172;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_campaignCreativeAssociations'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'ads.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_ads'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'sites.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_sites'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'directorySites.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_directorySites'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'placements.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_placements'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'placementGroups.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_placementGroups'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'placementStrategies.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_placementStrategies'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'creatives.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_creatives'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'creativeGroups.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_creativeGroups'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'sizes.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_sizes'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'creativeFields.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_creativeFields'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'creativeFieldValues.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT accountId, id AS creativeFieldId FROM `CM360_creativeFields`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_creativeFieldValues'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'browsers.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_browsers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'cities.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_cities'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'languages.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_languages'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'metros.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_metros'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'connectionTypes.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_connectionTypes'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'contentCategories.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_contentCategories'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'countries.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_countries'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'regions.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_regions'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'postalCodes.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_postalCodes'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'projects.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_projects'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'videoFormats.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_videoFormats'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'platformTypes.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_platformTypes'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'orders.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS projectId, accountId FROM `CM360_projects`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_orders'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'orderDocuments.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS projectId, accountId FROM `CM360_projects`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_orderDocuments'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'mobileApps.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_mobileApps'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'mobileCarriers.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_mobileCarriers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'operatingSystems.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_operatingSystems'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'operatingSystemVersions.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_operatingSystemVersions'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'remarketingLists.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT id AS advertiserId, id AS accountId FROM `CM360_accounts` where name='BROKEN API CALL SEE: b/183547271';",
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_remarketingLists'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'targetingTemplates.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT id AS advertiserId, id AS accountId FROM `CM360_accounts` where name='BROKEN API CALL SEE: b/183547271';",
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_targetingTemplates'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'targetableRemarketingLists.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':"SELECT id AS advertiserId, id AS accountId FROM `CM360_accounts` where name='BROKEN API CALL SEE: b/183547271';",
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_targetableRemarketingLists'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'inventoryItems.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS projectId, accountId FROM `CM360_projects`;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_inventoryItems'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'dynamicTargetingKeys.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT id AS accountId FROM `CM360_accounts` LIMIT 1;',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'CM360_dynamicTargetingKeys'
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('cm360_data_warehouse', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
