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
Trends Places To BigQuery Via Values

Move using hard coded WOEID values.

P
r
o
v
i
d
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
a
p
p
s
.
t
w
i
t
t
e
r
.
c
o
m
/
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
T
w
i
t
t
e
r
 
c
r
e
d
e
n
t
i
a
l
s
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
 
a
 
c
o
m
m
a
 
d
e
l
i
m
i
t
e
d
 
l
i
s
t
 
o
f
 
W
O
E
I
D
s
.


S
p
e
c
i
f
y
 
B
i
g
Q
u
e
r
y
 
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
 
t
o
 
w
r
i
t
e
 
A
P
I
 
c
a
l
l
 
r
e
s
u
l
t
s
 
t
o
.


W
r
i
t
e
s
:
 
W
O
E
I
D
,
 
N
a
m
e
,
 
U
r
l
,
 
P
r
o
m
o
t
e
d
_
C
o
n
t
e
n
t
,
 
Q
u
e
r
y
,
 
T
w
e
e
t
_
V
o
l
u
m
e


N
o
t
e
 
T
w
i
t
t
e
r
 
A
P
I
 
i
s
 
r
a
t
e
 
l
i
m
i
t
e
d
 
t
o
 
1
5
 
r
e
q
u
e
s
t
s
 
p
e
r
 
1
5
 
m
i
n
u
t
e
s
.
 
S
o
 
k
e
e
p
 
W
O
E
I
D
 
l
i
s
t
s
 
s
h
o
r
t
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'secret': '',
  'key': '',
  'woeids': [],
  'destination_dataset': '',
  'destination_table': '',
}

TASKS = [
  {
    'twitter': {
      'auth': 'service',
      'secret': {
        'field': {
          'name': 'secret',
          'kind': 'string',
          'order': 1,
          'default': ''
        }
      },
      'key': {
        'field': {
          'name': 'key',
          'kind': 'string',
          'order': 2,
          'default': ''
        }
      },
      'trends': {
        'places': {
          'single_cell': True,
          'values': {
            'field': {
              'name': 'woeids',
              'kind': 'integer_list',
              'order': 3,
              'default': [
              ]
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
              'order': 6,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'destination_table',
              'kind': 'string',
              'order': 7,
              'default': ''
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('trends_places_to_bigquery_via_value', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
