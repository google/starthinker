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

conversionStatus_Schema = [
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "ordinal"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "timestampMicros"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "childDirectedTreatment", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "encryptedUserId"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "treatmentForUnderage", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "gclid"
    }, 
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "U1, U10, U100, U11, U12, U13, U14, U15, U16, U17, U18, U19, U2, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U3, U30, U31, U32, U33, U34, U35, U36, U37, U38, U39, U4, U40, U41, U42, U43, U44, U45, U46, U47, U48, U49, U5, U50, U51, U52, U53, U54, U55, U56, U57, U58, U59, U6, U60, U61, U62, U63, U64, U65, U66, U67, U68, U69, U7, U70, U71, U72, U73, U74, U75, U76, U77, U78, U79, U8, U80, U81, U82, U83, U84, U85, U86, U87, U88, U89, U9, U90, U91, U92, U93, U94, U95, U96, U97, U98, U99", 
          "name": "type"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }
      ], 
      "type": "RECORD", 
      "name": "customVariables", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "floodlightConfigurationId"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "mobileDeviceId"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "FLOAT64", 
      "description": "", 
      "name": "value"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "nonPersonalizedAd", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "limitAdTracking", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "quantity"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "floodlightActivityId"
    }, 
    {
      "fields": {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "encryptedUserIdCandidates"
      }, 
      "type": "RECORD", 
      "name": "encryptedUserIdCandidates", 
      "mode": "REPEATED"
    }
  ], 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "INTERNAL, INVALID_ARGUMENT, NOT_FOUND, PERMISSION_DENIED", 
        "name": "code"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "message"
      }
    ], 
    "type": "RECORD", 
    "name": "errors", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }
]
