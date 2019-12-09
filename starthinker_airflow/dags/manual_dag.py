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
Test Script

Used by tests.

T
h
i
s
 
s
h
o
u
l
d
 
b
e
 
c
a
l
l
e
d
 
b
y
 
t
h
e
 
t
e
s
t
s
 
s
c
r
i
p
t
s
 
o
n
l
y
.


W
h
e
n
 
r
u
n
 
w
i
l
l
 
g
e
n
e
r
a
t
e
 
a
 
s
a
y
 
h
e
l
l
o
 
l
o
g
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  
}

TASKS = [
  {
    'hello': {
      'auth': 'user',
      'hour': [
      ],
      'say': 'Hello Manual',
      'sleep': 0
    }
  }
]

DAG_FACTORY = DAG_Factory('manual', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
