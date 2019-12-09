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
DCM Report

Create a DCM report from a JSON definition.

A
d
d
 
a
 
a
n
 
a
c
c
o
u
n
t
 
a
s
 
[
a
c
c
o
u
n
t
_
i
d
]
@
[
p
r
o
f
i
l
e
_
i
d
]


F
e
t
c
h
 
t
h
e
 
r
e
p
o
r
t
 
J
S
O
N
 
d
e
f
i
n
i
t
i
o
n
.
 
A
r
g
u
a
b
l
y
 
c
o
u
l
d
 
b
e
 
b
e
t
t
e
r
.


T
h
e
 
a
c
c
o
u
n
t
 
i
s
 
a
u
t
o
m
a
t
i
c
a
l
l
y
 
a
d
d
e
d
 
t
o
 
t
h
e
 
r
e
p
o
r
t
 
d
e
f
i
n
i
t
i
o
n
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'account': '',
  'body': '{}',
  'delete': False,
}

TASKS = [
  {
    'dcm': {
      'auth': 'user',
      'report': {
        'account': {
          'field': {
            'name': 'account',
            'kind': 'string',
            'order': 1,
            'default': ''
          }
        },
        'body': {
          'field': {
            'name': 'body',
            'kind': 'json',
            'order': 2,
            'default': '{}'
          }
        }
      },
      'delete': {
        'field': {
          'name': 'delete',
          'kind': 'boolean',
          'order': 3,
          'default': False
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
