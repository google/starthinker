###########################################################################
# 
#  Copyright 2019 Google Inc.
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

'''
DCM API To BigQuery

Write the current state of accounts, subaccounts, profiles, advertisers, campaigns, sites, roles, and reports to BigQuery for a given list of DCM accounts.

S
p
e
c
i
f
y
 
t
h
e
 
n
a
m
e
 
o
f
 
t
h
e
 
d
a
t
a
s
e
t
,
 
s
e
v
e
r
a
l
 
t
a
b
l
e
s
 
w
i
l
l
 
b
e
 
c
r
e
a
t
e
d
 
h
e
r
e
.


I
f
 
d
a
t
a
s
e
t
 
e
x
i
s
t
s
,
 
i
t
 
i
s
 
i
n
c
h
a
n
g
e
d
.


A
d
d
 
D
C
M
 
a
c
c
o
u
n
t
 
i
d
s
 
f
o
r
 
t
h
e
 
a
c
c
o
u
n
t
s
 
t
o
 
p
u
l
l
 
d
a
t
a
 
f
r
o
m
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'endpoint': '',
  'dataset': '',  # Google BigQuery dataset to create tables in.
  'accounts': '',  # Comma separated DCM account ids.
}

TASKS = [
  {
    'dcm_api': {
      'auth': 'user',
      'endpoints': {
        'field': {
          'name': 'endpoint',
          'kind': 'choice',
          'choices': [
            'accountPermissionGroups',
            'accountPermissions',
            'accountUserProfiles',
            'accounts',
            'ads',
            'advertiserGroups',
            'advertiserLandingPages',
            'advertisers',
            'browsers',
            'campaigns',
            'changeLogs',
            'cities',
            'connectionTypes',
            'contentCategories',
            'countries',
            'creativeFields',
            'creativeGroups',
            'creatives',
            'directorySites',
            'dynamicTargetingKeys',
            'eventTags',
            'files',
            'floodlightActivities',
            'floodlightActivityGroups',
            'floodlightConfigurations',
            'languages',
            'metros',
            'mobileApps',
            'mobileCarriers',
            'operatingSystemVersions',
            'operatingSystems',
            'placementGroups',
            'placementStrategies',
            'placements',
            'platformTypes',
            'postalCodes',
            'projects',
            'regions',
            'remarketingLists',
            'reports',
            'sites',
            'sizes',
            'subaccounts',
            'targetableRemarketingLists',
            'targetingTemplates',
            'userprofiles',
            'userRolePermissionGroups',
            'userRolePermissions',
            'userRoles',
            'videoFormats'
          ],
          'default': ''
        }
      },
      'accounts': {
        'single_cell': True,
        'values': {
          'field': {
            'name': 'accounts',
            'kind': 'integer_list',
            'order': 2,
            'default': '',
            'description': 'Comma separated DCM account ids.'
          }
        }
      },
      'out': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Google BigQuery dataset to create tables in.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_api_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
