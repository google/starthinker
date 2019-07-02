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

file_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "CANCELLED, FAILED, PROCESSING, REPORT_AVAILABLE", 
    "name": "status"
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
    "description": "CSV, EXCEL", 
    "name": "format"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "DATE", 
      "description": "", 
      "name": "startDate"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "DATE", 
      "description": "", 
      "name": "endDate"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY", 
      "name": "relativeDateRange"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "fileName"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "etag"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "reportId"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "browserUrl"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "apiUrl"
      }
    ], 
    "type": "RECORD", 
    "name": "urls", 
    "mode": "REQUIRED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "lastModifiedTime"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }
]
