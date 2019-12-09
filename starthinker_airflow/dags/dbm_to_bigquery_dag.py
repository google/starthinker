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
DBM To BigQuery

Move existing DBM reports into a BigQuery table.

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


A
 
s
c
h
e
m
a
 
i
s
 
r
e
c
o
m
m
e
n
d
e
d
,
 
i
f
 
n
o
t
 
p
r
o
v
i
d
e
d
 
i
t
 
w
i
l
l
 
b
e
 
g
u
e
s
s
e
d
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
  'dbm_report_id': '',  # DBM report ID given in UI, not needed if name used.
  'dbm_report_name': '',  # Name of report, not needed if ID used.
  'dbm_dataset': '',  # Existing BigQuery dataset.
  'dbm_table': '',  # Table to create from this report.
  'dbm_schema': '[]',  # Schema provided in JSON list format or empty list.
  'is_incremental_load': False,  # Clear data in destination table during this report's time period, then append report data to destination table.
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
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dbm_dataset',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Existing BigQuery dataset.'
            }
          },
          'table': {
            'field': {
              'name': 'dbm_table',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Table to create from this report.'
            }
          },
          'schema': {
            'field': {
              'name': 'dbm_schema',
              'kind': 'json',
              'order': 5,
              'default': '[]',
              'description': 'Schema provided in JSON list format or empty list.'
            }
          },
          'is_incremental_load': {
            'field': {
              'name': 'is_incremental_load',
              'kind': 'boolean',
              'order': 6,
              'default': False,
              'description': "Clear data in destination table during this report's time period, then append report data to destination table."
            }
          }
        }
      },
      'datastudio': True
    }
  }
]

DAG_FACTORY = DAG_Factory('dbm_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
