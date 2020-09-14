###########################################################################
#
#  Copyright 2020 Google LLC
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
"""--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

Say Hello

Recipe template for say hello.

This should be called for testing only.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'say_second': 'Hello Twice',  # Type in a greeting.
    'say_first': 'Hello Once',  # Type in a greeting.
    'error': '',  # Optional error for testing.
    'sleep': 0,  # Seconds to sleep.
}

TASKS = [{
    'hello': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'error': {
            'field': {
                'description': 'Optional error for testing.',
                'name': 'error',
                'default': '',
                'kind': 'string',
                'order': 3
            }
        },
        'sleep': {
            'field': {
                'description': 'Seconds to sleep.',
                'name': 'sleep',
                'default': 0,
                'kind': 'integer',
                'order': 4
            }
        },
        'say': {
            'field': {
                'description': 'Type in a greeting.',
                'name': 'say_first',
                'default': 'Hello Once',
                'kind': 'string',
                'order': 1
            }
        }
    }
}, {
    'hello': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'sleep': {
            'field': {
                'description': 'Seconds to sleep.',
                'name': 'sleep',
                'default': 0,
                'kind': 'integer',
                'order': 4
            }
        },
        'say': {
            'field': {
                'description': 'Type in a greeting.',
                'name': 'say_second',
                'default': 'Hello Twice',
                'kind': 'string',
                'order': 1
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('hello', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
