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

Campaign_Schema = [
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
        'name':
            'budget',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name': 'start_time_usec',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'end_time_usec',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'max_impressions',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'max_spend_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'pacing_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'pacing_max_impressions',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'pacing_max_spend_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'pacing_distribution',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
        ]
    },
    {
        'name':
            'frequency_cap',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name': 'max_impressions',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'time_unit',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'time_range',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
        ]
    },
    {
        'name':
            'default_target_list',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name':
                    'inventory_sources',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'geo_locations',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'ad_position',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'net_speed',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'browsers',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [
                    {
                        'name':
                            'union',
                        'type':
                            'RECORD',
                        'mode':
                            'REPEATED',
                        'fields': [
                            {
                                'name': 'criteria_id',
                                'type': 'INTEGER',
                                'mode': 'NULLABLE',
                            },
                            {
                                'name': 'parameter',
                                'type': 'STRING',
                                'mode': 'NULLABLE',
                            },
                        ]
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'device_criteria',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'languages',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [
                    {
                        'name':
                            'union',
                        'type':
                            'RECORD',
                        'mode':
                            'REPEATED',
                        'fields': [
                            {
                                'name': 'criteria_id',
                                'type': 'INTEGER',
                                'mode': 'NULLABLE',
                            },
                            {
                                'name': 'parameter',
                                'type': 'STRING',
                                'mode': 'NULLABLE',
                            },
                        ]
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'day_parting',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [
                    {
                        'name':
                            'union',
                        'type':
                            'RECORD',
                        'mode':
                            'REPEATED',
                        'fields': [
                            {
                                'name': 'criteria_id',
                                'type': 'INTEGER',
                                'mode': 'NULLABLE',
                            },
                            {
                                'name': 'parameter',
                                'type': 'STRING',
                                'mode': 'NULLABLE',
                            },
                        ]
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'audience_intersect',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name':
                            'union',
                        'type':
                            'RECORD',
                        'mode':
                            'REPEATED',
                        'fields': [
                            {
                                'name': 'criteria_id',
                                'type': 'INTEGER',
                                'mode': 'NULLABLE',
                            },
                            {
                                'name': 'parameter',
                                'type': 'STRING',
                                'mode': 'NULLABLE',
                            },
                        ]
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'keywords',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'parameter',
                        'type': 'STRING',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name': 'kct_include_uncrawled_sites',
                'type': 'BOOLEAN',
                'mode': 'NULLABLE',
            },
            {
                'name':
                    'page_categories',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'universal_channels',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'sites',
                'type':
                    'RECORD',
                'mode':
                    'REPEATED',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'parameter',
                        'type': 'STRING',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
            {
                'name':
                    'brand_safety',
                'type':
                    'RECORD',
                'mode':
                    'NULLABLE',
                'fields': [
                    {
                        'name': 'criteria_id',
                        'type': 'INTEGER',
                        'mode': 'NULLABLE',
                    },
                    {
                        'name': 'excluded',
                        'type': 'BOOLEAN',
                        'mode': 'NULLABLE',
                    },
                ]
            },
        ]
    },
    {
        'name': 'uses_video_creatives',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE',
    },
    {
        'name': 'uses_display_creatives',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE',
    },
    {
        'name': 'uses_audio_creatives',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE',
    },
    {
        'name': 'objective',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'objective_description',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'metric',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'metric_amount_micros',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
]
