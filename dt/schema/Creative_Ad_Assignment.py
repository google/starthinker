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

Creative_Ad_Assignment_Schema = [
  { "name":"ad_click_url", "type":"STRING", "mode":"NULLABLE" },
  { "name":"ad_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"advertiser_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"creative_end_date", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"creative_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"creative_group1", "type":"STRING", "mode":"NULLABLE" },
  { "name":"creative_group1_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"creative_group2", "type":"STRING", "mode":"NULLABLE" },
  { "name":"creative_group2_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"creative_rotation_type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"creative_rotation_type_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"creative_start_date", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"floodlight_config_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"account_id", "type":"INTEGER", "mode":"NULLABLE" }
]