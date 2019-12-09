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
Anonymize Dataset

Copies tables and view from one dataset to another and anynonamizes all rows.  Used to create sample datasets for dashboards.

E
n
s
u
r
e
 
y
o
u
 
h
a
v
e
 
u
s
e
r
 
a
c
c
e
s
s
 
t
o
 
b
o
t
h
 
d
a
t
a
s
e
t
s
.


P
r
o
v
i
d
e
 
t
h
e
 
s
o
u
r
c
e
 
p
r
o
j
e
c
t
 
a
n
d
 
d
a
t
a
s
e
t
.


P
r
o
v
i
d
e
 
t
h
e
 
d
e
s
t
i
n
a
t
i
o
n
 
p
r
o
j
e
c
t
 
a
n
d
 
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
  'from_project': '',  # Original project to copy from.
  'from_dataset': '',  # Original dataset to copy from.
  'to_project': '',  # Anonymous data will be writen to.
  'to_dataset': '',  # Anonymous data will be writen to.
}

TASKS = [
  {
    'anonymize': {
      'auth': 'user',
      'bigquery': {
        'from': {
          'project': {
            'field': {
              'name': 'from_project',
              'kind': 'string',
              'order': 1,
              'description': 'Original project to copy from.'
            }
          },
          'dataset': {
            'field': {
              'name': 'from_dataset',
              'kind': 'string',
              'order': 2,
              'description': 'Original dataset to copy from.'
            }
          }
        },
        'to': {
          'project': {
            'field': {
              'name': 'to_project',
              'kind': 'string',
              'order': 3,
              'description': 'Anonymous data will be writen to.'
            }
          },
          'dataset': {
            'field': {
              'name': 'to_dataset',
              'kind': 'string',
              'order': 4,
              'description': 'Anonymous data will be writen to.'
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('anonymize', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
