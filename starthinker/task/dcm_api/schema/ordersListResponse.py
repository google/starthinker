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

ordersListResponse_Schema = [
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
        "type": "STRING", 
        "description": "", 
        "name": "termsAndConditions"
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
        "description": "", 
        "name": "sellerOrganizationName"
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
        "type": "STRING", 
        "description": "", 
        "name": "buyerInvoiceId"
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
        "type": "STRING", 
        "description": "", 
        "name": "notes"
      }, 
      {
        "fields": [
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "signatureUserProfileId"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "contactTitle"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "contactInfo"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "contactName"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "PLANNING_ORDER_CONTACT_BUYER_BILLING_CONTACT, PLANNING_ORDER_CONTACT_BUYER_CONTACT, PLANNING_ORDER_CONTACT_SELLER_CONTACT", 
            "name": "contactType"
          }
        ], 
        "type": "RECORD", 
        "name": "contacts", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "buyerOrganizationName"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "comments"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "advertiserId"
      }, 
      {
        "type": "INT64", 
        "name": "approverUserProfileIds", 
        "mode": "REPEATED"
      }, 
      {
        "type": "INT64", 
        "name": "siteId", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "sellerOrderId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "projectId"
      }, 
      {
        "type": "STRING", 
        "name": "siteNames", 
        "mode": "REPEATED"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "planningTermId"
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
    "name": "orders", 
    "mode": "REPEATED"
  }
]
