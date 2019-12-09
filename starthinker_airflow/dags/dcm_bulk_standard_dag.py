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
DCM Standard Bulk

Aggregate multiple standard DCM reports into one BigQuery or Sheet.

S
e
e
 
A
P
I
 
d
o
c
s
 
f
o
r
 
<
a
 
h
r
e
f
=
'
h
t
t
p
s
:
/
/
d
e
v
e
l
o
p
e
r
s
.
g
o
o
g
l
e
.
c
o
m
/
d
o
u
b
l
e
c
l
i
c
k
-
a
d
v
e
r
t
i
s
e
r
s
/
v
3
.
2
/
d
i
m
e
n
s
i
o
n
s
'
 
t
a
r
g
e
t
=
'
_
b
l
a
n
k
'
>
M
e
t
r
i
c
s
<
/
a
>
.


D
C
M
 
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
 
f
o
r
m
a
t
 
'
[
R
e
p
o
r
t
 
N
a
m
e
]
 
[
A
c
c
o
u
n
t
 
I
D
]
 
(
 
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
 
)
'
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
 
b
u
c
k
e
t
 
a
n
d
 
p
a
t
h
 
o
r
 
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
  'accounts': '',
  'name': '',
  'range': 'LAST_7_DAYS',
  'dcm_dimensions': ['date', 'platformType', 'creativeType', 'state', 'dmaRegion'],
  'dcm_metrics': ['impressions'],
  'dataset': '',
  'table': '',
  'bucket': '',
  'path': 'DCM_Report',
  'delete': False,
  'datastudio': True,
}

TASKS = [
  {
    'dcm_bulk': {
      'auth': 'user',
      'accounts': {
        'field': {
          'name': 'accounts',
          'kind': 'integer_list',
          'order': 1,
          'default': ''
        }
      },
      'name': {
        'field': {
          'name': 'name',
          'kind': 'string',
          'order': 2,
          'default': ''
        }
      },
      'report': {
        'type': 'STANDARD',
        'timeout': 0,
        'relativeDateRange': {
          'field': {
            'name': 'range',
            'kind': 'choice',
            'order': 3,
            'default': 'LAST_7_DAYS',
            'choices': [
              'LAST_24_MONTHS',
              'LAST_30_DAYS',
              'LAST_365_DAYS',
              'LAST_7_DAYS',
              'LAST_90_DAYS',
              'MONTH_TO_DATE',
              'PREVIOUS_MONTH',
              'PREVIOUS_QUARTER',
              'PREVIOUS_WEEK',
              'PREVIOUS_YEAR',
              'QUARTER_TO_DATE',
              'TODAY',
              'WEEK_TO_DATE',
              'YEAR_TO_DATE',
              'YESTERDAY'
            ]
          }
        },
        'dimensions': {
          'field': {
            'name': 'dcm_dimensions',
            'kind': 'string_list',
            'order': 4,
            'default': [
              'date',
              'platformType',
              'creativeType',
              'state',
              'dmaRegion'
            ]
          }
        },
        'metrics': {
          'field': {
            'name': 'dcm_metrics',
            'kind': 'string_list',
            'order': 5,
            'default': [
              'impressions'
            ]
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 5,
              'default': ''
            }
          },
          'table': {
            'field': {
              'name': 'table',
              'kind': 'string',
              'order': 6,
              'default': ''
            }
          }
        },
        'storage': {
          'bucket': {
            'field': {
              'name': 'bucket',
              'kind': 'string',
              'order': 7,
              'default': ''
            }
          },
          'path': {
            'field': {
              'name': 'path',
              'kind': 'string',
              'order': 8,
              'default': 'DCM_Report'
            }
          }
        }
      },
      'delete': {
        'field': {
          'name': 'delete',
          'kind': 'boolean',
          'order': 10,
          'default': False
        }
      },
      'datastudio': {
        'field': {
          'name': 'datastudio',
          'kind': 'boolean',
          'order': 11,
          'default': True
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_bulk_standard', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
