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

DV360 User Audit

Gives DV clients ability to see which users have access to which parts of an account. Loads DV user profile mappings using the API into BigQuery and connects to a DataStudio dashboard.

  - DV360 only permits SERVICE accounts to access the user list API endpoint, be sure to provide and permission one.
  - Wait for <b>BigQuery->->->DV_*</b> to be created.
  - Wait for <b>BigQuery->->->Barnacle_*</b> to be created, then copy and connect the following data sources.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/reporting/9f6b9e62-43ec-4027-849a-287e9c1911bd' target='_blank'>Barnacle DV Report</a>.
  - Click Edit->Resource->Manage added data sources, then edit each connection to connect to your new tables above.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read':'user',  # Credentials used for writing data.
  'auth_write':'service',  # Credentials used for writing data.
  'partner':'',  # Partner ID to run user audit on.
  'recipe_slug':'',  # Name of Google BigQuery dataset to create.
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
      3,
      15
    ]
  },
  'tasks':[
    {
      'dataset':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for writing data.'}},
        'api':'doubleclickbidmanager',
        'version':'v1.1',
        'function':'queries.listqueries',
        'alias':'list',
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV_Reports'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for writing data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'partners.list',
        'kwargs':{
          'fields':'partners.displayName,partners.partnerId,nextPageToken'
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV_Partners'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for writing data.'}},
        'api':'displayvideo',
        'version':'v1',
        'function':'advertisers.list',
        'kwargs':{
          'partnerId':{'field':{'name':'partner','kind':'integer','order':2,'default':'','description':'Partner ID to run user audit on.'}},
          'fields':'advertisers.displayName,advertisers.advertiserId,nextPageToken'
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV_Advertisers'
          }
        }
      }
    },
    {
      'google_api':{
        'auth':'service',
        'api':'displayvideo',
        'version':'v1',
        'function':'users.list',
        'kwargs':{
        },
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
            'table':'DV_Users'
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'query':"SELECT           U.userId,           U.name,           U.email,           U.displayName,           REGEXP_EXTRACT(U.email, r'@(.+)') AS Domain,           IF (ENDS_WITH(U.email, '.gserviceaccount.com'), 'Service', 'User') AS Authentication,           IF((Select COUNT(advertiserId) from UNNEST(U.assignedUserRoles)) = 0, 'Partner', 'Advertiser') AS Scope,           STRUCT(             AUR.partnerId,             P.displayName AS partnerName,             AUR.userRole,             AUR.advertiserId,             A.displayName AS advertiserName,             AUR.assignedUserRoleId           ) AS assignedUserRoles,           FROM `{dataset}.DV_Users` AS U,           UNNEST(assignedUserRoles) AS AUR           LEFT JOIN `{dataset}.DV_Partners` AS P           ON AUR.partnerId=P.partnerId           LEFT JOIN `{dataset}.DV_Advertisers` AS A           ON AUR.advertiserId=A.advertiserId         ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'view':'Barnacle_User_Roles'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'query':"SELECT           R.*,           P.displayName AS partnerName,           A.displayName AS advertiserName,           FROM (           SELECT             queryId,             (SELECT CAST(value AS INT64) FROM UNNEST(R.params.filters) WHERE type = 'FILTER_PARTNER' LIMIT 1) AS partnerId,             (SELECT CAST(value AS INT64) FROM UNNEST(R.params.filters) WHERE type = 'FILTER_ADVERTISER' LIMIT 1) AS advertiserId,             R.schedule.frequency,             R.params.metrics,             R.params.type,             R.metadata.dataRange,             R.metadata.sendNotification,             DATE(TIMESTAMP_MILLIS(R.metadata.latestReportRunTimeMS)) AS latestReportRunTime,           FROM `{dataset}.DV_Reports` AS R) AS R           LEFT JOIN `{dataset}.DV_Partners` AS P           ON R.partnerId=P.partnerId           LEFT JOIN `{dataset}.DV_Advertisers` AS A           ON R.advertiserId=A.advertiserId         ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}},
          'view':'Barnacle_Reports'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('barnacle_dv360', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
