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

Storage Bucket

Create and permission a bucket in Storage.

Specify the name of the bucket and who will have owner permissions.
Existing buckets are preserved.
Adding a permission to the list will update the permissions but removing them
will not.
You have to manualy remove grants.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_write': 'service',  # Credentials used for writing data.
    'bucket_bucket': '',  # Name of Google Cloud Bucket to create.
    'bucket_emails': '',  # Comma separated emails.
    'bucket_groups': '',  # Comma separated groups.
}

TASKS = [{
    'bucket': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'bucket': {
            'field': {
                'description': 'Name of Google Cloud Bucket to create.',
                'name': 'bucket_bucket',
                'default': '',
                'kind': 'string',
                'order': 2
            }
        },
        'emails': {
            'field': {
                'description': 'Comma separated emails.',
                'name': 'bucket_emails',
                'default': '',
                'kind': 'string_list',
                'order': 3
            }
        },
        'groups': {
            'field': {
                'description': 'Comma separated groups.',
                'name': 'bucket_groups',
                'default': '',
                'kind': 'string_list',
                'order': 4
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('bucket', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
