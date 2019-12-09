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
Line Item To BigQuery Via Query

Move using an Id query.

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
 
q
u
e
r
y
 
t
h
a
t
 
w
i
l
l
 
p
u
l
l
 
t
h
e
 
l
i
n
e
i
t
e
m
 
i
d
s
 
t
o
 
d
o
w
n
l
o
a
d
.


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
 
d
a
t
a
s
e
t
 
a
n
d
 
t
a
b
l
e
 
w
h
e
r
e
 
t
h
e
 
l
i
n
e
i
t
e
m
s
 
w
i
l
l
 
b
e
 
w
r
i
t
t
e
n
.


T
h
e
 
s
c
h
e
m
a
 
w
i
l
l
 
m
a
t
c
h
 
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
g
u
i
d
e
s
/
e
n
t
i
t
y
-
w
r
i
t
e
/
f
o
r
m
a
t
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
E
n
t
i
t
y
 
W
r
i
t
e
 
F
o
r
m
a
t
<
/
a
>
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'id_dataset': '',
  'id_query': 'SELECT * FROM `Dataset.Table`;',
  'id_legacy': False,
  'destination_dataset': '',
  'destination_table': '',
}

TASKS = [
  {
    'lineitem': {
      'auth': 'user',
      'read': {
        'line_items': {
          'single_cell': True,
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'id_dataset',
                'kind': 'string',
                'order': 1,
                'default': ''
              }
            },
            'query': {
              'field': {
                'name': 'id_query',
                'kind': 'string',
                'order': 2,
                'default': 'SELECT * FROM `Dataset.Table`;'
              }
            },
            'legacy': {
              'field': {
                'name': 'id_legacy',
                'kind': 'boolean',
                'order': 3,
                'default': False
              }
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'destination_dataset',
                'kind': 'string',
                'order': 4,
                'default': ''
              }
            },
            'table': {
              'field': {
                'name': 'destination_table',
                'kind': 'string',
                'order': 5,
                'default': ''
              }
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('lineitem_read_to_bigquery_via_query', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
