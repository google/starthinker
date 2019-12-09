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
PoliceBot

A tool that helps enforce CM object name conventions by checking names against a set of client-defined patterns, and emailing violations to appropriate agency teams on a daily basis.

A
d
d
 
t
h
i
s
 
c
a
r
d
 
t
o
 
a
 
r
e
c
i
p
e
 
a
n
d
 
s
a
v
e
 
i
t
.


T
h
e
n
 
c
l
i
c
k
 
<
s
t
r
o
n
g
>
R
u
n
 
N
o
w
<
/
s
t
r
o
n
g
>
 
t
o
 
d
e
p
l
o
y
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
 
<
a
 
h
r
e
f
=
"
h
t
t
p
s
:
/
/
d
o
c
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
c
u
m
e
n
t
/
d
/
1
e
u
S
Z
t
5
V
F
m
a
M
f
V
-
v
S
h
b
6
N
H
6
L
W
f
A
7
a
5
K
S
P
p
S
l
1
h
Y
e
N
l
A
A
"
>
i
n
s
t
r
u
c
t
u
o
n
s
<
/
a
>
 
f
o
r
 
s
e
t
u
p
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'recipe_name': '',  # Name of document to deploy to.
}

TASKS = [
  {
    'drive': {
      'auth': 'user',
      'hour': [
      ],
      'copy': {
        'source': 'https://docs.google.com/spreadsheets/d/1dkESiK2s8YvdC03F3t4Jk_wvxJ0NMNk8CTGxO0HQk6I',
        'destination': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'PoliceBot For ',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('policebot', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
