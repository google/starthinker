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
Sheet To Table

Import data from a sheet and move it to a BigQuery table.

F
o
r
 
t
h
e
 
s
h
e
e
t
,
 
p
r
o
v
i
d
e
 
t
h
e
 
f
u
l
l
 
e
d
i
t
 
U
R
L
.


I
f
 
t
h
e
 
t
a
b
 
d
o
e
s
 
n
o
t
 
e
x
i
s
t
 
i
t
 
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
.


E
m
p
t
y
 
c
e
l
l
s
 
i
n
 
t
h
e
 
r
a
n
g
e
 
w
i
l
l
 
b
e
 
N
U
L
L
.


C
h
e
c
k
 
S
h
e
e
t
s
 
h
e
a
d
e
r
 
i
f
 
f
i
r
s
t
 
r
o
w
 
i
s
 
a
 
h
e
a
d
e
r

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'sheets_url': '',
  'sheets_tab': '',
  'sheets_range': '',
  'dataset': '',
  'table': '',
  'sheets_header': True,
}

TASKS = [
  {
    'sheets': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'sheets_url',
          'kind': 'string',
          'order': 1,
          'default': ''
        }
      },
      'tab': {
        'field': {
          'name': 'sheets_tab',
          'kind': 'string',
          'order': 2,
          'default': ''
        }
      },
      'range': {
        'field': {
          'name': 'sheets_range',
          'kind': 'string',
          'order': 3,
          'default': ''
        }
      },
      'header': {
        'field': {
          'name': 'sheets_header',
          'kind': 'boolean',
          'order': 9,
          'default': True
        }
      },
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 7,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 8,
              'default': ''
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('sheets_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
