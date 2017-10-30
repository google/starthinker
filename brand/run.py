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

from util.project import project 
from util.bigquery import datasets_create, datasets_access, query_to_table


def get_dbm_query(task):
  query = 'SELECT * FROM [Brand_Safety.Master_Transform] WHERE Partner_ID IN (%s)' % ','.join(map(lambda s:str(s), task['dbm_partners']))
  if task['dbm_advertisers']: query += ' AND Advertiser_ID IN (%s)' % ','.join(map(lambda s:str(s), task['dbm_advertisers'])) 
  return query


def get_dcm_query_all(task):
  query = 'SELECT * FROM [plx.google:cse_dclk.dcm_verification.AllSettingsReadable.all] WHERE dcm_account_id IN (%s)' % ','.join(map(lambda s:str(s), task['dcm_accounts']))
  if task['dcm_advertisers']: query += ' AND dcm_advertiser_id IN (%s)' % ','.join(map(lambda s:str(s), task['dcm_advertisers'])) 
  return query


def get_dcm_query_campaign(task):
  query = 'SELECT * FROM [plx.google:cse_dclk.dcm_verification.CampaignSettingsReadable.all] WHERE dcm_account_id IN (%s)' % ','.join(map(lambda s:str(s), task['dcm_accounts']))
  if task['dcm_advertisers']: query += ' AND dcm_advertiser_id IN (%s)' % ','.join(map(lambda s:str(s), task['dcm_advertisers'])) 
  return query


def brand():
  if project.verbose: print "CLIENT", project.task['dataset']

  # populate the dbm table
  if project.task.get('dbm_partners', None) or project.task.get('dbm_advertisers', None):
    query_to_table(project.task['auth'], project.id, project.task['dataset'], 'Brand_Safety_DBM', get_dbm_query(project.task))

  # populate the dcm tables
  if project.task.get('dcm_accounts', None) or project.task.get('dcm_advertisers', None):
    query_to_table(project.task['auth'], project.id, project.task['dataset'], 'Brand_Safety_DCM_All', get_dcm_query_all(project.task))
    query_to_table(project.task['auth'], project.id, project.task['dataset'], 'Brand_Safety_DCM_Campaign', get_dcm_query_campaign(project.task))

if __name__ == "__main__":
  project.load('brand')
  brand()
