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
Google Analytics Timeline

Download Google Analytics settings to a BigQuery table.

E
n
t
e
r
 
t
h
e
 
d
a
t
e
s
e
t
 
t
o
 
w
h
i
c
h
 
t
h
e
 
G
o
o
g
l
e
 
A
n
a
l
y
t
i
c
s
 
s
e
t
t
i
n
g
s
 
w
i
l
l
 
b
e
 
d
o
w
n
l
o
a
d
e
d
.


A
d
d
 
t
h
e
 
s
t
a
r
t
h
i
n
k
e
r
 
s
e
r
v
i
c
e
 
a
c
c
o
u
n
t
 
e
m
a
i
l
 
t
o
 
t
h
e
 
G
o
o
g
l
e
 
A
n
a
l
y
t
i
c
s
 
a
c
c
o
u
n
t
(
s
)
 
i
n
 
w
h
i
c
h
 
y
o
u
 
a
r
e
 
i
n
t
e
r
e
s
t
e
d
.


S
c
h
e
d
u
l
e
 
t
h
e
 
r
e
c
i
p
e
 
t
o
 
r
u
n
 
o
n
c
e
 
a
 
d
a
y
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'account_ids': [],
  'dataset': '',  # Dataset to be written to in BigQuery.
}

TASKS = [
  {
    'ga_settings_download': {
      'description': 'Will create tables with format ga_* to hold each endpoint via a call to the API list function.',
      'auth': 'user',
      'accounts': {
        'field': {
          'name': 'account_ids',
          'kind': 'integer_list',
          'order': 1,
          'default': [
          ]
        }
      },
      'dataset': {
        'field': {
          'name': 'dataset',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'Dataset to be written to in BigQuery.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('ga_timeline', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
