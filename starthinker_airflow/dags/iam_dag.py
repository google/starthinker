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
Project IAM

Sets project permissions for an email.

P
r
o
v
i
d
e
 
a
 
r
o
l
e
 
i
n
 
t
h
e
 
f
o
r
m
 
o
f
 
p
r
o
j
e
c
t
s
/
[
p
r
o
j
e
c
t
 
n
a
m
e
]
/
r
o
l
e
s
/
[
r
o
l
e
 
n
a
m
e
]


E
n
t
e
r
 
a
n
 
e
m
a
i
l
 
t
o
 
g
r
a
n
t
 
t
h
a
t
 
r
o
l
e
 
t
o
.


T
h
i
s
 
o
n
l
y
 
g
r
a
n
t
s
 
r
o
l
e
s
,
 
y
o
u
 
m
u
s
t
 
r
e
m
o
v
e
 
t
h
e
m
 
f
r
o
m
 
t
h
e
 
p
r
o
j
e
c
t
 
m
a
n
u
a
l
l
y
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'role': '',  # projects/[project name]/roles/[role name]
  'email': '',  # Email address to grant role to.
}

TASKS = [
  {
    'iam': {
      'auth': 'service',
      'role': {
        'field': {
          'name': 'role',
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'projects/[project name]/roles/[role name]'
        }
      },
      'email': {
        'field': {
          'name': 'email',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'Email address to grant role to.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('iam', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
