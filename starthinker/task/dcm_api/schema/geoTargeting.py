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

geoTargeting_Schema = [
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "dartId"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "sslEnabled", 
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
        "type": "STRING", 
        "description": "", 
        "name": "countryCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "name"
      }
    ], 
    "type": "RECORD", 
    "name": "countries", 
    "mode": "REPEATED"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "excludeCountries", 
    "mode": "NULLABLE"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "countryDartId"
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
        "name": "code"
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
        "name": "countryCode"
      }
    ], 
    "type": "RECORD", 
    "name": "postalCodes", 
    "mode": "REPEATED"
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
        "type": "INT64", 
        "description": "", 
        "name": "countryDartId"
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
        "name": "countryCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "regionCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "dartId"
      }
    ], 
    "type": "RECORD", 
    "name": "regions", 
    "mode": "REPEATED"
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
        "type": "INT64", 
        "description": "", 
        "name": "countryDartId"
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
        "name": "countryCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "metroCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "regionCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "metroDmaId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "dartId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "regionDartId"
      }
    ], 
    "type": "RECORD", 
    "name": "cities", 
    "mode": "REPEATED"
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
        "type": "INT64", 
        "description": "", 
        "name": "countryDartId"
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
        "name": "countryCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "metroCode"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "dmaId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "dartId"
      }
    ], 
    "type": "RECORD", 
    "name": "metros", 
    "mode": "REPEATED"
  }
]
