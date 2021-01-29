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

Advertiser_Schema = [
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
        'name': 'partner_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'currency_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'timezone_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'landing_page_url',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'available_channel_ids',
        'type': 'INTEGER',
        'mode': 'REPEATED',
    },
    {
        'name': 'blacklist_channel_id',
        'type': 'INTEGER',
        'mode': 'REPEATED',
    },
    {
        'name': 'dcm_configuration',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dcm_network_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dcm_network_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dcm_advertiser_id',
        'type': 'INTEGER',
        'mode': 'REPEATED',
    },
    {
        'name': 'dcm_advertiser_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dcm_floodlight_group_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dcm_syncable_site_ids',
        'type': 'INTEGER',
        'mode': 'REPEATED',
    },
    {
        'name': 'enable_oba_tags',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE',
    },
]
