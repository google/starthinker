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

InventorySource_Schema = [
    {
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'unclassified',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE',
    },
    {
        'name': 'inventory_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'exchange_id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'external_id',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'min_cpm_micros',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'min_cpm_currency_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'accessing_advertisers',
        'type': 'INTEGER',
        'mode': 'REPEATED',
    },
]
