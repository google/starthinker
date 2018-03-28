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

Rich_Media_Schema = [
  { "name":"Event Time", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"User ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Advertiser ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Campaign ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Ad ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Rendering ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Creative Version", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Site ID (DCM)", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Country Code", "type":"STRING", "mode":"NULLABLE" },
  { "name":"State/Region", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Browser/Platform ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Browser/Platform Version", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Placement ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Operating System ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Partner 1 ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Partner 2 ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Partner 3 ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Partner 4 ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Partner 5 ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Null User ID Reason Groups", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Rich Media Event ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Rich Media Event Type ID", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Impression ID", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Creative Pixel Size", "type":"STRING", "mode":"NULLABLE" },
  { "name":"Custom Event Counters", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Custom Event Timers", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Event Counters", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"Event Timers", "type":"FLOAT", "mode":"NULLABLE" }
]