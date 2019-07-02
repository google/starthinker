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

userRolesListResponse_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "nextPageToken"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  {
    "fields": [
      {
        "type": "BOOLEAN", 
        "name": "defaultUserRole", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "subaccountId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "name"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "parentUserRoleId"
      }, 
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "permissionGroupId"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "kind"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "ACCOUNT_ALWAYS, ACCOUNT_BY_DEFAULT, NOT_AVAILABLE_BY_DEFAULT, SUBACCOUNT_AND_ACCOUNT_ALWAYS, SUBACCOUNT_AND_ACCOUNT_BY_DEFAULT", 
            "name": "availability"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "id"
          }
        ], 
        "type": "RECORD", 
        "name": "permissions", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "id"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "accountId"
      }
    ], 
    "type": "RECORD", 
    "name": "userRoles", 
    "mode": "REPEATED"
  }
]
