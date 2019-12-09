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
Email Fetch

Import emailed csv or excel into a BigQuery table.

T
h
e
 
p
e
r
s
o
n
 
e
x
e
c
u
t
i
n
g
 
t
h
i
s
 
r
e
c
i
p
e
 
m
u
s
t
 
b
e
 
t
h
e
 
r
e
c
i
p
i
e
n
t
 
o
f
 
t
h
e
 
e
m
a
i
l
.


S
c
h
e
d
u
l
e
 
a
 
C
S
V
 
o
r
 
E
x
c
e
l
 
t
o
 
b
e
 
s
e
n
t
 
t
o
 
<
b
>
U
N
D
E
F
I
N
E
D
<
/
b
>
.


G
i
v
e
 
a
 
r
e
g
u
l
a
r
 
e
x
p
r
e
s
s
i
o
n
 
t
o
 
m
a
t
c
h
 
t
h
e
 
e
m
a
i
l
 
s
u
b
j
e
c
t
,
 
l
i
n
k
 
o
r
 
a
t
t
a
c
h
m
e
n
t
.


T
h
e
 
d
a
t
a
 
d
o
w
n
l
o
a
d
e
d
 
w
i
l
l
 
o
v
e
r
w
r
i
t
e
 
t
h
e
 
t
a
b
l
e
 
s
p
e
c
i
f
i
e
d
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'email_from': '',  # Must match from field.
  'email_to': '',  # Must match to field.
  'subject': '',  # Regular expression to match subject.
  'link': '',  # Regular expression to match email.
  'attachment': '',  # Regular expression to match atttachment.
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Name of table to be written to.
}

TASKS = [
  {
    'email': {
      'auth': 'user',
      'in': {
        'email': {
          'from': {
            'field': {
              'name': 'email_from',
              'kind': 'string',
              'order': 1,
              'default': '',
              'description': 'Must match from field.'
            }
          },
          'to': {
            'field': {
              'name': 'email_to',
              'kind': 'string',
              'order': 2,
              'default': '',
              'description': 'Must match to field.'
            }
          },
          'subject': {
            'field': {
              'name': 'subject',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Regular expression to match subject.'
            }
          },
          'link': {
            'field': {
              'name': 'link',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Regular expression to match email.'
            }
          },
          'attachment': {
            'field': {
              'name': 'attachment',
              'kind': 'string',
              'order': 5,
              'default': '',
              'description': 'Regular expression to match atttachment.'
            }
          }
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
              'description': 'Name of table to be written to.'
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('email_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
