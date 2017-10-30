###########################################################################
#
#  Copyright 2017 Google Inc.
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

#https://cloud.google.com/bigquery/docs/share-access-views

from util.project import project
from util.bigquery import datasets_create, datasets_access, query_to_table, query_to_view


# BUG: can't mic PLX with BigQuery, so thisneeds to be fixed.
def get_query(task):
  query = '''
    SELECT
      SESSION_USER() AS Current_User,
      *
    FROM `%s.%s.%s`
    WHERE
      Advertiser_ID IN (
        SELECT DISTINCT CAST(advertiser_id AS INT64)
        FROM `google.com:dbm-util.plximport.dbm_access_hourly`
        WHERE
          primary_email_hashed = SHA256(LOWER(SESSION_USER()))
            OR
          (
            SELECT has_global_read
            FROM `google.com:dbm-util.plximport.dbm_access_hourly` access
            WHERE
              primary_email_hashed = SHA256(LOWER(SESSION_USER()))
                AND
              has_global_read
            LIMIT 1
          )
      )
  ''' % (project.id, project.task['dataset'], project.task['table'])

  #print query
  return query


def dbm_authorize():
  if project.verbose: print "Authorizing", project.task['dataset'], project.task['table']

  authorized_dataset =  '%s_Authorized_DBM' % project.task['dataset']
  authorized_view =  '%s_Authorized_DBM' % project.task['table']

  # Create a separate dataset to store the authorized view
  datasets_create(project.task['auth'], project.id, authorized_dataset)

  # Create the authorized view in the new dataset
  query_to_view(project.task['auth'], project.id, authorized_dataset, authorized_view, get_query(project.task), legacy=False)

  # Assign access controls to the dataset containing the view
  datasets_access(project.task['auth'], project.id, authorized_dataset, groups=project.task['groups'], role='READER')

  # Authorize the view to access the source dataset
  datasets_access(project.task['auth'], project.id, project.task['dataset'], views=[{'dataset':authorized_dataset, 'view':authorized_view}])
  

if __name__ == "__main__":
  project.load('dbm_authorize')
  dbm_authorize()
