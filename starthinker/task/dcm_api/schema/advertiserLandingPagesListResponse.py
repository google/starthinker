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

advertiserLandingPagesListResponse_Schema = [
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
        "name": "archived", 
        "mode": "NULLABLE"
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
        "name": "url"
      }, 
      {
        "fields": [
          [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "APPLE_APP_STORE, GOOGLE_PLAY_STORE, UNKNOWN", 
              "name": "directory"
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
              "name": "publisherName"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "id"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "", 
              "name": "title"
            }
          ], 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "appUrl"
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
            "name": "fallbackUrl"
          }, 
          {
            "fields": {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "remarketingListIds"
            }, 
            "type": "RECORD", 
            "name": "remarketingListIds", 
            "mode": "REPEATED"
          }
        ], 
        "type": "RECORD", 
        "name": "deepLinks", 
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
        "name": "advertiserId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "id"
      }
    ], 
    "type": "RECORD", 
    "name": "landingPages", 
    "mode": "REPEATED"
  }
]
