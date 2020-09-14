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

DeviceCriteria_Schema = [
    {
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'criteria_type',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'is_mobile',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE',
    },
    {
        'name': 'mobile_brand_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'mobile_model_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'operating_system_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'device_type',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'mobile_make_model_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
]
