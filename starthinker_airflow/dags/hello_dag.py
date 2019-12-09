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
Say Hello

Recipe template for say hello.

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
 
f
o
r
 
t
e
s
t
i
n
g
 
o
n
l
y
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'say_first': 'Hello Once',  # Type in a greeting.
  'say_second': 'Hello Twice',  # Type in a greeting.
  'error': '',  # Optional error for testing.
  'sleep': 0,  # Seconds to sleep.
}

TASKS = [
  {
    'hello': {
      'auth': 'user',
      'say': {
        'field': {
          'name': 'say_first',
          'kind': 'string',
          'order': 1,
          'default': 'Hello Once',
          'description': 'Type in a greeting.'
        }
      },
      'error': {
        'field': {
          'name': 'error',
          'kind': 'string',
          'order': 3,
          'default': '',
          'description': 'Optional error for testing.'
        }
      },
      'sleep': {
        'field': {
          'name': 'sleep',
          'kind': 'integer',
          'order': 4,
          'default': 0,
          'description': 'Seconds to sleep.'
        }
      }
    }
  },
  {
    'hello': {
      'auth': 'user',
      'say': {
        'field': {
          'name': 'say_second',
          'kind': 'string',
          'order': 1,
          'default': 'Hello Twice',
          'description': 'Type in a greeting.'
        }
      },
      'sleep': {
        'field': {
          'name': 'sleep',
          'kind': 'integer',
          'order': 4,
          'default': 0,
          'description': 'Seconds to sleep.'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('hello', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
