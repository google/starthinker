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
Dataset

Create and permission a dataset in BigQuery.

Specify the name of the dataset.
If dataset exists, it is inchanged.
Add emails and / or groups to add read permission.
CAUTION: Removing permissions in StarThinker has no effect.
CAUTION: To remove permissions you have to edit the dataset.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  "dataset_dataset":"", # Name of Google BigQuery dataset to create.
  "dataset_emails":[], # Comma separated emails.
  "dataset_groups":[], # Comma separated groups.
}

TASKS = [
  {
    "dataset": {
      "auth": "service",
      "dataset": {
        "field": {
          "name": "dataset_dataset",
          "kind": "string",
          "order": 1,
          "default": "",
          "description": "Name of Google BigQuery dataset to create."
        }
      },
      "emails": {
        "field": {
          "name": "dataset_emails",
          "kind": "string_list",
          "order": 2,
          "default": [],
          "description": "Comma separated emails."
        }
      },
      "groups": {
        "field": {
          "name": "dataset_groups",
          "kind": "string_list",
          "order": 3,
          "default": [],
          "description": "Comma separated groups."
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dataset', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
