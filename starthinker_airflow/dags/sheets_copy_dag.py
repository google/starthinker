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
Sheet Copy

Copy tab from a sheet to a sheet.

Provide the full edit URL for both sheets.
Provide the tab name for both sheets.
The tab will only be copied if it does not already exist.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  "from_sheet":"",
  "from_tab":"",
  "to_sheet":"",
  "to_tab":"",
}

TASKS = [
  {
    "sheets": {
      "auth": "user",
      "template": {
        "sheet": {
          "field": {
            "name": "from_sheet",
            "kind": "string",
            "order": 1,
            "default": ""
          }
        },
        "tab": {
          "field": {
            "name": "from_tab",
            "kind": "string",
            "order": 2,
            "default": ""
          }
        }
      },
      "sheet": {
        "field": {
          "name": "to_sheet",
          "kind": "string",
          "order": 3,
          "default": ""
        }
      },
      "tab": {
        "field": {
          "name": "to_tab",
          "kind": "string",
          "order": 4,
          "default": ""
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('sheets_copy', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
