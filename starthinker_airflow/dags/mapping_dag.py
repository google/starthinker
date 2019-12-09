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
Column Mapping

Use sheet to define keyword to column mappings.

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
 
U
R
L
.


A
 
t
a
b
 
c
a
l
l
e
d
 
<
s
t
r
o
n
g
>
M
a
p
p
i
n
g
<
/
s
t
r
o
n
g
>
 
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


F
o
l
l
o
w
 
t
h
e
 
i
n
s
t
r
u
c
t
i
o
n
s
 
i
n
 
t
h
e
 
t
a
b
 
t
o
 
c
o
m
p
l
e
t
e
 
t
h
e
 
m
a
p
p
i
n
g
.


T
h
e
 
i
n
 
t
a
b
l
e
 
s
h
o
u
l
d
 
h
a
v
e
 
t
h
e
 
c
o
l
u
m
n
s
 
y
o
u
 
w
a
n
t
 
t
o
 
m
a
p
.


T
h
e
 
o
u
t
 
v
i
e
w
 
w
i
l
l
 
h
a
v
e
 
t
h
e
 
n
e
w
 
c
o
l
u
m
n
s
 
c
r
e
a
t
e
d
 
i
n
 
t
h
e
 
m
a
p
p
i
n
g
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'sheet': '',
  'tab': '',
  'in_dataset': '',
  'in_table': '',
  'out_dataset': '',
  'out_view': '',
}

TASKS = [
  {
    'mapping': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'sheet',
          'kind': 'string',
          'order': 1,
          'default': ''
        }
      },
      'tab': {
        'field': {
          'name': 'tab',
          'kind': 'string',
          'order': 2,
          'default': ''
        }
      },
      'in': {
        'dataset': {
          'field': {
            'name': 'in_dataset',
            'kind': 'string',
            'order': 3,
            'default': ''
          }
        },
        'table': {
          'field': {
            'name': 'in_table',
            'kind': 'string',
            'order': 4,
            'default': ''
          }
        }
      },
      'out': {
        'dataset': {
          'field': {
            'name': 'out_dataset',
            'kind': 'string',
            'order': 7,
            'default': ''
          }
        },
        'view': {
          'field': {
            'name': 'out_view',
            'kind': 'string',
            'order': 8,
            'default': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('mapping', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
