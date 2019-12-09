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
Entity Read Files

Import public and private <a href='https://developers.google.com/bid-manager/guides/entity-read/format-v2' target='_blank'>Entity Read Files</a> into a BigQuery dataset.<br/>CAUTION: PARTNER ONLY, ADVERTISER FILTER IS NOT APPLIED.

E
n
t
i
t
y
 
R
e
a
d
 
F
i
l
e
s
 
O
N
L
Y
 
w
o
r
k
 
a
t
 
t
h
e
 
p
a
r
t
n
e
r
 
l
e
v
e
l
.


A
d
v
e
r
t
i
s
e
r
 
f
i
l
t
e
r
 
i
s
 
N
O
T
 
A
P
P
L
I
E
D
.


S
p
e
c
i
f
y
 
o
n
e
 
o
r
 
m
o
r
e
 
p
a
r
t
n
e
r
s
 
t
o
 
b
e
 
m
o
v
e
d
 
i
n
t
o
 
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
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'partners': '[]',  # Comma sparated list of DBM partners.
  'dataset': '',  # BigQuery dataset to write tables for each entity.
}

TASKS = [
  {
    'dataset': {
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'dataset',
          'kind': 'string',
          'order': 3,
          'default': '',
          'description': 'BigQuery dataset to write tables for each entity.'
        }
      }
    }
  },
  {
    'entity': {
      'auth': 'user',
      'prefix': 'Entity',
      'entities': [
        'Campaign',
        'LineItem',
        'Creative',
        'UserList',
        'Partner',
        'Advertiser',
        'InsertionOrder',
        'Pixel',
        'InventorySource',
        'CustomAffinity',
        'UniversalChannel',
        'UniversalSite',
        'SupportedExchange',
        'DataPartner',
        'GeoLocation',
        'Language',
        'DeviceCriteria',
        'Browser',
        'Isp'
      ],
      'partners': {
        'single_cell': True,
        'values': {
          'field': {
            'name': 'partners',
            'kind': 'integer_list',
            'order': 1,
            'default': '[]',
            'description': 'Comma sparated list of DBM partners.'
          }
        }
      },
      'out': {
        'bigquery': {
          'auth': 'service',
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'BigQuery dataset to write tables for each entity.'
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('entity', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
