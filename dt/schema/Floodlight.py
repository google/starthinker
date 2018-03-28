###########################################################################
#
#  Copyright 2017 Google Inc.
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

Floodlight_Schema = [
  { "name":"Event Time", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"User ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Advertiser ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Campaign ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Ad ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Creative Version", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Site ID (DCM)", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Browser/Platform Version", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Event Type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Event Sub-Type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Auction ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Request Time", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Advertiser ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Line Item ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Creative ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM URL", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Site ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Language", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Adx Page Categories", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Matching Targeted Keywords", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Exchange ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Attributed Inventory Source External ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Attributed Inventory Source Is Public", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Ad Position", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Country Code", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM Browser/Platform ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Net Speed", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Matching Targeted Segments", "type":"STRING", "mode":"NULLABLE" },
  { "name":"DBM ISP ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Mobile Model ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Designated Market Area (DMA) ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM City ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Browser Timezone Offset Minutes", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"DBM Mobile Make ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Activity ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Creative Pixel Size", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Total Conversions", "type":"INTEGER", "mode":"NULLABLE" }
]