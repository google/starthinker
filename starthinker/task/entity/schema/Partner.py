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

Partner_Schema = [
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
        'name': 'currency_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name':
            'exchange_settings',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [
            {
                'name': 'exchange_id',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'seat_id',
                'type': 'STRING',
                'mode': 'NULLABLE',
            },
            {
                'name': 'seat_user_name',
                'type': 'STRING',
                'mode': 'NULLABLE',
            },
        ]
    },
    {
        'name':
            'default_partner_costs',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name': 'cpm_fee_1_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_2_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_3_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_4_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_5_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_1_millis',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_2_millis',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_3_millis',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_4_millis',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_5_millis',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_1_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_2_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_3_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_4_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_5_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_1_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_2_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_3_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_4_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_5_cost_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_1_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_2_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_3_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_4_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'cpm_fee_5_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_1_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_2_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_3_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_4_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_fee_percent_5_bill_to_type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
        ]
    },
    {
        'name':
            'default_partner_revenue_model',
        'type':
            'RECORD',
        'mode':
            'NULLABLE',
        'fields': [
            {
                'name': 'type',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'amount_advertiser_micros',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'media_cost_markup_percent_millis',
                'type': 'INTEGER',
                'mode': 'NULLABLE',
            },
            {
                'name': 'post_view_conversion_tracking_fraction',
                'type': 'FLOAT',
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
]
