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
Dataset

Create and permission a dataset in BigQuery.

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
 
d
a
t
a
s
e
t
.


I
f
 
d
a
t
a
s
e
t
 
e
x
i
s
t
s
,
 
i
t
 
i
s
 
i
n
c
h
a
n
g
e
d
.


A
d
d
 
e
m
a
i
l
s
 
a
n
d
 
/
 
o
r
 
g
r
o
u
p
s
 
t
o
 
a
d
d
 
r
e
a
d
 
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
.


C
A
U
T
I
O
N
:
 
R
e
m
o
v
i
n
g
 
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
 
i
n
 
S
t
a
r
T
h
i
n
k
e
r
 
h
a
s
 
n
o
 
e
f
f
e
c
t
.


C
A
U
T
I
O
N
:
 
T
o
 
r
e
m
o
v
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
 
y
o
u
 
h
a
v
e
 
t
o
 
e
d
i
t
 
t
h
e
 
d
a
t
a
s
e
t
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dataset_dataset': '',  # Name of Google BigQuery dataset to create.
  'dataset_emails': [],  # Comma separated emails.
  'dataset_groups': [],  # Comma separated groups.
}

TASKS = [
  {
    'dataset': {
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'dataset_dataset',
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'Name of Google BigQuery dataset to create.'
        }
      },
      'emails': {
        'field': {
          'name': 'dataset_emails',
          'kind': 'string_list',
          'order': 2,
          'default': [
          ],
          'description': 'Comma separated emails.'
        }
      },
      'groups': {
        'field': {
          'name': 'dataset_groups',
          'kind': 'string_list',
          'order': 3,
          'default': [
          ],
          'description': 'Comma separated groups.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dataset', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
