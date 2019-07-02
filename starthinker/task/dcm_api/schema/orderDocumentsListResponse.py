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

orderDocumentsListResponse_Schema = [
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
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "orderId"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "approvedByUserProfileIds"
        }, 
        "type": "RECORD", 
        "name": "approvedByUserProfileIds", 
        "mode": "REPEATED"
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
        "type": "DATE", 
        "description": "", 
        "name": "effectiveDate"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "DATETIME", 
        "description": "", 
        "name": "lastSentTime"
      }, 
      {
        "fields": {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "lastSentRecipients"
        }, 
        "type": "RECORD", 
        "name": "lastSentRecipients", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "title"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "amendedOrderDocumentId"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "signed", 
        "mode": "NULLABLE"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "time"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "advertiserId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "projectId"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "cancelled", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "PLANNING_ORDER_TYPE_CHANGE_ORDER, PLANNING_ORDER_TYPE_INSERTION_ORDER", 
        "name": "type"
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
    "name": "orderDocuments", 
    "mode": "REPEATED"
  }
]
