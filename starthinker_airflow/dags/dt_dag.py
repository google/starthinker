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
DT To Table

Move data from a DT bucket into a BigQuery table.

E
n
s
u
r
e
 
y
o
u
r
 
u
s
e
r
 
h
a
s
 
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
d
o
u
b
l
e
c
l
i
c
k
-
a
d
v
e
r
t
i
s
e
r
s
/
d
t
v
2
/
g
e
t
t
i
n
g
-
s
t
a
r
t
e
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
a
c
c
e
s
s
 
t
o
 
t
h
e
 
b
u
c
k
e
t
<
/
a
>
.


P
r
o
v
i
d
e
 
t
h
e
 
D
T
 
b
u
c
k
e
t
 
n
a
m
e
 
t
o
 
r
e
a
d
 
f
r
o
m
.


P
r
o
v
i
d
e
 
t
h
e
 
p
a
t
h
 
o
f
 
t
h
e
 
f
i
l
e
s
 
t
o
 
r
e
a
d
.


E
a
c
h
 
f
i
l
e
 
i
s
 
s
y
n
c
h
r
o
n
i
z
e
d
 
t
o
 
a
 
u
n
i
q
u
e
 
t
a
b
l
e
.
 
 
U
s
e
 
a
 
v
i
e
w
 
o
r
 
a
g
g
r
e
g
a
t
e
 
s
e
l
e
c
t
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'bucket': '',  # Name of bucket where DT files are stored.
  'paths': [],  # List of prefixes to pull specific DT files.
  'days': 2,  # Number of days back to synchronize.
  'hours': 0,  # Number of hours back to synchronize.
  'dataset': '',  # Existing dataset in BigQuery.
}

TASKS = [
  {
    'dt': {
      'auth': 'user',
      'from': {
        'bucket': {
          'field': {
            'name': 'bucket',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Name of bucket where DT files are stored.'
          }
        },
        'paths': {
          'field': {
            'name': 'paths',
            'kind': 'string_list',
            'order': 2,
            'default': [
            ],
            'description': 'List of prefixes to pull specific DT files.'
          }
        },
        'days': {
          'field': {
            'name': 'days',
            'kind': 'integer',
            'order': 3,
            'default': 2,
            'description': 'Number of days back to synchronize.'
          }
        },
        'hours': {
          'field': {
            'name': 'hours',
            'kind': 'integer',
            'order': 3,
            'default': 0,
            'description': 'Number of hours back to synchronize.'
          }
        }
      },
      'to': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Existing dataset in BigQuery.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dt', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
