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
from starthinker.task.bigquery.run import bigquery


def recipe_barnacle_dv360(config, auth_read, auth_write, partner, recipe_slug):
  """Gives DV clients ability to see which users have access to which parts of an
     account. Loads DV user profile mappings using the API into BigQuery and
     connects to a DataStudio dashboard.

     Args:
       auth_read (authentication) - Credentials used for writing data.
       auth_write (authentication) - Credentials used for writing data.
       partner (integer) - Partner ID to run user audit on.
       recipe_slug (string) - Name of Google BigQuery dataset to create.
  """

  dataset(config, {
    'auth':auth_write,
    'dataset':recipe_slug
  })

  google_api(config, {
    'auth':auth_read,
    'api':'doubleclickbidmanager',
    'version':'v1.1',
    'function':'queries.listqueries',
    'alias':'list',
    'results':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'DV_Reports'
      }
    }
  })

  google_api(config, {
    'auth':auth_read,
    'api':'displayvideo',
    'version':'v1',
    'function':'partners.list',
    'kwargs':{
      'fields':'partners.displayName,partners.partnerId,nextPageToken'
    },
    'results':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'DV_Partners'
      }
    }
  })

  google_api(config, {
    'auth':auth_read,
    'api':'displayvideo',
    'version':'v1',
    'function':'advertisers.list',
    'kwargs':{
      'partnerId':partner,
      'fields':'advertisers.displayName,advertisers.advertiserId,nextPageToken'
    },
    'results':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'DV_Advertisers'
      }
    }
  })

  google_api(config, {
    'auth':'service',
    'api':'displayvideo',
    'version':'v1',
    'function':'users.list',
    'kwargs':{
    },
    'results':{
      'bigquery':{
        'auth':auth_write,
        'dataset':recipe_slug,
        'table':'DV_Users'
      }
    }
  })

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':'''SELECT
         U.userId,
         U.name,
         U.email,
         U.displayName,
         REGEXP_EXTRACT(U.email, r'@(.+)') AS Domain,
         IF (ENDS_WITH(U.email, '.gserviceaccount.com'), 'Service', 'User') AS Authentication,
         IF((Select COUNT(advertiserId) from UNNEST(U.assignedUserRoles)) = 0, 'Partner', 'Advertiser') AS Scope,
         STRUCT(
           AUR.partnerId,
           P.displayName AS partnerName,
           AUR.userRole,
           AUR.advertiserId,
           A.displayName AS advertiserName,
           AUR.assignedUserRoleId
         ) AS assignedUserRoles,
         FROM `{dataset}.DV_Users` AS U,
         UNNEST(assignedUserRoles) AS AUR
         LEFT JOIN `{dataset}.DV_Partners` AS P
         ON AUR.partnerId=P.partnerId
         LEFT JOIN `{dataset}.DV_Advertisers` AS A
         ON AUR.advertiserId=A.advertiserId         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_User_Roles'
    }
  })

  bigquery(config, {
    'auth':auth_write,
    'from':{
      'query':'''SELECT
         R.*,
         P.displayName AS partnerName,
         A.displayName AS advertiserName,
         FROM (
         SELECT
           queryId,
           (SELECT CAST(value AS INT64) FROM UNNEST(R.params.filters) WHERE type = 'FILTER_PARTNER' LIMIT 1) AS partnerId,
           (SELECT CAST(value AS INT64) FROM UNNEST(R.params.filters) WHERE type = 'FILTER_ADVERTISER' LIMIT 1) AS advertiserId,
           R.schedule.frequency,
           R.params.metrics,
           R.params.type,
           R.metadata.dataRange,
           R.metadata.sendNotification,
           DATE(TIMESTAMP_MILLIS(R.metadata.latestReportRunTimeMS)) AS latestReportRunTime,
         FROM `{dataset}.DV_Reports` AS R) AS R
         LEFT JOIN `{dataset}.DV_Partners` AS P
         ON R.partnerId=P.partnerId
         LEFT JOIN `{dataset}.DV_Advertisers` AS A
         ON R.advertiserId=A.advertiserId         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Barnacle_Reports'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Gives DV clients ability to see which users have access to which parts of an account. Loads DV user profile mappings using the API into BigQuery and connects to a DataStudio dashboard.

      1. DV360 only permits SERVICE accounts to access the user list API endpoint, be sure to provide and permission one.
      2. Wait for BigQuery->->->DV_... to be created.
      3. Wait for BigQuery->->->Barnacle_... to be created, then copy and connect the following data sources.
      4. Join the 1-StarThinker Assets Group to access the following assets
         4.1 - StarThinker Assets Group: https://groups.google.com/d/forum/starthinker-assets
      5. Copy 1-Barnacle DV Report.
         5.1 - Barnacle DV Report: https://datastudio.google.com/c/u/0/reporting/9f6b9e62-43ec-4027-849a-287e9c1911bd
      6. Click Edit->Resource->Manage added data sources, then edit each connection to connect to your new tables above.
      7. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for writing data.", default='user')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-partner", help="Partner ID to run user audit on.", default='')
  parser.add_argument("-recipe_slug", help="Name of Google BigQuery dataset to create.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_barnacle_dv360(config, args.auth_read, args.auth_write, args.partner, args.recipe_slug)
