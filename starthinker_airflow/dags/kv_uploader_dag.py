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
Tag Key Value Uploader

A tool for bulk editing key value pairs for DCM pllacements.

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
 
i
n
 
t
h
e
 
s
h
e
e
t
 
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
        'source': 'https://docs.google.com/spreadsheets/d/19Sxy4BDtK9ocq_INKTiZ-rZHgqhfpiiokXOTsYzmah0/',
        'destination': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'Key Value Uploader For ',
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

DAG_FACTORY = DAG_Factory('kv_uploader', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
