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
Bucket

Create and permission a bucket in Storage.

Specify the name of the bucket and who will have owner permissions.
Existing buckets are preserved.
Adding a permission to the list will update the permissions but removing them will not.
You have to manualy remove grants.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  "bucket_bucket":"", # Name of Google Cloud Bucket to create.
  "bucket_emails":, # Comma separated emails.
  "bucket_groups":, # Comma separated groups.
}

TASKS = [
  {
    "bucket": {
      "auth": "service",
      "bucket": {
        "field": {
          "name": "bucket_bucket",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Name of Google Cloud Bucket to create."
        }
      },
      "emails": {
        "field": {
          "name": "bucket_emails",
          "kind": "string_list",
          "order": 3,
          "default": "",
          "description": "Comma separated emails."
        }
      },
      "groups": {
        "field": {
          "name": "bucket_groups",
          "kind": "string_list",
          "order": 4,
          "default": "",
          "description": "Comma separated groups."
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bucket', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
