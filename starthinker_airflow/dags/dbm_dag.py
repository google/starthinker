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
DBM Report

Create a DBM report.

R
e
f
e
r
e
n
c
e
 
f
i
e
l
d
 
v
a
l
u
e
s
 
f
r
o
m
 
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
/
r
e
p
o
r
t
s
'
>
D
B
M
 
A
P
I
<
/
a
>
 
t
o
 
b
u
i
l
d
 
a
 
r
e
p
o
r
t
.


C
o
p
y
 
a
n
d
 
p
a
s
t
e
 
t
h
e
 
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
 
o
f
 
a
 
r
e
p
o
r
t
.


T
h
e
 
r
e
p
o
r
t
 
i
s
 
o
n
l
y
 
c
r
e
a
t
e
d
,
 
u
s
e
 
a
 
m
o
v
e
 
s
c
r
i
p
t
 
t
o
 
m
o
v
e
 
i
t
.


T
o
 
r
e
s
e
t
 
a
 
r
e
p
o
r
t
,
 
d
e
l
e
t
e
 
i
t
 
f
r
o
m
 
D
B
M
 
r
e
p
o
r
t
i
n
g
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'body': '{}',
  'delete': False,
}

TASKS = [
  {
    'dbm': {
      'auth': 'user',
      'report': {
        'body': {
          'field': {
            'name': 'body',
            'kind': 'json',
            'order': 1,
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

DAG_FACTORY = DAG_Factory('dbm', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
