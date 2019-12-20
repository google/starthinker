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
SDF Download

Download SDF reports into a BigQuery table.

S
e
l
e
c
t
 
y
o
u
r
 
f
i
l
t
e
r
 
t
y
p
e
s
 
a
n
d
 
t
h
e
 
f
i
l
t
e
r
 
i
d
e
a
s
.


E
n
t
e
r
 
t
h
e
 
<
a
 
h
r
e
f
=
'
h
t
t
p
s
:
/
/
d
e
v
e
l
o
p
e
r
s
.
g
o
o
g
l
e
.
c
o
m
/
b
i
d
-
m
a
n
a
g
e
r
/
v
1
.
1
/
s
d
f
/
d
o
w
n
l
o
a
d
'
 
t
a
r
g
e
t
=
'
_
b
l
a
n
k
'
>
f
i
l
e
 
t
y
p
e
s
<
/
a
>
 
u
s
i
n
g
 
c
o
m
m
a
s
.


S
D
F
_
 
w
i
l
l
 
b
e
 
p
r
e
f
i
x
e
d
 
t
o
 
a
l
l
 
t
a
b
l
e
s
 
a
n
d
 
d
a
t
e
 
a
p
p
e
n
d
e
d
 
t
o
 
d
a
i
l
y
 
t
a
b
l
e
s
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'file_types': [],  # The sdf file types.
  'filter_type': '',  # The filter type for the filter ids.
  'filter_ids': '',  # The filter ids for the request.
  'version': '5',  # The sdf version to be returned.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'daily': False,  # Also create a unique record for each day the data is pulled.
}

TASKS = [
  {
    'sdf': {
      'auth': 'user',
      'version': {
        'field': {
          'name': 'version',
          'kind': 'choice',
          'order': 4,
          'default': '5',
          'description': 'The sdf version to be returned.',
          'choices': [
            '3.1',
            '5'
          ]
        }
      },
      'file_types': {
        'field': {
          'name': 'file_types',
          'kind': 'string_list',
          'order': 1,
          'default': [
          ],
          'description': 'The sdf file types.'
        }
      },
      'filter_type': {
        'field': {
          'name': 'filter_type',
          'kind': 'choice',
          'order': 2,
          'default': '',
          'description': 'The filter type for the filter ids.',
          'choices': [
            'ADVERTISER_ID',
            'CAMPAIGN_ID',
            'INSERTION_ORDER_ID',
            'INVENTORY_SOURCE_ID',
            'LINE_ITEM_ID',
            'PARTNER_ID'
          ]
        }
      },
      'read': {
        'filter_ids': {
          'single_cell': True,
          'values': {
            'field': {
              'name': 'filter_ids',
              'kind': 'integer_list',
              'order': 3,
              'default': '',
              'description': 'The filter ids for the request.'
            }
          }
        }
      },
      'daily': {
        'field': {
          'name': 'daily',
          'kind': 'boolean',
          'order': 6,
          'default': False,
          'description': 'Also create a unique record for each day the data is pulled.'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 5,
              'default': '',
              'description': 'Dataset to be written to in BigQuery.'
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('sdf_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
