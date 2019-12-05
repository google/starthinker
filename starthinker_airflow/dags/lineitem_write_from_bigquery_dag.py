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
Line Item From BigQuery

Upload Line Items From BigQuery To DBM.

Specify the table or view where the lineitem data is defined.
The schema should match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  "dataset":"",
  "query":"SELECT * FROM `Dataset.Table`;",
  "legacy":False,
}

TASKS = [
  {
    "lineitem": {
      "auth": "user",
      "write": {
        "dry_run": false,
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": ""
            }
          },
          "query": {
            "field": {
              "name": "query",
              "kind": "string",
              "order": 2,
              "default": "SELECT * FROM `Dataset.Table`;"
            }
          },
          "legacy": {
            "field": {
              "name": "legacy",
              "kind": "boolean",
              "order": 3,
              "default": false
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('lineitem_write_from_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
