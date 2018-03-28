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

Placement_Schema = [
  { "name":"activity_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"advertiser_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"campaign_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"content_category", "type":"STRING", "mode":"NULLABLE" },
  { "name":"content_category_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"flighting_activated", "type":"BOOLEAN", "mode":"NULLABLE" },
  { "name":"placement_cap_cost_option", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"placement_end_date", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"package_roadblock_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"package_roadblock_type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"package_roadblock_type_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"placement_cost_structure", "type":"STRING", "mode":"NULLABLE" },
  { "name":"placement_start_date", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"placement_strategy", "type":"STRING", "mode":"NULLABLE" },
  { "name":"placement_strategy_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"site_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"placement", "type":"STRING", "mode":"NULLABLE" },
  { "name":"placement_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"site_keyname", "type":"STRING", "mode":"NULLABLE" },
  { "name":"floodlight_config_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"account_id", "type":"INTEGER", "mode":"NULLABLE" }
]