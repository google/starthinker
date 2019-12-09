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
API To BigQuery

Execute a Google API function and store results to BigQuery.

E
n
t
e
r
 
a
n
 
a
p
i
 
n
a
m
e
 
a
n
d
 
v
e
r
s
i
o
n
.


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
 
f
u
n
c
t
i
o
n
 
u
s
i
n
g
 
d
o
t
 
n
o
t
a
t
i
o
n
 
a
n
d
 
a
r
g
u
m
e
n
t
s
 
u
s
i
n
g
 
j
s
o
n
.


I
f
 
n
e
x
t
P
a
g
e
T
o
k
e
n
 
c
a
n
 
b
e
 
i
n
 
r
e
s
p
o
n
s
e
 
c
h
e
c
k
 
i
t
e
r
a
t
e
.


G
i
v
e
 
B
i
g
Q
u
e
r
y
 
d
a
t
a
s
e
t
 
a
n
d
 
t
a
b
l
e
 
w
h
e
r
e
 
r
e
s
p
o
n
s
e
 
w
i
l
l
 
b
e
 
w
r
i
t
t
e
n
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'api': 'doubleclickbidmanager',  # See developer guide.
  'version': 'v1',  # Must be supported version.
  'function': 'reports.files.list',  # Full function dot notation path.
  'kwargs': {'accountId': 7480, 'profileId': 2782211, 'reportId': 132847265},  # Dictionray object of name value pairs.
  'iterate': False,  # Is the result a list?
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Table to write API call results to.
  'schema': [],  # Schema provided in JSON list format or empty list.
}

TASKS = [
  {
    'google_api': {
      'auth': 'user',
      'api': {
        'field': {
          'name': 'api',
          'kind': 'string',
          'order': 1,
          'default': 'doubleclickbidmanager',
          'description': 'See developer guide.'
        }
      },
      'version': {
        'field': {
          'name': 'version',
          'kind': 'string',
          'order': 2,
          'default': 'v1',
          'description': 'Must be supported version.'
        }
      },
      'function': {
        'field': {
          'name': 'function',
          'kind': 'string',
          'order': 3,
          'default': 'reports.files.list',
          'description': 'Full function dot notation path.'
        }
      },
      'kwargs': {
        'field': {
          'name': 'kwargs',
          'kind': 'json',
          'order': 4,
          'default': {
            'accountId': 7480,
            'profileId': 2782211,
            'reportId': 132847265
          },
          'description': 'Dictionray object of name value pairs.'
        }
      },
      'iterate': {
        'field': {
          'name': 'iterate',
          'kind': 'boolean',
          'order': 5,
          'default': False,
          'description': 'Is the result a list?'
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 6,
              'default': '',
              'description': 'Existing dataset in BigQuery.'
            }
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 7,
              'default': '',
              'description': 'Table to write API call results to.'
            }
          },
          'schema': {
            'field': {
              'name': 'schema',
              'kind': 'json',
              'order': 9,
              'default': [
              ],
              'description': 'Schema provided in JSON list format or empty list.'
            }
          },
          'format': 'JSON'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('google_api_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
