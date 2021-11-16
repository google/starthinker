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
from starthinker.task.barnacle.run import barnacle
from starthinker.task.bigquery.run import bigquery


def recipe_barnacle(config, recipe_slug, auth_read, auth_write, accounts, reports):
  """Gives CM clients ability to see which profiles have access to which parts of an
     account. Loads CM user profile mappings using the API into BigQuery and
     connects to a DataStudio dashboard.

     Args:
       recipe_slug (string) - Place where tables will be written in BigQuery.
       auth_read (authentication) - Credentials used for reading data.
       auth_write (authentication) - Credentials used for writing data.
       accounts (integer_list) - Comma separated CM account ids.
       reports (boolean) - Include report audit, consumes significant API and data.
  """

  dataset(config, {
    'description':'The dataset will hold multiple tables, make sure it exists.',
    'hour':[
      1
    ],
    'auth':auth_write,
    'dataset':recipe_slug
  })

  barnacle(config, {
    'description':'Will create tables with format CM_* to hold each endpoint via a call to the API list function. Exclude reports for its own task.',
    'hour':[
      1
    ],
    'auth':auth_read,
    'reports':reports,
    'accounts':{
      'single_cell':True,
      'values':accounts
    },
    'out':{
      'auth':auth_write,
      'dataset':recipe_slug
    }
  })

  bigquery(config, {
    'hour':[
      8
    ],
    'description':'Combine profile, account, subaccount, and roles into one view, used by other views in this workflow.',
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 P.profileId AS profileId,
 P.accountId AS accountId,
 P.subaccountId AS subaccountId,
 P.name AS Profile_Name,
 P.email AS Profile_Email,
 REGEXP_EXTRACT(P.email, r'@(.+)') AS Profile_Domain,
 P.userAccessType AS Profile_userAccessType,
 P.active AS Profie_active,
 P.traffickerType AS Profile_traffickerType,
 P.comments AS Profile_comments,
 P.userRoleId AS Profile_userRoleId,
 R.role_name AS Role_role_name,
 R.role_defaultUserRole AS Role_role_defaultUserRole,
 R.permission_name AS Role_permission_name,
 R.permission_availability AS Role_permission_availability,
 A.name AS Account_name,
 A.active AS Account_active,
 A.description AS Account_description,
 A.locale AS Account_locale,
 S.name AS SubAccount_name FROM `{dataset}.CM_Profiles` AS P LEFT JOIN `{dataset}.CM_Roles` AS R
 ON P.userRoleId=R.roleId LEFT JOIN `{dataset}.CM_Accounts` AS A
 ON P.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS S
 ON P.accountId=S.accountId
 AND P.subaccountId=S.subaccountId ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Profile_Role_Account_SubAccount_Map'
    }
  })

  bigquery(config, {
    'description':'Combine profiles and advertisers.',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 APRASM.*,
 A.advertiserId AS advertiserId,
 A.name AS Advertiser_name,
 A.status AS Advertiser_status,
 A.defaultEmail AS Advertiser_defaultEmail,
 A.suspended AS Advertiser_suspended FROM `{dataset}.CM_Profile_Advertisers` As PA LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM
 ON PA.profileID=APRASM.profileID LEFT JOIN `{dataset}.CM_Advertisers` AS A
 ON PA.advertiserId=A.advertiserId ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Profile_Advertiser_Map'
    }
  })

  bigquery(config, {
    'description':'Profile to campaign mapping.',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 APRASM.*,
 C.campaignId AS campaignId,
 C.name AS Campaign_name,
 C.archived AS Campaign_archived,
 IF(C.startDate <= CURRENT_DATE() AND C.endDate >= CURRENT_DATE(), True, False) AS Campaign_running,
 ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), C.lastModifiedInfo_time, DAY) / 7) AS Campaign_Modified_Weeks_Ago FROM `.{dataset}.CM_Profile_Campaigns` As PC LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM
 ON PC.profileID=APRASM.profileID LEFT JOIN `{dataset}.CM_Campaigns` AS C
 ON PC.campaignId=C.campaignId ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Profile_Campaign_Map'
    }
  })

  bigquery(config, {
    'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 APRASM.*,
 R.reportId AS reportId,
 R.name AS Report_name,
 R.type AS Report_type,
 R.format AS Report_format,
 R.schedule_active AS Report_schedule_active,
 R.schedule_repeats AS Report_schedule_repeats,
 ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), R.lastModifiedTime, DAY) / 7) AS Report_Modified_Weeks_Ago,
 DATE_DIFF(R.schedule_expirationDate, CURRENT_DATE(), MONTH) AS Report_Schedule_Weeks_To_Go FROM `{dataset}.CM_Reports` As R LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM
 ON R.profileID=APRASM.profileID ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Profile_Report_Map'
    }
  })

  bigquery(config, {
    'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 APRASM.*,
 S.siteId AS siteId,
 S.name AS Site_Name,
 S.keyName AS Site_keyName,
 S.approved AS Site_approved FROM `{dataset}.CM_Profile_Sites` As PS LEFT JOIN `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM
 ON PS.profileID=APRASM.profileID LEFT JOIN `{dataset}.CM_Sites` AS S
 ON PS.siteId=S.siteId ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Profile_Site_Map'
    }
  })

  bigquery(config, {
    'description':'The logic query for Deal Finder, transforms report into view used by datastudio.',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 APRASM.* FROM `{dataset}.Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM LEFT JOIN `{dataset}.CM_Profile_Advertisers` AS PA
 ON APRASM.profileId=PA.profileId LEFT JOIN `{dataset}.CM_Profile_Campaigns` AS PC
 ON APRASM.profileId=PC.profileId LEFT JOIN `{dataset}.CM_Profile_Sites` AS PS
 ON APRASM.profileId=PS.profileId WHERE
 PA.advertiserId IS NULL
 AND PC.campaignId IS NULL
 AND PS.siteId IS NULL  ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Profiles_Connections'
    }
  })

  bigquery(config, {
    'description':'',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 RD.accountId AS accountId,
 RD.subaccountId AS subaccountId,
 RD.reportId AS reportId,
 A.name AS Account_name,
 A.active AS Account_active,
 SA.name as SubAccount_name,
 R.name as Report_name,
 R.schedule_active AS Report_schedule_active,
 RD.emailOwnerDeliveryType AS Delivery_emailOwnerDeliveryType,
 RD.deliveryType AS Delivery_deliveryType,
 RD.email AS Delivery_email,
 RD.message AS Delivery_message,
 IF(RD.email in (SELECT email from `{dataset}.CM_Profiles`), True, False) AS Profile_Match_Exists FROM `{dataset}.CM_Report_Deliveries` AS RD LEFT JOIN `{dataset}.CM_Accounts` AS A
 ON RD.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA
 ON RD.subaccountId=SA.subaccountId LEFT JOIN `{dataset}.CM_Reports` AS R
 ON RD.reportId=R.reportId ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Report_Delivery_Profiles'
    }
  })

  bigquery(config, {
    'description':'',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 R.accountId AS accountId,
 R.subaccountId AS subaccountId,
 R.roleId AS roleId,
 A.name AS Account_name,
 A.active AS Account_active,
 SA.name AS SubAccount_name,
 R.role_name as Role_role_name,
 R.role_defaultUserRole AS Role_role_defaultUserRole,
 R.permission_name AS Role_permission_name,
 R.permission_availability AS Role_permission_availability FROM `{dataset}.CM_Roles` AS R LEFT JOIN `{dataset}.CM_Accounts` AS A on R.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA on R.subaccountId=SA.subaccountId WHERE roleId NOT IN (
 SELECT roleId FROM `{dataset}.CM_Profile_Roles` ) ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Roles_Not_Used'
    }
  })

  bigquery(config, {
    'description':'',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' SELECT
 SC.accountId AS accountId,
 SC.subaccountId AS subaccountId,
 SC.siteId AS siteId,
 SC.contactId AS contactId,
 A.name AS Account_name,
 A.active AS Account_active,
 SA.name as SubAccount_name,
 S.name as Site_name,
 S.approved AS Site_approved,
 SC.email AS Site_Contact_email,
 CONCAT(SC.firstName, ' ', sc.lastname) AS Site_Contact_Name,
 SC.phone AS Site_Contact_phone,
 SC.contactType AS Site_Contact_contactType,
 IF(sc.email in (SELECT email from `{dataset}.CM_Profiles`), True, False) AS Profile_Match_Exists FROM `{dataset}.CM_Site_Contacts` AS SC LEFT JOIN `{dataset}.CM_Accounts` AS A
 ON SC.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA
 ON SC.accountId=SA.accountId
 AND SC.subaccountId=SA.subaccountId LEFT JOIN `{dataset}.CM_Sites` AS S
 ON SC.siteId=S.siteId ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Site_Contacts_Profiles'
    }
  })

  bigquery(config, {
    'description':'',
    'hour':[
      8
    ],
    'auth':auth_write,
    'from':{
      'legacy':False,
      'query':''' WITH
profile_counts AS (
 SELECT userRoleId, COUNT(profileId) as profile_count
 FROM `{dataset}.CM_Profiles`
 GROUP BY 1 ),
permission_fingerprints AS (
 SELECT

 accountId,

 subaccountId,

 roleId,

 role_name,

 role_defaultUserRole,

 SUM(profile_count) AS profile_count,

 FARM_FINGERPRINT(


 ARRAY_TO_STRING(


 ARRAY_AGG(



 DISTINCT permission_name ORDER BY permission_name ASC


 ), ',', '-'

 )
 ) AS permissions_fingerprint
 FROM

 `{dataset}.CM_Roles` AS R
 LEFT JOIN profile_counts AS P
 ON R.roleId = P.userRoleId
 GROUP BY

 accountId,

 subaccountId,

 roleId,

 role_name,

 role_defaultUserRole )
SELECT
 PFL.accountId AS accountId,
 A.name AS Account_name,
 A.active AS Account_active,
 PFL.subaccountId AS subaccountId,
 SA.name AS SubAccount_name,
 PFL.roleId AS roleId,
 PFL.role_name AS role_name,
 PFL.role_defaultUserRole AS role_defaultUserRole,
 COALESCE(PFL.profile_count, 0) AS profile_count,
 PFR.roleId AS duplicate_roleId,
 PFR.role_name AS duplicate_role_name,
 PFR.role_defaultUserRole AS duplicate_role_defaultUserRole,
 COALESCE(PFR.profile_count, 0) AS duplicate_profile_count FROM permission_fingerprints AS PFL LEFT JOIN `{dataset}.CM_Accounts` AS A on PFL.accountId=A.accountId LEFT JOIN `{dataset}.CM_SubAccounts` AS SA on PFL.subaccountId=SA.subaccountId LEFT JOIN permission_fingerprints AS PFR
 ON PFL.permissions_fingerprint=PFR.permissions_fingerprint
 AND PFL.accountId=PFR.accountId
 AND COALESCE(PFL.subaccountId, 0)=COALESCE(PFR.subaccountId, 0) WHERE PFL.roleId != PFR.roleId ; ''',
      'parameters':{
        'dataset':recipe_slug
      }
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Roles_Duplicates'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Gives CM clients ability to see which profiles have access to which parts of an account. Loads CM user profile mappings using the API into BigQuery and connects to a DataStudio dashboard.

      1. Wait for BigQuery->->->CM_... to be created.
      2. Wait for BigQuery->->->Barnacle_... to be created, then copy and connect the following data sources.
      3. Join the 1-StarThinker Assets Group to access the following assets
         3.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      4. Copy 1-Barnacle Profile Advertiser Map and connect.
         4.1 - Barnacle Profile Advertiser Map: https://datastudio.google.com/open/1a6K-XdPUzCYRXZp1ZcmeOUOURc9wn2Jj
      5. Copy 1-Barnacle Profile Campaign Map and connect.
         5.1 - Barnacle Profile Campaign Map: https://datastudio.google.com/open/1NEzrQWWnPjkD90iUwN-ASKbVBzoeBdoT
      6. Copy 1-Barnacle Profile Site Map and connect.
         6.1 - Barnacle Profile Site Map: https://datastudio.google.com/open/1v_GRaitwPaHHKUzfJZYNBhzotvZ-bR7Y
      7. Copy 1-Barnacle Profiles Connections and connect.
         7.1 - Barnacle Profiles Connections: https://datastudio.google.com/open/14tWlh7yiqzxKJIppMFVOw2MoMtQV_ucE
      8. Copy 1-Barnacle Report Delivery Profiles and connect.
         8.1 - Barnacle Report Delivery Profiles: https://datastudio.google.com/open/1mavjxvHSEPfJq5aW4FYgCXsBCE5rthZG
      9. Copy 1-Barnacle Roles Duplicates and connect.
         9.1 - Barnacle Roles Duplicates: https://datastudio.google.com/open/1Azk_Nul-auinf4NnDq8T9fDyiKkUWD7A
      10. Copy 1-Barnacle Roles Not Used and connect.
         10.1 - Barnacle Roles Not Used: https://datastudio.google.com/open/1ogoofpKtqkLwcW9qC_Ju_JvJdIajsjNI
      11. Copy 1-Barnacle Site Contacts Profiles and connect.
         11.1 - Barnacle Site Contacts Profiles: https://datastudio.google.com/open/1xLgZPjOPDtmPyEqYMiMbWwMI8-WTslfj
      12. If reports checked, copy 1-Barnacle Profile Report Map and connect.
         12.1 - Barnacle Profile Report Map: https://datastudio.google.com/open/1-YGDiQPDnk0gD78_QOY5XdTXRlTrLeEq
      13. Copy 1-Barnacle Report.
         13.1 - Barnacle Report: https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT
      14. When prompted choose the new data sources you just created.
      15. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-recipe_slug", help="Place where tables will be written in BigQuery.", default=None)
  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-accounts", help="Comma separated CM account ids.", default=[])
  parser.add_argument("-reports", help="Include report audit, consumes significant API and data.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_barnacle(config, args.recipe_slug, args.auth_read, args.auth_write, args.accounts, args.reports)
