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

DV360 Data Warehouse

Deploy a BigQuery dataset mirroring DV360 account structure. Foundation for solutions on top.

  - Wait for <b>BigQuery->->->*</b> to be created.
  - Every table mimics the <a href='https://developers.google.com/display-video/api/reference/rest' target='_blank'>DV360 API Endpoints</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_bigquery':'service',  # Credentials used for writing data.
  'auth_dv':'service',  # Credentials used for reading data.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
  'partners':[],  # List of account ids to pull.
}

RECIPE = {
  'tasks':[
    {
      'dataset':{
        'description':'Create a dataset for bigquery tables.',
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}}
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'partners.get',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be created in BigQuery.'}},
            'legacy':False,
            'query':'SELECT CAST(partnerId AS STRING) partnerId FROM (SELECT DISTINCT * FROM UNNEST({partners}) AS partnerId)',
            'parameters':{
              'partners':{'field':{'name':'partners','kind':'integer_list','order':4,'default':[],'description':'List of account ids to pull.'}}
            }
          }
        },
        'iterate':False,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Partners'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(partnerId  AS STRING) partnerId FROM `DV360_Partners`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Advertisers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.insertionOrders.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_InsertionOrders'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.lineItems.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_LineItems'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.campaigns.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Campaigns'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.channels.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Channels'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.creatives.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Creatives'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'inventorySources.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Inventory_Sources'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'googleAudiences.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Google_Audiences'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_dv','kind':'authentication','order':1,'default':'service','description':'Credentials used for reading data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'combinedAudiences.list',
        'kwargs_remote':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'Credentials to use for BigQuery reads and writes.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':0,'default':'','description':'Google BigQuery dataset to create tables in.'}},
            'query':'SELECT DISTINCT CAST(advertiserId AS STRING) AS advertiserId FROM `DV360_Advertisers`',
            'legacy':False
          }
        },
        'iterate':True,
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV360_Combined_Audiences'
          }
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dv360_data_warehouse', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
