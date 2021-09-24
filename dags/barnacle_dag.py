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

CM360 User Audit

Gives CM clients ability to see which profiles have access to which parts of an account. Loads CM user profile mappings using the API into BigQuery and connects to a DataStudio dashboard.

  - Wait for <b>BigQuery->->->CM_*</b> to be created.
  - Wait for <b>BigQuery->->->Barnacle_*</b> to be created, then copy and connect the following data sources.
  - Join the <a href='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/open/1a6K-XdPUzCYRXZp1ZcmeOUOURc9wn2Jj' target='_blank'>Barnacle Profile Advertiser Map</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1NEzrQWWnPjkD90iUwN-ASKbVBzoeBdoT' target='_blank'>Barnacle Profile Campaign Map</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1v_GRaitwPaHHKUzfJZYNBhzotvZ-bR7Y' target='_blank'>Barnacle Profile Site Map</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/14tWlh7yiqzxKJIppMFVOw2MoMtQV_ucE' target='_blank'>Barnacle Profiles Connections</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1mavjxvHSEPfJq5aW4FYgCXsBCE5rthZG' target='_blank'>Barnacle Report Delivery Profiles</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1Azk_Nul-auinf4NnDq8T9fDyiKkUWD7A' target='_blank'>Barnacle Roles Duplicates</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1ogoofpKtqkLwcW9qC_Ju_JvJdIajsjNI' target='_blank'>Barnacle Roles Not Used</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1xLgZPjOPDtmPyEqYMiMbWwMI8-WTslfj' target='_blank'>Barnacle Site Contacts Profiles</a> and connect.
  - If reports checked, copy <a href='https://datastudio.google.com/open/1-YGDiQPDnk0gD78_QOY5XdTXRlTrLeEq' target='_blank'>Barnacle Profile Report Map</a> and connect.
  - Copy <a href='https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT' target='_blank'>Barnacle Report</a>.
  - When prompted choose the new data sources you just created.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug':'',  # Place where tables will be written in BigQuery.
  'auth_read':'user',  # Credentials used for reading data.
  'auth_write':'service',  # Credentials used for writing data.
  'accounts':[],  # Comma separated CM account ids.
  'reports':False,  # Include report audit, consumes significant API and data.
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
      1,
      3,
      8
    ]
  },
  'tasks':[
    {
      'dataset':{
        'description':'The dataset will hold multiple tables, make sure it exists.',
        'hour':[
          1
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Name of Google BigQuery dataset to create.'}}
      }
    },
    {
      'barnacle':{
        'description':'Will create tables with format CM_* to hold each endpoint via a call to the API list function. Exclude reports for its own task.',
        'hour':[
          1
        ],
        'auth':{'field':{'name':'auth_read','kind':'authentication','order':0,'default':'user','description':'Credentials used for reading data.'}},
        'reports':{'field':{'name':'reports','kind':'boolean','order':3,'default':False,'description':'Include report audit, consumes significant API and data.'}},
        'accounts':{
          'single_cell':True,
          'values':{'field':{'name':'accounts','kind':'integer_list','order':2,'default':[],'description':'Comma separated CM account ids.'}}
        },
        'out':{
          'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':4,'default':'','description':'Google BigQuery dataset to create tables in.'}}
        }
      }
    },
    {
      'bigquery':{
        'hour':[
          8
        ],
        'description':'Combine profile, account, subaccount, and roles into one view, used by other views in this workflow.',
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':" SELECT   P.profileId AS profileId,   P.accountId AS accountId,   P.subaccountId AS subaccountId,   P.name AS Profile_Name,   P.email AS Profile_Email,   REGEXP_EXTRACT(P.email, r'@(.+)') AS Profile_Domain,   P.userAccessType AS Profile_userAccessType,   P.active AS Profie_active,   P.traffickerType AS Profile_traffickerType,   P.comments AS Profile_comments,   P.userRoleId AS Profile_userRoleId,   R.role_name AS Role_role_name,   R.role_defaultUserRole AS Role_role_defaultUserRole,   R.permission_name AS Role_permission_name,   R.permission_availability AS Role_permission_availability,   A.name AS Account_name,   A.active AS Account_active,   A.description AS Account_description,   A.locale AS Account_locale,   S.name AS SubAccount_name FROM `{dataset}.CM_Profiles` AS P LEFT JOIN `{dataset}.CM_Roles` AS R   ON P.userRoleId=R.roleId LEFT JOIN `{dataset}.CM_Accounts` AS A   ON P.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS S   ON P.accountId=S.accountId   AND P.subaccountId=S.subaccountId ; ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Profile_Role_Account_SubAccount_Map'
        }
      }
    },
    {
      'bigquery':{
        'description':'Combine profiles and advertisers.',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   APRASM.*,   A.advertiserId AS advertiserId,   A.name AS Advertiser_name,   A.status AS Advertiser_status,   A.defaultEmail AS Advertiser_defaultEmail,   A.suspended AS Advertiser_suspended FROM `{dataset}.CM_Profile_Advertisers` As PA LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM   ON PA.profileID=APRASM.profileID LEFT JOIN `{dataset}.CM_Advertisers` AS A   ON PA.advertiserId=A.advertiserId ; ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Profile_Advertiser_Map'
        }
      }
    },
    {
      'bigquery':{
        'description':'Profile to campaign mapping.',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   APRASM.*,   C.campaignId AS campaignId,   C.name AS Campaign_name,   C.archived AS Campaign_archived,   IF(C.startDate <= CURRENT_DATE() AND C.endDate >= CURRENT_DATE(), True, False) AS Campaign_running,   ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), C.lastModifiedInfo_time, DAY) / 7) AS Campaign_Modified_Weeks_Ago FROM `.{dataset}.CM_Profile_Campaigns` As PC LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM   ON PC.profileID=APRASM.profileID LEFT JOIN `{dataset}.CM_Campaigns` AS C   ON PC.campaignId=C.campaignId ; ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Profile_Campaign_Map'
        }
      }
    },
    {
      'bigquery':{
        'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   APRASM.*,   R.reportId AS reportId,   R.name AS Report_name,   R.type AS Report_type,   R.format AS Report_format,   R.schedule_active AS Report_schedule_active,   R.schedule_repeats AS Report_schedule_repeats,   ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), R.lastModifiedTime, DAY) / 7) AS Report_Modified_Weeks_Ago,   DATE_DIFF(R.schedule_expirationDate, CURRENT_DATE(), MONTH) AS Report_Schedule_Weeks_To_Go FROM `{dataset}.CM_Reports` As R LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM   ON R.profileID=APRASM.profileID ; ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Profile_Report_Map'
        }
      }
    },
    {
      'bigquery':{
        'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   APRASM.*,   S.siteId AS siteId,   S.name AS Site_Name,   S.keyName AS Site_keyName,   S.approved AS Site_approved FROM `{dataset}.CM_Profile_Sites` As PS LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM   ON PS.profileID=APRASM.profileID LEFT JOIN `{dataset}.CM_Sites` AS S   ON PS.siteId=S.siteId ; ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Profile_Site_Map'
        }
      }
    },
    {
      'bigquery':{
        'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   APRASM.* FROM `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM LEFT JOIN `{dataset}.CM_Profile_Advertisers` AS PA   ON APRASM.profileId=PA.profileId LEFT JOIN `{dataset}.CM_Profile_Campaigns` AS PC   ON APRASM.profileId=PC.profileId LEFT JOIN `{dataset}.CM_Profile_Sites` AS PS   ON APRASM.profileId=PS.profileId WHERE   PA.advertiserId IS NULL   AND PC.campaignId IS NULL   AND PS.siteId IS NULL  ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Profiles_Connections'
        }
      }
    },
    {
      'bigquery':{
        'description':'',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   RD.accountId AS accountId,   RD.subaccountId AS subaccountId,   RD.reportId AS reportId,   A.name AS Account_name,   A.active AS Account_active,   SA.name as SubAccount_name,   R.name as Report_name,   R.schedule_active AS Report_schedule_active,   RD.emailOwnerDeliveryType AS Delivery_emailOwnerDeliveryType,   RD.deliveryType AS Delivery_deliveryType,   RD.email AS Delivery_email,   RD.message AS Delivery_message,   IF(RD.email in (SELECT email from `{dataset}.CM_Profiles`), True, False) AS Profile_Match_Exists FROM `{dataset}.CM_Report_Deliveries` AS RD LEFT JOIN `{dataset}.CM_Accounts` AS A   ON RD.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA   ON RD.subaccountId=SA.subaccountId LEFT JOIN `{dataset}.CM_Reports` AS R   ON RD.reportId=R.reportId ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Report_Delivery_Profiles'
        }
      }
    },
    {
      'bigquery':{
        'description':'',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':' SELECT   R.accountId AS accountId,   R.subaccountId AS subaccountId,   R.roleId AS roleId,   A.name AS Account_name,   A.active AS Account_active,   SA.name AS SubAccount_name,   R.role_name as Role_role_name,   R.role_defaultUserRole AS Role_role_defaultUserRole,   R.permission_name AS Role_permission_name,   R.permission_availability AS Role_permission_availability FROM `{dataset}.CM_Roles` AS R LEFT JOIN `{dataset}.CM_Accounts` AS A on R.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA on R.subaccountId=SA.subaccountId WHERE roleId NOT IN (   SELECT roleId FROM `{dataset}.CM_Profile_Roles` ) ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Roles_Not_Used'
        }
      }
    },
    {
      'bigquery':{
        'description':'',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':" SELECT   SC.accountId AS accountId,   SC.subaccountId AS subaccountId,   SC.siteId AS siteId,   SC.contactId AS contactId,   A.name AS Account_name,   A.active AS Account_active,   SA.name as SubAccount_name,   S.name as Site_name,   S.approved AS Site_approved,   SC.email AS Site_Contact_email,   CONCAT(SC.firstName, ' ', sc.lastname) AS Site_Contact_Name,   SC.phone AS Site_Contact_phone,   SC.contactType AS Site_Contact_contactType,   IF(sc.email in (SELECT email from `{dataset}.CM_Profiles`), True, False) AS Profile_Match_Exists FROM `{dataset}.CM_Site_Contacts` AS SC LEFT JOIN `{dataset}.CM_Accounts` AS A   ON SC.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA   ON SC.accountId=SA.accountId   AND SC.subaccountId=SA.subaccountId LEFT JOIN `{dataset}.CM_Sites` AS S   ON SC.siteId=S.siteId ; ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Site_Contacts_Profiles'
        }
      }
    },
    {
      'bigquery':{
        'description':'',
        'hour':[
          8
        ],
        'auth':{'field':{'name':'auth_write','kind':'authentication','order':1,'default':'service','description':'Credentials used for writing data.'}},
        'from':{
          'legacy':False,
          'query':" WITH  profile_counts AS (   SELECT userRoleId, COUNT(profileId) as profile_count   FROM `{dataset}.CM_Profiles`   GROUP BY 1 ),  permission_fingerprints AS (   SELECT     accountId,     subaccountId,     roleId,     role_name,     role_defaultUserRole,     SUM(profile_count) AS profile_count,     FARM_FINGERPRINT(       ARRAY_TO_STRING(       ARRAY_AGG(         DISTINCT permission_name ORDER BY permission_name ASC       ), ',', '-'     )   ) AS permissions_fingerprint   FROM     `{dataset}.CM_Roles` AS R   LEFT JOIN profile_counts AS P   ON R.roleId = P.userRoleId   GROUP BY     accountId,     subaccountId,     roleId,     role_name,     role_defaultUserRole )  SELECT   PFL.accountId AS accountId,   A.name AS Account_name,   A.active AS Account_active,   PFL.subaccountId AS subaccountId,   SA.name AS SubAccount_name,   PFL.roleId AS roleId,   PFL.role_name AS role_name,   PFL.role_defaultUserRole AS role_defaultUserRole,   COALESCE(PFL.profile_count, 0) AS profile_count,   PFR.roleId AS duplicate_roleId,   PFR.role_name AS duplicate_role_name,   PFR.role_defaultUserRole AS duplicate_role_defaultUserRole,   COALESCE(PFR.profile_count, 0) AS duplicate_profile_count FROM permission_fingerprints AS PFL LEFT JOIN `{dataset}.CM_Accounts` AS A on PFL.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA on PFL.subaccountId=SA.subaccountId LEFT JOIN permission_fingerprints AS PFR   ON PFL.permissions_fingerprint=PFR.permissions_fingerprint   AND PFL.accountId=PFR.accountId   AND COALESCE(PFL.subaccountId, 0)=COALESCE(PFR.subaccountId, 0) WHERE PFL.roleId != PFR.roleId ; ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}}
          }
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','description':'Place where tables will be written in BigQuery.'}},
          'view':'Barnacle_Roles_Duplicates'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('barnacle', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
