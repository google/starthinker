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


S
e
l
e
c
t
 
t
h
e
 
f
i
l
e
 
t
y
p
e
s
 
y
o
u
 
w
a
n
t
 
f
r
o
m
 
t
h
e
 
s
d
f
.


T
h
e
 
j
o
b
 
w
i
l
l
 
g
r
a
b
 
t
h
e
 
e
n
t
i
r
e
 
s
d
f
 
a
n
d
 
u
p
l
o
a
d
 
t
o
 
y
o
u
r
 
t
a
b
l
e
.


T
h
e
 
j
o
b
 
w
i
l
l
 
a
p
p
e
n
d
 
a
n
 
u
n
d
e
r
s
c
o
r
e
 
a
n
d
 
t
h
e
 
f
i
l
e
 
t
y
p
e
 
t
o
 
t
h
e
 
p
r
o
v
i
d
e
d
 
t
a
b
l
e
 
n
a
m
e
 
f
o
r
 
t
h
e
 
r
e
s
u
l
t
 
t
a
b
l
e
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'file_types': '',  # The sdf file types to be returned.
  'filter_type': '',  # The filter type for the filter ids.
  'filter_ids': '',  # The filter ids for the request.
  'version': '3.1',  # The sdf version to be returned.
  'dataset': '',  # Dataset to be written to in BigQuery.
  'table': '',  # Table to be written to in BigQuery.
  'is_time_partition': False,  # Whether the end table is time partitioned.
}

TASKS = [
  {
    'sdf': {
      'auth': 'user',
      'version': {
        'field': {
          'name': 'version',
          'kind': 'string',
          'order': 4,
          'default': '3.1',
          'description': 'The sdf version to be returned.'
        }
      },
      'file_types': {
        'field': {
          'name': 'file_types',
          'kind': 'string_list',
          'order': 1,
          'default': '',
          'description': 'The sdf file types to be returned.'
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
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 6,
              'default': '',
              'description': 'Table to be written to in BigQuery.'
            }
          },
          'is_time_partition': {
            'field': {
              'name': 'is_time_partition',
              'kind': 'boolean',
              'order': 7,
              'default': False,
              'description': 'Whether the end table is time partitioned.'
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
