###########################################################################
#
#  Copyright 2020 Google LLC
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

from starthinker.util.bigquery import table_create
from starthinker.util.sheets import sheets_clear

from starthinker.tasks.dv_targeting.types import TARGETING_SCHEMA
from starthinker.tasks.dv_targeting.types import TARGETING_TYPES

def clear():
  for targeting_type in TARGETING_TYPES:
    table_create(
      project.task['auth_bigquery'],
      project.id,
      project.task['dataset'],
      'DV_Targeting_%s' % targeting_type,
      TARGETING_SCHEMA[targeting_type]
    )

    sheets_clear(
      project.task['auth_sheets'],
      project.task['sheet'],
      targeting_type,
      'A2:Z'
    )
