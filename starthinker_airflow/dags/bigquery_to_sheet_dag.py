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
Query to Sheet

Copy the contents of a query into a Google Sheet.

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
 
s
h
e
e
t
 
a
n
d
 
t
h
e
 
q
u
e
r
y
.


L
e
a
v
e
 
r
a
n
g
e
 
b
l
a
n
k
 
o
r
 
s
e
t
 
t
o
 
A
2
 
t
o
 
i
n
s
e
r
t
 
o
n
e
 
l
i
n
e
 
d
o
w
n
.


T
h
e
 
r
a
n
g
e
 
i
s
 
c
l
e
a
r
e
d
 
b
e
f
o
r
e
 
t
h
e
 
s
h
e
e
t
 
i
s
 
w
r
i
t
t
e
n
 
t
o
.


T
o
 
s
e
l
e
c
t
 
a
 
t
a
b
l
e
 
u
s
e
 
S
E
L
E
C
T
 
*
 
F
R
O
M
 
t
a
b
l
e
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'sheet': '',  # Either sheet url or sheet name.
  'tab': '',  # Name of the tab where to put the data.
  'range': '',  # Range in the sheet to place the data, leave blank for whole sheet.
  'dataset': '',  # Existing BigQuery dataset.
  'query': '',  # Query to pull data from the table.
  'legacy': True,  # Use Legacy SQL
}

TASKS = [
  {
    'bigquery': {
      'auth': 'user',
      'from': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Existing BigQuery dataset.'
          }
        },
        'query': {
          'field': {
            'name': 'query',
            'kind': 'string',
            'order': 5,
            'default': '',
            'description': 'Query to pull data from the table.'
          }
        },
        'legacy': {
          'field': {
            'name': 'legacy',
            'kind': 'boolean',
            'order': 6,
            'default': True,
            'description': 'Use Legacy SQL'
          }
        }
      },
      'to': {
        'sheet': {
          'field': {
            'name': 'sheet',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Either sheet url or sheet name.'
          }
        },
        'tab': {
          'field': {
            'name': 'tab',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name of the tab where to put the data.'
          }
        },
        'range': {
          'field': {
            'name': 'range',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Range in the sheet to place the data, leave blank for whole sheet.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_to_sheet', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
