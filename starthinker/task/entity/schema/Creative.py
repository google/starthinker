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

Creative_Schema = [
    {
        'name':
            'common_data',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
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
                'name': 'active',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE',
            },
            {
                'name': 'integration_code',
                'type': 'STRING',
                'mode': 'NULLABLE',
            },
        ]
    },
    {
        'name': 'advertiser_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dcm_placement_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'width_pixels',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'height_pixels',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name':
            'approval_status',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [
            {
                'name': 'auditor',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'status',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'feedback',
                'type': 'STRING',
                'mode': 'NULLABLE',
            },
            {
                'name': 'sync_time',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'external_id',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
        ]
    },
    {
        'name': 'expanding_direction',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'creative_type',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
]
