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
Bucket

Create and permission a bucket in Storage.

S
p
e
c
i
f
y
 
t
h
e
 
n
a
m
e
 
o
f
 
t
h
e
 
b
u
c
k
e
t
 
a
n
d
 
w
h
o
 
w
i
l
l
 
h
a
v
e
 
o
w
n
e
r
 
p
e
r
m
i
s
s
i
o
n
s
.


E
x
i
s
t
i
n
g
 
b
u
c
k
e
t
s
 
a
r
e
 
p
r
e
s
e
r
v
e
d
.


A
d
d
i
n
g
 
a
 
p
e
r
m
i
s
s
i
o
n
 
t
o
 
t
h
e
 
l
i
s
t
 
w
i
l
l
 
u
p
d
a
t
e
 
t
h
e
 
p
e
r
m
i
s
s
i
o
n
s
 
b
u
t
 
r
e
m
o
v
i
n
g
 
t
h
e
m
 
w
i
l
l
 
n
o
t
.


Y
o
u
 
h
a
v
e
 
t
o
 
m
a
n
u
a
l
y
 
r
e
m
o
v
e
 
g
r
a
n
t
s
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'bucket_bucket': '',  # Name of Google Cloud Bucket to create.
  'bucket_emails': '',  # Comma separated emails.
  'bucket_groups': '',  # Comma separated groups.
}

TASKS = [
  {
    'bucket': {
      'auth': 'service',
      'bucket': {
        'field': {
          'name': 'bucket_bucket',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'Name of Google Cloud Bucket to create.'
        }
      },
      'emails': {
        'field': {
          'name': 'bucket_emails',
          'kind': 'string_list',
          'order': 3,
          'default': '',
          'description': 'Comma separated emails.'
        }
      },
      'groups': {
        'field': {
          'name': 'bucket_groups',
          'kind': 'string_list',
          'order': 4,
          'default': '',
          'description': 'Comma separated groups.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bucket', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
