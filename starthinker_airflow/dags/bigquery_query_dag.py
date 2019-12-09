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
Query To Table

Save query results into a BigQuery table.

S
p
e
c
i
f
y
 
a
 
s
i
n
g
l
e
 
q
u
e
r
y
 
a
n
d
 
c
h
o
o
s
e
 
l
e
g
a
c
y
 
o
r
 
s
t
a
n
d
a
r
d
 
m
o
d
e
.


F
o
r
 
P
L
X
 
u
s
e
:
 
S
E
L
E
C
T
 
*
 
F
R
O
M
 
[
p
l
x
.
g
o
o
g
l
e
:
F
U
L
L
_
T
A
B
L
E
_
N
A
M
E
.
a
l
l
]
 
W
H
E
R
E
.
.
.


E
v
e
r
y
 
t
i
m
e
 
t
h
e
 
q
u
e
r
y
 
r
u
n
s
 
i
t
 
w
i
l
l
 
o
v
e
r
w
r
i
t
e
 
t
h
e
 
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
  'query': '',  # SQL with newlines and all.
  'dataset': '',  # Existing BigQuery dataset.
  'table': '',  # Table to create from this query.
  'legacy': True,  # Query type must match source tables.
}

TASKS = [
  {
    'bigquery': {
      'auth': 'service',
      'from': {
        'query': {
          'field': {
            'name': 'query',
            'kind': 'text',
            'order': 1,
            'default': '',
            'description': 'SQL with newlines and all.'
          }
        },
        'legacy': {
          'field': {
            'name': 'legacy',
            'kind': 'boolean',
            'order': 4,
            'default': True,
            'description': 'Query type must match source tables.'
          }
        }
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Existing BigQuery dataset.'
          }
        },
        'table': {
          'field': {
            'name': 'table',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Table to create from this query.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_query', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
