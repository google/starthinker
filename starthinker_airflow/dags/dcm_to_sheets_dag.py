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
DCM To Sheets

Move existing DCM report into a Sheet tab.

S
p
e
c
i
f
y
 
a
n
 
a
c
c
o
u
n
t
 
i
d
.


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
 
s
h
e
e
t
.


S
c
h
e
m
a
 
i
s
 
p
u
l
l
e
d
 
f
r
o
m
 
t
h
e
 
o
f
f
i
c
i
a
l
 
D
C
M
 
s
p
e
c
i
f
i
c
a
t
i
o
n
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'account': '',
  'report_id': '',
  'report_name': '',
  'sheet': '',
  'tab': '',
}

TASKS = [
  {
    'dcm': {
      'auth': 'user',
      'report': {
        'account': {
          'field': {
            'name': 'account',
            'kind': 'integer',
            'order': 2,
            'default': ''
          }
        },
        'report_id': {
          'field': {
            'name': 'report_id',
            'kind': 'integer',
            'order': 3,
            'default': ''
          }
        },
        'name': {
          'field': {
            'name': 'report_name',
            'kind': 'string',
            'order': 4,
            'default': ''
          }
        }
      },
      'out': {
        'sheets': {
          'sheet': {
            'field': {
              'name': 'sheet',
              'kind': 'string',
              'order': 5,
              'default': ''
            }
          },
          'tab': {
            'field': {
              'name': 'tab',
              'kind': 'string',
              'order': 6,
              'default': ''
            }
          },
          'range': 'A1'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_to_sheets', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
