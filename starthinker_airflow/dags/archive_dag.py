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
Archive

Wipe old information from a Storage bucket.

S
p
e
c
i
f
y
 
h
o
w
 
m
a
n
y
 
d
a
y
s
 
b
a
c
k
 
t
o
 
r
e
t
a
i
n
 
d
a
t
a
 
a
n
d
 
w
h
i
c
h
 
b
u
c
k
e
t
s
 
a
n
d
 
p
a
t
h
s
 
t
o
 
p
u
r
g
e
.


E
v
e
r
y
t
h
i
n
g
 
u
n
d
e
r
 
a
 
p
a
t
h
 
w
i
l
l
 
b
e
 
m
o
v
e
d
 
t
o
 
a
r
c
h
i
v
e
 
o
r
 
d
e
l
e
t
e
d
 
d
e
p
e
n
d
i
n
g
 
o
n
 
y
o
u
r
 
c
h
o
i
c
e
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'archive_days': 7,
  'archive_bucket': '',
  'archive_path': '',
  'archive_delete': False,
}

TASKS = [
  {
    'archive': {
      'auth': 'service',
      'days': {
        'field': {
          'name': 'archive_days',
          'kind': 'integer',
          'order': 1,
          'default': 7
        }
      },
      'storage': {
        'bucket': {
          'field': {
            'name': 'archive_bucket',
            'kind': 'string',
            'order': 2,
            'default': ''
          }
        },
        'path': {
          'field': {
            'name': 'archive_path',
            'kind': 'string',
            'order': 3,
            'default': ''
          }
        }
      },
      'delete': {
        'field': {
          'name': 'archive_delete',
          'kind': 'boolean',
          'order': 4,
          'default': False
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('archive', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
