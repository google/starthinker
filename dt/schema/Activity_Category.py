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

Activity_Category_Schema = [
  { "name":"activity", "type":"STRING", "mode":"NULLABLE" },
  { "name":"activity_group_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"activity_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"activity_sub_type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"activity_type", "type":"STRING", "mode":"NULLABLE" },
  { "name":"advertiser_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"floodlight_config_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"tag_counting_method_id", "type":"INTEGER", "mode":"NULLABLE" },
  { "name":"account_id", "type":"INTEGER", "mode":"NULLABLE" }
]