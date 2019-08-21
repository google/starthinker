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

videoSettings_Schema = [
  [
    {
      "type": "BOOLEAN", 
      "name": "skippable", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "offsetPercentage"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "offsetSeconds"
      }
    ], 
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "offsetPercentage"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "offsetSeconds"
      }
    ]
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "companionsDisabled", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "imageOnly", 
      "mode": "NULLABLE"
    }, 
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "width"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "iab", 
          "mode": "NULLABLE"
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
          "name": "height"
        }
      ], 
      "type": "RECORD", 
      "name": "enabledSizes", 
      "mode": "REPEATED"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ANY, LANDSCAPE, PORTRAIT", 
    "name": "orientation"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "type": "INT64", 
      "name": "enabledVideoFormats", 
      "mode": "REPEATED"
    }
  ]
]