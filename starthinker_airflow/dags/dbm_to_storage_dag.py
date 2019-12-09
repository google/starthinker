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
DBM To Storage

Move existing DBM report into a Storage bucket.

S
p
e
c
i
f
y
 
e
i
t
h
e
r
 
r
e
p
o
r
t
 
n
a
m
e
 
o
r
 
r
e
p
o
r
t
 
i
d
 
t
o
 
m
o
v
e
 
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
 
m
o
s
t
 
r
e
c
e
n
t
 
v
a
l
i
d
 
f
i
l
e
 
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
 
t
h
e
 
b
u
c
k
e
t
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dbm_report_id': '',  # DBM report ID given in UI, not needed if name used.
  'dbm_report_name': '',  # Name of report, not needed if ID used.
  'dbm_bucket': '',  # Google cloud bucket.
  'dbm_path': '',  # Path and filename to write to.
  'dbm_datastudio': True,  # Format date and column nulls for DataStudio?
}

TASKS = [
  {
    'dbm': {
      'auth': 'user',
      'report': {
        'report_id': {
          'field': {
            'name': 'dbm_report_id',
            'kind': 'integer',
            'order': 1,
            'default': '',
            'description': 'DBM report ID given in UI, not needed if name used.'
          }
        },
        'name': {
          'field': {
            'name': 'dbm_report_name',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name of report, not needed if ID used.'
          }
        }
      },
      'out': {
        'storage': {
          'bucket': {
            'field': {
              'name': 'dbm_bucket',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Google cloud bucket.'
            }
          },
          'path': {
            'field': {
              'name': 'dbm_path',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Path and filename to write to.'
            }
          }
        }
      },
      'datastudio': {
        'field': {
          'name': 'dbm_datastudio',
          'kind': 'boolean',
          'order': 5,
          'default': True,
          'description': 'Format date and column nulls for DataStudio?'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dbm_to_storage', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
